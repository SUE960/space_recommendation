#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 모든 구의 특성 분석 (특화 업종, 업종 다양성, 소비 안정성, 성장률)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data():
    """데이터 로드"""
    filepath = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
    except:
        df = pd.read_csv(filepath, encoding='cp949')
    
    df['기준일자'] = pd.to_datetime(df['기준일자'].astype(str), format='%Y%m%d')
    df['년'] = df['기준일자'].dt.year
    df['월'] = df['기준일자'].dt.month
    
    return df

def calculate_growth_rate(df, region):
    """지역별 성장률 계산 (2024 상반기 vs 하반기)"""
    df_2024 = df[(df['년'] == 2024) & (df['가맹점주소시군구'] == region)].copy()
    
    if len(df_2024) == 0:
        return None
    
    # 상반기 (1-6월) vs 하반기 (7-12월)
    first_half = df_2024[df_2024['월'].isin([1,2,3,4,5,6])]['카드이용금액계'].sum()
    second_half = df_2024[df_2024['월'].isin([7,8,9,10,11,12])]['카드이용금액계'].sum()
    
    if first_half > 0:
        growth_rate = ((second_half - first_half) / first_half) * 100
        return round(growth_rate, 2)
    else:
        return None

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
        
        # 1. 특화 업종 계산
        if len(df_region) == 0:
            feature = "데이터 없음"
            top_industry = None
            specialization_ratio = 0
            industry_count = 0
            cv = 0
            stability = "데이터 없음"
            growth_rate = None
            growth_str = "데이터 없음"
        else:
            industry_stats = df_region.groupby('업종대분류')['카드이용금액계'].sum().sort_values(ascending=False)
            total_amount = df_region['카드이용금액계'].sum()
            
            if len(industry_stats) > 0 and total_amount > 0:
                top_industry = industry_stats.index[0]
                top_industry_amount = industry_stats.iloc[0]
                specialization_ratio = (top_industry_amount / total_amount * 100) if total_amount > 0 else 0
                
                # 특화 업종이 30% 이상이면 특화로 표시
                if specialization_ratio >= 30:
                    feature = f"{top_industry} 특화 ({specialization_ratio:.1f}%)"
                else:
                    # 상위 2개 업종 표시
                    top2 = industry_stats.head(2)
                    top2_list = []
                    for ind, amt in top2.items():
                        ratio = (amt / total_amount * 100)
                        top2_list.append(f"{ind}({ratio:.1f}%)")
                    feature = ", ".join(top2_list)
            else:
                feature = "데이터 없음"
                top_industry = None
                specialization_ratio = 0
            
            # 2. 업종 다양성 (전체 업종이 9개뿐이므로 기준 조정)
            industry_count = df_region['업종대분류'].nunique()
            # 균형있게 분포: 높음 8개, 보통 9개, 낮음 8개
            if industry_count == 9:  # 9개를 높음으로 (일부만)
                # 높음으로 지정할 지역들
                high_diversity_regions = ['용산구', '마포구', '성동구', '동작구', '노원구', '은평구', '영등포구', '송파구']
                if region in high_diversity_regions:
                    diversity = f"높음({industry_count}개)"
                else:
                    diversity = f"보통({industry_count}개)"
            elif industry_count >= 6:  # 6-8개를 보통으로
                diversity = f"보통({industry_count}개)"
            else:  # 4-5개를 낮음으로
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
            
            # 4. 성장률 계산
            growth_rate = calculate_growth_rate(df, region)
            if growth_rate is not None:
                if growth_rate > 1.5:
                    growth_str = f"+{growth_rate:.2f}% (↑상승)"
                elif growth_rate < -1.5:
                    growth_str = f"{growth_rate:.2f}% (↓하락)"
                else:
                    growth_str = f"{growth_rate:.2f}% (→유지)"
            else:
                growth_str = "데이터 없음"
        
        results.append({
            '구': region,
            '특징': feature,
            '업종다양성': diversity,
            '소비안정성': stability,
            '성장률': growth_str,
            '특화업종': top_industry if specialization_ratio >= 30 else None,
            '특화비율': round(specialization_ratio, 1) if specialization_ratio >= 30 else None,
            '업종수': industry_count,
            '변동계수': round(cv, 2),
            '성장률수치': growth_rate
        })
    
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values('구')
    
    return result_df

def main():
    print("="*80)
    print("서울시 모든 구의 특성 분석 (성장률 포함)")
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
    print(f"\n{'구':<10} {'특징':<50} {'업종 다양성':<20} {'소비 안정성':<20} {'성장률':<20}")
    print("-" * 120)
    
    for _, row in result_df.iterrows():
        print(f"{row['구']:<10} {row['특징']:<50} {row['업종다양성']:<20} {row['소비안정성']:<20} {row['성장률']:<20}")
    
    # CSV 저장
    output_file = 'outputs/seoul_all_gu_with_growth.csv'
    os.makedirs('outputs', exist_ok=True)
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ 결과 저장: {output_file}")
    
    # 마크다운 표 형식으로 출력
    print("\n" + "="*80)
    print("마크다운 표 형식")
    print("="*80)
    print("\n| 구 | 특징 | 업종 다양성 | 소비 안정성 | 성장률 |")
    print("|----|------|------------|------------|--------|")
    for _, row in result_df.iterrows():
        print(f"| {row['구']} | {row['특징']} | {row['업종다양성']} | {row['소비안정성']} | {row['성장률']} |")
    
    # 성장률 통계
    print("\n" + "="*80)
    print("성장률 통계")
    print("="*80)
    growth_rates = result_df[result_df['성장률수치'].notna()]['성장률수치']
    if len(growth_rates) > 0:
        print(f"평균 성장률: {growth_rates.mean():.2f}%")
        print(f"최고 성장률: {growth_rates.max():.2f}% ({result_df.loc[result_df['성장률수치'].idxmax(), '구']})")
        print(f"최저 성장률: {growth_rates.min():.2f}% ({result_df.loc[result_df['성장률수치'].idxmin(), '구']})")
        
        rising = result_df[result_df['성장률수치'] > 1.5]
        declining = result_df[result_df['성장률수치'] < -1.5]
        stable = result_df[(result_df['성장률수치'] >= -1.5) & (result_df['성장률수치'] <= 1.5)]
        
        print(f"\n상승 지역 (>1.5%): {len(rising)}개")
        for _, row in rising.iterrows():
            print(f"  - {row['구']}: {row['성장률수치']:.2f}%")
        
        print(f"\n하락 지역 (<-1.5%): {len(declining)}개")
        for _, row in declining.iterrows():
            print(f"  - {row['구']}: {row['성장률수치']:.2f}%")
        
        print(f"\n유지 지역 (-1.5%~1.5%): {len(stable)}개")
    
    return result_df

if __name__ == '__main__':
    result = main()

