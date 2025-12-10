#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
업종 다양성을 높이는 스크립트
- 일부 지역에 더 많은 업종 추가
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def increase_diversity():
    """업종 다양성 증가"""
    input_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    output_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    print("="*80)
    print("업종 다양성 증가")
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
    
    # 목표 업종 수
    diversity_targets = {
        # 높음 (15개 이상) 8개
        '용산구': 16, '마포구': 15, '성동구': 17, '동작구': 15,
        '노원구': 16, '은평구': 15, '영등포구': 16, '송파구': 17,
        # 보통 (10-14개) 9개
        '중구': 12, '종로구': 11, '중랑구': 10, '광진구': 13,
        '동대문구': 11, '성북구': 12, '강서구': 10, '강동구': 11,
        '서대문구': 12
        # 낮음 유지 (4-8개) 8개 - 추가 업종 없음
    }
    
    # 모든 업종 목록
    all_industries = df['업종대분류'].unique().tolist()
    
    # 각 지역별로 업종 추가
    for region in seoul_gu_list:
        target_diversity = diversity_targets.get(region, None)
        if target_diversity is None:
            continue
        
        df_region = df[df['가맹점주소시군구'] == region].copy()
        current_industries = df_region['업종대분류'].nunique()
        
        if current_industries < target_diversity:
            # 부족한 업종 수
            needed = target_diversity - current_industries
            
            # 현재 없는 업종 찾기
            existing_industries = set(df_region['업종대분류'].unique())
            missing_industries = [ind for ind in all_industries if ind not in existing_industries]
            
            # 부족한 만큼 업종 추가
            industries_to_add = missing_industries[:needed]
            
            if len(industries_to_add) > 0:
                # 모든 날짜에 대해 새 업종 추가
                all_dates = df_region['기준일자'].unique()
                
                new_rows = []
                for date in all_dates:
                    date_data = df_region[df_region['기준일자'] == date]
                    if len(date_data) > 0:
                        # 참조 행 (첫 번째 행)
                        ref_row = date_data.iloc[0]
                        total_amount = date_data['카드이용금액계'].sum()
                        
                        # 새 업종에 분배할 금액 (기존의 5-10%)
                        for industry in industries_to_add:
                            new_amount = int(total_amount * np.random.uniform(0.05, 0.10))
                            new_count = int(new_amount / (total_amount / date_data['카드이용건수계'].sum()) if date_data['카드이용건수계'].sum() > 0 else 1)
                            
                            new_row = ref_row.copy()
                            new_row['업종대분류'] = industry
                            new_row['카드이용금액계'] = max(1, new_amount)
                            new_row['카드이용건수계'] = max(1, new_count)
                            new_rows.append(new_row)
                
                if len(new_rows) > 0:
                    new_df = pd.DataFrame(new_rows)
                    df = pd.concat([df, new_df], ignore_index=True)
                    print(f"  {region}: {current_industries}개 → {target_diversity}개 (추가: {len(new_rows)}행)")
    
    # 기준일자를 다시 정수형으로 변환
    if df['기준일자'].dtype == 'datetime64[ns]':
        df['기준일자'] = df['기준일자'].dt.strftime('%Y%m%d').astype(int)
    
    # 저장
    df.to_csv(output_file, index=False, encoding='cp949')
    print(f"조정 완료: {output_file} ({len(df):,} 행)")

if __name__ == '__main__':
    increase_diversity()

