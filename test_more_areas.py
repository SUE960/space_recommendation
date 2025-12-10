#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'data_api')
from api_client import SeoulCommercialAreaAPI

api_key = "6863727948726b6436345862527950"
client = SeoulCommercialAreaAPI(api_key=api_key)

# 더 많은 지역 시도
test_areas = [
    "강남역", "홍대입구", "광화문·덕수궁", "명동", "이태원", 
    "신촌", "건대입구", "잠실", "압구정", "성수동", 
    "여의도", "종로", "동대문", "가로수길", "경복궁"
]

print("="*80)
print("지역별 API 테스트")
print("="*80)

for area in test_areas:
    try:
        df = client.get_commercial_area_status(area)
        if len(df) > 0:
            print(f"✓ {area}: {len(df)}개 업종 데이터")
        else:
            print(f"✗ {area}: 데이터 없음")
    except Exception as e:
        print(f"✗ {area}: 에러 - {str(e)[:50]}")
