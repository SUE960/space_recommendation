#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실제 제공된 XML 데이터를 파싱하여 분석
"""

import pandas as pd
import numpy as np
import os
import json
import xml.etree.ElementTree as ET

# 실제 제공된 XML 데이터
REAL_API_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Map><list_total_count>8</list_total_count><LIVE_CMRCL_STTS><AREA_CMRCL_LVL>보통</AREA_CMRCL_LVL><AREA_SH_PAYMENT_CNT>92</AREA_SH_PAYMENT_CNT><AREA_SH_PAYMENT_AMT_MIN>3400000</AREA_SH_PAYMENT_AMT_MIN><AREA_SH_PAYMENT_AMT_MAX>3500000</AREA_SH_PAYMENT_AMT_MAX><CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>음식·음료</RSB_LRG_CTGR><RSB_MID_CTGR>한식</RSB_MID_CTGR><RSB_PAYMENT_LVL>보통</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>12</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>800000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>850000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>374</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>음식·음료</RSB_LRG_CTGR><RSB_MID_CTGR>일식/중식/양식</RSB_MID_CTGR><RSB_PAYMENT_LVL>한산한</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>4</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>450000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>500000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>179</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>음식·음료</RSB_LRG_CTGR><RSB_MID_CTGR>제과/커피/패스트푸드</RSB_MID_CTGR><RSB_PAYMENT_LVL>한산한</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>8</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>100000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>150000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>107</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>음식·음료</RSB_LRG_CTGR><RSB_MID_CTGR>기타요식</RSB_MID_CTGR><RSB_PAYMENT_LVL>한산한</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>7</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>150000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>200000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>310</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>유통</RSB_LRG_CTGR><RSB_MID_CTGR>할인점/슈퍼마켓</RSB_MID_CTGR><RSB_PAYMENT_LVL>분주한</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>8</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>100000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>150000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>12</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>유통</RSB_LRG_CTGR><RSB_MID_CTGR>편의점</RSB_MID_CTGR><RSB_PAYMENT_LVL>보통</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>13</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>100000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>150000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>39</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>패션·뷰티</RSB_LRG_CTGR><RSB_MID_CTGR>의복/의류</RSB_MID_CTGR><RSB_PAYMENT_LVL>보통</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>4</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>300000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>350000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>27</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB><CMRCL_RSB><RSB_LRG_CTGR>여가·오락</RSB_LRG_CTGR><RSB_MID_CTGR>스포츠/문화/레저</RSB_MID_CTGR><RSB_PAYMENT_LVL>바쁜</RSB_PAYMENT_LVL><RSB_SH_PAYMENT_CNT>36</RSB_SH_PAYMENT_CNT><RSB_SH_PAYMENT_AMT_MIN>1100000</RSB_SH_PAYMENT_AMT_MIN><RSB_SH_PAYMENT_AMT_MAX>1200000</RSB_SH_PAYMENT_AMT_MAX><RSB_MCT_CNT>75</RSB_MCT_CNT><RSB_MCT_TIME>202511</RSB_MCT_TIME></CMRCL_RSB></CMRCL_RSB><CMRCL_MALE_RATE>38.3</CMRCL_MALE_RATE><CMRCL_FEMALE_RATE>61.7</CMRCL_FEMALE_RATE><CMRCL_10_RATE>0.3</CMRCL_10_RATE><CMRCL_20_RATE>15.9</CMRCL_20_RATE><CMRCL_30_RATE>32.0</CMRCL_30_RATE><CMRCL_40_RATE>31.9</CMRCL_40_RATE><CMRCL_50_RATE>8.5</CMRCL_50_RATE><CMRCL_60_RATE>11.4</CMRCL_60_RATE><CMRCL_PERSONAL_RATE>95.0</CMRCL_PERSONAL_RATE><CMRCL_CORPORATION_RATE>5.0</CMRCL_CORPORATION_RATE><CMRCL_TIME>20251206 2100</CMRCL_TIME></LIVE_CMRCL_STTS><AREA_NM>광화문·덕수궁</AREA_NM><RESULT><resultCode>INFO-000</resultCode><resultMsg>정상 처리되었습니다.</resultMsg></RESULT><AREA_CD>POI009</AREA_CD></Map>
"""


