#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET

api_key = "6863727948726b6436345862527950"

# 서울시 도시데이터 API 엔드포인트 (핫스팟 목록)
# citydata와 citydata_cmrcl은 다른 API입니다
base_url = "http://openapi.seoul.go.kr:8088"

# 여러 가능한 핫스팟 코드 시도
print("="*80)
print("핫스팟 코드 탐색")
print("="*80)

# POI 코드 범위 테스트
for i in range(1, 100):
    poi_code = f"POI{i:03d}"
    url = f"{base_url}/{api_key}/xml/citydata_cmrcl/1/5/{poi_code}/"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and 'INFO-000' in response.text:
            # 성공한 경우 지역명 추출
            root = ET.fromstring(response.text)
            area_nm = root.find('.//AREA_NM')
            if area_nm is not None:
                print(f"✓ {poi_code}: {area_nm.text}")
        elif i % 10 == 0:
            print(f"  ... {poi_code} 시도중")
    except:
        pass

print("\n완료!")
