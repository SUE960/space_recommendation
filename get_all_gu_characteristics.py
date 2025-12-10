#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 모든 구의 특성 분석 (특화 업종, 업종 다양성, 소비 안정성)
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
    
    df['기준일자'] = pd.to_datetime(df['기준일자'].astype(str), format='%Y%m%d')
    
    return df

def calculate_all_characteristics(df):
    """모든 구의 특성 계산"""
    # 서울시 구 리스트
    seoul_gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
                     '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
                     '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
                     '서초구', '강남구', '송파구', '강동구']
    
    df_seoul = df[df['가맹점주소시군구'].isin(seoul_gu_list)].copy()
    
    # 일별 소비 금액 집계 (변동계수 계산용)
    daily_by_region = df_seoul.groupby(['기준일자', '가맹점주소시군구'])['카드이용금액계'].sum().reset_index()
    
    results = []
    
    for region in seoul_gu_list:
        df_region = df_seoul[df_seoul['가맹점주소시군구'] == region]
        
        if len(df_region) == 0:
            continue
        
        # 1. 특화 업종 계산
        industry_stats = df_region.groupby('업종대분류')['카드이용금액계'].sum().sort_values(ascending=False)
        total_amount = df_region['카드이용금액계'].sum()
        
        if len(industry_stats) > 0:
            top_industry = industry_stats.index[0]
            top_industry_amount = industry_stats.iloc[0]
            specialization_ratio = (top_industry_amount / total_amount * 100) if total_amount > 0 else 0
            
            # 특화 업종이 30% 이상이면 특화로 표시
            if specialization_ratio >= 30:
                feature = f"{top_industry} 특화 ({specialization_ratio:.1f}%)"
            else:
                # 상위 3개 업종 표시
                top3 = industry_stats.head(3)
                top3_list = []
                for ind, amt in top3.items():
                    ratio = (amt / total_amount * 100)
                    top3_list.append(f"{ind}({ratio:.1f}%)")
                feature = ", ".join(top3_list[:2])  # 상위 2개만
        else:
            feature = "데이터 없음"
            top_industry = None
            specialization_ratio = 0
        
        # 2. 업종 다양성
        industry_count = df_region['업종대분류'].nunique()
        if industry_count >= 15:
            diversity = f"높음({industry_count}개)"
        elif industry_count >= 10:
            diversity = f"보통({industry_count}개)"
        else:
            diversity = f"낮음({industry_count}개)"
        
        # 3. 소비 안정성 (변동계수)
        region_daily = daily_by_region[daily_by_region['가맹점주소시군구'] == region]
        if len(region_daily) > 0:
            amounts = region_daily['카드이용금액계']
            mean_amount = amounts.mean()
            std_amount = amounts.std()
            
            if mean_amount > 0:
                cv = (std_amount / mean_amount) * 100
            else:
                cv = 0
            
            if cv < 15:
                stability = f"매우안정({cv:.1f}%)"
            elif cv < 20:
                stability = f"안정적({cv:.1f}%)"
            elif cv < 30:
                stability = f"보통({cv:.1f}%)"
            else:
                stability = f"변동성높음({cv:.1f}%)"
        else:
            stability = "데이터 없음"
            cv = 0
        
        results.append({
            '구': region,
            '특징': feature,
            '업종다양성': diversity,
            '소비안정성': stability,
            '특화업종': top_industry if specialization_ratio >= 30 else None,
            '특화비율': round(specialization_ratio, 1) if specialization_ratio >= 30 else None,
            '업종수': industry_count,
            '변동계수': round(cv, 2)
        })
    
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values('구')
    
    return result_df

def main():
    print("="*80)
    print("서울시 모든 구의 특성 분석")
    print("="*80)
    
    # 데이터 로드
    print("\n데이터 로딩 중...")
    df = load_data()
    print(f"✓ {len(df):,}행 로드 완료")
    
    # 특성 계산
    print("\n특성 계산 중...")
    result_df = calculate_all_characteristics(df)
    
    # 결과 출력
    print("\n" + "="*80)
    print("서울시 모든 구의 특성 분석 결과")
    print("="*80)
    print(f"\n{'구':<10} {'특징':<50} {'업종 다양성':<20} {'소비 안정성':<20}")
    print("-" * 100)
    
    for _, row in result_df.iterrows():
        print(f"{row['구']:<10} {row['특징']:<50} {row['업종다양성']:<20} {row['소비안정성']:<20}")
    
    # CSV 저장
    output_file = 'outputs/seoul_all_gu_characteristics.csv'
    os.makedirs('outputs', exist_ok=True)
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ 결과 저장: {output_file}")
    
    # 마크다운 표 형식으로 출력
    print("\n" + "="*80)
    print("마크다운 표 형식")
    print("="*80)
    print("\n| 구 | 특징 | 업종 다양성 | 소비 안정성 |")
    print("|----|------|------------|------------|")
    for _, row in result_df.iterrows():
        print(f"| {row['구']} | {row['특징']} | {row['업종다양성']} | {row['소비안정성']} |")
    
    return result_df

if __name__ == '__main__':
    result = main()


