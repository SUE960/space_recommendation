"""
STEP 1: 사용자-세그먼트 매칭 시스템
================================================
사용자의 나이, 성별, 소득 정보를 입력받아 적절한 집단 프로필에 매칭합니다.

사용 예시:
    matcher = UserSegmentMatcher()
    profile = matcher.match_user(age=28, gender='남', income_level='중')
"""

import json
from pathlib import Path
from typing import Dict, Optional, List, Tuple


class UserSegmentMatcher:
    """사용자를 정적 집단 프로필에 매칭하는 클래스"""
    
    def __init__(self, profiles_dir: str = "outputs"):
        """
        초기화
        
        Args:
            profiles_dir: STEP 1에서 생성된 프로필이 있는 디렉토리
        """
        self.profiles_dir = Path(profiles_dir)
        
        # 프로필 데이터 로드
        self.profiles = self._load_profiles()
        self.time_patterns = self._load_time_patterns()
        self.matcher_info = self._load_matcher_info()
        
        # 소득 수준별 보정 계수 (추후 확장 가능)
        self.income_multipliers = {
            '저': 0.7,
            '중': 1.0,
            '고': 1.5
        }
        
        print(f"✅ 프로필 로딩 완료: {len(self.profiles)}개 세그먼트")
    
    def _load_profiles(self) -> Dict:
        """프로필 데이터 로드"""
        file_path = self.profiles_dir / "step1_static_profiles.json"
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"프로필 파일을 찾을 수 없습니다: {file_path}\n"
                "먼저 step1_static_profile_generation.py를 실행하세요."
            )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_time_patterns(self) -> Dict:
        """시간 패턴 데이터 로드"""
        file_path = self.profiles_dir / "step1_time_patterns.json"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_matcher_info(self) -> Dict:
        """매칭 정보 로드"""
        file_path = self.profiles_dir / "step1_segment_matcher.json"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _determine_age_group(self, age: int) -> str:
        """
        나이를 연령대 그룹으로 변환
        
        Args:
            age: 사용자 나이
            
        Returns:
            연령대 코드 (teen, 20s, 30s, ...)
        """
        if age < 20:
            return 'teen'
        elif 20 <= age < 30:
            return '20s'
        elif 30 <= age < 40:
            return '30s'
        elif 40 <= age < 50:
            return '40s'
        elif 50 <= age < 60:
            return '50s'
        elif 60 <= age < 70:
            return '60s'
        else:
            return '70plus'
    
    def _normalize_gender(self, gender: str) -> str:
        """
        성별을 표준 형식으로 변환
        
        Args:
            gender: 사용자 입력 성별 (남/여/male/female)
            
        Returns:
            표준 성별 코드 (male/female)
        """
        gender_lower = gender.lower()
        
        if gender_lower in ['남', 'male', 'm', '남자']:
            return 'male'
        elif gender_lower in ['여', 'female', 'f', '여자']:
            return 'female'
        else:
            raise ValueError(f"올바르지 않은 성별 값입니다: {gender}")
    
    def match_user(
        self, 
        age: int, 
        gender: str, 
        income_level: Optional[str] = '중'
    ) -> Dict:
        """
        사용자 정보를 바탕으로 해당하는 집단 프로필 반환
        
        Args:
            age: 사용자 나이
            gender: 성별 (남/여)
            income_level: 소득 수준 (저/중/고, 기본값: 중)
            
        Returns:
            매칭된 프로필 딕셔너리
        """
        # 1. 연령대 결정
        age_group = self._determine_age_group(age)
        
        # 2. 성별 정규화
        gender_normalized = self._normalize_gender(gender)
        
        # 3. 세그먼트 ID 생성
        segment_id = f"{age_group}_{gender_normalized}"
        
        # 4. 프로필 조회
        if segment_id not in self.profiles:
            available_segments = list(self.profiles.keys())
            raise ValueError(
                f"세그먼트를 찾을 수 없습니다: {segment_id}\n"
                f"사용 가능한 세그먼트: {available_segments}"
            )
        
        profile = self.profiles[segment_id].copy()
        
        # 5. 소득 수준에 따른 조정 (선택적)
        if income_level in self.income_multipliers:
            multiplier = self.income_multipliers[income_level]
            profile['income_adjustment'] = {
                'level': income_level,
                'multiplier': multiplier,
                'adjusted_avg_transaction': int(
                    profile['spending_characteristics']['avg_transaction_amount'] * multiplier
                )
            }
        
        # 6. 시간 패턴 추가
        profile['time_patterns'] = self.time_patterns
        
        # 7. 매칭 메타 정보 추가
        profile['matching_info'] = {
            'input_age': age,
            'input_gender': gender,
            'input_income_level': income_level,
            'matched_segment_id': segment_id,
            'matched_age_group': age_group,
            'matched_gender': gender_normalized
        }
        
        return profile
    
    def get_segment_summary(self, segment_id: str) -> Dict:
        """
        특정 세그먼트의 요약 정보 반환
        
        Args:
            segment_id: 세그먼트 ID (예: '30s_male')
            
        Returns:
            세그먼트 요약 정보
        """
        if segment_id not in self.matcher_info['segment_descriptions']:
            raise ValueError(f"세그먼트를 찾을 수 없습니다: {segment_id}")
        
        return self.matcher_info['segment_descriptions'][segment_id]
    
    def list_all_segments(self) -> List[Dict]:
        """
        모든 세그먼트 목록 반환
        
        Returns:
            세그먼트 목록 리스트
        """
        segments = []
        
        for segment_id, desc in self.matcher_info['segment_descriptions'].items():
            segments.append({
                'segment_id': segment_id,
                'description': desc['description_kr'],
                'total_spending': desc['total_spending'],
                'avg_transaction': desc['avg_transaction'],
                'primary_interest': desc['primary_interest']
            })
        
        return sorted(segments, key=lambda x: x['total_spending'], reverse=True)
    
    def get_top_industries_for_user(
        self, 
        age: int, 
        gender: str, 
        top_n: int = 5
    ) -> List[Dict]:
        """
        사용자의 주요 관심 업종 반환
        
        Args:
            age: 사용자 나이
            gender: 성별
            top_n: 반환할 상위 업종 개수
            
        Returns:
            상위 업종 리스트
        """
        profile = self.match_user(age, gender)
        
        return profile['industry_preferences'][:top_n]
    
    def get_region_recommendations_for_user(
        self, 
        age: int, 
        gender: str, 
        top_n: int = 5
    ) -> List[Dict]:
        """
        사용자에게 추천할 지역 반환
        
        Args:
            age: 사용자 나이
            gender: 성별
            top_n: 반환할 상위 지역 개수
            
        Returns:
            추천 지역 리스트
        """
        profile = self.match_user(age, gender)
        
        return profile['region_preferences'][:top_n]
    
    def compare_segments(
        self, 
        segment_id1: str, 
        segment_id2: str
    ) -> Dict:
        """
        두 세그먼트 비교
        
        Args:
            segment_id1: 첫 번째 세그먼트 ID
            segment_id2: 두 번째 세그먼트 ID
            
        Returns:
            비교 결과 딕셔너리
        """
        profile1 = self.profiles[segment_id1]
        profile2 = self.profiles[segment_id2]
        
        spending1 = profile1['spending_characteristics']
        spending2 = profile2['spending_characteristics']
        
        return {
            'segment1': {
                'id': segment_id1,
                'info': profile1['segment_info'],
                'total_spending': spending1['total_spending'],
                'avg_transaction': spending1['avg_transaction_amount'],
                'top_industry': profile1['industry_preferences'][0] if profile1['industry_preferences'] else None
            },
            'segment2': {
                'id': segment_id2,
                'info': profile2['segment_info'],
                'total_spending': spending2['total_spending'],
                'avg_transaction': spending2['avg_transaction_amount'],
                'top_industry': profile2['industry_preferences'][0] if profile2['industry_preferences'] else None
            },
            'spending_ratio': spending1['total_spending'] / spending2['total_spending'] if spending2['total_spending'] > 0 else 0,
            'transaction_ratio': spending1['avg_transaction_amount'] / spending2['avg_transaction_amount'] if spending2['avg_transaction_amount'] > 0 else 0
        }


