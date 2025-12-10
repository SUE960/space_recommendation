#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 25개 구 종합 결과 정리
"""

import pandas as pd
import json

print("="*100)
print("서울시 25개 구 종합 분석 결과 정리")
print("="*100)

# 1. Level 1 점수 로드
print("\n1. Level 1 (지역 품질 점수) 로드...")
level1_df = pd.read_csv('outputs/seoul_25gu_level1_scores.csv', encoding='utf-8-sig')
print(f"✓ {len(level1_df)}개 구 데이터 로드")

# 2. 실제 데이터 프로필 로드
print("\n2. 실제 데이터 프로필 로드...")
with open('outputs/integrated_gu_profiles_real_data.json', 'r', encoding='utf-8') as f:
    profiles = json.load(f)
print(f"✓ {len(profiles)}개 구 프로필 로드")

# 3. Level 2 매칭 결과 로드
print("\n3. Level 2 매칭 결과 로드...")
level2_df = pd.read_csv('outputs/level2_matching_real_data_results.csv', encoding='utf-8-sig')
print(f"✓ {len(level2_df)}개 매칭 결과 로드")

# 4. 페르소나별 TOP 5 정리
print("\n4. 페르소나별 추천 결과 정리...")

personas = level2_df['페르소나'].unique()

summary_data = []

for persona in personas:
    persona_data = level2_df[level2_df['페르소나'] == persona].copy()
    persona_data = persona_data.sort_values('최종점수', ascending=False).head(5)
    
    print(f"\n{'='*100}")
    print(f"👤 {persona}")
    print(f"{'='*100}")
    print(f"\n{'순위':<4} {'구':<10} {'최종점수':<8} {'L1품질':<8} {'L2매칭':<8} {'인구통계':<8} {'소비패턴':<8}")
    print("-"*70)
    
    for idx, row in enumerate(persona_data.itertuples(), 1):
        print(f"{idx:<4} {row.구:<10} {row.최종점수:<8.1f} {row.L1_품질:<8.1f} {row.L2_매칭:<8.1f} {row.인구통계:<8.1f} {row.소비패턴:<8.1f}")
        
        summary_data.append({
            '페르소나': persona,
            '추천순위': idx,
            '구': row.구,
            '최종점수': row.최종점수,
            'Level1_품질': row.L1_품질,
            'Level2_매칭': row.L2_매칭,
            '인구통계매칭': row.인구통계,
            '소비패턴매칭': row.소비패턴,
            '소득매칭': row.소득,
            '업종매칭': row.업종
        })

# 5. 전체 구별 종합 정보
print(f"\n{'='*100}")
print("5. 전체 25개 구 상세 정보")
print(f"{'='*100}")

comprehensive_data = []

for _, row in level1_df.iterrows():
    gu = row['구']
    
    # 프로필 정보
    if gu in profiles:
        prof = profiles[gu]
        age_dist = prof['인구통계']
        gender_dist = prof['성별분포']
        consumption = prof['소비패턴']
        
        # 주요 연령대 찾기
        valid_ages = {k: v for k, v in age_dist.items() if pd.notna(v) and v > 0}
        main_age = max(valid_ages, key=valid_ages.get) if valid_ages else 'N/A'
        main_age_pct = valid_ages.get(main_age, 0) if valid_ages else 0
        
        # 주요 소비 카테고리
        valid_consumption = {k: v for k, v in consumption.items() if pd.notna(v) and v > 0}
        main_consumption = max(valid_consumption, key=valid_consumption.get) if valid_consumption else 'N/A'
        main_consumption_pct = valid_consumption.get(main_consumption, 0) if valid_consumption else 0
        
        # 성별
        male_pct = gender_dist.get('남성', 50)
        female_pct = gender_dist.get('여성', 50)
        if pd.isna(male_pct):
            male_pct = 0 if not pd.isna(female_pct) and female_pct == 100 else 50
        if pd.isna(female_pct):
            female_pct = 0 if not pd.isna(male_pct) and male_pct == 100 else 50
            
    else:
        main_age = 'N/A'
        main_age_pct = 0
        main_consumption = 'N/A'
        main_consumption_pct = 0
        male_pct = 50
        female_pct = 50
    
    comprehensive_data.append({
        '순위': row['순위'],
        '구': gu,
        '종합점수': row['종합점수'],
        '등급': row['등급'],
        '상업활동점수': row['상업활동점수'],
        '특화도점수': row['특화도점수'],
        '인구통계점수': row['인구통계점수'],
        '경제력점수': row['경제력점수'],
        '주요특화업종': row['주요특화업종'],
        '성장률': row['성장률'],
        '변동계수': row['CV'],
        '업종다양성': row['업종수'],
        '주요연령대': main_age,
        '연령대비율': round(main_age_pct, 1),
        '남성비율': round(male_pct, 1),
        '여성비율': round(female_pct, 1),
        '주요소비': main_consumption,
        '소비비율': round(main_consumption_pct, 1),
        '등급설명': row['등급설명']
    })

# 6. 저장
print("\n6. 결과 저장 중...")

# 페르소나별 추천
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('outputs/종합_페르소나별_추천결과.csv', index=False, encoding='utf-8-sig')
print(f"✓ 페르소나별 추천: outputs/종합_페르소나별_추천결과.csv")

# 전체 구 상세 정보
comprehensive_df = pd.DataFrame(comprehensive_data)
comprehensive_df.to_csv('outputs/종합_25개구_상세정보.csv', index=False, encoding='utf-8-sig')
print(f"✓ 전체 구 상세: outputs/종합_25개구_상세정보.csv")

# 7. 요약 통계
print(f"\n{'='*100}")
print("7. 요약 통계")
print(f"{'='*100}")

print(f"\n등급별 분포:")
grade_counts = comprehensive_df['등급'].value_counts().sort_index()
for grade, count in grade_counts.items():
    print(f"  {grade}급: {count}개 구")

print(f"\n점수 분포:")
print(f"  평균 종합점수: {comprehensive_df['종합점수'].mean():.1f}점")
print(f"  최고 점수: {comprehensive_df['종합점수'].max():.1f}점 ({comprehensive_df.loc[comprehensive_df['종합점수'].idxmax(), '구']})")
print(f"  최저 점수: {comprehensive_df['종합점수'].min():.1f}점 ({comprehensive_df.loc[comprehensive_df['종합점수'].idxmin(), '구']})")

print(f"\n특화업종 분포:")
industry_counts = comprehensive_df['주요특화업종'].value_counts().head(5)
for industry, count in industry_counts.items():
    print(f"  {industry}: {count}개 구")

print(f"\n{'='*100}")
print("✅ 전체 결과 정리 완료!")
print(f"{'='*100}")

