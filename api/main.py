#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울 카드 데이터 기반 추천 서비스 API - 이중 매칭 알고리즘 적용
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
from datetime import datetime

app = FastAPI(title="서울 카드 데이터 기반 추천 서비스 - 이중 매칭 알고리즘")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GitHub raw URL - 데이터 파일 직접 로드
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/SUE960/space_recommendation/main/outputs"
STATIC_PROFILES_URL = f"{GITHUB_RAW_BASE}/step1_static_profiles.json"
REALTIME_PROFILES_URL = f"{GITHUB_RAW_BASE}/realtime_area_profiles.json"

# 전역 변수로 데이터 캐싱
static_profiles_cache = None
realtime_profiles_cache = None

def load_data():
    """데이터 로드 - GitHub에서 직접 로드"""
    global static_profiles_cache, realtime_profiles_cache
    
    import requests
    
    # 1. 정적 프로필 로드
    if static_profiles_cache is None:
        try:
            print(f"🔄 정적 프로필 로드 중... {STATIC_PROFILES_URL}")
            response = requests.get(STATIC_PROFILES_URL, timeout=10)
            response.raise_for_status()
            static_profiles_cache = response.json()
            print(f"✅ 정적 프로필 로드 완료 ({len(static_profiles_cache)} 세그먼트)")
        except Exception as e:
            print(f"⚠️ 정적 프로필 로드 실패: {e}")
            static_profiles_cache = {}
    
    # 2. 실시간 프로필 로드
    if realtime_profiles_cache is None:
        try:
            print(f"🔄 실시간 프로필 로드 중... {REALTIME_PROFILES_URL}")
            response = requests.get(REALTIME_PROFILES_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            # 리스트를 딕셔너리로 변환
            realtime_profiles_cache = {item['basic_info']['area_nm']: item for item in data}
            print(f"✅ 실시간 프로필 로드 완료 ({len(realtime_profiles_cache)}개 지역)")
        except Exception as e:
            print(f"⚠️ 실시간 프로필 로드 실패: {e}")
            realtime_profiles_cache = {}
    
    return static_profiles_cache, realtime_profiles_cache

# 업종 매핑 (카드 데이터 -> API 카테고리)
INDUSTRY_MAPPING = {
    '한식': '음식·음료',
    '중식': '음식·음료',
    '일식': '음식·음료',
    '양식': '음식·음료',
    '기타요식': '음식·음료',
    '카페': '음식·음료',
    '커피전문점': '음식·음료',
    '편의점': '유통',
    '대형마트': '유통',
    '슈퍼마켓': '유통',
    '영화관': '여가·오락',
    '영화/공연': '여가·오락',
    '노래방': '여가·오락',
    '게임방': '여가·오락',
}

# 요청 모델 - 이중 매칭 알고리즘 적용
class RecommendationRequest(BaseModel):
    # 정적 프로필 매칭용
    age: int  # 나이
    gender: str  # 성별: "남" | "여"
    income_level: str = "중"  # 소득 수준: "저" | "중" | "고"
    
    # 실시간 프로필 매칭용
    preferred_industries: List[str]  # 선호 업종 리스트
    time_period: str  # 시간대: "새벽" | "오전" | "오후" | "저녁"
    is_weekend: bool = False  # 주말 여부
    preference_type: str = "활발한"  # 지역 특성: "활발한" | "안정적인" | "특화된"
    
    # 선택 사항
    budget_range: Optional[dict] = None  # {"min": 10000, "max": 50000}
    location_preference: Optional[dict] = None  # {"gu": "강남구"}

# 응답 모델 - 이중 매칭 알고리즘 적용
class RegionRecommendation(BaseModel):
    rank: int  # 순위
    region: str  # 지역명
    final_score: float  # 최종 점수
    
    # 점수 세부사항
    static_score: float  # 정적 매칭 점수
    realtime_score: float  # 실시간 매칭 점수
    
    static_details: dict  # 정적 매칭 세부 점수
    realtime_details: dict  # 실시간 매칭 세부 점수
    
    # 지역 정보
    comprehensive_score: float  # 실시간 종합 점수
    grade: str  # 등급
    specialized_industries: List[str]  # 특화 업종
    
    reasons: List[str]  # 추천 이유

class RecommendationResponse(BaseModel):
    recommendations: List[RegionRecommendation]
    user_profile: dict

def calculate_static_matching(static_profile: dict, realtime_profile: dict, user_input: dict) -> dict:
    """
    정적 프로필 매칭 점수 계산
    
    Args:
        static_profile: 2단계에서 가져온 사용자 세그먼트 프로필
        realtime_profile: 3단계에서 가져온 실시간 지역 프로필
        user_input: 사용자 입력
        
    Returns:
        정적 매칭 점수 및 세부사항
    """
    # 1. 업종 선호도 매칭 (40%)
    static_industries = set([ind['industry'] for ind in static_profile['industry_preferences'][:5]])
    realtime_industries = set(realtime_profile['scores']['specialization']['all_scores'].keys())
    
    # 매핑 적용
    static_mapped = set([INDUSTRY_MAPPING.get(ind, ind) for ind in static_industries])
    common_industries = static_mapped & realtime_industries
    
    industry_match = (len(common_industries) / len(static_industries) * 100) if static_industries else 0
    
    # 2. 인구통계 매칭 (30%)
    demographic_score = realtime_profile['scores']['demographic']['demographic_score']
    demographic_normalized = (demographic_score / 200 * 100) if demographic_score > 0 else 0
    
    # 사용자 연령대 보너스
    user_age_group = static_profile['segment_info']['age_group_kr']
    age_details = realtime_profile['scores']['demographic']['age_details']
    
    age_bonus = 0
    for age_label, age_data in age_details.items():
        if user_age_group in age_label or age_label in user_age_group:
            if age_data['rate'] > 20:  # 상위 연령대
                age_bonus = 10
                break
    
    demographic_match = min(demographic_normalized + age_bonus, 100)
    
    # 3. 소비 수준 매칭 (20%)
    user_avg_spending = static_profile['spending_characteristics']['avg_transaction_amount']
    if 'income_adjustment' in static_profile:
        user_avg_spending = static_profile['income_adjustment']['adjusted_avg_transaction']
    
    area_activity = realtime_profile['scores']['activity']['activity_score']
    
    # 소비 수준 갭 계산
    spending_gap = abs(area_activity - (user_avg_spending / 500))
    spending_match = max(100 - spending_gap, 0)
    
    # 4. 시간대 패턴 매칭 (10%)
    time_period = user_input.get('time_period', '저녁')
    time_patterns = static_profile.get('time_patterns', {}).get('period_summary', [])
    
    time_ratio = 50  # 기본값
    for t in time_patterns:
        if t['period'] == time_period:
            time_ratio = t['spending_ratio']
            break
    
    time_match = min(time_ratio, 100)
    
    # 최종 정적 매칭 점수
    static_score = (
        industry_match * 0.40 +
        demographic_match * 0.30 +
        spending_match * 0.20 +
        time_match * 0.10
    )
    
    return {
        'score': round(static_score, 2),
        'details': {
            'industry_match': round(industry_match, 2),
            'demographic_match': round(demographic_match, 2),
            'spending_match': round(spending_match, 2),
            'time_match': round(time_match, 2)
        }
    }


def calculate_realtime_matching(user_input: dict, realtime_profile: dict) -> dict:
    """
    실시간 프로필 매칭 점수 계산
    
    Args:
        user_input: 사용자 입력 (선호 업종, 시간대 등)
        realtime_profile: 3단계에서 가져온 실시간 지역 프로필
        
    Returns:
        실시간 매칭 점수 및 세부사항
    """
    # 1. 사용자 선호 업종 매칭 (35%)
    user_preferred = set(user_input.get('preferred_industries', []))
    area_specialized = set(realtime_profile['scores']['specialization']['all_scores'].keys())
    
    # 매핑 적용
    user_mapped = set([INDUSTRY_MAPPING.get(ind, ind) for ind in user_preferred])
    common = user_mapped & area_specialized
    
    user_industry_match = (len(common) / len(user_preferred) * 100) if user_preferred else 0
    
    # 2. 실시간 종합 점수 (30%)
    comprehensive_score = realtime_profile['scores']['comprehensive']['comprehensive_score']
    
    # 3. 특화도 매칭 (20%)
    specialization_score = realtime_profile['scores']['specialization']['top_score']
    preference_type = user_input.get('preference_type', '활발한')
    
    if preference_type == '특화된':
        specialization_match = specialization_score
    elif preference_type == '활발한':
        # 특화도가 50점 근처가 이상적 (균형)
        specialization_match = 100 - abs(specialization_score - 50)
    else:  # 안정적인
        # 특화도가 40점 근처가 이상적
        specialization_match = 100 - abs(specialization_score - 40)
    
    # 4. 시간대 적합도 (15%)
    is_weekend = user_input.get('is_weekend', False)
    activity_score = realtime_profile['scores']['activity']['activity_score']
    
    base_time_score = 70
    if is_weekend:
        time_match = 100 if activity_score > 80 else 70
    else:
        if activity_score > 80:
            time_match = 85
        elif activity_score > 60:
            time_match = 90
        else:
            time_match = 75
    
    # 최종 실시간 매칭 점수
    realtime_score = (
        user_industry_match * 0.35 +
        comprehensive_score * 0.30 +
        specialization_match * 0.20 +
        time_match * 0.15
    )
    
    return {
        'score': round(realtime_score, 2),
        'details': {
            'user_industry_match': round(user_industry_match, 2),
            'comprehensive_score': round(comprehensive_score, 2),
            'specialization_match': round(specialization_match, 2),
            'time_match': round(time_match, 2)
        }
    }


def calculate_final_score(static_result: dict, realtime_result: dict, user_input: dict, area_name: str) -> dict:
    """
    최종 추천 점수 산출 (5단계)
    
    Args:
        static_result: 정적 매칭 결과
        realtime_result: 실시간 매칭 결과
        user_input: 사용자 입력
        area_name: 지역명
        
    Returns:
        최종 점수 및 세부사항
    """
    # 기본 통합 (50:50)
    final_score = (static_result['score'] * 0.50) + (realtime_result['score'] * 0.50)
    
    # 추가 보정
    # 1. 주말 보너스
    if user_input.get('is_weekend'):
        final_score *= 1.1
    
    # 2. 예산 범위 매칭
    if user_input.get('budget_range'):
        budget_range = user_input['budget_range']
        # 간단한 예산 체크 (실제로는 지역 평균 거래액과 비교)
        # 여기서는 생략
        pass
    
    # 3. 위치 선호도
    if user_input.get('location_preference'):
        pref_gu = user_input['location_preference'].get('gu')
        if pref_gu and pref_gu in area_name:
            final_score *= 1.05
    
    return {
        'final_score': round(min(final_score, 100), 2),
        'static_score': static_result['score'],
        'realtime_score': realtime_result['score'],
        'static_details': static_result['details'],
        'realtime_details': realtime_result['details']
    }


def generate_reasons(static_profile: dict, realtime_profile: dict, user_input: dict, final_result: dict) -> List[str]:
    """추천 이유 생성"""
    reasons = []
    
    # 선호 업종 매칭
    user_industries = user_input.get('preferred_industries', [])
    if user_industries:
        reasons.append(f"선호하시는 {', '.join(user_industries[:2])} 업종이 특화된 지역")
    
    # 세그먼트 기반
    segment_info = static_profile['segment_info']
    reasons.append(f"{segment_info['age_group_kr']} {segment_info['gender_kr']}에게 인기")
    
    # 실시간 상태
    grade = realtime_profile['scores']['comprehensive']['grade']
    if '활성화' in grade or 'Hot' in grade:
        reasons.append(f"현재 {grade}")
    
    # 시간대
    time_period = user_input.get('time_period', '')
    if time_period:
        reasons.append(f"{time_period} 시간대에 적합")
    
    return reasons[:4]  # 최대 4개

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 데이터 로드"""
    load_data()
    print("✓ 데이터 로드 완료")

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "서울 카드 데이터 기반 추천 서비스 API",
        "version": "1.0.0"
    }

@app.get("/api/regions")
async def get_regions():
    """모든 지역 정보 조회"""
    characteristics, growth = load_data()
    
    if characteristics.empty:
        raise HTTPException(status_code=404, detail="지역 데이터를 찾을 수 없습니다")
    
    # 성장률 데이터 병합
    result = characteristics.copy()
    if not growth.empty and '구' in growth.columns:
        # 성장률수치 컬럼이 있으면 사용, 없으면 성장률 컬럼 사용
        growth_col = '성장률수치' if '성장률수치' in growth.columns else '성장률'
        if growth_col in growth.columns:
            result = result.merge(
                growth[['구', growth_col]],
                on='구',
                how='left'
            )
            result['성장률'] = pd.to_numeric(result[growth_col], errors='coerce').fillna(0)
            result = result.drop(columns=[growth_col])
    
    return result.to_dict('records')

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    이중 매칭 알고리즘 기반 지역 추천
    
    프로세스:
    1. 사용자 입력 처리
    2. 정적 프로필 매칭 (14개 세그먼트 중 선택)
    3. 실시간 프로필 로드 (73개 지역)
    4. 이중 매칭 점수 계산 (정적 + 실시간)
    5. 최종 점수 산출
    6. 상위 N개 지역 추천
    """
    static_profiles, realtime_profiles = load_data()
    
    if not static_profiles:
        raise HTTPException(status_code=500, detail="정적 프로필을 로드할 수 없습니다")
    
    if not realtime_profiles:
        raise HTTPException(status_code=500, detail="실시간 프로필을 로드할 수 없습니다")
    
    # 1-2단계: 정적 프로필 매칭 (간단한 버전)
    try:
        # 나이대 결정
        if request.age < 20:
            age_group = "10s"
        elif request.age < 30:
            age_group = "20s"
        elif request.age < 40:
            age_group = "30s"
        elif request.age < 50:
            age_group = "40s"
        elif request.age < 60:
            age_group = "50s"
        elif request.age < 70:
            age_group = "60s"
        else:
            age_group = "70s"
        
        # 세그먼트 ID
        segment_id = f"{age_group}_{request.gender}"
        
        # 정적 프로필 가져오기
        static_profile = static_profiles.get(segment_id, static_profiles.get("20s_남", {}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"사용자 프로필 매칭 실패: {str(e)}")
    
    # 사용자 입력을 딕셔너리로 변환
    user_input = {
        'age': request.age,
        'gender': request.gender,
        'income_level': request.income_level,
        'preferred_industries': request.preferred_industries,
        'time_period': request.time_period,
        'is_weekend': request.is_weekend,
        'preference_type': request.preference_type,
        'budget_range': request.budget_range,
        'location_preference': request.location_preference
    }
    
    # 3-5단계: 각 지역에 대해 이중 매칭 점수 계산
    recommendations = []
    
    for area_name, realtime_profile in profiles.items():
        try:
            # 4-1. 정적 매칭 점수 계산
            static_result = calculate_static_matching(static_profile, realtime_profile, user_input)
            
            # 4-2. 실시간 매칭 점수 계산
            realtime_result = calculate_realtime_matching(user_input, realtime_profile)
            
            # 5. 최종 점수 산출
            final_result = calculate_final_score(static_result, realtime_result, user_input, area_name)
            
            # 추천 이유 생성
            reasons = generate_reasons(static_profile, realtime_profile, user_input, final_result)
            
            recommendations.append({
                'rank': 0,  # 나중에 정렬 후 설정
                'region': area_name,
                'final_score': final_result['final_score'],
                'static_score': final_result['static_score'],
                'realtime_score': final_result['realtime_score'],
                'static_details': final_result['static_details'],
                'realtime_details': final_result['realtime_details'],
                'comprehensive_score': realtime_profile['scores']['comprehensive']['comprehensive_score'],
                'grade': realtime_profile['scores']['comprehensive']['grade'],
                'specialized_industries': list(realtime_profile['scores']['specialization']['all_scores'].keys()),
                'reasons': reasons
            })
        except Exception as e:
            print(f"⚠️ {area_name} 점수 계산 실패: {e}")
            continue
    
    # 6. 점수 순으로 정렬
    recommendations.sort(key=lambda x: x['final_score'], reverse=True)
    
    # 순위 설정
    for idx, rec in enumerate(recommendations, 1):
        rec['rank'] = idx
    
    # 상위 10개만 반환
    top_recommendations = recommendations[:10]
    
    return RecommendationResponse(
        recommendations=[
            RegionRecommendation(**rec) for rec in top_recommendations
        ],
        user_profile={
            'age': request.age,
            'gender': request.gender,
            'income_level': request.income_level,
            'matched_segment': static_profile['matching_info']['matched_segment_id'],
            'segment_description': f"{static_profile['segment_info']['age_group_kr']} {static_profile['segment_info']['gender_kr']}",
            'preferred_industries': request.preferred_industries,
            'time_period': request.time_period,
            'is_weekend': request.is_weekend,
            'preference_type': request.preference_type,
            'top_segment_industries': [ind['industry'] for ind in static_profile['industry_preferences'][:5]]
        }
    )

@app.get("/api/industries")
async def get_industries():
    """사용 가능한 업종 목록 조회"""
    characteristics, _ = load_data()
    
    if characteristics.empty:
        return []
    
    industries = characteristics['특화업종'].dropna().unique().tolist()
    return sorted(industries)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

