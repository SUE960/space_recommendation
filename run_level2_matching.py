#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEP 3: Level 2 매칭 시스템 실제 적용
5개 대표 구 × 3개 페르소나 매칭 검증
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime


# ============================================================================
# 5개 대표 구 상세 프로필
# ============================================================================

REPRESENTATIVE_GUS = {
    '중구': {
        # Level 1 점수
        '종합점수': 66.9,
        '상업활동점수': 79.6,
        '특화도점수': 70.0,
        '인구통계점수': 49.1,
        '경제력점수': 62.8,
        
        # Level 2용 상세 데이터
        '평균소득': 4500000,
        '인구통계': {
            '10대': 5,
            '20대': 20,
            '30대': 28,
            '40대': 25,
            '50대': 12,
            '60대이상': 10
        },
        '성별분포': {'남성': 52, '여성': 48},
        '소비패턴': {
            '식료품': 28.0,
            '의류신발': 15.0,
            '생활용품': 8.0,
            '의료': 10.0,
            '교통': 18.0,
            '여가': 5.0,
            '문화': 8.0,
            '교육': 5.0,
            '오락': 3.0
        },
        '특화업종': ['금융', '업무시설', '호텔', '백화점'],
        '특징': '비즈니스 중심지, 업종 다양성 최고'
    },
    
    '강남구': {
        '종합점수': 59.4,
        '상업활동점수': 70.9,
        '특화도점수': 51.4,
        '인구통계점수': 49.8,
        '경제력점수': 61.2,
        
        '평균소득': 5800000,
        '인구통계': {
            '10대': 12,
            '20대': 22,
            '30대': 32,
            '40대': 20,
            '50대': 10,
            '60대이상': 4
        },
        '성별분포': {'남성': 48, '여성': 52},
        '소비패턴': {
            '식료품': 22.0,
            '의류신발': 18.0,
            '생활용품': 7.0,
            '의료': 12.0,
            '교통': 12.0,
            '여가': 8.0,
            '문화': 6.0,
            '교육': 12.0,
            '오락': 3.0
        },
        '특화업종': ['학원', '학습지', '고급레스토랑', '명품매장'],
        '특징': '고소득층, 교육·자기계발 중심'
    },
    
    '마포구': {  # 홍대
        '종합점수': 64.8,
        '상업활동점수': 57.8,
        '특화도점수': 72.7,
        '인구통계점수': 48.6,
        '경제력점수': 78.3,
        
        '평균소득': 3200000,
        '인구통계': {
            '10대': 8,
            '20대': 42,
            '30대': 28,
            '40대': 12,
            '50대': 7,
            '60대이상': 3
        },
        '성별분포': {'남성': 52, '여성': 48},
        '소비패턴': {
            '식료품': 26.0,
            '의류신발': 16.0,
            '생활용품': 6.0,
            '의료': 5.0,
            '교통': 10.0,
            '여가': 12.0,
            '문화': 18.0,
            '교육': 4.0,
            '오락': 3.0
        },
        '특화업종': ['카페', '술집', '클럽', '공연장', '독립서점'],
        '특징': '젊은 문화 중심지, 2030 밀집'
    },
    
    '영등포구': {
        '종합점수': 64.1,
        '상업활동점수': 48.1,
        '특화도점수': 80.2,
        '인구통계점수': 48.2,
        '경제력점수': 80.0,
        
        '평균소득': 4200000,
        '인구통계': {
            '10대': 10,
            '20대': 25,
            '30대': 30,
            '40대': 20,
            '50대': 10,
            '60대이상': 5
        },
        '성별분포': {'남성': 54, '여성': 46},
        '소비패턴': {
            '식료품': 30.0,
            '의류신발': 12.0,
            '생활용품': 8.0,
            '의료': 8.0,
            '교통': 20.0,
            '여가': 6.0,
            '문화': 5.0,
            '교육': 8.0,
            '오락': 3.0
        },
        '특화업종': ['비즈니스 레스토랑', '프랜차이즈', '편의점'],
        '특징': '직장인 밀집, 평일 중심 상권'
    },
    
    '서초구': {
        '종합점수': 64.0,
        '상업활동점수': 54.5,
        '특화도점수': 96.8,
        '인구통계점수': 40.2,
        '경제력점수': 61.6,
        
        '평균소득': 6200000,
        '인구통계': {
            '10대': 15,
            '20대': 18,
            '30대': 28,
            '40대': 24,
            '50대': 12,
            '60대이상': 3
        },
        '성별분포': {'남성': 49, '여성': 51},
        '소비패턴': {
            '식료품': 32.0,
            '의류신발': 14.0,
            '생활용품': 10.0,
            '의료': 12.0,
            '교통': 10.0,
            '여가': 8.0,
            '문화': 6.0,
            '교육': 6.0,
            '오락': 2.0
        },
        '특화업종': ['한식', '고급레스토랑', '병원', '학원'],
        '특징': '고급 주거지, 가족 단위 소비'
    }
}


