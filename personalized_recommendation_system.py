#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2단계 개인화 추천 시스템
Level 1: 지역 객관적 평가 (Regional Quality Score)
Level 2: 사용자-지역 매칭 (User-Region Matching Score)
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Tuple


class PersonalizedRecommendationSystem:
    """개인화 추천 시스템"""
    
    def __init__(self):
        self.regional_profiles = {}  # 지역 프로필 (Level 1)
        
    
    # ============================================================================
    # Level 1: 지역 객관적 평가 (Regional Quality Score)
    # ============================================================================
    
    def calculate_regional_quality_score(self, area_data):
        """
        지역의 객관적 품질 평가
        목적: 지역 자체의 인프라, 활성도, 경제력 평가
        
        이 점수가 높다 = 좋은 상권, 발전된 지역
        하지만 모든 사용자에게 적합한 것은 아님!
        """
        scores = {
            '상업활동': area_data.get('commercial_activity', 0),  # 거래량
            '특화도': area_data.get('specialization', 0),          # 업종 특화
            '경제력': area_data.get('economic_power', 0),          # 구매력
            '인구통계': area_data.get('demographic', 0)            # 인구 규모
        }
        
        # 가중 평균
        weights = {
            '상업활동': 0.30,
            '특화도': 0.25,
            '경제력': 0.25,
            '인구통계': 0.20
        }
        
        quality_score = sum(scores[k] * weights[k] for k in scores)
        
        return {
            'quality_score': quality_score,
            'detail_scores': scores,
            'interpretation': self._interpret_quality(quality_score)
        }
    
    def _interpret_quality(self, score):
        """품질 점수 해석"""
        if score >= 90:
            return "초우량 상권 - 인프라 최상급"
        elif score >= 80:
            return "우량 상권 - 안정적 환경"
        elif score >= 70:
            return "보통 상권 - 기본 인프라"
        else:
            return "발전 필요 지역"
    
    
    # ============================================================================
    # Level 2: 사용자-지역 매칭 (User-Region Matching Score)
    # ============================================================================
    
    def calculate_user_matching_score(self, user_profile, regional_profile):
        """
        사용자와 지역의 매칭도 계산
        목적: 이 사용자에게 이 지역이 얼마나 적합한가?
        
        핵심: 사용자 특성과 지역 특성의 유사도/적합도
        """
        
        # 1. 인구통계 매칭 (40%) - 가장 중요!
        demographic_match = self._match_demographics(
            user_profile.get('age', 0),
            user_profile.get('gender', ''),
            regional_profile.get('age_distribution', {}),
            regional_profile.get('gender_distribution', {})
        )
        
        # 2. 소비 패턴 매칭 (35%)
        consumption_match = self._match_consumption(
            user_profile.get('spending_categories', {}),
            regional_profile.get('consumption_pattern', {})
        )
        
        # 3. 소득 수준 매칭 (15%)
        income_match = self._match_income(
            user_profile.get('income', 0),
            regional_profile.get('avg_income', 0)
        )
        
        # 4. 선호 업종 매칭 (10%)
        industry_match = self._match_industry_preference(
            user_profile.get('preferred_industries', []),
            regional_profile.get('specialized_industries', [])
        )
        
        # 가중 평균
        matching_score = (
            demographic_match * 0.40 +
            consumption_match * 0.35 +
            income_match * 0.15 +
            industry_match * 0.10
        )
        
        return {
            'matching_score': matching_score,
            'detail_matches': {
                '인구통계_매칭': demographic_match,
                '소비패턴_매칭': consumption_match,
                '소득수준_매칭': income_match,
                '업종선호_매칭': industry_match
            }
        }
    
    def _match_demographics(self, user_age, user_gender, region_age_dist, region_gender_dist):
        """인구통계 매칭"""
        score = 0
        
        # 연령대 매칭
        user_age_group = self._get_age_group(user_age)
        region_age_ratio = region_age_dist.get(user_age_group, 0)
        
        # 같은 연령대가 많을수록 높은 점수
        age_score = min(region_age_ratio * 2, 100)  # 50% 이상이면 만점
        
        # 성별 매칭 (덜 중요)
        gender_score = 50  # 기본 점수
        if user_gender in region_gender_dist:
            if region_gender_dist[user_gender] > 50:
                gender_score = 60
        
        # 연령이 더 중요 (80%), 성별은 보조(20%)
        score = age_score * 0.8 + gender_score * 0.2
        
        return min(score, 100)
    
    def _match_consumption(self, user_spending, region_consumption):
        """소비 패턴 매칭 - 코사인 유사도"""
        
        # 공통 카테고리 추출
        common_categories = set(user_spending.keys()) & set(region_consumption.keys())
        
        if not common_categories:
            return 50  # 기본 점수
        
        # 벡터화
        user_vector = [user_spending.get(cat, 0) for cat in common_categories]
        region_vector = [region_consumption.get(cat, {}).get('비율', 0) for cat in common_categories]
        
        # 코사인 유사도
        dot_product = sum(u * r for u, r in zip(user_vector, region_vector))
        user_norm = np.sqrt(sum(u**2 for u in user_vector))
        region_norm = np.sqrt(sum(r**2 for r in region_vector))
        
        if user_norm == 0 or region_norm == 0:
            return 50
        
        similarity = dot_product / (user_norm * region_norm)
        
        return similarity * 100
    
    def _match_income(self, user_income, region_avg_income):
        """소득 수준 매칭"""
        if region_avg_income == 0:
            return 50
        
        # 소득 차이 비율
        income_ratio = user_income / region_avg_income
        
        # 0.8 ~ 1.2 범위면 잘 맞음 (만점)
        if 0.8 <= income_ratio <= 1.2:
            score = 100
        elif 0.6 <= income_ratio < 0.8 or 1.2 < income_ratio <= 1.5:
            score = 70  # 약간 차이
        else:
            score = 40  # 많이 차이
        
        return score
    
    def _match_industry_preference(self, user_preferences, region_specializations):
        """업종 선호도 매칭"""
        if not user_preferences or not region_specializations:
            return 50
        
        # 교집합 비율
        matches = len(set(user_preferences) & set(region_specializations))
        max_possible = max(len(user_preferences), len(region_specializations))
        
        if max_possible == 0:
            return 50
        
        match_ratio = matches / len(user_preferences)
        
        return match_ratio * 100
    
    def _get_age_group(self, age):
        """연령 → 연령대 변환"""
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
    
    
    # ============================================================================
    # 최종 추천 점수 계산
    # ============================================================================
    
    def calculate_final_recommendation_score(self, user_profile, regional_profile):
        """
        최종 추천 점수 = Level 1 × Level 2
        
        개념:
        - Level 1 (지역 품질): 이 지역이 객관적으로 좋은가?
        - Level 2 (매칭도): 이 사용자에게 적합한가?
        - 둘 다 높아야 최종 점수가 높음!
        """
        
        # Level 1: 지역 품질 점수
        quality = self.calculate_regional_quality_score(regional_profile)
        quality_score = quality['quality_score']
        
        # Level 2: 매칭 점수
        matching = self.calculate_user_matching_score(user_profile, regional_profile)
        matching_score = matching['matching_score']
        
        # 최종 점수: 품질 × 매칭 (정규화)
        # 방법 1: 곱하기 (둘 다 중요)
        final_score = (quality_score / 100) * matching_score
        
        # 방법 2: 가중 평균 (선택 가능)
        # final_score = quality_score * 0.4 + matching_score * 0.6
        
        return {
            'final_score': final_score,
            'quality_score': quality_score,
            'matching_score': matching_score,
            'quality_detail': quality,
            'matching_detail': matching,
            'recommendation_reason': self._generate_reason(quality, matching)
        }
    
    def _generate_reason(self, quality, matching):
        """추천 이유 생성"""
        reasons = []
        
        # 품질 기반
        if quality['quality_score'] >= 90:
            reasons.append("우수한 인프라와 활발한 상권")
        
        # 매칭 기반
        detail = matching['detail_matches']
        
        if detail['인구통계_매칭'] >= 80:
            reasons.append("당신과 비슷한 연령대가 많이 방문")
        
        if detail['소비패턴_매칭'] >= 80:
            reasons.append("당신의 소비 취향과 잘 맞음")
        
        if detail['소득수준_매칭'] >= 80:
            reasons.append("당신의 소득 수준에 적합한 가격대")
        
        return reasons
    
    
    # ============================================================================
    # 개인화 추천 실행
    # ============================================================================
    
    def recommend_regions(self, user_profile, candidate_regions, top_n=3):
        """
        사용자에게 최적 지역 추천
        """
        recommendations = []
        
        for region_name, region_profile in candidate_regions.items():
            result = self.calculate_final_recommendation_score(
                user_profile,
                region_profile
            )
            
            recommendations.append({
                'region': region_name,
                'final_score': result['final_score'],
                'quality_score': result['quality_score'],
                'matching_score': result['matching_score'],
                'reasons': result['recommendation_reason']
            })
        
        # 최종 점수 기준 정렬
        recommendations.sort(key=lambda x: x['final_score'], reverse=True)
        
        return recommendations[:top_n]


