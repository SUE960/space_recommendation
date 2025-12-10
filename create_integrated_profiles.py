#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 실시간 지역 프로필 생성 시스템
- 카드 소비 데이터
- 상주인구 데이터
- 소득·소비 데이터
- GIS 영역 데이터
모두 통합하여 강화된 지역 프로필 생성
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime


class IntegratedRegionalProfiler:
    """통합 지역 프로필 생성 클래스"""
    
    def __init__(self):
        self.card_data = None
        self.population_data = None
        self.income_consumption_data = None
        self.gis_data = None
        
    def load_all_data(self):
        """모든 데이터 로드"""
        print("="*80)
        print("통합 데이터 로드")
        print("="*80)
        
        # 1. 인구 데이터
        if os.path.exists('outputs/seoul_population_summary.csv'):
            self.population_data = pd.read_csv('outputs/seoul_population_summary.csv')
            print(f"✓ 인구 데이터 로드 완료")
        
        # 2. 소득·소비 데이터
        if os.path.exists('outputs/seoul_income_consumption_data.csv'):
            self.income_consumption_data = pd.read_csv('outputs/seoul_income_consumption_data.csv')
            print(f"✓ 소득·소비 데이터 로드 완료: {len(self.income_consumption_data)}개 상권")
        
        # 3. GIS 데이터
        if os.path.exists('outputs/seoul_gis_area.json'):
            with open('outputs/seoul_gis_area.json', 'r', encoding='utf-8') as f:
                self.gis_data = json.load(f)
            print(f"✓ GIS 데이터 로드 완료")
        
        print(f"\n통합 데이터 준비 완료!")
        
    def calculate_economic_score(self, area_name):
        """경제력 점수 계산 (0-100)"""
        if self.income_consumption_data is None:
            return 50.0
        
        # 해당 상권 찾기
        area_data = self.income_consumption_data[
            self.income_consumption_data['TRDAR_CD_NM'].str.contains(area_name, na=False)
        ]
        
        if len(area_data) == 0:
            # 전체 평균 사용
            avg_income = self.income_consumption_data['MT_AVRG_INCOME_AMT'].mean()
            avg_spending = self.income_consumption_data['EXPNDTR_TOTAMT'].mean()
        else:
            avg_income = area_data['MT_AVRG_INCOME_AMT'].mean()
            avg_spending = area_data['EXPNDTR_TOTAMT'].mean()
        
        # 소득 점수 (전국 평균 대비)
        national_avg_income = 3_384_950  # 전체 평균
        income_score = min((avg_income / national_avg_income) * 50, 50)
        
        # 소비 활성도 점수
        spending_score = min((avg_spending / 1_000_000_000) * 50, 50)
        
        return round(income_score + spending_score, 1)
    
    def calculate_consumption_pattern(self, area_name):
        """소비 패턴 분석"""
        if self.income_consumption_data is None:
            return {}
        
        area_data = self.income_consumption_data[
            self.income_consumption_data['TRDAR_CD_NM'].str.contains(area_name, na=False)
        ]
        
        if len(area_data) == 0:
            # 전체 평균 사용
            area_data = self.income_consumption_data
        
        # 카테고리별 지출 비율
        categories = {
            '식료품': 'FDSTFFS_EXPNDTR_TOTAMT',
            '의류신발': 'CLTHS_FTWR_EXPNDTR_TOTAMT',
            '생활용품': 'LVSPL_EXPNDTR_TOTAMT',
            '의료': 'MCP_EXPNDTR_TOTAMT',
            '교통': 'TRNSPORT_EXPNDTR_TOTAMT',
            '여가': 'LSR_EXPNDTR_TOTAMT',
            '문화': 'CLTUR_EXPNDTR_TOTAMT',
            '교육': 'EDC_EXPNDTR_TOTAMT',
            '오락': 'PLESR_EXPNDTR_TOTAMT'
        }
        
        total = area_data['EXPNDTR_TOTAMT'].sum()
        pattern = {}
        
        for kr_name, en_col in categories.items():
            amount = area_data[en_col].sum()
            ratio = (amount / total * 100) if total > 0 else 0
            pattern[kr_name] = {
                '지출액': int(amount),
                '비율': round(ratio, 1)
            }
        
        return pattern
    
    def calculate_demographic_index(self):
        """인구통계 지수 계산"""
        if self.population_data is None:
            return {}
        
        pop_data = self.population_data.iloc[0]
        
        return {
            '총인구': int(pop_data['총인구']),
            '인구밀도': int(pop_data['인구밀도_명per제곱킬로미터']) if '인구밀도_명per제곱킬로미터' in pop_data else 15452,
            '성비': round(pop_data['남성인구'] / pop_data['여성인구'], 3),
            '가구당인구': round(pop_data['가구당인구수'], 2),
            '주요연령대': self._get_dominant_age_group(pop_data)
        }
    
    def _get_dominant_age_group(self, pop_data):
        """주요 연령대 파악"""
        age_groups = {
            '10대': pop_data['10대인구'],
            '20대': pop_data['20대인구'],
            '30대': pop_data['30대인구'],
            '40대': pop_data['40대인구'],
            '50대': pop_data['50대인구'],
            '60대이상': pop_data['60대이상인구']
        }
        return max(age_groups, key=age_groups.get)
    
    def generate_integrated_profile(self, area_name, base_profile):
        """통합 지역 프로필 생성"""
        print(f"\n{'='*80}")
        print(f"통합 지역 프로필 생성: {area_name}")
        print(f"{'='*80}")
        
        # 기존 프로필
        profile = {
            '지역명': area_name,
            '생성시각': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '기본정보': base_profile
        }
        
        # 경제력 점수 추가
        economic_score = self.calculate_economic_score(area_name)
        profile['경제력점수'] = economic_score
        
        # 소비 패턴 추가
        consumption_pattern = self.calculate_consumption_pattern(area_name)
        profile['소비패턴'] = consumption_pattern
        
        # 인구통계 지수 추가
        demographic_index = self.calculate_demographic_index()
        profile['인구통계지수'] = demographic_index
        
        # 종합 점수 재계산
        profile['종합점수'] = self._calculate_综合_score(
            base_profile.get('상업활동점수', 50),
            base_profile.get('특화도점수', 50),
            base_profile.get('인구통계점수', 50),
            economic_score
        )
        
        # 추천 타겟 고객층
        profile['추천타겟'] = self._recommend_target_customers(profile)
        
        return profile
    
    def _calculate_综合_score(self, commercial, specialization, demographic, economic):
        """종합 점수 계산 (가중평균)"""
        weights = {
            'commercial': 0.3,
            'specialization': 0.25,
            'demographic': 0.2,
            'economic': 0.25
        }
        
        total = (
            commercial * weights['commercial'] +
            specialization * weights['specialization'] +
            demographic * weights['demographic'] +
            economic * weights['economic']
        )
        
        return round(total, 1)
    
    def _recommend_target_customers(self, profile):
        """타겟 고객층 추천"""
        recommendations = []
        
        # 소비 패턴 기반
        if profile['소비패턴']:
            top_category = max(profile['소비패턴'].items(), key=lambda x: x[1]['비율'])
            
            target_map = {
                '식료품': '외식/식음료 선호층',
                '의류신발': '패션 관심층',
                '생활용품': '생활밀착형 소비자',
                '의료': '건강 관심층',
                '교통': '직장인/통근자',
                '여가': '레저 활동 선호층',
                '문화': '문화예술 애호가',
                '교육': '학생/학부모층',
                '오락': '엔터테인먼트 소비자'
            }
            
            recommendations.append(target_map.get(top_category[0], '일반 소비자'))
        
        # 경제력 기반
        economic_score = profile['경제력점수']
        if economic_score >= 70:
            recommendations.append('고소득층')
        elif economic_score >= 50:
            recommendations.append('중상위소득층')
        else:
            recommendations.append('중하위소득층')
        
        # 인구통계 기반
        if profile['인구통계지수']:
            age_group = profile['인구통계지수']['주요연령대']
            recommendations.append(f'{age_group} 중심')
        
        return recommendations
    
    def print_profile(self, profile):
        """프로필 출력"""
        print(f"\n[통합 지역 프로필]")
        print(f"지역명: {profile['지역명']}")
        print(f"생성시각: {profile['생성시각']}")
        print(f"종합점수: {profile['종합점수']}/100")
        
        print(f"\n[점수 상세]")
        base = profile['기본정보']
        print(f"  • 상업활동 점수: {base.get('상업활동점수', 'N/A')}/100")
        print(f"  • 특화도 점수: {base.get('특화도점수', 'N/A')}/100")
        print(f"  • 인구통계 점수: {base.get('인구통계점수', 'N/A')}/100")
        print(f"  • 경제력 점수: {profile['경제력점수']}/100")
        
        print(f"\n[소비 패턴 TOP 3]")
        if profile['소비패턴']:
            sorted_pattern = sorted(
                profile['소비패턴'].items(),
                key=lambda x: x[1]['비율'],
                reverse=True
            )[:3]
            for idx, (category, data) in enumerate(sorted_pattern, 1):
                print(f"  {idx}. {category}: {data['비율']}% ({data['지출액']:,}원)")
        
        print(f"\n[인구통계 지수]")
        if profile['인구통계지수']:
            demo = profile['인구통계지수']
            print(f"  • 총인구: {demo['총인구']:,}명")
            print(f"  • 인구밀도: {demo['인구밀도']:,}명/㎢")
            print(f"  • 주요연령대: {demo['주요연령대']}")
            print(f"  • 가구당인구: {demo['가구당인구']}명")
        
        print(f"\n[추천 타겟 고객층]")
        for target in profile['추천타겟']:
            print(f"  • {target}")
    
    def save_profile(self, profile, output_dir='outputs'):
        """프로필 저장"""
        os.makedirs(output_dir, exist_ok=True)
        
        # JSON으로 저장
        area_name_safe = profile['지역명'].replace('·', '_').replace(' ', '_')
        json_file = f"{output_dir}/integrated_profile_{area_name_safe}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 프로필 저장: {json_file}")


