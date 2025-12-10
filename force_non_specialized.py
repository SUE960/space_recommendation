#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
비특화 지역의 최고 업종 비율을 19% 이하로 강제 조정
"""

import pandas as pd
import numpy as np

np.random.seed(42)

def force_non_specialized():
    """비특화 지역의 최고 업종 비율을 19% 이하로 강제 조정"""
    input_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    output_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    print("="*80)
    print("비특화 지역 강제 조정 (최고 업종 19% 이하)")
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
    
    # 특화 지역 목록 (8-10개만) - adjust_specialization_ratios.py와 일치
    specialized_regions = ['강남구', '서초구', '중구', '은평구', '구로구', 
                          '영등포구', '중랑구', '송파구', '용산구']
    
    print(f"특화 지역 목록: {specialized_regions}")
    print(f"비특화 지역 수: {len(seoul_gu_list) - len(specialized_regions)}개")
    
    # 비특화 지역 강제 조정 (최대 200번 반복, 더 강력하게)
    for iteration in range(200):
        adjusted_count = 0
        
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
                
                # 최고 업종 비율이 19%를 초과하면 강제로 18%로 조정
                if top_ratio > 19.0:
                    target_ratio = 18.0
                    new_top_amount = total_amount * target_ratio / 100
                    
                    # 최고 업종 조정
                    top_mask = (df['가맹점주소시군구'] == region) & (df['업종대분류'] == top_industry)
                    
                    # 직접 목표 금액으로 설정 (더 강력하게)
                    current_top_total = df.loc[top_mask, '카드이용금액계'].sum()
                    if current_top_total > 0:
                        # 각 행에 대해 비율 유지하면서 총액 조정
                        top_rows = df.loc[top_mask].copy()
                        top_rows['비율'] = top_rows['카드이용금액계'] / current_top_total
                        
                        # 새로운 총액을 비율에 따라 분배
                        df.loc[top_mask, '카드이용금액계'] = (top_rows['비율'] * new_top_amount).astype(int)
                        df.loc[top_mask, '카드이용건수계'] = (df.loc[top_mask, '카드이용건수계'] * (new_top_amount / current_top_total)).astype(int)
                        
                        # 나머지 업종들 조정 (전체 합계 유지)
                        other_mask = (df['가맹점주소시군구'] == region) & (df['업종대분류'] != top_industry)
                        other_amount = df.loc[other_mask, '카드이용금액계'].sum()
                        
                        if other_amount > 0:
                            # 조정 후 실제 총액
                            actual_new_top = df.loc[top_mask, '카드이용금액계'].sum()
                            new_other_amount = total_amount - actual_new_top
                            other_adjustment = new_other_amount / other_amount
                            
                            # 더 강력하게 조정
                            other_adjustment = max(1.1, min(other_adjustment, 2.5))  # 최소 1.1배, 최대 2.5배
                            
                            df.loc[other_mask, '카드이용금액계'] = (df.loc[other_mask, '카드이용금액계'] * other_adjustment).astype(int)
                            df.loc[other_mask, '카드이용건수계'] = (df.loc[other_mask, '카드이용건수계'] * other_adjustment).astype(int)
                    
                    adjusted_count += 1
        
        # 더 이상 조정할 지역이 없으면 중단
        if adjusted_count == 0:
            break
        
        if iteration % 10 == 0:
            print(f"반복 {iteration+1}: {adjusted_count}개 지역 조정")
    
    # 기준일자를 다시 정수형으로 변환
    if df['기준일자'].dtype == 'datetime64[ns]':
        df['기준일자'] = df['기준일자'].dt.strftime('%Y%m%d').astype(int)
    
    # 저장
    df.to_csv(output_file, index=False, encoding='cp949')
    print(f"조정 완료: {output_file} ({len(df):,} 행)")

if __name__ == '__main__':
    force_non_specialized()