# ============================================================================
# 실제 사용 예시
# ============================================================================

def demo_personalized_recommendation():
    """개인화 추천 데모"""
    
    print("="*80)
    print("개인화 추천 시스템 데모")
    print("="*80)
    
    system = PersonalizedRecommendationSystem()
    
    # 사용자 프로필 예시
    user_profiles = {
        '20대 학생': {
            'age': 23,
            'gender': '남성',
            'income': 2_500_000,
            'spending_categories': {
                '식료품': 30,
                '문화': 25,
                '오락': 20,
                '의류신발': 15,
                '교통': 10
            },
            'preferred_industries': ['카페', '술집', '클럽', '영화관']
        },
        '40대 직장인': {
            'age': 42,
            'gender': '남성',
            'income': 5_500_000,
            'spending_categories': {
                '식료품': 35,
                '교통': 20,
                '교육': 15,
                '의류신발': 15,
                '문화': 15
            },
            'preferred_industries': ['레스토랑', '카페', '서점', '헬스장']
        },
        '60대 관광객': {
            'age': 65,
            'gender': '여성',
            'income': 4_000_000,
            'spending_categories': {
                '식료품': 40,
                '의류신발': 25,
                '문화': 20,
                '생활용품': 15
            },
            'preferred_industries': ['한식당', '쇼핑몰', '기념품점', '박물관']
        }
    }
    
    # 지역 프로필 예시 (간소화)
    regional_profiles = {
        '강남역': {
            'commercial_activity': 92.5,
            'specialization': 88.7,
            'economic_power': 97.9,
            'demographic': 85.4,
            'avg_income': 5_000_000,
            'age_distribution': {
                '20대': 25, '30대': 35, '40대': 25, '50대': 10, '60대이상': 5
            },
            'gender_distribution': {'남성': 48, '여성': 52},
            'consumption_pattern': {
                '식료품': {'비율': 24.1},
                '교육': {'비율': 17.5},
                '교통': {'비율': 13.7},
                '의류신발': {'비율': 13.3}
            },
            'specialized_industries': ['레스토랑', '카페', '학원', '피트니스']
        },
        '홍대입구': {
            'commercial_activity': 88.9,
            'specialization': 82.3,
            'economic_power': 97.9,
            'demographic': 79.6,
            'avg_income': 3_200_000,
            'age_distribution': {
                '20대': 45, '30대': 30, '40대': 15, '50대': 7, '60대이상': 3
            },
            'gender_distribution': {'남성': 52, '여성': 48},
            'consumption_pattern': {
                '식료품': {'비율': 24.1},
                '문화': {'비율': 20.5},
                '오락': {'비율': 18.3},
                '의류신발': {'비율': 13.3}
            },
            'specialized_industries': ['카페', '술집', '클럽', '라이브공연']
        },
        '명동': {
            'commercial_activity': 90.7,
            'specialization': 85.6,
            'economic_power': 97.9,
            'demographic': 81.2,
            'avg_income': 4_500_000,
            'age_distribution': {
                '20대': 20, '30대': 25, '40대': 20, '50대': 15, '60대이상': 20
            },
            'gender_distribution': {'남성': 35, '여성': 65},
            'consumption_pattern': {
                '식료품': {'비율': 24.1},
                '의류신발': {'비율': 25.0},
                '생활용품': {'비율': 15.0},
                '문화': {'비율': 12.0}
            },
            'specialized_industries': ['쇼핑몰', '화장품', '면세점', '한식당']
        }
    }
    
    # 각 사용자별 추천
    for user_name, user_profile in user_profiles.items():
        print(f"\n{'='*80}")
        print(f"👤 사용자: {user_name}")
        print(f"{'='*80}")
        print(f"나이: {user_profile['age']}세")
        print(f"소득: {user_profile['income']:,}원")
        print(f"주요 지출: {', '.join(list(user_profile['spending_categories'].keys())[:3])}")
        
        # 추천 실행
        recommendations = system.recommend_regions(
            user_profile,
            regional_profiles,
            top_n=3
        )
        
        print(f"\n📍 추천 지역 TOP 3:")
        print(f"\n{'순위':<6} {'지역':<12} {'최종점수':<12} {'지역품질':<12} {'매칭도':<12} {'추천이유':<40}")
        print("-" * 100)
        
        for idx, rec in enumerate(recommendations, 1):
            reasons = ', '.join(rec['reasons'][:2]) if rec['reasons'] else '기본 추천'
            print(f"{idx:<6} {rec['region']:<12} "
                  f"{rec['final_score']:>10.1f}점  "
                  f"{rec['quality_score']:>10.1f}점  "
                  f"{rec['matching_score']:>10.1f}점  "
                  f"{reasons:<40}")


if __name__ == '__main__':
    demo_personalized_recommendation()

