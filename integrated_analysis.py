#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 분석 스크립트
카드 소비 데이터와 실시간 상권현황데이터를 통합하여 분석합니다.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
from data_api.api_client import SeoulCommercialAreaAPI
from data_api.data_processor import CommercialAreaDataProcessor
from data_api.config import SEOUL_OPEN_DATA_API_KEY


def load_card_data():
    """카드 소비 데이터 로드"""
    print("카드 소비 데이터 로딩 중...")
    filepath = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
    except:
        df = pd.read_csv(filepath, encoding='cp949')
    
    df['기준일자'] = pd.to_datetime(df['기준일자'].astype(str), format='%Y%m%d')
    df['년'] = df['기준일자'].dt.year
    df['월'] = df['기준일자'].dt.month
    df['요일'] = df['기준일자'].dt.day_name()
    
    print(f"✓ 카드 데이터 로드 완료: {len(df):,}행")
    return df


def load_commercial_area_data(area_nm_list=None):
    """실시간 상권현황데이터 로드"""
    if SEOUL_OPEN_DATA_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  API 키가 설정되지 않아 실시간 상권현황데이터를 건너뜁니다.")
        return pd.DataFrame()
    
    print("\n실시간 상권현황데이터 수집 중...")
    
    if area_nm_list is None:
        # 주요 핫스팟 목록 (기본값)
        area_nm_list = [
            "광화문·덕수궁",
            "강남역",
            "홍대입구",
            "명동",
            "잠실",
            "이태원",
            "압구정",
            "신촌"
        ]
    
    try:
        client = SeoulCommercialAreaAPI(api_key=SEOUL_OPEN_DATA_API_KEY)
        df = client.get_all_data(area_nm_list)
        
        if len(df) > 0:
            print(f"✓ 상권현황데이터 수집 완료: {len(df):,}행")
        else:
            print("⚠️  상권현황데이터가 없습니다.")
        
        return df
    except Exception as e:
        print(f"⚠️  상권현황데이터 수집 실패: {e}")
        return pd.DataFrame()


def analyze_commercial_area_activity(card_df, commercial_df):
    """
    상권 활성도 분석
    - 카드 데이터의 지역별/업종별 소비 패턴
    - 실시간 상권현황데이터의 결제 건수 및 금액
    """
    print("\n" + "="*80)
    print("1. 상권 활성도 분석")
    print("="*80)
    
    results = {}
    
    # 카드 데이터 기반 분석
    if len(card_df) > 0:
        # 지역별 총 소비 금액
        region_consumption = card_df.groupby('가맹점주소시군구')['카드이용금액계'].sum().sort_values(ascending=False)
        
        # 업종별 총 소비 금액
        industry_consumption = card_df.groupby('업종대분류')['카드이용금액계'].sum().sort_values(ascending=False)
        
        # 시간대별 소비 패턴 (시간대 데이터가 있는 경우)
        if '시간대' in card_df.columns:
            time_consumption = card_df.groupby('시간대')['카드이용금액계'].sum().sort_values(ascending=False)
        else:
            time_consumption = pd.Series()
        
        results['카드데이터'] = {
            '지역별소비': region_consumption.head(10),
            '업종별소비': industry_consumption.head(10),
            '시간대별소비': time_consumption
        }
        
        print("\n[카드 데이터 기반 상권 활성도]")
        print("\n상위 10개 지역 (총 소비 금액):")
        for region, amount in region_consumption.head(10).items():
            print(f"  {region}: {amount:,.0f}원")
        
        print("\n상위 10개 업종 (총 소비 금액):")
        for industry, amount in industry_consumption.head(10).items():
            print(f"  {industry}: {amount:,.0f}원")
    
    # 실시간 상권현황데이터 기반 분석
    if len(commercial_df) > 0:
        processor = CommercialAreaDataProcessor(commercial_df)
        
        # 지역별 결제 건수
        if 'AREA_NM' in commercial_df.columns and 'RSB_SH_PAYMENT_CNT' in commercial_df.columns:
            area_payment = commercial_df.groupby('AREA_NM')['RSB_SH_PAYMENT_CNT'].sum().sort_values(ascending=False)
            
            print("\n[실시간 상권현황데이터 기반 상권 활성도]")
            print("\n지역별 실시간 결제 건수:")
            for area, count in area_payment.head(10).items():
                print(f"  {area}: {count:,}건")
        
        # 업종별 결제 건수
        if 'RSB_LRG_CTGR' in commercial_df.columns:
            industry_payment = commercial_df.groupby('RSB_LRG_CTGR')['RSB_SH_PAYMENT_CNT'].sum().sort_values(ascending=False)
            
            print("\n업종별 실시간 결제 건수:")
            for industry, count in industry_payment.head(10).items():
                print(f"  {industry}: {count:,}건")
        
        results['실시간상권데이터'] = {
            '지역별결제건수': area_payment if 'area_payment' in locals() else pd.Series(),
            '업종별결제건수': industry_payment if 'industry_payment' in locals() else pd.Series()
        }
    
    return results


