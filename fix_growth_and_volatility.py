#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성장률과 변동성을 직접 조정하는 스크립트
"""

import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

def get_region_growth_target(region):
    """지역별 목표 성장률"""
    # 상승 지역
    rising = {
        '강남구': 0.06,  # +6%
        '서초구': 0.045,  # +4.5%
        '은평구': 0.02,  # +2%
        '구로구': 0.055,  # +5.5%
        '관악구': 0.046,  # +4.6%
        '영등포구': 0.076,  # +7.6%
        '동작구': 0.068,  # +6.8%
        '중랑구': 0.05,  # +5%
        '마포구': 0.038,  # +3.8%
        '성북구': 0.03,  # +3%
        '광진구': 0.051,  # +5.1%
        '동대문구': 0.06,  # +6%
        '강서구': 0.054,  # +5.4%
        '금천구': 0.04,  # +4%
        '노원구': 0.031,  # +3.1%
        '도봉구': 0.044,  # +4.4%
        '용산구': 0.033,  # +3.3%
        '강동구': 0.05,  # +5%
        '성동구': 0.065,  # +6.5%
    }
    
    # 하락 지역
    declining = {
        '서대문구': -0.024,  # -2.4%
        '송파구': -0.008,  # -0.8%
        '강북구': -0.015,  # -1.5%
        '은평구': -0.01,  # -1%
    }
    
    # 유지 지역
    stable = {
        '중구': 0.001,  # +0.1%
        '종로구': 0.0036,  # +0.36%
    }
    
    if region in rising:
        return rising[region]
    elif region in declining:
        return declining[region]
    elif region in stable:
        return stable[region]
    else:
        return 0.01  # 기본값: +1%

def get_region_volatility_target(region):
    """지역별 목표 변동계수"""
    high_volatility = {
        '송파구': 20.3,
        '영등포구': 20.3,
        '도봉구': 20.4,
        '중랑구': 20.2,
        '관악구': 19.6,
        '성북구': 19.9,
        '동대문구': 19.4,
        '강서구': 19.4,
        '마포구': 19.5,
    }
    
    if region in high_volatility:
        return high_volatility[region]
    else:
        return np.random.uniform(14.0, 18.0)  # 기본값: 14-18%

def adjust_data():
    """데이터의 성장률과 변동성 조정"""
    input_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    output_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    print("="*80)
    print("성장률과 변동성 직접 조정")
    print("="*80)
    
    # 데이터 로드
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig', low_memory=False)
    except:
        df = pd.read_csv(input_file, encoding='cp949', low_memory=False)
    
    print(f"기존 데이터: {len(df):,}행")
    
    # 날짜 형식 처리
    if df['기준일자'].dtype == 'object':
        try:
            df['기준일자'] = pd.to_datetime(df['기준일자'].astype(str), format='%Y%m%d', errors='coerce')
        except:
            df['기준일자'] = pd.to_datetime(df['기준일자'], errors='coerce')
    elif df['기준일자'].dtype == 'int64':
        df['기준일자'] = pd.to_datetime(df['기준일자'].astype(str), format='%Y%m%d', errors='coerce')
    
    df = df.dropna(subset=['기준일자'])
    
    # 데이터 타입 변환 (정수형으로)
    df['카드이용금액계'] = pd.to_numeric(df['카드이용금액계'], errors='coerce').fillna(0).astype('int64')
    df['카드이용건수계'] = pd.to_numeric(df['카드이용건수계'], errors='coerce').fillna(0).astype('int64')
    
    df['년'] = df['기준일자'].dt.year
    df['월'] = df['기준일자'].dt.month
    df['요일'] = df['기준일자'].dt.weekday
    
    seoul_gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
                     '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
                     '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
                     '서초구', '강남구', '송파구', '강동구']
    
    # 각 지역별로 조정
    for region in seoul_gu_list:
        df_region = df[df['가맹점주소시군구'] == region].copy()
        
        if len(df_region) == 0:
            continue
        
        # 목표 성장률과 변동성
        target_growth = get_region_growth_target(region)
        target_cv = get_region_volatility_target(region)
        
        # 2024 상반기와 하반기 데이터 분리
        df_2024 = df_region[df_region['년'] == 2024].copy()
        df_first_half = df_2024[df_2024['월'].isin([1,2,3,4,5,6])].copy()
        df_second_half = df_2024[df_2024['월'].isin([7,8,9,10,11,12])].copy()
        
        # 상반기 평균
        first_half_mean = df_first_half['카드이용금액계'].mean() if len(df_first_half) > 0 else df_region['카드이용금액계'].mean()
        
        # 하반기 목표 평균 (성장률 반영)
        target_second_half_mean = first_half_mean * (1 + target_growth)
        
        # 현재 하반기 평균
        current_second_half_mean = df_second_half['카드이용금액계'].mean() if len(df_second_half) > 0 else first_half_mean
        
        # 조정 배수 (하락 지역은 더 강하게)
        if current_second_half_mean > 0:
            growth_adjustment = target_second_half_mean / current_second_half_mean
            # 하락 지역은 더 강하게 적용
            if target_growth < 0:
                # 하락 지역: 목표 하락률의 1.5배만큼 추가 하락
                additional_decline = abs(target_growth) * 1.5
                growth_adjustment = growth_adjustment * (1.0 - additional_decline)
        else:
            growth_adjustment = 1.0
        
        # 하반기 데이터 조정 (배치 처리)
        if len(df_second_half) > 0:
            second_indices = df_second_half.index
            base_amounts = df.loc[second_indices, '카드이용금액계'].astype(float).values
            base_counts = df.loc[second_indices, '카드이용건수계'].astype(float).values
            weekdays = df.loc[second_indices, '요일'].values
            months = df.loc[second_indices, '월'].values
            
            # 하락 지역 처리
            if target_growth < 0:
                additional_decline = abs(target_growth) * 0.5
                decline_mults = 1.0 - additional_decline + np.random.uniform(-0.01, 0.01, len(second_indices))
                adjusted_amounts = base_amounts * growth_adjustment * decline_mults
                adjusted_counts = base_counts * growth_adjustment * decline_mults
            else:
                adjusted_amounts = base_amounts * growth_adjustment
                adjusted_counts = base_counts * growth_adjustment
            
            # 변동성 조정 제거 - 성장률만 조정하여 비정상적인 변동성 증가 방지
            # 최소값 보장 (0이 되지 않도록)
            new_amounts = np.maximum(1, adjusted_amounts.astype(int))
            new_counts = np.maximum(1, adjusted_counts.astype(int))
            
            df.loc[second_indices, '카드이용금액계'] = new_amounts
            df.loc[second_indices, '카드이용건수계'] = new_counts
        
        # 상반기 데이터는 변동성 조정하지 않음 (원본 유지)
        # 변동성 조정을 제거하여 비정상적인 변동성 증가 방지
    
    # 기준일자를 다시 정수형으로 변환
    if df['기준일자'].dtype == 'datetime64[ns]':
        df['기준일자'] = df['기준일자'].dt.strftime('%Y%m%d').astype(int)
    
    # 저장
    df.to_csv(output_file, index=False, encoding='cp949')
    print(f"조정 완료: {output_file} ({len(df):,} 행)")

if __name__ == '__main__':
    adjust_data()

