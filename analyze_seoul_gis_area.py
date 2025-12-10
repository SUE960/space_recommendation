#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 GIS 광역 영역 정보(TbgisMegaRelmW) 분석
좌표 및 면적 데이터 파싱
"""

import pandas as pd
import xml.etree.ElementTree as ET
import os
import json


# 실제 제공된 GIS 영역 데이터 XML
GIS_AREA_XML = """<?xml version="1.0" encoding="UTF-8"?>
<TbgisMegaRelmW>
<list_total_count>1</list_total_count>
<RESULT>
<CODE>INFO-000</CODE>
<MESSAGE>정상 처리되었습니다</MESSAGE>
</RESULT>
<row>
<MEGA_CD>11</MEGA_CD>
<MEGA_NM>서울특별시</MEGA_NM>
<XCNTS_VALUE>199275</XCNTS_VALUE>
<YDNTS_VALUE>450264</YDNTS_VALUE>
<RELM_AR>605754669</RELM_AR>
</row>
</TbgisMegaRelmW>
"""


def parse_gis_area_data(xml_text):
    """GIS 영역 데이터 XML 파싱"""
    root = ET.fromstring(xml_text)
    
    data_rows = []
    for row in root.findall('.//row'):
        row_data = {}
        for child in row:
            tag = child.tag
            text = child.text
            
            if text and text.strip():
                # 숫자 필드는 적절한 타입으로 변환
                if tag in ['MEGA_CD', 'XCNTS_VALUE', 'YDNTS_VALUE', 'RELM_AR']:
                    try:
                        row_data[tag] = int(text)
                    except ValueError:
                        row_data[tag] = text
                else:
                    row_data[tag] = text
            else:
                row_data[tag] = None
        
        data_rows.append(row_data)
    
    df = pd.DataFrame(data_rows)
    return df


def analyze_gis_data(df):
    """GIS 데이터 분석"""
    print("\n" + "="*80)
    print("서울시 GIS 광역 영역 정보 분석")
    print("="*80)
    
    row = df.iloc[0]
    
    # 기본 정보
    print("\n[기본 정보]")
    print(f"지역 코드: {row['MEGA_CD']}")
    print(f"지역 명: {row['MEGA_NM']}")
    
    # 좌표 정보 (TM 좌표계로 추정)
    print("\n[중심점 좌표]")
    print(f"X 좌표 (경도): {row['XCNTS_VALUE']:,}")
    print(f"Y 좌표 (위도): {row['YDNTS_VALUE']:,}")
    print("※ TM (Transverse Mercator) 좌표계로 추정")
    
    # 면적 정보
    area_m2 = row['RELM_AR']
    area_km2 = area_m2 / 1_000_000  # 제곱미터 -> 제곱킬로미터
    
    print("\n[면적 정보]")
    print(f"영역 면적: {area_m2:,} ㎡")
    print(f"           {area_km2:,.2f} ㎢")
    print(f"※ 서울시 실제 면적: 약 605.2 ㎢")
    
    # 데이터 특성 분석
    print("\n[데이터 특성]")
    print("✓ 이 데이터는 서울시 전체의 지리적 정보입니다")
    print("✓ 중심점 좌표는 GIS 시스템에서 서울시의 기준점으로 사용됩니다")
    print("✓ 면적 데이터는 행정구역 경계 면적을 나타냅니다")
    
    return row


def suggest_data_usage():
    """데이터 활용 방안 제시"""
    print("\n" + "="*80)
    print("데이터 활용 방안")
    print("="*80)
    
    suggestions = [
        {
            "번호": 1,
            "용도": "지도 시각화 기준점",
            "설명": "서울시 지도 시각화 시 중심점 좌표로 활용",
            "예시": "카드 소비 데이터를 지도에 표시할 때 기준 좌표"
        },
        {
            "번호": 2,
            "용도": "공간 분석 기준",
            "설명": "구별 데이터를 서울시 전체 면적 대비로 분석",
            "예시": "강남구 면적 / 서울시 전체 면적 비율 계산"
        },
        {
            "번호": 3,
            "용도": "인구 밀도 계산",
            "설명": "인구 데이터와 결합하여 인구 밀도 산출",
            "예시": "서울시 인구 9,360,421명 / 605.75㎢ = 15,452명/㎢"
        },
        {
            "번호": 4,
            "용도": "상권 밀집도 분석",
            "설명": "단위 면적당 상권 수, 소비액 등 계산",
            "예시": "㎢당 평균 카드 소비액 계산"
        }
    ]
    
    for sug in suggestions:
        print(f"\n[활용방안 {sug['번호']}] {sug['용도']}")
        print(f"  설명: {sug['설명']}")
        print(f"  예시: {sug['예시']}")


def calculate_with_population():
    """인구 데이터와 결합한 계산"""
    print("\n" + "="*80)
    print("인구 데이터 결합 분석")
    print("="*80)
    
    # 앞서 분석한 인구 데이터 활용
    seoul_population = 9_360_421  # 2025Q1 기준
    seoul_area_km2 = 605.754669
    
    population_density = seoul_population / seoul_area_km2
    
    print(f"\n서울시 인구 밀도 계산:")
    print(f"  총 인구: {seoul_population:,}명")
    print(f"  총 면적: {seoul_area_km2:.2f}㎢")
    print(f"  인구 밀도: {population_density:,.0f}명/㎢")
    
    print(f"\n비교:")
    print(f"  - 서울시는 세계에서 가장 인구밀도가 높은 도시 중 하나입니다")
    print(f"  - 이는 약 0.01㎢(10,000㎡)당 155명에 해당합니다")


def save_gis_data(df):
    """GIS 데이터 저장"""
    os.makedirs('outputs', exist_ok=True)
    
    # 원본 데이터 저장
    output_file = 'outputs/seoul_gis_area.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ GIS 데이터 저장: {output_file}")
    
    # JSON 형태로도 저장 (API 응답 형태 유지)
    row = df.iloc[0]
    gis_info = {
        '지역코드': int(row['MEGA_CD']),
        '지역명': row['MEGA_NM'],
        '중심X좌표': int(row['XCNTS_VALUE']),
        '중심Y좌표': int(row['YDNTS_VALUE']),
        '면적_제곱미터': int(row['RELM_AR']),
        '면적_제곱킬로미터': round(row['RELM_AR'] / 1_000_000, 2),
        '인구밀도_명per제곱킬로미터': round(9_360_421 / (row['RELM_AR'] / 1_000_000), 0)
    }
    
    json_file = 'outputs/seoul_gis_area.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(gis_info, f, ensure_ascii=False, indent=2)
    print(f"✓ GIS JSON 저장: {json_file}")


def main():
    """메인 실행 함수"""
    print("="*80)
    print("서울시 GIS 광역 영역 정보 파싱 및 분석")
    print("="*80)
    
    # XML 데이터 파싱
    print("\n[1단계] XML 데이터 파싱")
    print("-" * 80)
    df = parse_gis_area_data(GIS_AREA_XML)
    print(f"✓ 데이터 파싱 완료: {len(df)}행")
    
    # 데이터 분석
    print("\n[2단계] 데이터 분석")
    print("-" * 80)
    row_data = analyze_gis_data(df)
    
    # 인구 데이터와 결합
    print("\n[3단계] 통합 분석")
    print("-" * 80)
    calculate_with_population()
    
    # 활용 방안
    suggest_data_usage()
    
    # 결과 저장
    print("\n[4단계] 결과 저장")
    print("-" * 80)
    save_gis_data(df)
    
    print("\n" + "="*80)
    print("분석 완료!")
    print("="*80)
    print("\n💡 이 GIS 데이터는 지도 시각화와 공간 분석의 기준으로 활용할 수 있습니다.")
    
    return df


if __name__ == '__main__':
    result = main()

