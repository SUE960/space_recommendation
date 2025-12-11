#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
연령대별 적합 지역 추천 시스템
================================================
각 연령대의 라이프스타일과 선호도에 맞는 지역을 추천합니다.

핵심 개선사항:
- 50세에게 홍대 대신 적절한 지역 추천
- 연령대별 라이프스타일 고려
- 지역 특성과 연령대 매칭
"""

from typing import Dict, List, Tuple
import pandas as pd
import json
from pathlib import Path


class AgeAppropriateRecommender:
    """연령대별 적합 지역 추천 시스템"""
    
    def __init__(self):
        # 연령대별 선호 특성 정의
        self.age_preferences = self._define_age_preferences()
        
        # 지역별 연령 적합도 정의
        self.region_age_suitability = self._define_region_age_suitability()
    
    def _define_age_preferences(self) -> Dict:
        """
        연령대별 선호 특성 정의
        
        Returns:
            연령대별 선호 특성 딕셔너리
        """
        return {
            '10대': {
                'lifestyle': '학업 중심, 문화생활',
                'preferred_industries': ['게임방/오락실', '편의점', '패스트푸드', '카페', '영화관'],
                'atmosphere': ['활기찬', '트렌디한', '젊은'],
                'spending_level': '낮음',
                'time_preference': '방과후(15-22시)',
                'suitable_regions': ['강남역', '홍대', '신촌', '명동', '코엑스']
            },
            '20대': {
                'lifestyle': '사회 초년생, 문화/여가 활동',
                'preferred_industries': ['카페', '술집', '클럽', '영화관', '노래방', '패션'],
                'atmosphere': ['활기찬', '트렌디한', '다양한'],
                'spending_level': '중하',
                'time_preference': '저녁/밤(18-24시)',
                'suitable_regions': ['홍대', '강남역', '이태원', '건대', '신촌', '성수']
            },
            '30대': {
                'lifestyle': '직장인, 가족 형성기',
                'preferred_industries': ['레스토랑', '카페', '헬스장', '학원', '서점', '영화관'],
                'atmosphere': ['세련된', '편안한', '실용적인'],
                'spending_level': '중상',
                'time_preference': '저녁(18-22시)',
                'suitable_regions': ['강남역', '서초', '잠실', '여의도', '판교', '성수']
            },
            '40대': {
                'lifestyle': '중년 직장인, 자녀 양육',
                'preferred_industries': ['한식당', '학원', '카페', '백화점', '골프장', '등산용품'],
                'atmosphere': ['안정적인', '품격있는', '가족친화적인'],
                'spending_level': '상',
                'time_preference': '저녁(17-21시)',
                'suitable_regions': ['서초', '강남', '잠실', '여의도', '청담', '압구정']
            },
            '50대': {
                'lifestyle': '중장년, 건강/여가 중시',
                'preferred_industries': ['한식당', '골프장', '헬스장', '백화점', '전통시장', '카페'],
                'atmosphere': ['안정적인', '전통적인', '고급스러운', '조용한'],
                'spending_level': '상',
                'time_preference': '낮/저녁(11-20시)',
                'suitable_regions': ['종로', '인사동', '서초', '강남', '청담', '압구정', '잠실']
            },
            '60대이상': {
                'lifestyle': '은퇴/반은퇴, 건강/문화 중시',
                'preferred_industries': ['한식당', '전통시장', '병원', '약국', '공원', '문화센터'],
                'atmosphere': ['조용한', '전통적인', '접근성좋은'],
                'spending_level': '중',
                'time_preference': '낮(10-18시)',
                'suitable_regions': ['종로', '인사동', '남대문', '동대문', '강동', '송파']
            }
        }
    
    def _define_region_age_suitability(self) -> Dict:
        """
        지역별 연령 적합도 정의
        
        Returns:
            지역별 연령 적합도 점수 (0-100)
        """
        return {
            # 젊은 층(10-20대) 특화 지역
            '홍대': {'10대': 90, '20대': 100, '30대': 70, '40대': 40, '50대': 20, '60대이상': 10},
            '강남역': {'10대': 85, '20대': 95, '30대': 90, '40대': 70, '50대': 60, '60대이상': 40},
            '이태원': {'10대': 70, '20대': 95, '30대': 85, '40대': 60, '50대': 40, '60대이상': 20},
            '건대': {'10대': 95, '20대': 100, '30대': 70, '40대': 40, '50대': 20, '60대이상': 10},
            '신촌': {'10대': 90, '20대': 95, '30대': 60, '40대': 35, '50대': 20, '60대이상': 15},
            '명동': {'10대': 85, '20대': 80, '30대': 70, '40대': 60, '50대': 50, '60대이상': 40},
            '성수': {'10대': 70, '20대': 90, '30대': 95, '40대': 75, '50대': 60, '60대이상': 40},
            
            # 중장년층(30-50대) 특화 지역
            '서초': {'10대': 40, '20대': 50, '30대': 85, '40대': 95, '50대': 95, '60대이상': 75},
            '강남': {'10대': 60, '20대': 75, '30대': 90, '40대': 95, '50대': 95, '60대이상': 70},
            '청담': {'10대': 30, '20대': 60, '30대': 85, '40대': 95, '50대': 95, '60대이상': 70},
            '압구정': {'10대': 40, '20대': 65, '30대': 85, '40대': 95, '50대': 95, '60대이상': 75},
            '여의도': {'10대': 35, '20대': 70, '30대': 90, '40대': 95, '50대': 90, '60대이상': 70},
            '잠실': {'10대': 70, '20대': 75, '30대': 90, '40대': 95, '50대': 90, '60대이상': 80},
            
            # 전통/중장년층(50-60대이상) 특화 지역
            '종로': {'10대': 50, '20대': 55, '30대': 70, '40대': 85, '50대': 95, '60대이상': 100},
            '인사동': {'10대': 40, '20대': 50, '30대': 70, '40대': 85, '50대': 95, '60대이상': 100},
            '남대문': {'10대': 45, '20대': 50, '30대': 65, '40대': 80, '50대': 90, '60대이상': 95},
            '동대문': {'10대': 60, '20대': 70, '30대': 75, '40대': 85, '50대': 90, '60대이상': 90},
            
            # 전 연령 적합 지역
            '코엑스': {'10대': 80, '20대': 85, '30대': 90, '40대': 85, '50대': 80, '60대이상': 70},
            '롯데월드': {'10대': 90, '20대': 85, '30대': 90, '40대': 90, '50대': 80, '60대이상': 70},
        }
    
    def get_age_group(self, age: int) -> str:
        """
        나이를 연령대로 변환
        
        Args:
            age: 나이
            
        Returns:
            연령대 문자열
        """
        if age < 20:
            return '10대'
        elif age < 30:
            return '20대'
        elif age < 40:
            return '30대'
        elif age < 50:
            return '40대'
        elif age < 60:
            return '50대'
        else:
            return '60대이상'
    
    def calculate_age_appropriateness_score(
        self, 
        age: int, 
        region: str
    ) -> float:
        """
        연령대-지역 적합도 점수 계산
        
        Args:
            age: 사용자 나이
            region: 지역명
            
        Returns:
            적합도 점수 (0-100)
        """
        age_group = self.get_age_group(age)
        
        # 지역별 연령 적합도에서 점수 추출
        if region in self.region_age_suitability:
            return self.region_age_suitability[region].get(age_group, 50.0)
        
        # 등록되지 않은 지역은 기본 점수
        return 50.0
    
    def apply_age_penalty_to_recommendations(
        self,
        age: int,
        recommendations: List[Dict]
    ) -> List[Dict]:
        """
        추천 목록에 연령 적합도 반영
        
        Args:
            age: 사용자 나이
            recommendations: 기존 추천 목록
            
        Returns:
            연령 적합도가 반영된 추천 목록
        """
        age_group = self.get_age_group(age)
        
        for rec in recommendations:
            region_name = rec.get('region_name', rec.get('region', ''))
            
            # 연령 적합도 점수 계산
            age_score = self.calculate_age_appropriateness_score(age, region_name)
            
            # 기존 점수에 연령 적합도 반영 (가중 평균: 기존 70%, 연령 30%)
            original_score = rec.get('match_score', rec.get('final_score', 0))
            adjusted_score = original_score * 0.70 + age_score * 0.30
            
            # 점수 업데이트
            rec['original_score'] = original_score
            rec['age_appropriateness_score'] = age_score
            rec['adjusted_score'] = adjusted_score
            rec['match_score'] = adjusted_score
            
            # 연령 적합도 설명 추가
            if age_score >= 90:
                age_fit = "매우 적합"
            elif age_score >= 70:
                age_fit = "적합"
            elif age_score >= 50:
                age_fit = "보통"
            elif age_score >= 30:
                age_fit = "다소 부적합"
            else:
                age_fit = "부적합"
            
            rec['age_fit'] = age_fit
            
            # 추천 이유에 연령 정보 추가
            if 'reason' in rec:
                age_reason = f"{age_group}에게 {age_fit}한 지역"
                rec['reason'] = f"{age_reason}, {rec['reason']}"
            else:
                rec['reason'] = f"{age_group}에게 {age_fit}한 지역"
        
        # 조정된 점수로 재정렬
        recommendations.sort(key=lambda x: x['adjusted_score'], reverse=True)
        
        return recommendations
    
    def get_age_appropriate_industries(self, age: int) -> List[str]:
        """
        연령대에 적합한 업종 리스트 반환
        
        Args:
            age: 사용자 나이
            
        Returns:
            적합한 업종 리스트
        """
        age_group = self.get_age_group(age)
        return self.age_preferences[age_group]['preferred_industries']
    
    def get_age_lifestyle_info(self, age: int) -> Dict:
        """
        연령대별 라이프스타일 정보 반환
        
        Args:
            age: 사용자 나이
            
        Returns:
            라이프스타일 정보 딕셔너리
        """
        age_group = self.get_age_group(age)
        return {
            'age_group': age_group,
            **self.age_preferences[age_group]
        }
    
    def explain_age_based_recommendation(self, age: int, region: str) -> str:
        """
        연령 기반 추천 설명 생성
        
        Args:
            age: 사용자 나이
            region: 추천 지역
            
        Returns:
            설명 문자열
        """
        age_group = self.get_age_group(age)
        age_info = self.age_preferences[age_group]
        age_score = self.calculate_age_appropriateness_score(age, region)
        
        explanation = f"""
