#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
비특화 지역의 최고 업종 비율을 직접 18%로 강제 설정
"""

import pandas as pd
import numpy as np

np.random.seed(42)

def force_non_specialized_direct():
    """비특화 지역의 최고 업종 비율을 직접 18%로 강제 설정"""
    input_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    output_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    print("="*80)
    print("비특화 지역 강제 조정 (최고 업종 직접 18%로 설정)")
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
    
    seoul_gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
                     '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
                     '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
                     '서초구', '강남구', '송파구', '강동구']
    
    # 특화 지역 목록 (9개만)
    specialized_regions = ['강남구', '서초구', '중구', '은평구', '구로구', '영등포구', 
                          '중랑구', '송파구', '용산구']
    
    # 데이터 타입 변환 (먼저 float로 변환)
    df['카드이용금액계'] = pd.to_numeric(df['카드이용금액계'], errors='coerce').fillna(0).astype('float64')
    df['카드이용건수계'] = pd.to_numeric(df['카드이용건수계'], errors='coerce').fillna(0).astype('float64')
    
    adjusted_count = 0
    
    # 비특화 지역 처리
    for region in seoul_gu_list:
        if region in specialized_regions:
            continue  # 특화 지역은 건너뛰기
        
        df_region = df[df['가맹점주소시군구'] == region].copy()
        
        if len(df_region) == 0:
            continue
        
        current_totals = df_region.groupby('업종대분류')['카드이용금액계'].sum()
        total_amount = df_region['카드이용금액계'].sum()
        
        if total_amount > 0 and len(current_totals) > 0:
            top_industry = current_totals.idxmax()
            top_amount = current_totals.max()
            top_ratio = (top_amount / total_amount * 100)
            
            # 최고 업종 비율이 19%를 초과하면 강제로 15%로 설정 (더 강력하게)
            if top_ratio > 19.0:
                target_ratio = 0.15  # 15% (여유를 두고)
                new_top_amount = total_amount * target_ratio
                
                # 최고 업종 조정
                top_mask = (df['가맹점주소시군구'] == region) & (df['업종대분류'] == top_industry)
                current_top_total = df.loc[top_mask, '카드이용금액계'].sum()
                
                if current_top_total > 0:
                    # 각 행의 비율 유지하면서 총액만 조정
                    top_rows = df.loc[top_mask].copy()
                    top_rows['비율'] = top_rows['카드이용금액계'] / current_top_total
                    
                    # 새로운 총액을 비율에 따라 분배 (직접 할당)
                    adjustment_factor = new_top_amount / current_top_total
                    df.loc[top_mask, '카드이용금액계'] = df.loc[top_mask, '카드이용금액계'] * adjustment_factor
                    df.loc[top_mask, '카드이용건수계'] = df.loc[top_mask, '카드이용건수계'] * adjustment_factor
                    
                    # 나머지 업종들 조정 (전체 합계 유지)
                    other_mask = (df['가맹점주소시군구'] == region) & (df['업종대분류'] != top_industry)
                    other_amount = df.loc[other_mask, '카드이용금액계'].sum()
                    
                    if other_amount > 0:
                        # 조정 후 실제 총액
                        actual_new_top = df.loc[top_mask, '카드이용금액계'].sum()
                        new_other_amount = total_amount - actual_new_top
                        other_adjustment = new_other_amount / other_amount
                        
                        # 다른 업종들 조정
                        df.loc[other_mask, '카드이용금액계'] = df.loc[other_mask, '카드이용금액계'] * other_adjustment
                        df.loc[other_mask, '카드이용건수계'] = df.loc[other_mask, '카드이용건수계'] * other_adjustment
                    
                    adjusted_count += 1
    
    print(f"조정된 지역 수: {adjusted_count}개")
    
    # 정수형으로 변환
    df['카드이용금액계'] = df['카드이용금액계'].fillna(0).clip(lower=0, upper=1e12).astype('int64')
    df['카드이용건수계'] = df['카드이용건수계'].fillna(0).clip(lower=0, upper=1e10).astype('int64')
    
    # 기준일자를 다시 정수형으로 변환
    if df['기준일자'].dtype == 'datetime64[ns]':
        df['기준일자'] = df['기준일자'].dt.strftime('%Y%m%d').astype(int)
    
    # 저장
    df.to_csv(output_file, index=False, encoding='cp949')
    print(f"조정 완료: {output_file} ({len(df):,} 행)")

if __name__ == '__main__':
    force_non_specialized_direct()