# ============================================================================
# 3개 페르소나 정의
# ============================================================================

PERSONAS = {
    '20대_대학생': {
        '이름': '20대 대학생 김민수',
        '나이': 23,
        '성별': '남성',
        '소득': 2500000,
        '소비패턴': {
            '식료품': 28,
            '의류신발': 12,
            '생활용품': 5,
            '의료': 3,
            '교통': 15,
            '여가': 10,
            '문화': 20,
            '교육': 5,
            '오락': 2
        },
        '선호업종': ['카페', '술집', '클럽', '영화관', '패스트푸드'],
        '특성': '문화·오락 중심, 저렴한 가격 선호, 친구들과 시간 보내기'
    },
    
    '40대_직장인': {
        '이름': '40대 직장인 박영희',
        '나이': 42,
        '성별': '여성',
        '소득': 5500000,
        '소비패턴': {
            '식료품': 32,
            '의류신발': 15,
            '생활용품': 8,
            '의료': 10,
            '교통': 18,
            '여가': 5,
            '문화': 4,
            '교육': 6,
            '오락': 2
        },
        '선호업종': ['레스토랑', '카페', '헬스장', '백화점', '서점'],
        '특성': '점심·저녁 외식, 업무 관련 소비, 자기계발'
    },
    
    '30대_맞벌이부부': {
        '이름': '30대 맞벌이 부부 이지훈·최수진',
        '나이': 35,
        '성별': '부부',
        '소득': 8000000,
        '소비패턴': {
            '식료품': 35,
            '의류신발': 12,
            '생활용품': 12,
            '의료': 10,
            '교통': 8,
            '여가': 8,
            '문화': 6,
            '교육': 7,
            '오락': 2
        },
        '선호업종': ['대형마트', '백화점', '레스토랑', '키즈카페', '학원'],
        '특성': '가족 단위 소비, 편의성 중시, 교육 관심 높음'
    }
}


# ============================================================================
# 매칭 계산 함수
# ============================================================================

def calculate_demographic_matching(persona, gu_profile):
    """인구통계 매칭 (40%)"""
    
    # 연령대 매칭
    age = persona['나이']
    if age < 20:
        age_group = '10대'
    elif age < 30:
        age_group = '20대'
    elif age < 40:
        age_group = '30대'
    elif age < 50:
        age_group = '40대'
    elif age < 60:
        age_group = '50대'
    else:
        age_group = '60대이상'
    
    gu_age_ratio = gu_profile['인구통계'].get(age_group, 0)
    age_score = min(gu_age_ratio * 2, 100)  # 50% 이상이면 만점
    
    # 성별 매칭 (부부는 50점)
    if persona['성별'] == '부부':
        gender_score = 50
    else:
        gender_score = gu_profile['성별분포'].get(persona['성별'], 50)
    
    # 가중 평균 (연령 80%, 성별 20%)
    demo_score = age_score * 0.8 + gender_score * 0.2
    
    return min(demo_score, 100)


