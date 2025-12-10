#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'data_api')
from api_client import SeoulCommercialAreaAPI
sys.path.insert(0, '.')
from analyze_realtime_profiles import analyze_all_areas

api_key = "6863727948726b6436345862527950"
client = SeoulCommercialAreaAPI(api_key=api_key)

# 데이터 수집 가능한 전체 지역
all_areas = ["강남역", "연남동", "가로수길", "광화문·덕수궁", "여의도"]

print("="*80)
print("서울 전체 지역 실시간 점수표 (API 기반)")
print("="*80)

df = client.get_all_data(all_areas)
profiles = analyze_all_areas(df)

# 점수별 정렬
profiles_sorted = sorted(profiles, key=lambda x: x['scores']['comprehensive']['comprehensive_score'], reverse=True)

print("\n" + "="*80)
print("전체 지역 순위표")
print("="*80)

print(f"\n{'순위':<4} {'지역명':<15} {'종합':<8} {'활성도':<8} {'특화':<8} {'인구':<8} {'등급':<15} {'특화업종':<20}")
print("-" * 100)

for idx, profile in enumerate(profiles_sorted, 1):
    basic = profile['basic_info']
    comp = profile['scores']['comprehensive']
    activity = profile['scores']['activity']
    spec = profile['scores']['specialization']
    demo = profile['scores']['demographic']
    
    print(f"{idx:<4} {basic['area_nm']:<15} "
          f"{comp['comprehensive_score']:>6.2f}  "
          f"{activity['activity_score']:>6.2f}  "
          f"{spec['top_score']:>6.2f}  "
          f"{demo['demographic_score']/2:>6.2f}  "
          f"{comp['grade']:<15} "
          f"{spec['top_industry']} {spec['top_score']:.1f}%")

# 상세 정보 출력
print("\n" + "="*80)
print("상세 분석")
print("="*80)

for idx, profile in enumerate(profiles_sorted, 1):
    basic = profile['basic_info']
    comp = profile['scores']['comprehensive']
    activity = profile['scores']['activity']
    spec = profile['scores']['specialization']
    demo = profile['scores']['demographic']
    
    print(f"\n【{idx}위】 {basic['area_nm']} ({basic['area_cd']}) - {comp['comprehensive_score']:.2f}점")
    print(f"├─ 상권레벨: {basic['area_level']}")
    print(f"├─ 등급: {comp['grade']}")
    print(f"│")
    print(f"├─ 📊 상권활성도: {activity['activity_score']:.2f}점")
    print(f"│   ├─ 결제건수: {activity['payment_cnt']}건")
    print(f"│   ├─ 결제금액: {activity['payment_amt']:,.0f}원")
    print(f"│   └─ 업종다양성: {activity['industry_diversity']}개")
    print(f"│")
    print(f"├─ 🎯 특화점수: {spec['top_score']:.2f}점")
    print(f"│   └─ {spec['top_industry']}: {spec['top_score']:.1f}%")
    print(f"│")
    print(f"├─ 👥 인구통계: {demo['demographic_score']:.2f}점")
    print(f"│   ├─ 성별: 남 {demo['gender_info'].get('male', 0):.1f}% / 여 {demo['gender_info'].get('female', 0):.1f}%")
    
    # 주요 연령대 찾기
    age_details = demo['age_details']
    top_age = max(age_details.items(), key=lambda x: x[1]['rate'])
    print(f"│   └─ 주요연령: {top_age[0]} {top_age[1]['rate']:.1f}%")
    print(f"│")
    print(f"└─ 🏪 주요업종: {len(profile['industry_info'])}개")
    for i, ind in enumerate(profile['industry_info'][:3], 1):
        print(f"    {i}. {ind['large_category']}/{ind['mid_category']}: {ind['payment_cnt']}건 (가맹점 {ind['merchant_cnt']}개)")

print("\n" + "="*80)
print("완료!")
print("="*80)
