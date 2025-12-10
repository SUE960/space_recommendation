#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
import time

api_key = "6863727948726b6436345862527950"
base_url = "http://openapi.seoul.go.kr:8088"

found_hotspots = []

print("="*80)
print("서울시 전체 핫스팟 탐색 (POI001~POI100)")
print("="*80)

for i in range(1, 101):
    poi_code = f"POI{i:03d}"
    url = f"{base_url}/{api_key}/xml/citydata_cmrcl/1/5/{poi_code}/"
    
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200 and 'INFO-000' in response.text:
            root = ET.fromstring(response.text)
            area_nm = root.find('.//AREA_NM')
            if area_nm is not None and area_nm.text:
                found_hotspots.append((poi_code, area_nm.text))
                print(f"✓ {poi_code}: {area_nm.text}")
    except:
        pass
    
    if i % 20 == 0:
        print(f"  ... {i}/100 진행중")
    
    time.sleep(0.1)  # API 부하 방지

print("\n" + "="*80)
print(f"발견된 핫스팟: {len(found_hotspots)}개")
print("="*80)

for code, name in found_hotspots:
    print(f"{code}: {name}")

# 저장
with open('all_hotspots.txt', 'w', encoding='utf-8') as f:
    for code, name in found_hotspots:
        f.write(f"{code}\t{name}\n")
        
print(f"\n✓ all_hotspots.txt 저장 완료")
