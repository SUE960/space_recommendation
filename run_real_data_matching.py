#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실제 데이터를 사용한 Level 2 매칭 재실행
"""

import pandas as pd
import numpy as np
import json
import os


# 페르소나는 동일
PERSONAS = {
    '20대_대학생': {
        '이름': '20대 대학생 김민수',
        '나이': 23,
        '성별': '남성',
        '소득': 2500000,
        '소비패턴': {'식료품': 33, '교통': 18, '생활용품': 22, '기타': 27},
        '선호업종': ['카페', '술집', '클럽'],
        '특성': '문화·오락 중심'
    },
    '40대_직장인': {
        '이름': '40대 직장인 박영희',
        '나이': 42,
        '성별': '여성',
        '소득': 5500000,
        '소비패턴': {'식료품': 33, '교통': 18, '생활용품': 22, '기타': 27},
        '선호업종': ['레스토랑', '카페'],
        '특성': '외식·업무 중심'
    },
    '30대_맞벌이부부': {
        '이름': '30대 맞벌이 부부',
        '나이': 35,
        '성별': '부부',
        '소득': 8000000,
        '소비패턴': {'식료품': 35, '교통': 15, '생활용품': 25, '기타': 25},
        '선호업종': ['대형마트', '백화점'],
        '특성': '가족 단위 소비'
    }
}


def calculate_demographic_matching(persona, gu_profile):
    """인구통계 매칭 (실제 데이터 사용)"""
    
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
    
    # 연령대 비율 (NaN 처리)
    gu_age_ratio = gu_profile['인구통계'].get(age_group, 0)
    if pd.isna(gu_age_ratio) or gu_age_ratio is None:
        gu_age_ratio = 15  # 기본값
    
    age_score = min(float(gu_age_ratio) * 2, 100)
    
    # 성별
    gender_score = 50
    if persona['성별'] != '부부':
        gender_key = '남성' if persona['성별'] == '남성' else '여성'
        gender_ratio = gu_profile['성별분포'].get(gender_key, 50)
        if not pd.isna(gender_ratio):
            gender_score = float(gender_ratio)
    
    demo_score = age_score * 0.8 + gender_score * 0.2
    
    return min(demo_score, 100)


def calculate_consumption_matching(persona, gu_profile):
    """소비패턴 매칭 (코사인 유사도)"""
    
    # 공통 카테고리
    categories = ['식료품', '교통', '생활용품', '기타']
    
    user_vector = [persona['소비패턴'].get(cat, 0) for cat in categories]
    
    # NaN 처리
    gu_vector = []
    for cat in categories:
        val = gu_profile['소비패턴'].get(cat, 25)
        if pd.isna(val):
            val = 25
        gu_vector.append(float(val))
    
    # 코사인 유사도
    dot_product = sum(u * g for u, g in zip(user_vector, gu_vector))
    user_norm = np.sqrt(sum(u**2 for u in user_vector))
    gu_norm = np.sqrt(sum(g**2 for g in gu_vector))
    
    if user_norm == 0 or gu_norm == 0:
        return 50
    
    similarity = dot_product / (user_norm * gu_norm)
    
    return similarity * 100


def calculate_income_matching(persona, gu_profile):
    """소득수준 매칭"""
    
    user_income = persona['소득']
    gu_income = gu_profile['평균소득']
    
    ratio = user_income / gu_income
    
    if 0.8 <= ratio <= 1.2:
        return 100
    elif 0.6 <= ratio < 0.8 or 1.2 < ratio <= 1.5:
        return 70
    else:
        return 40


def calculate_industry_matching(persona, gu_profile):
    """업종선호 매칭"""
    
    user_prefs = set(persona['선호업종'])
    gu_industries = set(gu_profile['특화업종'])
    
    if not user_prefs:
        return 50
    
    matches = len(user_prefs & gu_industries)
    match_ratio = matches / len(user_prefs)
    
    return match_ratio * 100


def run_real_data_matching():
    """실제 데이터로 매칭 실행"""
    
    print("="*100)
    print("실제 데이터를 사용한 Level 2 매칭 재실행")
    print("="*100)
    
    # 실제 데이터 로드
    with open('outputs/integrated_gu_profiles_real_data.json', 'r', encoding='utf-8') as f:
        gu_profiles = json.load(f)
    
    print(f"\n✓ 실제 데이터 로드: {len(gu_profiles)}개 구")
    
    all_results = []
    
    for persona_key, persona in PERSONAS.items():
        print(f"\n{'='*100}")
        print(f"👤 {persona['이름']}")
        print(f"{'='*100}")
        
        persona_results = []
        
        for gu_name, gu_profile in gu_profiles.items():
            # Level 2 매칭 계산
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
            
            # 최종 점수
            quality_score = gu_profile['종합점수']
            final_score = (quality_score / 100) * matching_score
            
            persona_results.append({
                '페르소나': persona['이름'],
                '구': gu_name,
                'L1_품질': quality_score,
                'L2_매칭': round(matching_score, 1),
                '최종점수': round(final_score, 1),
                '인구통계': round(demo, 1),
                '소비패턴': round(consumption, 1),
                '소득': round(income, 1),
                '업종': round(industry, 1)
            })
        
        # 정렬
        persona_results.sort(key=lambda x: x['최종점수'], reverse=True)
        
        # 출력
        print(f"\n📍 실제 데이터 기반 추천 TOP 5:")
        print(f"\n{'순위':<4} {'구':<12} {'최종':<8} {'L1':<8} {'L2':<8} {'인구':<6} {'소비':<6} {'소득':<6}")
        print("-" * 70)
        
        for idx, result in enumerate(persona_results[:5], 1):
            result['순위'] = idx
            print(f"{idx:<4} {result['구']:<12} "
                  f"{result['최종점수']:>6.1f}  "
                  f"{result['L1_품질']:>6.1f}  "
                  f"{result['L2_매칭']:>6.1f}  "
                  f"{result['인구통계']:>4.0f}  "
                  f"{result['소비패턴']:>4.0f}  "
                  f"{result['소득']:>4.0f}")
        
        all_results.extend(persona_results)
    
    # 저장
    df = pd.DataFrame(all_results)
    csv_file = 'outputs/level2_matching_real_data_results.csv'
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    print(f"\n{'='*100}")
    print("✅ 실제 데이터 기반 매칭 완료!")
    print(f"{'='*100}")
    print(f"\n✓ 결과 저장: {csv_file}")
    
    return all_results


if __name__ == '__main__':
    results = run_real_data_matching()