【{age_group} 맞춤 추천】
• 라이프스타일: {age_info['lifestyle']}
• 선호 분위기: {', '.join(age_info['atmosphere'])}
• 적합 업종: {', '.join(age_info['preferred_industries'][:3])}
• 주요 활동 시간: {age_info['time_preference']}
• 이 지역 적합도: {age_score:.1f}점
        """
        
        # 50대에게 홍대를 추천하는 경우 경고
        if age >= 50 and region in ['홍대', '건대', '신촌']:
            explanation += f"\n⚠️  {region}은 젊은 층 중심 지역으로, 다소 시끄럽거나 혼잡할 수 있습니다."
        
        return explanation.strip()


def demo_age_appropriate_recommendation():
    """연령대별 추천 데모"""
    
    print("=" * 80)
    print("연령대별 적합 지역 추천 시스템 데모")
    print("=" * 80)
    
    recommender = AgeAppropriateRecommender()
    
    # 테스트 케이스
    test_cases = [
        {'age': 22, 'name': '20대 대학생'},
        {'age': 35, 'name': '30대 직장인'},
        {'age': 50, 'name': '50대 중장년'},
        {'age': 68, 'name': '60대 이상 시니어'}
    ]
    
    # 샘플 추천 목록 (기존 시스템에서 나온 결과라고 가정)
    sample_recommendations = [
        {'region': '홍대', 'match_score': 85.0, 'reason': '활기찬 문화 거리'},
        {'region': '강남역', 'match_score': 82.0, 'reason': '다양한 상권'},
        {'region': '서초', 'match_score': 78.0, 'reason': '안정적인 소비 패턴'},
        {'region': '종로', 'match_score': 75.0, 'reason': '전통 중심가'},
        {'region': '잠실', 'match_score': 73.0, 'reason': '가족 친화적'},
    ]
    
    for test_case in test_cases:
        print(f"\n{'=' * 80}")
        print(f"👤 사용자: {test_case['name']} ({test_case['age']}세)")
        print(f"{'=' * 80}")
        
        # 라이프스타일 정보
        lifestyle = recommender.get_age_lifestyle_info(test_case['age'])
        print(f"\n[라이프스타일 프로필]")
        print(f"  • 연령대: {lifestyle['age_group']}")
        print(f"  • 특징: {lifestyle['lifestyle']}")
        print(f"  • 선호 분위기: {', '.join(lifestyle['atmosphere'])}")
        print(f"  • 선호 업종: {', '.join(lifestyle['preferred_industries'][:5])}")
        
        # 추천 목록에 연령 적합도 반영
        adjusted_recs = recommender.apply_age_penalty_to_recommendations(
            test_case['age'],
            sample_recommendations.copy()
        )
        
        print(f"\n[추천 지역 TOP 5]")
        print(f"{'순위':<6} {'지역':<10} {'원점수':<10} {'연령적합도':<12} {'최종점수':<10} {'적합성':<10}")
        print("-" * 80)
        
        for idx, rec in enumerate(adjusted_recs, 1):
            print(f"{idx:<6} {rec['region']:<10} "
                  f"{rec['original_score']:>8.1f}  "
                  f"{rec['age_appropriateness_score']:>10.1f}  "
                  f"{rec['adjusted_score']:>8.1f}  "
                  f"{rec['age_fit']:<10}")
        
        # 1위 지역에 대한 상세 설명
        if adjusted_recs:
            top_region = adjusted_recs[0]['region']
            print(f"\n[1위 지역 '{top_region}' 추천 이유]")
            print(recommender.explain_age_based_recommendation(test_case['age'], top_region))


if __name__ == '__main__':
    demo_age_appropriate_recommendation()

