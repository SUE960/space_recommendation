#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 서울시 구의 변동계수 계산
"""

import pandas as pd
import numpy as np
import os

def load_data():
    """데이터 로드"""
    filepath = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
    except:
        df = pd.read_csv(filepath, encoding='cp949')
    
    # 날짜 변환
    df['기준일자'] = pd.to_datetime(df['기준일자'].astype(str), format='%Y%m%d')
    
    return df

def calculate_cv_by_region(df):
    """지역별 변동계수 계산"""
    # 서울시 구만 필터링 (성남시 등 경기권 제외)
    seoul_gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
                     '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
                     '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
                     '서초구', '강남구', '송파구', '강동구']
    
    df_seoul = df[df['가맹점주소시군구'].isin(seoul_gu_list)].copy()
    
    # 각 구별로 일별 소비 금액 집계
    daily_by_region = df_seoul.groupby(['기준일자', '가맹점주소시군구'])['카드이용금액계'].sum().reset_index()
    
    # 각 구별 변동계수 계산
    cv_results = []
    
    for region in seoul_gu_list:
        region_data = daily_by_region[daily_by_region['가맹점주소시군구'] == region]
        
        if len(region_data) > 0:
            amounts = region_data['카드이용금액계']
            mean_amount = amounts.mean()
            std_amount = amounts.std()
            
            if mean_amount > 0:
                cv = (std_amount / mean_amount) * 100
            else:
                cv = 0
            
            total_amount = amounts.sum()
            total_days = len(region_data)
            avg_daily = mean_amount
            
            cv_results.append({
                '구': region,
                '변동계수(%)': round(cv, 2),
                '총소비금액(원)': int(total_amount),
                '평균일일소비(원)': int(avg_daily),
                '데이터일수': total_days
            })
    
    cv_df = pd.DataFrame(cv_results)
    cv_df = cv_df.sort_values('변동계수(%)')
    
    return cv_df

def main():
    print("="*80)
    print("서울시 모든 구의 변동계수 계산")
    print("="*80)
    
    # 데이터 로드
    print("\n데이터 로딩 중...")
    df = load_data()
    print(f"✓ {len(df):,}행 로드 완료")
    
    # 변동계수 계산
    print("\n변동계수 계산 중...")
    cv_df = calculate_cv_by_region(df)
    
    # 결과 출력
    print("\n" + "="*80)
    print("서울시 모든 구의 변동계수 (안정성 순위)")
    print("="*80)
    print(f"\n{'순위':<5} {'구':<10} {'변동계수(%)':<15} {'평균일일소비(원)':<20} {'총소비금액(원)':<20}")
    print("-" * 80)
    
    for idx, row in cv_df.iterrows():
        rank = idx + 1
        stability = "매우안정" if row['변동계수(%)'] < 15 else "안정" if row['변동계수(%)'] < 20 else "보통" if row['변동계수(%)'] < 30 else "변동성높음"
        print(f"{rank:<5} {row['구']:<10} {row['변동계수(%)']:<15.2f} {row['평균일일소비(원)']:<20,} {row['총소비금액(원)']:<20,} ({stability})")
    
    # 통계 요약
    print("\n" + "="*80)
    print("변동계수 통계 요약")
    print("="*80)
    print(f"평균 변동계수: {cv_df['변동계수(%)'].mean():.2f}%")
    print(f"최소 변동계수: {cv_df['변동계수(%)'].min():.2f}% ({cv_df.loc[cv_df['변동계수(%)'].idxmin(), '구']})")
    print(f"최대 변동계수: {cv_df['변동계수(%)'].max():.2f}% ({cv_df.loc[cv_df['변동계수(%)'].idxmax(), '구']})")
    print(f"표준편차: {cv_df['변동계수(%)'].std():.2f}%")
    
    # 안정성 구분
    print("\n" + "="*80)
    print("안정성 구분")
    print("="*80)
    very_stable = cv_df[cv_df['변동계수(%)'] < 15]
    stable = cv_df[(cv_df['변동계수(%)'] >= 15) & (cv_df['변동계수(%)'] < 20)]
    normal = cv_df[(cv_df['변동계수(%)'] >= 20) & (cv_df['변동계수(%)'] < 30)]
    high_variance = cv_df[cv_df['변동계수(%)'] >= 30]
    
    print(f"\n매우 안정적 (변동계수 < 15%): {len(very_stable)}개 구")
    for _, row in very_stable.iterrows():
        print(f"  - {row['구']}: {row['변동계수(%)']:.2f}%")
    
    print(f"\n안정적 (15% ≤ 변동계수 < 20%): {len(stable)}개 구")
    for _, row in stable.iterrows():
        print(f"  - {row['구']}: {row['변동계수(%)']:.2f}%")
    
    print(f"\n보통 (20% ≤ 변동계수 < 30%): {len(normal)}개 구")
    for _, row in normal.iterrows():
        print(f"  - {row['구']}: {row['변동계수(%)']:.2f}%")
    
    if len(high_variance) > 0:
        print(f"\n변동성 높음 (변동계수 ≥ 30%): {len(high_variance)}개 구")
        for _, row in high_variance.iterrows():
            print(f"  - {row['구']}: {row['변동계수(%)']:.2f}%")
    
    # CSV 저장
    output_file = 'outputs/seoul_all_gu_cv.csv'
    os.makedirs('outputs', exist_ok=True)
    cv_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ 결과 저장: {output_file}")
    
    return cv_df

if __name__ == '__main__':
    result = main()


