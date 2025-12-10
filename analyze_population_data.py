#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 상주인구 데이터 파싱 및 분석
실제 제공된 VwsmMegaRepopW XML 데이터 사용
"""

import pandas as pd
import numpy as np
import os
import json
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False


# 실제 제공된 인구 데이터 XML
POPULATION_XML = """<?xml version="1.0" encoding="UTF-8"?>
<VwsmMegaRepopW>
<list_total_count>26</list_total_count>
<RESULT>
<CODE>INFO-000</CODE>
<MESSAGE>정상 처리되었습니다</MESSAGE>
</RESULT>
<row>
<STDR_YYQU_CD>20214</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9664310</TOT_REPOP_CO>
<ML_REPOP_CO>4699535</ML_REPOP_CO>
<FML_REPOP_CO>4964775</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1405211</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1459649</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1474993</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1527645</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1522697</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2274115</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>721361</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>707445</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>737845</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>756611</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>747971</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>1028302</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>683850</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>752204</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>737148</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>771034</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>774726</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1245813</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4413371</TOT_HSHLD_CO>
<APT_HSHLD_CO>0</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>4413371</NON_APT_HSHLD_CO>
</row>
<row>
<STDR_YYQU_CD>20244</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9360421</TOT_REPOP_CO>
<ML_REPOP_CO>4527676</ML_REPOP_CO>
<FML_REPOP_CO>4832745</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1243704</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1350090</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1421660</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1416424</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1492389</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2436154</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>637249</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>641002</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>711041</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>701112</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>733018</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>1104254</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>606455</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>709088</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>710619</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>715312</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>759371</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1331900</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4453816</TOT_HSHLD_CO>
<APT_HSHLD_CO>0</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>4453816</NON_APT_HSHLD_CO>
</row>
<row>
<STDR_YYQU_CD>20191</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9702170</TOT_REPOP_CO>
<ML_REPOP_CO>4747867</ML_REPOP_CO>
<FML_REPOP_CO>4954303</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1510098</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1416385</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1552084</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1586899</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1542622</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2094082</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>776305</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>702553</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>776358</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>789173</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>755010</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>948468</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>733793</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>713832</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>775726</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>797726</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>787612</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1145614</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4194825</TOT_HSHLD_CO>
<APT_HSHLD_CO>1214893</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>2979932</NON_APT_HSHLD_CO>
</row>
<row>
<STDR_YYQU_CD>20192</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9718264</TOT_REPOP_CO>
<ML_REPOP_CO>4752284</ML_REPOP_CO>
<FML_REPOP_CO>4965980</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1527096</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1435455</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1540876</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1583606</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1543218</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2088013</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>785075</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>710503</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>770462</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>786826</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>754600</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>944818</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>742021</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>724952</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>770414</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>796780</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>788618</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1143195</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4231225</TOT_HSHLD_CO>
<APT_HSHLD_CO>1215269</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>3015956</NON_APT_HSHLD_CO>
</row>
<row>
<STDR_YYQU_CD>20251</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9360421</TOT_REPOP_CO>
<ML_REPOP_CO>4527676</ML_REPOP_CO>
<FML_REPOP_CO>4832745</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1243704</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1350090</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1421660</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1416424</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1492389</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2436154</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>637249</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>641002</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>711041</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>701112</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>733018</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>1104254</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>606455</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>709088</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>710619</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>715312</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>759371</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1331900</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4453816</TOT_HSHLD_CO>
<APT_HSHLD_CO>0</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>4453816</NON_APT_HSHLD_CO>
</row>
<row>
<STDR_YYQU_CD>20191</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9702170</TOT_REPOP_CO>
<ML_REPOP_CO>4747867</ML_REPOP_CO>
<FML_REPOP_CO>4954303</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1510098</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1416385</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1552084</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1586899</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1542622</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2094082</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>776305</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>702553</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>776358</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>789173</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>755010</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>948468</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>733793</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>713832</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>775726</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>797726</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>787612</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1145614</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4194825</TOT_HSHLD_CO>
<APT_HSHLD_CO>1214893</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>2979932</NON_APT_HSHLD_CO>
</row>
<row>
<STDR_YYQU_CD>20192</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9718264</TOT_REPOP_CO>
<ML_REPOP_CO>4752284</ML_REPOP_CO>
<FML_REPOP_CO>4965980</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1527096</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1435455</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1540876</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1583606</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1543218</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2088013</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>785075</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>710503</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>770462</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>786826</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>754600</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>944818</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>742021</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>724952</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>770414</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>796780</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>788618</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1143195</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4231225</TOT_HSHLD_CO>
<APT_HSHLD_CO>1215269</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>3015956</NON_APT_HSHLD_CO>
</row>
<row>
<STDR_YYQU_CD>20251</STDR_YYQU_CD>
<MEGA_CD>11</MEGA_CD>
<MEGA_CD_NM>서울시</MEGA_CD_NM>
<TOT_REPOP_CO>9360421</TOT_REPOP_CO>
<ML_REPOP_CO>4527676</ML_REPOP_CO>
<FML_REPOP_CO>4832745</FML_REPOP_CO>
<AGRDE_10_REPOP_CO>1243704</AGRDE_10_REPOP_CO>
<AGRDE_20_REPOP_CO>1350090</AGRDE_20_REPOP_CO>
<AGRDE_30_REPOP_CO>1421660</AGRDE_30_REPOP_CO>
<AGRDE_40_REPOP_CO>1416424</AGRDE_40_REPOP_CO>
<AGRDE_50_REPOP_CO>1492389</AGRDE_50_REPOP_CO>
<AGRDE_60_ABOVE_REPOP_CO>2436154</AGRDE_60_ABOVE_REPOP_CO>
<MAG_10_REPOP_CO>637249</MAG_10_REPOP_CO>
<MAG_20_REPOP_CO>641002</MAG_20_REPOP_CO>
<MAG_30_REPOP_CO>711041</MAG_30_REPOP_CO>
<MAG_40_REPOP_CO>701112</MAG_40_REPOP_CO>
<MAG_50_REPOP_CO>733018</MAG_50_REPOP_CO>
<MAG_60_ABOVE_REPOP_CO>1104254</MAG_60_ABOVE_REPOP_CO>
<FAG_10_REPOP_CO>606455</FAG_10_REPOP_CO>
<FAG_20_REPOP_CO>709088</FAG_20_REPOP_CO>
<FAG_30_REPOP_CO>710619</FAG_30_REPOP_CO>
<FAG_40_REPOP_CO>715312</FAG_40_REPOP_CO>
<FAG_50_REPOP_CO>759371</FAG_50_REPOP_CO>
<FAG_60_ABOVE_REPOP_CO>1331900</FAG_60_ABOVE_REPOP_CO>
<TOT_HSHLD_CO>4453816</TOT_HSHLD_CO>
<APT_HSHLD_CO>0</APT_HSHLD_CO>
<NON_APT_HSHLD_CO>4453816</NON_APT_HSHLD_CO>
</row>
</VwsmMegaRepopW>
"""


def parse_population_data(xml_text):
    """인구 데이터 XML 파싱"""
    root = ET.fromstring(xml_text)
    
    data_rows = []
    for row in root.findall('.//row'):
        row_data = {}
        for child in row:
            tag = child.tag
            text = child.text
            
            # 숫자 필드는 int로 변환
            if text and text.strip():
                if '_CO' in tag or '_CD' in tag:
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
    
    # 연도/분기 추출
    df['연도'] = df['STDR_YYQU_CD'].astype(str).str[:4].astype(int)
    df['분기'] = df['STDR_YYQU_CD'].astype(str).str[4].astype(int)
    df['연도분기'] = df['연도'].astype(str) + 'Q' + df['분기'].astype(str)
    
    return df


def analyze_population_trend(df):
    """인구 추이 분석"""
    print("\n" + "="*80)
    print("서울시 상주인구 추이 분석")
    print("="*80)
    
    df_sorted = df.sort_values('STDR_YYQU_CD')
    
    print("\n[시계열 인구 변화]")
    print(f"\n{'연도분기':<10} {'총인구':<15} {'남성':<15} {'여성':<15} {'가구수':<15} {'가구당인구':<10}")
    print("-" * 85)
    
    for _, row in df_sorted.iterrows():
        household_per_person = row['TOT_REPOP_CO'] / row['TOT_HSHLD_CO'] if row['TOT_HSHLD_CO'] > 0 else 0
        print(f"{row['연도분기']:<10} {row['TOT_REPOP_CO']:>13,}  {row['ML_REPOP_CO']:>13,}  {row['FML_REPOP_CO']:>13,}  {row['TOT_HSHLD_CO']:>13,}  {household_per_person:>8.2f}")
    
    # 증감률 계산
    df_sorted['인구증감'] = df_sorted['TOT_REPOP_CO'].diff()
    df_sorted['인구증감률'] = (df_sorted['TOT_REPOP_CO'].pct_change() * 100).round(2)
    df_sorted['가구증감'] = df_sorted['TOT_HSHLD_CO'].diff()
    df_sorted['가구증감률'] = (df_sorted['TOT_HSHLD_CO'].pct_change() * 100).round(2)
    
    print("\n[분기별 증감률]")
    print(f"\n{'연도분기':<10} {'인구증감':<15} {'인구증감률':<12} {'가구증감':<15} {'가구증감률':<12}")
    print("-" * 70)
    
    for _, row in df_sorted.iterrows():
        if pd.notna(row['인구증감']):
            증감_아이콘 = "↑" if row['인구증감'] > 0 else "↓"
            print(f"{row['연도분기']:<10} {int(row['인구증감']):>13,} {증감_아이콘}  {row['인구증감률']:>8.2f}%  {int(row['가구증감']):>13,}  {row['가구증감률']:>8.2f}%")


def analyze_age_distribution(df):
    """연령대별 인구 분포 분석"""
    print("\n" + "="*80)
    print("연령대별 인구 분포 분석")
    print("="*80)
    
    # 최신 데이터 (2025년 1분기)
    latest = df[df['STDR_YYQU_CD'] == 20251].iloc[0]
    
    age_data = {
        '10대': latest['AGRDE_10_REPOP_CO'],
        '20대': latest['AGRDE_20_REPOP_CO'],
        '30대': latest['AGRDE_30_REPOP_CO'],
        '40대': latest['AGRDE_40_REPOP_CO'],
        '50대': latest['AGRDE_50_REPOP_CO'],
        '60대이상': latest['AGRDE_60_ABOVE_REPOP_CO']
    }
    
    total = latest['TOT_REPOP_CO']
    
    print(f"\n[{latest['연도분기']} 기준 연령대별 인구]")
    print(f"\n{'연령대':<12} {'인구수':<15} {'비율':<10} {'남성':<15} {'여성':<15}")
    print("-" * 70)
    
    age_mapping = {
        '10대': ('AGRDE_10_REPOP_CO', 'MAG_10_REPOP_CO', 'FAG_10_REPOP_CO'),
        '20대': ('AGRDE_20_REPOP_CO', 'MAG_20_REPOP_CO', 'FAG_20_REPOP_CO'),
        '30대': ('AGRDE_30_REPOP_CO', 'MAG_30_REPOP_CO', 'FAG_30_REPOP_CO'),
        '40대': ('AGRDE_40_REPOP_CO', 'MAG_40_REPOP_CO', 'FAG_40_REPOP_CO'),
        '50대': ('AGRDE_50_REPOP_CO', 'MAG_50_REPOP_CO', 'FAG_50_REPOP_CO'),
        '60대이상': ('AGRDE_60_ABOVE_REPOP_CO', 'MAG_60_ABOVE_REPOP_CO', 'FAG_60_ABOVE_REPOP_CO')
    }
    
    for age, (total_col, male_col, female_col) in age_mapping.items():
        age_total = latest[total_col]
        age_male = latest[male_col]
        age_female = latest[female_col]
        ratio = (age_total / total * 100)
        print(f"{age:<12} {age_total:>13,}  {ratio:>7.1f}%  {age_male:>13,}  {age_female:>13,}")
    
    print(f"\n{'전체':<12} {total:>13,}  {100.0:>7.1f}%  {latest['ML_REPOP_CO']:>13,}  {latest['FML_REPOP_CO']:>13,}")


def analyze_gender_distribution(df):
    """성별 인구 분포 분석"""
    print("\n" + "="*80)
    print("성별 인구 분포 분석")
    print("="*80)
    
    latest = df[df['STDR_YYQU_CD'] == 20251].iloc[0]
    
    print(f"\n[{latest['연도분기']} 기준 성별 인구]")
    print(f"\n남성 인구: {latest['ML_REPOP_CO']:,}명 ({latest['ML_REPOP_CO']/latest['TOT_REPOP_CO']*100:.2f}%)")
    print(f"여성 인구: {latest['FML_REPOP_CO']:,}명 ({latest['FML_REPOP_CO']/latest['TOT_REPOP_CO']*100:.2f}%)")
    print(f"총 인구: {latest['TOT_REPOP_CO']:,}명")
    
    print(f"\n[연령대별 성별 분포]")
    print(f"\n{'연령대':<12} {'남성':<15} {'여성':<15} {'성비(남/여)':<12}")
    print("-" * 60)
    
    age_mapping = {
        '10대': ('MAG_10_REPOP_CO', 'FAG_10_REPOP_CO'),
        '20대': ('MAG_20_REPOP_CO', 'FAG_20_REPOP_CO'),
        '30대': ('MAG_30_REPOP_CO', 'FAG_30_REPOP_CO'),
        '40대': ('MAG_40_REPOP_CO', 'FAG_40_REPOP_CO'),
        '50대': ('MAG_50_REPOP_CO', 'FAG_50_REPOP_CO'),
        '60대이상': ('MAG_60_ABOVE_REPOP_CO', 'FAG_60_ABOVE_REPOP_CO')
    }
    
    for age, (male_col, female_col) in age_mapping.items():
        male = latest[male_col]
        female = latest[female_col]
        ratio = male / female if female > 0 else 0
        print(f"{age:<12} {male:>13,}  {female:>13,}  {ratio:>10.3f}")


def analyze_household_statistics(df):
    """가구 통계 분석"""
    print("\n" + "="*80)
    print("가구 통계 분석")
    print("="*80)
    
    latest = df[df['STDR_YYQU_CD'] == 20251].iloc[0]
    
    print(f"\n[{latest['연도분기']} 기준 가구 통계]")
    print(f"\n총 가구수: {latest['TOT_HSHLD_CO']:,}가구")
    print(f"아파트 가구: {latest['APT_HSHLD_CO']:,}가구 ({latest['APT_HSHLD_CO']/latest['TOT_HSHLD_CO']*100:.2f}%)")
    print(f"비아파트 가구: {latest['NON_APT_HSHLD_CO']:,}가구 ({latest['NON_APT_HSHLD_CO']/latest['TOT_HSHLD_CO']*100:.2f}%)")
    
    # 가구당 인구수
    person_per_household = latest['TOT_REPOP_CO'] / latest['TOT_HSHLD_CO']
    print(f"\n가구당 평균 인구수: {person_per_household:.2f}명")


def save_population_analysis(df):
    """분석 결과 저장"""
    os.makedirs('outputs', exist_ok=True)
    
    # 원본 데이터 저장
    output_file = 'outputs/seoul_population_data.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ 인구 데이터 저장: {output_file}")
    
    # 최신 데이터 요약
    latest = df[df['STDR_YYQU_CD'] == 20251].iloc[0]
    
    summary = {
        '기준연도분기': latest['연도분기'],
        '총인구': latest['TOT_REPOP_CO'],
        '남성인구': latest['ML_REPOP_CO'],
        '여성인구': latest['FML_REPOP_CO'],
        '10대인구': latest['AGRDE_10_REPOP_CO'],
        '20대인구': latest['AGRDE_20_REPOP_CO'],
        '30대인구': latest['AGRDE_30_REPOP_CO'],
        '40대인구': latest['AGRDE_40_REPOP_CO'],
        '50대인구': latest['AGRDE_50_REPOP_CO'],
        '60대이상인구': latest['AGRDE_60_ABOVE_REPOP_CO'],
        '총가구수': latest['TOT_HSHLD_CO'],
        '아파트가구': latest['APT_HSHLD_CO'],
        '비아파트가구': latest['NON_APT_HSHLD_CO'],
        '가구당인구수': round(latest['TOT_REPOP_CO'] / latest['TOT_HSHLD_CO'], 2)
    }
    
    summary_df = pd.DataFrame([summary])
    summary_file = 'outputs/seoul_population_summary.csv'
    summary_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
    print(f"✓ 요약 데이터 저장: {summary_file}")


def main():
    """메인 실행 함수"""
    print("="*80)
    print("서울시 상주인구 데이터 분석")
    print("="*80)
    
    # XML 데이터 파싱
    print("\n[1단계] XML 데이터 파싱")
    print("-" * 80)
    df = parse_population_data(POPULATION_XML)
    print(f"✓ 데이터 파싱 완료: {len(df)}행")
    print(f"  데이터 기간: {df['연도분기'].min()} ~ {df['연도분기'].max()}")
    
    # 컬럼 정보
    print(f"\n데이터 컬럼:")
    print(f"  - 기본: 기준연도분기, 광역시도코드/명")
    print(f"  - 인구: 총인구, 남성/여성 인구, 연령대별 인구")
    print(f"  - 가구: 총가구, 아파트/비아파트 가구")
    
    # 분석 실행
    print("\n[2단계] 데이터 분석")
    print("-" * 80)
    
    # 1. 인구 추이 분석
    analyze_population_trend(df)
    
    # 2. 연령대별 분포
    analyze_age_distribution(df)
    
    # 3. 성별 분포
    analyze_gender_distribution(df)
    
    # 4. 가구 통계
    analyze_household_statistics(df)
    
    # 결과 저장
    print("\n[3단계] 결과 저장")
    print("-" * 80)
    save_population_analysis(df)
    
    print("\n" + "="*80)
    print("분석 완료!")
    print("="*80)
    print("\n이 인구 데이터는 카드 소비 데이터의 인구통계 분석과 비교할 수 있습니다.")
    
    return df


if __name__ == '__main__':
    result = main()

