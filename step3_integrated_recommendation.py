"""
STEP 3: 사용자-지역 매칭 시스템 (STEP 1 + STEP 2 통합)
================================================
STEP 1의 사용자 프로필과 STEP 2의 지역 점수를 결합하여
사용자에게 최적의 지역을 추천합니다.

통합 프로세스:
1. 사용자 정보 입력 (나이, 성별, 소득, 선호사항)
2. STEP 1: 사용자를 집단 프로필에 매칭
3. STEP 2: 실시간 지역 프로필 점수 로드
4. STEP 3: 사용자 선호도와 지역 특성 매칭
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class IntegratedRecommendationSystem:
    """STEP 1 + STEP 2 통합 추천 시스템"""
    
    def __init__(
        self, 
        step1_dir: str = "outputs",
        step2_file: Optional[str] = None
    ):
        """
        초기화
        
        Args:
            step1_dir: STEP 1 프로필이 저장된 디렉토리
            step2_file: STEP 2 지역 점수 파일 (JSON 또는 CSV)
        """
        from step1_user_matcher import UserSegmentMatcher
        
        self.step1_dir = Path(step1_dir)
        
        # STEP 1 매칭 시스템 초기화
        print("📥 STEP 1 사용자 프로필 로딩...")
        self.user_matcher = UserSegmentMatcher(step1_dir)
        
        # STEP 2 지역 점수 로드
        self.region_scores = {}
        if step2_file:
            print("📥 STEP 2 지역 점수 로딩...")
            self.region_scores = self._load_step2_scores(step2_file)
            print(f"✅ {len(self.region_scores)}개 지역 점수 로드 완료")
        else:
            print("⚠️  STEP 2 파일이 지정되지 않았습니다.")
            print("   지역 점수 없이 STEP 1 기반 추천만 제공됩니다.")
        
        # 업종 카테고리 매핑
        self.industry_categories = self._create_industry_categories()
    
    def _load_step2_scores(self, file_path: str) -> Dict:
        """
        STEP 2 지역 점수 파일 로드
        
        Args:
            file_path: 지역 점수 파일 경로
            
        Returns:
            지역별 점수 딕셔너리
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"STEP 2 파일을 찾을 수 없습니다: {file_path}")
        
        # JSON 형식
        if file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        
        # CSV 형식
        elif file_path.suffix == '.csv':
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # 지역명을 키로 사용
            if '구' in df.columns or 'region' in df.columns or 'gu' in df.columns:
                region_col = '구' if '구' in df.columns else ('region' if 'region' in df.columns else 'gu')
                return df.set_index(region_col).to_dict('index')
            else:
                return df.to_dict('index')
        
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {file_path.suffix}")
    
    def _create_industry_categories(self) -> Dict:
        """
        업종을 카테고리로 그룹화
        
        Returns:
            카테고리별 업종 매핑
        """
        return {
            '음식점': ['한식', '중식', '일식', '양식', '기타요식', '커피전문점', '제과점'],
            '쇼핑': ['대형마트', '편의점', '슈퍼마켓일반형', '슈퍼마켓기업형', '패션잡화', 
                    '생활잡화/수입상품점', '컴퓨터/소프트웨어', '가구', '가전제품'],
            '문화여가': ['영화/공연', '게임방/오락실', '노래방', '스포츠', '서점'],
            '생활서비스': ['미용실', '싸우나/목욕탕', '안마/마사지', '세탁소', '병원'],
            '교통': ['주유소', 'LPG가스', '자동차정비'],
            '기타': ['보험', '부동산', 'ZZ_나머지']
        }
    
    def recommend_regions(
        self,
        age: int,
        gender: str,
        income_level: str = '중',
        preferences: Optional[Dict] = None,
        top_n: int = 5,
        use_step2: bool = True
    ) -> Dict:
        """
        사용자에게 지역 추천
        
        Args:
            age: 사용자 나이
            gender: 성별 (남/여)
            income_level: 소득 수준 (저/중/고)
            preferences: 사용자 선호사항 딕셔너리
                {
                    'preferred_industries': ['한식', '커피전문점'],  # 선호 업종
                    'time_preference': '저녁',  # 주요 활동 시간대
                    'budget': 50000,  # 평균 예산
                    'priorities': {'price': 0.3, 'variety': 0.5, 'accessibility': 0.2}
                }
            top_n: 추천할 상위 지역 개수
            use_step2: STEP 2 점수 사용 여부
            
        Returns:
            추천 결과 딕셔너리
        """
        print("\n" + "=" * 70)
        print("🎯 사용자 맞춤 지역 추천 시작")
        print("=" * 70)
        
        # STEP 1: 사용자 프로필 매칭
        print(f"\n[STEP 1] 사용자 프로필 매칭 중...")
        print(f"  입력: {age}세 {gender}, 소득 수준: {income_level}")
        
        user_profile = self.user_matcher.match_user(age, gender, income_level)
        
        segment_info = user_profile['segment_info']
        spending = user_profile['spending_characteristics']
        
        print(f"  ✓ 매칭 세그먼트: {segment_info['age_group_kr']} {segment_info['gender_kr']}")
        print(f"  ✓ 평균 거래액: {spending['avg_transaction_amount']:,}원")
        
        # 사용자의 주요 관심 업종 (STEP 1 기반)
        user_industries = user_profile['industry_preferences'][:10]
        print(f"  ✓ 주요 관심 업종: {', '.join([ind['industry'] for ind in user_industries[:3]])}")
        
        # 선호사항 병합
        if preferences is None:
            preferences = {}
        
        # 기본 선호사항 설정
        if 'preferred_industries' not in preferences:
            preferences['preferred_industries'] = [ind['industry'] for ind in user_industries[:5]]
        
        if 'budget' not in preferences:
            preferences['budget'] = spending['avg_transaction_amount']
        
        if 'priorities' not in preferences:
            preferences['priorities'] = {'preference_match': 0.6, 'score': 0.4}
        
        # STEP 2: 지역 점수 기반 추천
        recommendations = []
        
        if use_step2 and self.region_scores:
            print(f"\n[STEP 2] 지역 점수 반영 중...")
            recommendations = self._calculate_step2_recommendations(
                user_profile, preferences, top_n
            )
        else:
            print(f"\n[STEP 1 전용] 사용자 선호 기반 추천...")
            recommendations = self._calculate_step1_recommendations(
                user_profile, preferences, top_n
            )
        
        # 결과 구성
        result = {
            'user_info': {
                'age': age,
                'gender': gender,
                'income_level': income_level,
                'matched_segment': f"{segment_info['age_group_kr']} {segment_info['gender_kr']}",
                'avg_budget': preferences['budget']
            },
            'preferences': preferences,
            'recommendations': recommendations,
            'recommendation_count': len(recommendations),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"\n✅ {len(recommendations)}개 지역 추천 완료!")
        
        return result
    
    def _calculate_step1_recommendations(
        self,
        user_profile: Dict,
        preferences: Dict,
        top_n: int
    ) -> List[Dict]:
        """
        STEP 1 전용: 사용자 선호 기반 지역 추천
        
        Args:
            user_profile: 사용자 프로필
            preferences: 사용자 선호사항
            top_n: 추천 개수
            
        Returns:
            추천 지역 리스트
        """
        # 사용자가 선호하는 업종이 많이 있는 지역 추천
        region_preferences = user_profile['region_preferences'][:top_n * 2]
        
        recommendations = []
        
        for idx, region in enumerate(region_preferences[:top_n], 1):
            region_code = region['region_code']
            
            # 행정동 코드를 구 이름으로 변환 (앞 5자리)
            gu_code = region_code[:5] if len(region_code) >= 5 else region_code
            
            # 구 이름 매핑 (임시)
            gu_name = self._get_gu_name_from_code(gu_code)
            
            recommendation = {
                'rank': idx,
                'region_code': region_code,
                'gu_name': gu_name,
                'match_score': 100 - (idx - 1) * 10,  # 단순 순위 기반 점수
                'reason': f"해당 지역에서 {region['visit_count']:,}회 방문 기록",
                'spending_amount': region['spending_amount'],
                'visit_count': region['visit_count'],
                'matching_factors': {
                    'user_preference': 100 - (idx - 1) * 10,
                    'visit_frequency': min(100, region['visit_count'] / 100)
                }
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_step2_recommendations(
        self,
        user_profile: Dict,
        preferences: Dict,
        top_n: int
    ) -> List[Dict]:
        """
        STEP 2 포함: 사용자 선호도 + 지역 점수 통합 추천
        
        Args:
            user_profile: 사용자 프로필
            preferences: 사용자 선호사항
            top_n: 추천 개수
            
        Returns:
            추천 지역 리스트
        """
        # 가중치
        w_preference = preferences['priorities'].get('preference_match', 0.6)
        w_score = preferences['priorities'].get('score', 0.4)
        
        # 지역별 점수 계산
        region_scores_list = []
        
        for region_name, region_data in self.region_scores.items():
            # 1. 사용자 선호도 점수
            preference_score = self._calculate_preference_score(
                user_profile, region_name, region_data, preferences
            )
            
            # 2. STEP 2 지역 점수
            step2_score = self._extract_step2_score(region_data)
            
            # 3. 통합 점수
            total_score = w_preference * preference_score + w_score * step2_score
            
            region_scores_list.append({
                'region_name': region_name,
                'region_data': region_data,
                'preference_score': preference_score,
                'step2_score': step2_score,
                'total_score': total_score
            })
        
        # 점수 기준 정렬
        region_scores_list.sort(key=lambda x: x['total_score'], reverse=True)
        
        # 상위 N개 지역 추천
        recommendations = []
        
        for idx, region_info in enumerate(region_scores_list[:top_n], 1):
            recommendation = {
                'rank': idx,
                'region_name': region_info['region_name'],
                'match_score': round(region_info['total_score'], 2),
                'preference_score': round(region_info['preference_score'], 2),
                'step2_score': round(region_info['step2_score'], 2),
                'reason': self._generate_recommendation_reason(
                    user_profile, region_info, preferences
                ),
                'region_details': region_info['region_data']
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_preference_score(
        self,
        user_profile: Dict,
        region_name: str,
        region_data: Dict,
        preferences: Dict
    ) -> float:
        """
        사용자 선호도 점수 계산
        
        Args:
            user_profile: 사용자 프로필
            region_name: 지역명
            region_data: 지역 데이터
            preferences: 사용자 선호사항
            
        Returns:
            선호도 점수 (0-100)
        """
        score = 40.0  # 기본 점수
        
        # 사용자의 주요 관심 업종
        user_industries = {ind['industry']: ind['preference_ratio'] 
                          for ind in user_profile['industry_preferences'][:10]}
        
        preferred_industries = preferences.get('preferred_industries', [])
        
        # 1. 지역의 특화 업종과 사용자 선호 업종 매칭
        if '특징' in region_data:
            region_specialty = str(region_data['특징'])
            
            # 특화 업종 추출 (예: "한식 특화 (78.2%)")
            for industry in user_industries.keys():
                if industry in region_specialty:
                    # 사용자의 해당 업종 선호도에 비례하여 점수 추가
                    score += user_industries[industry] * 0.5
                    break
            
            # 사용자가 명시적으로 선호한 업종과 매칭
            for pref_ind in preferred_industries:
                if pref_ind in region_specialty:
                    score += 15
                    break
        
        # 2. 업종 다양성과 사용자 성향 매칭
        if '업종다양성' in region_data:
            diversity = str(region_data['업종다양성'])
            
            # 다양성을 선호하는지 체크 (사용자의 관심 업종 수가 많으면 다양성 선호)
            user_diversity_pref = len(user_industries) > 5
            
            if user_diversity_pref:
                if '높음' in diversity or '보통' in diversity:
                    score += 10
            else:
                # 특정 업종에 집중된 사용자는 특화된 지역 선호
                if '특화' in str(region_data.get('특징', '')):
                    score += 10
        
        # 3. 성장세와 연령대 매칭
        if '성장률' in region_data:
            growth = str(region_data['성장률'])
            age_group = user_profile['segment_info']['age_group']
            
            # 젊은 세대는 성장하는 지역 선호
            if age_group in ['teen', '20s', '30s']:
                if '↑상승' in growth or '+' in growth:
                    score += 15
            else:
                # 중장년층은 안정적인 지역 선호
                if '→유지' in growth or '안정적' in str(region_data.get('소비안정성', '')):
                    score += 10
        
        # 4. 소득 수준과 지역 매칭 (소득 조정 반영)
        if 'income_adjustment' in user_profile:
            income_level = user_profile['income_adjustment']['level']
            
            # 고소득자는 다양성 높은 지역 선호
            if income_level == '고':
                diversity_str = str(region_data.get('업종다양성', ''))
                import re
                match = re.search(r'\((\d+)개\)', diversity_str)
                if match and int(match.group(1)) > 10:
                    score += 10
        
        return min(100.0, max(0.0, score))
    
    def _extract_step2_score(self, region_data: Dict) -> float:
        """
        STEP 2에서 계산된 지역 점수 추출
        
        Args:
            region_data: 지역 데이터
            
        Returns:
            지역 점수 (0-100)
        """
        # STEP 2 파일 구조에 맞게 점수 추출
        # 가능한 키: 'score', 'total_score', '종합점수' 등
        
        score_keys = ['score', 'total_score', '종합점수', 'final_score', 'overall_score']
        
        for key in score_keys:
            if key in region_data:
                score = region_data[key]
                # 점수 정규화 (0-100 범위로)
                if score > 100:
                    score = score / 10  # 1000점 만점이면 10으로 나누기
                return float(score)
        
        # CSV 데이터에서 점수 계산 (업종다양성, 소비안정성, 성장률 기반)
        score = 50.0  # 기본값
        
        # 업종다양성 점수
        if '업종다양성' in region_data:
            diversity = region_data['업종다양성']
            if '높음' in str(diversity):
                score += 15
            elif '보통' in str(diversity):
                score += 7
            elif '낮음' in str(diversity):
                score -= 5
            
            # 숫자 추출 (예: "보통(14개)" -> 14)
            import re
            match = re.search(r'\((\d+)개\)', str(diversity))
            if match:
                num_industries = int(match.group(1))
                # 업종 수에 비례하여 점수 추가 (최대 20점)
                score += min(20, num_industries * 1.5)
        
        # 소비안정성 점수
        if '소비안정성' in region_data:
            stability = region_data['소비안정성']
            if '안정적' in str(stability):
                score += 10
            elif '보통' in str(stability):
                score += 5
        
        # 성장률 점수
        if '성장률' in region_data:
            growth = str(region_data['성장률'])
            if '↑상승' in growth or '+' in growth:
                score += 15
            elif '→유지' in growth:
                score += 5
            elif '↓하락' in growth or '-' in growth:
                score -= 10
        
        return min(100.0, max(0.0, score))
    
    def _generate_recommendation_reason(
        self,
        user_profile: Dict,
        region_info: Dict,
        preferences: Dict
    ) -> str:
        """
        추천 이유 생성
        
        Args:
            user_profile: 사용자 프로필
            region_info: 지역 정보
            preferences: 사용자 선호사항
            
        Returns:
            추천 이유 문자열
        """
        segment = user_profile['segment_info']
        top_industries = user_profile['industry_preferences'][:3]
        
        reasons = []
        
        # 세그먼트 기반 추천 이유
        reasons.append(f"{segment['age_group_kr']} {segment['gender_kr']}에게 인기")
        
        # 선호 업종 매칭
        if top_industries:
            top_industry = top_industries[0]['industry']
            reasons.append(f"{top_industry} 관심사에 적합")
        
        # 지역 점수 기반
        if region_info['step2_score'] >= 70:
            reasons.append("실시간 활성도가 높은 지역")
        
        return ", ".join(reasons)
    
    def _get_gu_name_from_code(self, gu_code: str) -> str:
        """
        행정동 코드에서 구 이름 추출
        
        Args:
            gu_code: 행정동 코드 (앞 5자리)
            
        Returns:
            구 이름
        """
        # 서울시 구 코드 매핑
        gu_code_map = {
            '11110': '종로구', '11140': '중구', '11170': '용산구',
            '11200': '성동구', '11215': '광진구', '11230': '동대문구',
            '11260': '중랑구', '11290': '성북구', '11305': '강북구',
            '11320': '도봉구', '11350': '노원구', '11380': '은평구',
            '11410': '서대문구', '11440': '마포구', '11470': '양천구',
            '11500': '강서구', '11530': '구로구', '11545': '금천구',
            '11560': '영등포구', '11590': '동작구', '11620': '관악구',
            '11650': '서초구', '11680': '강남구', '11710': '송파구',
            '11740': '강동구'
        }
        
        return gu_code_map.get(gu_code, f"코드{gu_code}")
    
    def save_recommendations(self, result: Dict, output_file: str = None):
        """
        추천 결과 저장
        
        Args:
            result: 추천 결과 딕셔너리
            output_file: 출력 파일 경로 (없으면 자동 생성)
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"outputs/recommendation_{timestamp}.json"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 추천 결과 저장: {output_path}")
    
    def print_recommendations(self, result: Dict):
        """
        추천 결과 출력
        
        Args:
            result: 추천 결과 딕셔너리
        """
        print("\n" + "=" * 70)
        print("🎁 추천 결과")
        print("=" * 70)
        
        user = result['user_info']
        print(f"\n[사용자 정보]")
        print(f"  • 나이: {user['age']}세")
        print(f"  • 성별: {user['gender']}")
        print(f"  • 소득 수준: {user['income_level']}")
        print(f"  • 매칭 세그먼트: {user['matched_segment']}")
        print(f"  • 평균 예산: {user['avg_budget']:,}원")
        
        print(f"\n[추천 지역 TOP {len(result['recommendations'])}]")
        print("-" * 70)
        
        for rec in result['recommendations']:
            print(f"\n{rec['rank']}위. {rec.get('region_name', rec.get('gu_name', 'Unknown'))}")
            print(f"   매칭 점수: {rec['match_score']:.1f}점")
            
            if 'preference_score' in rec:
                print(f"   - 선호도 점수: {rec['preference_score']:.1f}점")
                print(f"   - 지역 점수: {rec['step2_score']:.1f}점")
            
            print(f"   이유: {rec['reason']}")
        
        print("\n" + "=" * 70)


def demo():
    """통합 시스템 데모"""
    
    print("=" * 70)
    print("🚀 STEP 3: 통합 추천 시스템 데모")
    print("=" * 70)
    
    # 시스템 초기화
    # STEP 2 파일이 있다면 경로 지정, 없으면 None
    step2_file = None
    
    # STEP 2 파일 찾기 시도
    possible_step2_files = [
        "outputs/gu_score_table.csv",
        "outputs/comprehensive_summary.json",
        "outputs/step2_region_scores.json"
    ]
    
    for file_path in possible_step2_files:
        if Path(file_path).exists():
            step2_file = file_path
            break
    
    system = IntegratedRecommendationSystem(
        step1_dir="outputs",
        step2_file=step2_file
    )
    
    print("\n" + "=" * 70)
    print("📝 사용자 시나리오")
    print("=" * 70)
    
    # 테스트 사용자
    test_user = {
        'age': 28,
        'gender': '남',
        'income_level': '중',
        'preferences': {
            'preferred_industries': ['한식', '커피전문점', '영화/공연'],
            'time_preference': '저녁',
            'budget': 30000,
            'priorities': {'preference_match': 0.7, 'score': 0.3}
        }
    }
    
    # 추천 실행
    result = system.recommend_regions(**test_user, top_n=5)
    
    # 결과 출력
    system.print_recommendations(result)
    
    # 결과 저장
    system.save_recommendations(result)
    
    print("\n✅ 데모 완료!")


if __name__ == "__main__":
    demo()

