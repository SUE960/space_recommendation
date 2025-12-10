#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'data_api')
from api_client import SeoulCommercialAreaAPI

api_key = "6863727948726b6436345862527950"
client = SeoulCommercialAreaAPI(api_key=api_key)

# 서울 주요 상권/핫스팟 리스트 (50개 이상)
test_areas = [
    # 강남권
    "강남역", "역삼", "선릉", "삼성", "청담", "압구정", "신사동", "가로수길", "논현동",
    # 강북권
    "광화문", "광화문·덕수궁", "시청", "종로", "종각", "을지로", "명동", "남대문", "동대문",
    # 홍대/신촌권
    "홍대", "홍대입구", "신촌", "이대", "연남동", "망원동",
    # 이태원/한남권
    "이태원", "한남동", "경리단길", "해방촌",
    # 여의도/영등포권
    "여의도", "영등포", "문래동", "양평동",
    # 잠실/송파권
    "잠실", "잠실새내", "석촌", "방이", "송파",
    # 강동권
    "천호", "길동", "둔촌동", "고덕",
    # 성동/광진권
    "건대", "건대입구", "성수", "성수동", "왕십리", "뚝섬",
    # 용산권
    "용산", "삼각지", "숙대입구",
    # 서초권
    "서초", "교대", "방배", "반포",
    # 마포권
    "공덕", "마포", "상암동", "DMC",
    # 은평/서대문권
    "신촌", "연신내", "불광", "녹번",
    # 성북/강북권
    "성신여대", "미아", "수유", "노원", "상계",
    # 기타
    "혜화", "대학로", "이촌동", "경복궁", "창덕궁", "덕수궁", "N서울타워", "63빌딩"
]

print("="*80)
print("서울 전체 지역 API 데이터 가용성 테스트")
print("="*80)

working_areas = []
failed_areas = []

for area in test_areas:
    try:
        df = client.get_commercial_area_status(area)
        if len(df) > 0:
            working_areas.append((area, len(df)))
            print(f"✓ {area}: {len(df)}개 업종")
        else:
            failed_areas.append(area)
    except Exception as e:
        failed_areas.append(area)

print("\n" + "="*80)
print(f"결과: 성공 {len(working_areas)}개 / 실패 {len(failed_areas)}개")
print("="*80)

print("\n✅ 데이터 수집 가능 지역:")
for area, count in sorted(working_areas, key=lambda x: -x[1]):
    print(f"  - {area}: {count}개 업종")

# 작동하는 지역 리스트 저장
with open('working_areas.txt', 'w') as f:
    for area, _ in working_areas:
        f.write(f"{area}\n")
        
print(f"\n✓ working_areas.txt 저장 완료 ({len(working_areas)}개 지역)")