def calculate_consumption_matching(persona, gu_profile):
    """소비패턴 매칭 - 코사인 유사도 (35%)"""
    
    # 공통 카테고리
    categories = ['식료품', '의류신발', '생활용품', '의료', '교통', '여가', '문화', '교육', '오락']
    
    user_vector = [persona['소비패턴'].get(cat, 0) for cat in categories]
    gu_vector = [gu_profile['소비패턴'].get(cat, 0) for cat in categories]
    
    # 코사인 유사도
    dot_product = sum(u * g for u, g in zip(user_vector, gu_vector))
    user_norm = np.sqrt(sum(u**2 for u in user_vector))
    gu_norm = np.sqrt(sum(g**2 for g in gu_vector))
    
    if user_norm == 0 or gu_norm == 0:
        return 50
    
    similarity = dot_product / (user_norm * gu_norm)
    
    return similarity * 100


def calculate_income_matching(persona, gu_profile):
    """소득수준 매칭 (15%)"""
    
    user_income = persona['소득']
    gu_income = gu_profile['평균소득']
    
    ratio = user_income / gu_income
    
    if 0.8 <= ratio <= 1.2:  # ±20% 이내
        return 100
    elif 0.6 <= ratio < 0.8 or 1.2 < ratio <= 1.5:  # ±50% 이내
        return 70
    else:
        return 40


def calculate_industry_matching(persona, gu_profile):
    """업종선호 매칭 (10%)"""
    
    user_prefs = set(persona['선호업종'])
    gu_industries = set(gu_profile['특화업종'])
    
    if not user_prefs:
        return 50
    
    matches = len(user_prefs & gu_industries)
    match_ratio = matches / len(user_prefs)
    
    return match_ratio * 100


def calculate_matching_score(persona, gu_profile):
    """Level 2 매칭 점수 계산"""
    
    demo = calculate_demographic_matching(persona, gu_profile)
    consumption = calculate_consumption_matching(persona, gu_profile)
    income = calculate_income_matching(persona, gu_profile)
    industry = calculate_industry_matching(persona, gu_profile)
    
    matching_score = (
        demo * 0.40 +
        consumption * 0.35 +
        income * 0.15 +
        industry * 0.10
    )
    
    return {
        'matching_score': round(matching_score, 1),
        'demo': round(demo, 1),
        'consumption': round(consumption, 1),
        'income': round(income, 1),
        'industry': round(industry, 1)
    }


def calculate_final_score(gu_name, gu_profile, matching_result):
    """최종 추천 점수"""
    
    quality_score = gu_profile['종합점수']
    matching_score = matching_result['matching_score']
    
    final_score = (quality_score / 100) * matching_score
    
    return round(final_score, 1)


# ============================================================================
# 추천 이유 생성
# ============================================================================

def generate_recommendation_reason(persona_name, gu_name, gu_profile, matching_result):
    """추천 이유 자동 생성"""
    
    reasons = []
    
    # 매칭 점수 기반
    if matching_result['demo'] >= 80:
        reasons.append(f"같은 연령대가 많이 방문하는 지역")
    
    if matching_result['consumption'] >= 80:
        reasons.append(f"소비 취향이 잘 맞음")
    
    if matching_result['income'] >= 80:
        reasons.append(f"가격대가 적절함")
    
    if matching_result['industry'] >= 70:
        reasons.append(f"선호하는 업종이 많음")
    
    # 지역 특성 기반
    reasons.append(gu_profile['특징'])
    
    return reasons


# ============================================================================
# 메인 실행
# ============================================================================