def parse_real_api_data(xml_text):
    """실제 제공된 XML 데이터 파싱"""
    root = ET.fromstring(xml_text)
    
    # 기본 정보
    area_nm = root.find('.//AREA_NM').text
    area_cd = root.find('.//AREA_CD').text
    
    # LIVE_CMRCL_STTS
    live_stts = root.find('.//LIVE_CMRCL_STTS')
    
    area_cmrcl_lvl = live_stts.find('AREA_CMRCL_LVL').text
    area_sh_payment_cnt = int(live_stts.find('AREA_SH_PAYMENT_CNT').text)
    area_sh_payment_amt_min = int(live_stts.find('AREA_SH_PAYMENT_AMT_MIN').text)
    area_sh_payment_amt_max = int(live_stts.find('AREA_SH_PAYMENT_AMT_MAX').text)
    
    # 인구통계
    male_rate = float(live_stts.find('CMRCL_MALE_RATE').text)
    female_rate = float(live_stts.find('CMRCL_FEMALE_RATE').text)
    age_10_rate = float(live_stts.find('CMRCL_10_RATE').text)
    age_20_rate = float(live_stts.find('CMRCL_20_RATE').text)
    age_30_rate = float(live_stts.find('CMRCL_30_RATE').text)
    age_40_rate = float(live_stts.find('CMRCL_40_RATE').text)
    age_50_rate = float(live_stts.find('CMRCL_50_RATE').text)
    age_60_rate = float(live_stts.find('CMRCL_60_RATE').text)
    personal_rate = float(live_stts.find('CMRCL_PERSONAL_RATE').text)
    corporation_rate = float(live_stts.find('CMRCL_CORPORATION_RATE').text)
    cmrcl_time = live_stts.find('CMRCL_TIME').text
    
    # 업종별 데이터
    data_rows = []
    cmrcl_rsb = live_stts.find('CMRCL_RSB')
    
    for rsb in cmrcl_rsb.findall('CMRCL_RSB'):
        row = {
            'AREA_NM': area_nm,
            'AREA_CD': area_cd,
            'AREA_CMRCL_LVL': area_cmrcl_lvl,
            'AREA_SH_PAYMENT_CNT': area_sh_payment_cnt,
            'AREA_SH_PAYMENT_AMT_MIN': area_sh_payment_amt_min,
            'AREA_SH_PAYMENT_AMT_MAX': area_sh_payment_amt_max,
            'RSB_LRG_CTGR': rsb.find('RSB_LRG_CTGR').text,
            'RSB_MID_CTGR': rsb.find('RSB_MID_CTGR').text,
            'RSB_PAYMENT_LVL': rsb.find('RSB_PAYMENT_LVL').text,
            'RSB_SH_PAYMENT_CNT': int(rsb.find('RSB_SH_PAYMENT_CNT').text),
            'RSB_SH_PAYMENT_AMT_MIN': int(rsb.find('RSB_SH_PAYMENT_AMT_MIN').text),
            'RSB_SH_PAYMENT_AMT_MAX': int(rsb.find('RSB_SH_PAYMENT_AMT_MAX').text),
            'RSB_MCT_CNT': int(rsb.find('RSB_MCT_CNT').text),
            'RSB_MCT_TIME': rsb.find('RSB_MCT_TIME').text,
            'CMRCL_MALE_RATE': male_rate,
            'CMRCL_FEMALE_RATE': female_rate,
            'CMRCL_10_RATE': age_10_rate,
            'CMRCL_20_RATE': age_20_rate,
            'CMRCL_30_RATE': age_30_rate,
            'CMRCL_40_RATE': age_40_rate,
            'CMRCL_50_RATE': age_50_rate,
            'CMRCL_60_RATE': age_60_rate,
            'CMRCL_PERSONAL_RATE': personal_rate,
            'CMRCL_CORPORATION_RATE': corporation_rate,
            'CMRCL_TIME': cmrcl_time
        }
        data_rows.append(row)
    
    return pd.DataFrame(data_rows)


def main():
    print("="*80)
    print("실제 제공된 XML 데이터 파싱 및 분석")
    print("="*80)
    
    # XML 데이터 파싱
    print("\n[1단계] 실제 XML 데이터 파싱")
    print("-" * 80)
    df = parse_real_api_data(REAL_API_XML)
    print(f"✓ 데이터 파싱 완료: {len(df)}행")
    print(f"  핫스팟: {df['AREA_NM'].iloc[0]}")
    print(f"  업종 수: {df['RSB_LRG_CTGR'].nunique()}개")
    
    # 데이터 출력
    print("\n[2단계] 파싱된 데이터 확인")
    print("-" * 80)
    print(f"\n기본 정보:")
    print(f"  핫스팟명: {df['AREA_NM'].iloc[0]}")
    print(f"  핫스팟코드: {df['AREA_CD'].iloc[0]}")
    print(f"  상권 레벨: {df['AREA_CMRCL_LVL'].iloc[0]}")
    print(f"  총 결제 건수: {df['AREA_SH_PAYMENT_CNT'].iloc[0]}건")
    print(f"  결제 금액 범위: {df['AREA_SH_PAYMENT_AMT_MIN'].iloc[0]:,} ~ {df['AREA_SH_PAYMENT_AMT_MAX'].iloc[0]:,}원")
    
    print(f"\n인구통계:")
    print(f"  성별: 남성 {df['CMRCL_MALE_RATE'].iloc[0]}%, 여성 {df['CMRCL_FEMALE_RATE'].iloc[0]}%")
    print(f"  연령대:")
    print(f"    - 10대이하: {df['CMRCL_10_RATE'].iloc[0]}%")
    print(f"    - 20대: {df['CMRCL_20_RATE'].iloc[0]}%")
    print(f"    - 30대: {df['CMRCL_30_RATE'].iloc[0]}%")
    print(f"    - 40대: {df['CMRCL_40_RATE'].iloc[0]}%")
    print(f"    - 50대: {df['CMRCL_50_RATE'].iloc[0]}%")
    print(f"    - 60대이상: {df['CMRCL_60_RATE'].iloc[0]}%")
    
    print(f"\n업종별 정보:")
    for idx, row in df.iterrows():
        print(f"\n  {idx+1}. {row['RSB_LRG_CTGR']} - {row['RSB_MID_CTGR']}")
        print(f"     결제 건수: {row['RSB_SH_PAYMENT_CNT']}건")
        print(f"     결제 금액: {row['RSB_SH_PAYMENT_AMT_MIN']:,} ~ {row['RSB_SH_PAYMENT_AMT_MAX']:,}원")
        print(f"     상권 현황: {row['RSB_PAYMENT_LVL']}")
        print(f"     가맹점 수: {row['RSB_MCT_CNT']}개")
    
    # CSV 저장
    print("\n[3단계] 데이터 저장")
    print("-" * 80)
    os.makedirs('outputs', exist_ok=True)
    output_file = 'outputs/real_api_data_parsed.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✓ CSV 저장: {output_file}")
    
    print("\n" + "="*80)
    print("파싱 완료!")
    print("="*80)
    print(f"\n이 데이터를 analyze_realtime_profiles.py에서 사용할 수 있습니다.")
    
    return df


if __name__ == '__main__':
    result = main()