def analyze_payment_by_industry(card_df, commercial_df):
    """
    업종별 결제 건수 분석
    - 카드 데이터의 업종별 이용 건수
    - 실시간 상권현황데이터의 업종별 결제 건수
    """
    print("\n" + "="*80)
    print("2. 업종별 결제 건수 분석")
    print("="*80)
    
    results = {}
    
    # 카드 데이터 기반
    if len(card_df) > 0 and '카드이용건수계' in card_df.columns:
        industry_count = card_df.groupby('업종대분류')['카드이용건수계'].sum().sort_values(ascending=False)
        
        print("\n[카드 데이터] 업종별 총 결제 건수:")
        for industry, count in industry_count.head(15).items():
            print(f"  {industry}: {count:,}건")
        
        results['카드데이터'] = industry_count
    
    # 실시간 상권현황데이터 기반
    if len(commercial_df) > 0 and 'RSB_SH_PAYMENT_CNT' in commercial_df.columns:
        if 'RSB_LRG_CTGR' in commercial_df.columns:
            commercial_industry_count = commercial_df.groupby('RSB_LRG_CTGR')['RSB_SH_PAYMENT_CNT'].sum().sort_values(ascending=False)
            
            print("\n[실시간 상권현황데이터] 업종별 실시간 결제 건수:")
            for industry, count in commercial_industry_count.head(15).items():
                print(f"  {industry}: {count:,}건")
            
            results['실시간상권데이터'] = commercial_industry_count
    
    return results


def analyze_visitor_age_groups(card_df, commercial_df):
    """
    방문 연령층 분석
    - 카드 데이터의 연령대별 소비 패턴
    - 실시간 상권현황데이터의 연령대별 소비 비율
    """
    print("\n" + "="*80)
    print("3. 방문 연령층 분석")
    print("="*80)
    
    results = {}
    
    # 카드 데이터 기반 (연령대 데이터가 있는 경우)
    age_columns = [col for col in card_df.columns if '연령대' in col or '연령' in col]
    
    if len(age_columns) > 0:
        print("\n[카드 데이터] 연령대별 소비 패턴:")
        for col in age_columns[:5]:  # 상위 5개만 표시
            if col in card_df.columns:
                age_consumption = card_df.groupby(col)['카드이용금액계'].sum().sort_values(ascending=False)
                print(f"\n{col} 기준:")
                for age, amount in age_consumption.head(10).items():
                    print(f"  {age}: {amount:,.0f}원")
    
    # 실시간 상권현황데이터 기반
    if len(commercial_df) > 0:
        age_rate_columns = [
            'CMRCL_10_RATE', 'CMRCL_20_RATE', 'CMRCL_30_RATE',
            'CMRCL_40_RATE', 'CMRCL_50_RATE', 'CMRCL_60_RATE'
        ]
        
        available_age_columns = [col for col in age_rate_columns if col in commercial_df.columns]
        
        if len(available_age_columns) > 0:
            print("\n[실시간 상권현황데이터] 연령대별 소비 비율 (평균):")
            age_rates = {}
            for col in available_age_columns:
                age_label = col.replace('CMRCL_', '').replace('_RATE', '')
                avg_rate = commercial_df[col].mean()
                age_rates[age_label] = avg_rate
                print(f"  {age_label}: {avg_rate:.2f}%")
            
            results['실시간상권데이터'] = age_rates
    
    return results


def analyze_amount_range(card_df, commercial_df):
    """
    금액 범위 분석
    - 카드 데이터의 평균 결제 금액
    - 실시간 상권현황데이터의 결제 금액 범위 (최소/최대)
    """
    print("\n" + "="*80)
    print("4. 금액 범위 분석")
    print("="*80)
    
    results = {}
    
    # 카드 데이터 기반
    if len(card_df) > 0:
        avg_amount = card_df['카드이용금액계'].mean()
        median_amount = card_df['카드이용금액계'].median()
        min_amount = card_df['카드이용금액계'].min()
        max_amount = card_df['카드이용금액계'].max()
        
        print("\n[카드 데이터] 결제 금액 통계:")
        print(f"  평균: {avg_amount:,.0f}원")
        print(f"  중앙값: {median_amount:,.0f}원")
        print(f"  최소: {min_amount:,.0f}원")
        print(f"  최대: {max_amount:,.0f}원")
        
        # 업종별 평균 금액
        if '업종대분류' in card_df.columns:
            industry_avg = card_df.groupby('업종대분류')['카드이용금액계'].mean().sort_values(ascending=False)
            print("\n업종별 평균 결제 금액 (상위 10개):")
            for industry, amount in industry_avg.head(10).items():
                print(f"  {industry}: {amount:,.0f}원")
        
        results['카드데이터'] = {
            '평균': avg_amount,
            '중앙값': median_amount,
            '최소': min_amount,
            '최대': max_amount
        }
    
    # 실시간 상권현황데이터 기반
    if len(commercial_df) > 0:
        if 'RSB_SH_PAYMENT_AMT_MIN' in commercial_df.columns and 'RSB_SH_PAYMENT_AMT_MAX' in commercial_df.columns:
            avg_min = commercial_df['RSB_SH_PAYMENT_AMT_MIN'].mean()
            avg_max = commercial_df['RSB_SH_PAYMENT_AMT_MAX'].mean()
            
            print("\n[실시간 상권현황데이터] 결제 금액 범위:")
            print(f"  평균 최소 금액: {avg_min:,.0f}원")
            print(f"  평균 최대 금액: {avg_max:,.0f}원")
            print(f"  평균 금액 범위: {avg_min:,.0f}원 ~ {avg_max:,.0f}원")
            
            results['실시간상권데이터'] = {
                '평균최소금액': avg_min,
                '평균최대금액': avg_max
            }
    
    return results