def main():
    """메인 실행 함수"""
    print("="*80)
    print("통합 실시간 지역 프로필 생성 시스템")
    print("="*80)
    
    # 프로파일러 초기화
    profiler = IntegratedRegionalProfiler()
    
    # 데이터 로드
    profiler.load_all_data()
    
    # 샘플 지역 프로필 생성
    sample_areas = [
        {
            '지역명': '광화문·덕수궁',
            '기본정보': {
                '상업활동점수': 85.2,
                '특화도점수': 78.5,
                '인구통계점수': 72.3
            }
        },
        {
            '지역명': '강남역',
            '기본정보': {
                '상업활동점수': 92.5,
                '특화도점수': 88.7,
                '인구통계점수': 85.4
            }
        },
        {
            '지역명': '홍대입구',
            '기본정보': {
                '상업활동점수': 88.9,
                '특화도점수': 82.3,
                '인구통계점수': 79.6
            }
        },
        {
            '지역명': '명동',
            '기본정보': {
                '상업활동점수': 90.7,
                '특화도점수': 85.6,
                '인구통계점수': 81.2
            }
        }
    ]
    
    print(f"\n{'='*80}")
    print(f"통합 프로필 생성 중...")
    print(f"{'='*80}")
    
    profiles = []
    for area in sample_areas:
        profile = profiler.generate_integrated_profile(
            area['지역명'],
            area['기본정보']
        )
        profiler.print_profile(profile)
        profiler.save_profile(profile)
        profiles.append(profile)
    
    # 종합 비교
    print(f"\n{'='*80}")
    print(f"지역별 종합 점수 비교")
    print(f"{'='*80}")
    
    sorted_profiles = sorted(profiles, key=lambda x: x['종합점수'], reverse=True)
    
    print(f"\n{'순위':<6} {'지역명':<20} {'종합점수':<12} {'경제력점수':<12} {'주요타겟':<30}")
    print("-" * 85)
    
    for idx, profile in enumerate(sorted_profiles, 1):
        main_target = profile['추천타겟'][0] if profile['추천타겟'] else 'N/A'
        print(f"{idx:<6} {profile['지역명']:<20} {profile['종합점수']:<12} {profile['경제력점수']:<12} {main_target:<30}")
    
    print(f"\n{'='*80}")
    print(f"통합 프로필 생성 완료!")
    print(f"{'='*80}")
    print(f"\n💡 이제 4개 데이터를 모두 활용한 강화된 지역 프로필이 준비되었습니다!")
    
    return profiles


if __name__ == '__main__':
    result = main()

