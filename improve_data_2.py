#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_2 데이터 개선 스크립트
- 지역별 특성 반영
- 시기별 트렌드 반영
- 업종 다양성 보장
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

def get_region_characteristics():
    """지역별 특성 업종 정의"""
    return {
        '강남구': {
            '주요': ['학원/학습지', '백화점', '카페', '한식', '일식'],
            '보조': ['편의점', '주유소', '결제대행(PG)', '의료기관', '미용실']
        },
        '서초구': {
            '주요': ['한식', '일식', '카페', '양식', '백화점'],
            '보조': ['편의점', '주유소', '결제대행(PG)', '미용실', '의료기관']
        },
        '중구': {
            '주요': ['결제대행(PG)', '호텔/콘도', '한식', '일식', '백화점'],
            '보조': ['편의점', '주유소', '카페', '의료기관', '택시']
        },
        '은평구': {
            '주요': ['대형마트', '편의점', '한식', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '강동구': {
            '주요': ['대형마트', '편의점', '한식', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '금천구': {
            '주요': ['대형마트', '편의점', '한식', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '강북구': {
            '주요': ['한식', '편의점', '카페', '대형마트'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '관악구': {
            '주요': ['일식', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '대형마트']
        },
        '구로구': {
            '주요': ['결제대행(PG)', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '마포구': {
            '주요': ['ZZ_나머지', '한식', '카페', '일식'],
            '보조': ['편의점', '주유소', '의료기관', '미용실']
        },
        '영등포구': {
            '주요': ['ZZ_나머지', '한식', '카페', '일식'],
            '보조': ['편의점', '주유소', '의료기관', '미용실']
        },
        '중랑구': {
            '주요': ['미용실', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '일식', '대형마트']
        },
        '성북구': {
            '주요': ['제과점', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '광진구': {
            '주요': ['제과점', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '동작구': {
            '주요': ['슈퍼마켓기업형', '편의점', '한식', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '강서구': {
            '주요': ['기타요식', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '서대문구': {
            '주요': ['백화점', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '송파구': {
            '주요': ['전자상거래(다품목취급)', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '용산구': {
            '주요': ['호텔/콘도', '결제대행(PG)', '한식', '카페'],
            '보조': ['편의점', '주유소', '의료기관', '미용실']
        },
        '종로구': {
            '주요': ['한식', '일식', '카페', '편의점'],
            '보조': ['주유소', '의료기관', '미용실', '대형마트']
        },
        '성동구': {
            '주요': ['주유소', '한식', '편의점', '카페'],
            '보조': ['의료기관', '미용실', '일식', '대형마트']
        },
        '동대문구': {
            '주요': ['생활잡화/수입상품점', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '도봉구': {
            '주요': ['실내/실외골프장', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        },
        '노원구': {
            '주요': ['기타식품', '한식', '편의점', '카페'],
            '보조': ['주유소', '의료기관', '미용실', '일식']
        }
    }

def get_region_growth_trend(region):
    """지역별 성장 트렌드 정의"""
    # 상승 지역 (성장 가능성이 높은 지역)
    rising_regions = {
        '강남구': 1.06,  # +6% 성장
        '서초구': 1.045,  # +4.5% 성장
        '은평구': 1.02,  # +2% 성장
        '구로구': 1.055,  # +5.5% 성장
        '관악구': 1.046,  # +4.6% 성장
        '영등포구': 1.076,  # +7.6% 성장
        '동작구': 1.068,  # +6.8% 성장
        '중랑구': 1.05,  # +5% 성장
        '마포구': 1.038,  # +3.8% 성장
        '성북구': 1.03,  # +3% 성장
        '광진구': 1.051,  # +5.1% 성장
        '동대문구': 1.06,  # +6% 성장
        '강서구': 1.054,  # +5.4% 성장
        '금천구': 1.04,  # +4% 성장
        '노원구': 1.031,  # +3.1% 성장
        '도봉구': 1.044,  # +4.4% 성장
        '용산구': 1.033,  # +3.3% 성장
        '강동구': 1.05,  # +5% 성장
        '성동구': 1.065,  # +6.5% 성장
    }
    
    # 하락 지역 (쇼퇴하는 지역)
    declining_regions = {
        '서대문구': 0.976,  # -2.4% 하락
        '송파구': 0.994,  # -0.6% 하락 (거의 유지)
        '강북구': 0.99,  # -1% 하락
    }
    
    # 유지 지역 (안정적인 지역)
    stable_regions = {
        '중구': 1.004,  # +0.4% (거의 유지)
        '종로구': 1.0036,  # +0.36% (거의 유지)
        '강북구': 1.0037,  # +0.37% (거의 유지)
    }
    
    if region in rising_regions:
        return rising_regions[region]
    elif region in declining_regions:
        return declining_regions[region]
    elif region in stable_regions:
        return stable_regions[region]
    else:
        # 기본값: 약간의 성장
        return 1.01

def get_trend_multiplier(year, month, industry):
    """시기별 트렌드 배수 (2024 하반기 상승 트렌드 반영)"""
    is_second_half_2024 = (year == 2024 and month >= 7)
    is_2025 = (year == 2025)
    
    # 상승 트렌드 업종 (2024 하반기부터 증가)
    rising_industries = {
        '양식': 1.0348,  # +3.48%
        '연구/번역서비스': 1.0321,  # +3.21%
        '미용실': 1.0298,  # +2.98%
        '완구/아동용자전거': 1.0288,  # +2.88%
        '택시': 1.0216,  # +2.16%
        '상품권/복권': 1.0211  # +2.11%
    }
    
    if industry in rising_industries:
        if is_second_half_2024 or is_2025:
            base_mult = rising_industries[industry]
            if is_2025:
                return base_mult * 1.02
            return base_mult
    return 1.0

def get_region_volatility_level(region):
    """지역별 변동성 수준 정의 (일부 지역은 더 불안정)"""
    high_volatility_regions = {
        '송파구': 1.5,  # 변동성 50% 증가 (20-25% 목표)
        '영등포구': 1.45,  # 변동성 45% 증가
        '도봉구': 1.4,  # 변동성 40% 증가
        '중랑구': 1.35,  # 변동성 35% 증가
        '관악구': 1.3,  # 변동성 30% 증가
        '성북구': 1.3,
        '동대문구': 1.25,
        '강서구': 1.25,
        '마포구': 1.25,
        '동작구': 1.2
    }
    return high_volatility_regions.get(region, 1.0)

def improve_data():
    """data_2의 첫 번째 파일 개선"""
    input_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    output_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    print("="*80)
    print("data_2 데이터 개선 시작 (변동성 다양화)")
    print("="*80)
    
    # 기존 데이터 로드
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
    else:
        # 이미 datetime인 경우
        pass
    
    df = df.dropna(subset=['기준일자'])
    df['년'] = df['기준일자'].dt.year
    df['월'] = df['기준일자'].dt.month
    
    # 지역별 특성 정의
    region_chars = get_region_characteristics()
    
    seoul_gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
                     '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
                     '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
                     '서초구', '강남구', '송파구', '강동구']
    
    # 각 지역별로 업종 다양성 보장
    new_rows = []
    
    for region in seoul_gu_list:
        if region not in region_chars:
            continue
        
        df_region = df[df['가맹점주소시군구'] == region]
        if len(df_region) == 0:
            continue
        
        # 기존 업종 확인
        existing_industries = set(df_region['업종대분류'].unique())
        chars = region_chars[region]
        all_industries = chars['주요'] + chars['보조']
        
        # 기존 데이터의 평균 금액/건수 계산
        base_amount = df_region['카드이용금액계'].mean() if len(df_region) > 0 else 1000000
        base_count = df_region['카드이용건수계'].mean() if len(df_region) > 0 else 100
        
        # 행정동 코드들
        dong_codes = df_region['고객행정동코드'].unique()
        if len(dong_codes) == 0:
            continue
        
        # 기존에 없는 업종 추가 (모든 업종 추가)
        for industry in all_industries:
            # 주요 업종은 더 높은 비율, 보조 업종은 낮은 비율
            if industry in chars['주요']:
                ratio = np.random.uniform(0.20, 0.45)  # 주요 업종: 20-45%
            else:
                ratio = np.random.uniform(0.05, 0.15)  # 보조 업종: 5-15%
                
                # 각 날짜별로 생성
                for date in df['기준일자'].unique():
                    year = date.year
                    month = date.month
                    weekday = date.weekday()  # 0=월요일, 6=일요일
                    
                    # 주말/평일 변동성 (적절한 차이)
                    if weekday >= 5:  # 주말
                        weekend_mult = np.random.uniform(1.1, 1.4)  # 주말 10-40% 증가
                    else:  # 평일
                        weekend_mult = np.random.uniform(0.85, 1.1)  # 평일 0-15% 감소
                    
                    # 계절성 변동 (적절한 차이)
                    if month in [12, 1, 2]:  # 겨울
                        seasonal_mult = np.random.uniform(0.95, 1.15)
                    elif month in [6, 7, 8]:  # 여름
                        seasonal_mult = np.random.uniform(1.05, 1.25)
                    elif month in [3, 4, 5]:  # 봄
                        seasonal_mult = np.random.uniform(1.0, 1.15)
                    else:  # 가을
                        seasonal_mult = np.random.uniform(1.0, 1.2)
                    
                    # 시기별 트렌드 반영
                    trend_mult = get_trend_multiplier(year, month, industry)
                    
                    # 지역별 변동성 수준 적용
                    volatility_level = get_region_volatility_level(region)
                    
                    # 변동성 수준에 따라 랜덤 범위 조정
                    if volatility_level > 1.2:
                        # 불안정한 지역: 더 큰 변동성 (20-30% 목표)
                        random_mult = np.random.uniform(0.5, 1.5) * (1 + (volatility_level - 1) * 0.3)
                    elif volatility_level > 1.1:
                        # 중간 변동성 지역
                        random_mult = np.random.uniform(0.65, 1.35) * volatility_level
                    else:
                        # 안정적인 지역: 작은 변동성
                        random_mult = np.random.uniform(0.75, 1.25)
                    
                    # 행정동별로 생성 (최대 3개)
                    for dong_code in dong_codes[:3]:
                        final_mult = ratio * trend_mult * weekend_mult * seasonal_mult * random_mult
                        new_amount = int(base_amount * final_mult)
                        new_count = int(base_count * final_mult)
                        
                        new_rows.append({
                            '기준일자': int(date.strftime('%Y%m%d')),
                            '가맹점주소광역시도': '서울특별시',
                            '가맹점주소시군구': region,
                            '고객행정동코드': dong_code,
                            '업종대분류': industry,
                            '카드이용금액계': max(1, new_amount),
                            '카드이용건수계': max(1, new_count)
                        })
        
        # 기존 업종에 시기별 트렌드 및 변동성 반영
        # 지역별 성장 트렌드 가져오기
        region_growth = get_region_growth_trend(region)
        
        # 모든 행에 대해 처리 (하락 지역은 더 강하게 적용)
        for idx in df_region.index:
            row = df_region.loc[idx]
            year = row['년']
            month = row['월']
            industry = row['업종대분류']
            date = row['기준일자']
            weekday = date.weekday() if hasattr(date, 'weekday') else pd.to_datetime(str(date)).weekday()
            
            # 주말/평일 변동성
            if weekday >= 5:  # 주말
                weekend_mult = np.random.uniform(1.1, 1.4)
            else:  # 평일
                weekend_mult = np.random.uniform(0.85, 1.1)
            
            # 계절성 변동
            if month in [12, 1, 2]:  # 겨울
                seasonal_mult = np.random.uniform(0.95, 1.15)
            elif month in [6, 7, 8]:  # 여름
                seasonal_mult = np.random.uniform(1.05, 1.25)
            elif month in [3, 4, 5]:  # 봄
                seasonal_mult = np.random.uniform(1.0, 1.15)
            else:  # 가을
                seasonal_mult = np.random.uniform(1.0, 1.2)
            
            # 시기별 트렌드
            trend_mult = get_trend_multiplier(year, month, industry)
            
            # 지역별 성장 트렌드 적용 (2024 하반기부터)
            if year == 2024 and month >= 7:
                # 하반기부터 지역별 성장 트렌드 점진적 적용
                # 7월부터 12월까지 점진적으로 적용
                month_progress = (month - 6) / 6.0  # 0.167 ~ 1.0
                # 하락 지역은 더 강하게 적용
                if region_growth < 1.0:
                    # 하락 지역: 더 빠르게 하락
                    growth_mult = 1.0 + (region_growth - 1.0) * month_progress * 1.2
                else:
                    growth_mult = 1.0 + (region_growth - 1.0) * month_progress
            elif year == 2025:
                # 2025년에는 전체 성장 트렌드 적용
                growth_mult = region_growth
            else:
                # 상반기에는 성장 트렌드 없음
                growth_mult = 1.0
            
            # 지역별 변동성 수준 적용
            volatility_level = get_region_volatility_level(region)
            
            # 변동성 수준에 따라 랜덤 범위 조정
            if volatility_level > 1.2:
                # 불안정한 지역: 더 큰 변동성 (20-30% 목표)
                random_mult = np.random.uniform(0.5, 1.5) * (1 + (volatility_level - 1) * 0.3)
            elif volatility_level > 1.1:
                # 중간 변동성 지역
                random_mult = np.random.uniform(0.65, 1.35) * volatility_level
            else:
                # 안정적인 지역: 작은 변동성
                random_mult = np.random.uniform(0.75, 1.25)
            
            # 최종 배수 적용 (지역별 성장 트렌드 포함)
            base_mult = trend_mult * weekend_mult * seasonal_mult * random_mult
            
            # 하락 지역은 더 강하게 적용
            if region_growth < 1.0:
                # 하락 지역: 추가 하락 배수 적용 (더 강하게)
                decline_additional = 0.92 + np.random.uniform(-0.02, 0.02)  # 추가 8% 하락
                base_mult = base_mult * decline_additional
            
            # 성장 트렌드 적용
            final_mult = base_mult * growth_mult
            
            new_amount = int(row['카드이용금액계'] * final_mult)
            new_count = int(row['카드이용건수계'] * final_mult)
            
            # 데이터 타입 변환 후 할당
            df.loc[idx, '카드이용금액계'] = max(1, int(new_amount))
            df.loc[idx, '카드이용건수계'] = max(1, int(new_count))
    
    # 새 행 추가
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True)
        print(f"추가된 행: {len(new_rows):,}행")
    
    # 기준일자를 다시 정수형으로 변환
    if df['기준일자'].dtype == 'datetime64[ns]':
        df['기준일자'] = df['기준일자'].dt.strftime('%Y%m%d').astype(int)
    elif df['기준일자'].dtype == 'object':
        # 이미 문자열이면 그대로
        pass
    
    # 저장
    df.to_csv(output_file, index=False, encoding='cp949')
    print(f"개선 완료: {output_file} ({len(df):,} 행)")
    
    # 결과 확인
    print("\n" + "="*80)
    print("개선 결과 확인")
    print("="*80)
    
    for region in seoul_gu_list[:5]:  # 상위 5개만 확인
        df_region = df[df['가맹점주소시군구'] == region]
        if len(df_region) > 0:
            industry_count = df_region['업종대분류'].nunique()
            industries = df_region.groupby('업종대분류')['카드이용금액계'].sum().sort_values(ascending=False)
            top_industry = industries.index[0] if len(industries) > 0 else None
            top_ratio = (industries.iloc[0] / industries.sum() * 100) if len(industries) > 0 else 0
            
            print(f"{region}: 업종 {industry_count}개, 최고 특화: {top_industry} ({top_ratio:.1f}%)")

if __name__ == '__main__':
    improve_data()

