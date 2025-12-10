#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'data_api')
from api_client import SeoulCommercialAreaAPI
sys.path.insert(0, '.')
from analyze_realtime_profiles import analyze_all_areas, save_analysis_results, print_analysis_results

api_key = "6863727948726b6436345862527950"
client = SeoulCommercialAreaAPI(api_key=api_key)

# 작동하는 지역만
working_areas = ["강남역", "광화문·덕수궁", "여의도", "가로수길"]

print("="*80)
print("실제 API 데이터 기반 지역 점수 분석")
print("="*80)

df = client.get_all_data(working_areas)
print(f"\n✓ 총 {len(df)}행 수집 완료")

# 프로필 생성
profiles = analyze_all_areas(df)
print(f"\n✓ {len(profiles)}개 지역 프로필 생성")

# 결과 출력
print_analysis_results(profiles)

# 저장
summary_df = save_analysis_results(profiles)

print("\n" + "="*80)
print("완료!")
print("="*80)
