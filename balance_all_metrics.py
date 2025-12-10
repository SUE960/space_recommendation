#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 지표를 균형있게 조정하는 스크립트
- 성장률: 상승, 하락, 유지 골고루
- 업종 다양성: 낮음, 보통, 높음 골고루
- 소비 안정성: 변동성높음, 안정적, 보통, 매우안정 골고루
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def balance_metrics():
    """모든 지표를 균형있게 조정"""
    input_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    output_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    print("="*80)
    print("모든 지표 균형 조정 시작")
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
    df['년'] = df['기준일자'].dt.year
    df['월'] = df['기준일자'].dt.month
    
    seoul_gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
                     '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
                     '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
                     '서초구', '강남구', '송파구', '강동구']
    
    # 지역별 목표 설정
    # 성장률: 상승 8개, 하락 8개, 유지 9개
    growth_targets = {
        # 상승 지역 (8개)
        '강남구': 0.08, '서초구': 0.06, '송파구': 0.05, '영등포구': 0.07,
        '용산구': 0.04, '마포구': 0.05, '성동구': 0.06, '동작구': 0.05,
        # 하락 지역 (8개) - 더 강하게
        '구로구': -0.08, '금천구': -0.06, '양천구': -0.09, '관악구': -0.05,
        '강북구': -0.06, '도봉구': -0.05, '노원구': -0.04, '은평구': -0.05,
        # 유지 지역 (9개)
        '중구': 0.001, '종로구': -0.001, '중랑구': 0.002, '광진구': 0.001,
        '동대문구': -0.001, '성북구': 0.001, '강서구': -0.001, '강동구': 0.001,
        '서대문구': 0.0
    }
    
    # 업종 다양성 목표: 낮음(4-9개) 8개, 보통(10-14개) 9개, 높음(15개 이상) 8개
    diversity_targets = {
        # 낮음 (8개)
        '강남구': 5, '서초구': 6, '구로구': 4, '금천구': 5,
        '양천구': 4, '관악구': 5, '강북구': 4, '도봉구': 5,
        # 보통 (9개)
        '중구': 12, '종로구': 11, '중랑구': 10, '광진구': 13,
        '동대문구': 11, '성북구': 12, '강서구': 10, '강동구': 11,
        '서대문구': 12,
        # 높음 (8개)
        '용산구': 16, '마포구': 15, '성동구': 17, '동작구': 15,
        '노원구': 16, '은평구': 15, '영등포구': 16, '송파구': 17
    }
    
    # 소비 안정성 목표 (CV 기준)
    # 변동성높음(>30%) 6개, 보통(20-30%) 7개, 안정적(15-20%) 6개, 매우안정(<15%) 6개
    stability_targets = {
        # 변동성높음 (>30%) 6개
        '구로구': 35.0, '금천구': 32.0, '양천구': 38.0, '관악구': 33.0,
        '강북구': 31.0, '도봉구': 34.0,
        # 보통 (20-30%) 7개
        '중구': 25.0, '종로구': 22.0, '중랑구': 24.0, '광진구': 26.0,
        '동대문구': 23.0, '성북구': 25.0, '강서구': 27.0,
        # 안정적 (15-20%) 6개
        '강동구': 18.0, '서대문구': 17.0, '노원구': 19.0, '은평구': 16.0,
        '영등포구': 18.5, '송파구': 19.5,
        # 매우안정 (<15%) 6개
        '강남구': 12.0, '서초구': 13.0, '용산구': 14.0, '마포구': 12.5,
        '성동구': 13.5, '동작구': 14.5
    }
    
    # 각 지역별로 조정
    for region in seoul_gu_list:
        if region not in growth_targets:
            continue
        
        df_region = df[df['가맹점주소시군구'] == region].copy()
        
        if len(df_region) == 0:
            continue
        
        # 1. 성장률 조정
        target_growth = growth_targets.get(region, 0.0)
        df_2024 = df_region[df_region['년'] == 2024].copy()
        df_first_half = df_2024[df_2024['월'].isin([1,2,3,4,5,6])]
        df_second_half = df_2024[df_2024['월'].isin([7,8,9,10,11,12])]
        
        if len(df_first_half) > 0 and len(df_second_half) > 0:
            first_half_mean = df_first_half['카드이용금액계'].mean()
            current_second_half_mean = df_second_half['카드이용금액계'].mean()
            
            if current_second_half_mean > 0:
                target_second_half_mean = first_half_mean * (1 + target_growth)
                growth_adjustment = target_second_half_mean / current_second_half_mean
                
                # 하반기 데이터 조정
                second_indices = df_second_half.index
                df.loc[second_indices, '카드이용금액계'] = (df.loc[second_indices, '카드이용금액계'] * growth_adjustment).astype(int)
                df.loc[second_indices, '카드이용건수계'] = (df.loc[second_indices, '카드이용건수계'] * growth_adjustment).astype(int)
        
        # 2. 업종 다양성 조정
        target_diversity = diversity_targets.get(region, None)
        if target_diversity is not None:
            current_industries = df_region['업종대분류'].nunique()
            
            if current_industries < target_diversity:
                # 업종 추가 필요 - 기타 업종을 세분화
                # 실제로는 업종을 추가하는 것이 복잡하므로, 기존 업종 비율을 조정
                pass  # 업종 다양성은 데이터 생성 단계에서 결정되므로 여기서는 조정하지 않음
        
        # 3. 소비 안정성 조정 (CV 조정)
        target_cv = stability_targets.get(region, None)
        if target_cv is not None:
            # 일별 데이터의 변동성 조정
            daily_data = df_region.groupby('기준일자')['카드이용금액계'].sum()
            
            if len(daily_data) > 1:
                current_mean = daily_data.mean()
                current_std = daily_data.std()
                current_cv = (current_std / current_mean * 100) if current_mean > 0 else 0
                
                if current_cv > 0:
                    # 목표 CV에 맞춰 조정
                    target_std = current_mean * (target_cv / 100)
                    cv_adjustment = target_std / current_std if current_std > 0 else 1.0
                    
                    # 각 날짜별로 조정
                    for date, group_df in df_region.groupby('기준일자'):
                        daily_total = group_df['카드이용금액계'].sum()
                        deviation = daily_total - current_mean
                        
                        # 변동성 조정 (평균은 유지하면서 표준편차만 조정)
                        new_total = current_mean + (deviation * cv_adjustment)
                        
                        if new_total > 0 and daily_total > 0:
                            adjustment_factor = new_total / daily_total
                            date_indices = group_df.index
                            df.loc[date_indices, '카드이용금액계'] = (df.loc[date_indices, '카드이용금액계'] * adjustment_factor).astype(int)
                            df.loc[date_indices, '카드이용건수계'] = (df.loc[date_indices, '카드이용건수계'] * adjustment_factor).astype(int)
    
    # 기준일자를 다시 정수형으로 변환
    if df['기준일자'].dtype == 'datetime64[ns]':
        df['기준일자'] = df['기준일자'].dt.strftime('%Y%m%d').astype(int)
    
    # 저장
    df.to_csv(output_file, index=False, encoding='cp949')
    print(f"조정 완료: {output_file} ({len(df):,} 행)")

if __name__ == '__main__':
    balance_metrics()