def main():
    """메인 실행 함수"""
    
    print("="*100)
    print("STEP 3: Level 2 매칭 시스템 - 5개 대표 구 × 3개 페르소나")
    print("="*100)
    
    all_results = []
    
    for persona_key, persona in PERSONAS.items():
        print(f"\n{'='*100}")
        print(f"👤 페르소나: {persona['이름']}")
        print(f"{'='*100}")
        print(f"나이: {persona['나이']}세 | 소득: {persona['소득']:,}원 | 특성: {persona['특성']}")
        
        persona_results = []
        
        for gu_name, gu_profile in REPRESENTATIVE_GUS.items():
            # Level 2 매칭 계산
            matching_result = calculate_matching_score(persona, gu_profile)
            
            # 최종 점수
            final_score = calculate_final_score(gu_name, gu_profile, matching_result)
            
            # 추천 이유
            reasons = generate_recommendation_reason(persona['이름'], gu_name, gu_profile, matching_result)
            
            persona_results.append({
                '페르소나': persona['이름'],
                '구': gu_name,
                'L1_품질점수': gu_profile['종합점수'],
                'L2_매칭점수': matching_result['matching_score'],
                '최종점수': final_score,
                '인구통계': matching_result['demo'],
                '소비패턴': matching_result['consumption'],
                '소득수준': matching_result['income'],
                '업종선호': matching_result['industry'],
                '추천이유': ' / '.join(reasons[:3])
            })
        
        # 정렬
        persona_results.sort(key=lambda x: x['최종점수'], reverse=True)
        
        # 출력
        print(f"\n📍 추천 순위:")
        print(f"\n{'순위':<4} {'구':<10} {'최종점수':<10} {'L1품질':<10} {'L2매칭':<10} {'주요 매칭 지표':<40}")
        print("-" * 100)
        
        for idx, result in enumerate(persona_results, 1):
            result['순위'] = idx
            print(f"{idx:<4} {result['구']:<10} "
                  f"{result['최종점수']:>8.1f}  "
                  f"{result['L1_품질점수']:>8.1f}  "
                  f"{result['L2_매칭점수']:>8.1f}  "
                  f"인구{result['인구통계']:.0f} 소비{result['소비패턴']:.0f} "
                  f"소득{result['소득수준']:.0f} 업종{result['업종선호']:.0f}")
        
        print(f"\n🥇 TOP 1 추천: {persona_results[0]['구']}")
        print(f"   이유: {persona_results[0]['추천이유']}")
        
        all_results.extend(persona_results)
    
    # 저장
    save_results(all_results)
    
    # 최종 요약
    print(f"\n{'='*100}")
    print("✅ STEP 3 완료: Level 2 매칭 시스템 검증 성공!")
    print(f"{'='*100}")
    
    return all_results


def save_results(results):
    """결과 저장"""
    
    os.makedirs('outputs', exist_ok=True)
    
    # CSV 저장
    df = pd.DataFrame(results)
    csv_file = 'outputs/level2_matching_results.csv'
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV 저장: {csv_file}")
    
    # Markdown 저장
    md_file = 'outputs/Level2_매칭결과_5개구.md'
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# STEP 3: Level 2 매칭 결과\n\n")
        f.write(f"**생성일시:** {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n\n")
        f.write("**분석 대상:** 5개 대표 구 × 3개 페르소나\n\n")
        f.write("---\n\n")
        
        for persona_name in ['20대 대학생 김민수', '40대 직장인 박영희', '30대 맞벌이 부부 이지훈·최수진']:
            persona_data = [r for r in results if r['페르소나'] == persona_name]
            
            f.write(f"## 👤 {persona_name}\n\n")
            f.write("| 순위 | 구 | 최종점수 | L1품질 | L2매칭 | 인구통계 | 소비패턴 | 소득수준 | 업종선호 |\n")
            f.write("|:----:|:---|:--------:|:------:|:------:|:--------:|:--------:|:--------:|:--------:|\n")
            
            for result in persona_data:
                f.write(f"| {result['순위']} | {result['구']} | **{result['최종점수']:.1f}** | "
                       f"{result['L1_품질점수']:.1f} | {result['L2_매칭점수']:.1f} | "
                       f"{result['인구통계']:.1f} | {result['소비패턴']:.1f} | "
                       f"{result['소득수준']:.1f} | {result['업종선호']:.1f} |\n")
            
            f.write(f"\n**🥇 TOP 1 추천:** {persona_data[0]['구']}\n\n")
            f.write(f"**추천 이유:** {persona_data[0]['추천이유']}\n\n")
            f.write("---\n\n")
    
    print(f"✓ Markdown 저장: {md_file}")


if __name__ == '__main__':
    results = main()