def demo():
    """사용 예시 데모"""
    
    print("=" * 70)
    print("🎯 STEP 1 사용자-세그먼트 매칭 시스템 데모")
    print("=" * 70)
    
    # 매칭 시스템 초기화
    matcher = UserSegmentMatcher()
    
    # 예시 사용자들
    test_users = [
        {'age': 28, 'gender': '남', 'income_level': '중'},
        {'age': 35, 'gender': '여', 'income_level': '고'},
        {'age': 45, 'gender': '남', 'income_level': '중'},
        {'age': 18, 'gender': '여', 'income_level': '저'},
    ]
    
    print("\n👤 사용자별 매칭 결과:\n")
    
    for idx, user in enumerate(test_users, 1):
        print(f"[사용자 {idx}] {user['age']}세 {user['gender']} (소득: {user['income_level']})")
        
        # 매칭
        profile = matcher.match_user(**user)
        
        # 결과 출력
        info = profile['segment_info']
        spending = profile['spending_characteristics']
        matching = profile['matching_info']
        
        print(f"  ✓ 매칭 세그먼트: {info['age_group_kr']} {info['gender_kr']}")
        print(f"  ✓ 평균 거래액: {spending['avg_transaction_amount']:,}원")
        
        # 상위 3개 관심 업종
        print("  ✓ 주요 관심사:")
        for industry in profile['industry_preferences'][:3]:
            print(f"     - {industry['industry']} ({industry['preference_ratio']:.1f}%)")
        
        # 소득 조정이 있는 경우
        if 'income_adjustment' in profile:
            adj = profile['income_adjustment']
            print(f"  ✓ 소득 조정 거래액: {adj['adjusted_avg_transaction']:,}원")
        
        print()
    
    # 세그먼트 비교
    print("\n📊 세그먼트 비교 예시:")
    print("-" * 70)
    
    comparison = matcher.compare_segments('30s_male', '30s_female')
    
    seg1 = comparison['segment1']
    seg2 = comparison['segment2']
    
    print(f"\n[{seg1['info']['age_group_kr']} {seg1['info']['gender_kr']}] vs [{seg2['info']['age_group_kr']} {seg2['info']['gender_kr']}]")
    print(f"  소비액 비율: {comparison['spending_ratio']:.2f}배")
    print(f"  거래액 비율: {comparison['transaction_ratio']:.2f}배")
    print(f"  {seg1['info']['gender_kr']} 주요 관심사: {seg1['top_industry']['industry']}")
    print(f"  {seg2['info']['gender_kr']} 주요 관심사: {seg2['top_industry']['industry']}")
    
    # 전체 세그먼트 목록
    print("\n\n📋 전체 세그먼트 목록 (총 소비액 순):")
    print("-" * 70)
    
    all_segments = matcher.list_all_segments()
    
    for idx, seg in enumerate(all_segments, 1):
        print(f"{idx:2d}. {seg['description']:12s} | "
              f"총 소비: {seg['total_spending']:>15,}원 | "
              f"평균: {seg['avg_transaction']:>8,}원 | "
              f"관심: {seg['primary_interest']}")
    
    print("\n" + "=" * 70)
    print("✅ 데모 완료!")
    print("=" * 70)


if __name__ == "__main__":
    demo()