def analyze_current_time_patterns(card_df, commercial_df):
    """
    현재 시간 기준 상권 특성 파악
    - 시간대별 소비 패턴
    - 요일별 소비 패턴
    """
    print("\n" + "="*80)
    print("5. 현재 시간 기준 상권 특성 분석")
    print("="*80)
    
    results = {}
    
    # 카드 데이터 기반 시간대 분석
    if len(card_df) > 0:
        # 요일별 패턴
        if '요일' in card_df.columns:
            weekday_consumption = card_df.groupby('요일')['카드이용금액계'].sum().sort_values(ascending=False)
            
            print("\n[카드 데이터] 요일별 소비 패턴:")
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekday_kr = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            
            for eng, kr in zip(weekday_order, weekday_kr):
                if eng in weekday_consumption.index:
                    print(f"  {kr}: {weekday_consumption[eng]:,.0f}원")
            
            results['요일별패턴'] = weekday_consumption
        
        # 시간대별 패턴 (시간대 데이터가 있는 경우)
        if '시간대' in card_df.columns:
            time_consumption = card_df.groupby('시간대')['카드이용금액계'].sum().sort_values(ascending=False)
            
            print("\n[카드 데이터] 시간대별 소비 패턴:")
            for time_slot, amount in time_consumption.head(10).items():
                print(f"  {time_slot}: {amount:,.0f}원")
            
            results['시간대별패턴'] = time_consumption
    
    # 실시간 상권현황데이터의 업데이트 시간 분석
    if len(commercial_df) > 0 and 'CMRCL_TIME' in commercial_df.columns:
        print("\n[실시간 상권현황데이터] 최신 업데이트 시간:")
        latest_time = commercial_df['CMRCL_TIME'].max()
        print(f"  {latest_time}")
        
        results['최신업데이트시간'] = latest_time
    
    return results


def save_integrated_results(results_dict, output_dir='outputs'):
    """통합 분석 결과 저장"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 결과를 CSV로 저장
    summary_data = []
    
    # 상권 활성도 결과 저장
    if '상권활성도' in results_dict:
        activity = results_dict['상권활성도']
        if '카드데이터' in activity and '지역별소비' in activity['카드데이터']:
            region_df = activity['카드데이터']['지역별소비'].reset_index()
            region_df.columns = ['지역', '총소비금액']
            region_df.to_csv(f'{output_dir}/지역별_상권활성도.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n✓ 분석 결과 저장 완료: {output_dir}/")


def main():
    """메인 실행 함수"""
    print("="*80)
    print("통합 분석: 카드 소비 데이터 + 실시간 상권현황데이터")
    print("="*80)
    
    # 데이터 로드
    card_df = load_card_data()
    
    # 실시간 상권현황데이터 로드 (API 키가 설정된 경우)
    commercial_df = load_commercial_area_data()
    
    # 통합 분석 실행
    results = {}
    
    # 1. 상권 활성도 파악
    results['상권활성도'] = analyze_commercial_area_activity(card_df, commercial_df)
    
    # 2. 업종별 결제 건수
    results['업종별결제건수'] = analyze_payment_by_industry(card_df, commercial_df)
    
    # 3. 방문 연령층
    results['방문연령층'] = analyze_visitor_age_groups(card_df, commercial_df)
    
    # 4. 금액 범위
    results['금액범위'] = analyze_amount_range(card_df, commercial_df)
    
    # 5. 현재 시간 기준 상권 특성
    results['시간기준특성'] = analyze_current_time_patterns(card_df, commercial_df)
    
    # 결과 저장
    save_integrated_results(results)
    
    print("\n" + "="*80)
    print("통합 분석 완료!")
    print("="*80)
    print("\n분석 항목:")
    print("  1. 상권 활성도 파악")
    print("  2. 업종별 결제 건수")
    print("  3. 방문 연령층")
    print("  4. 금액 범위")
    print("  5. 현재 시간 기준 상권 특성")
    print("\n결과는 outputs/ 폴더에 저장되었습니다.")


if __name__ == '__main__':
    main()

