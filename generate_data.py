#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울 시민 소비 데이터 생성 스크립트
2024년 1월 1일부터 2025년 6월 30일까지의 데이터를 생성합니다.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

# 랜덤 시드 설정 (재현 가능성을 위해)
np.random.seed(42)
random.seed(42)

def get_day_of_week(date_str):
    """날짜 문자열로부터 요일 반환"""
    date_obj = datetime.strptime(str(date_str), '%Y%m%d')
    weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    return weekdays[date_obj.weekday()]

def get_season(month):
    """월로부터 계절 반환"""
    if month in [12, 1, 2]:
        return '겨울'
    elif month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    else:
        return '가을'

def get_weekend_multiplier(date_str):
    """주말 여부에 따른 소비 패턴 배수"""
    date_obj = datetime.strptime(str(date_str), '%Y%m%d')
    weekday = date_obj.weekday()
    # 토요일(5), 일요일(6)은 주말
    if weekday >= 5:
        # 주말: 외식, 쇼핑, 여가 활동 증가
        return 1.3 + np.random.uniform(-0.1, 0.2)
    else:
        # 평일: 통근, 업무 관련 소비
        return 1.0 + np.random.uniform(-0.1, 0.1)

def get_seasonal_multiplier(month, 업종):
    """계절별 업종 소비 패턴 배수"""
    season = get_season(month)
    
    # 계절별 업종별 패턴
    seasonal_patterns = {
        '봄': {
            '패션잡화': 1.2,  # 봄 옷 구매
            '외식': 1.1,     # 봄 나들이
            '여행/관광': 1.3, # 봄 여행
            '편의점': 1.0,
            '할인점/슈퍼마켓/양판점': 1.0,
        },
        '여름': {
            '외식': 1.2,     # 여름 휴가
            '여행/관광': 1.4, # 여름 휴가
            '편의점': 1.1,   # 음료 구매 증가
            '할인점/슈퍼마켓/양판점': 1.0,
            '패션잡화': 0.9,  # 여름 옷은 이미 구매
        },
        '가을': {
            '패션잡화': 1.3,  # 가을 옷 구매
            '외식': 1.1,
            '여행/관광': 1.2, # 단풍 관광
            '편의점': 1.0,
            '할인점/슈퍼마켓/양판점': 1.0,
        },
        '겨울': {
            '패션잡화': 1.2,  # 겨울 옷 구매
            '외식': 1.1,     # 연말 모임
            '여행/관광': 0.9, # 겨울은 감소
            '편의점': 1.0,
            '할인점/슈퍼마켓/양판점': 1.1, # 연말 장보기
        }
    }
    
    return seasonal_patterns.get(season, {}).get(업종, 1.0) + np.random.uniform(-0.1, 0.1)

def get_time_multiplier(time_slot):
    """시간대별 소비 패턴 배수"""
    # 시간대별 패턴 (1: 새벽, 2: 아침, 3: 점심, 4: 오후, 5: 저녁, 6: 밤)
    time_patterns = {
        1: 0.3,  # 새벽: 매우 낮음
        2: 0.8,  # 아침: 통근
        3: 1.2,  # 점심: 외식 증가
        4: 1.0,  # 오후: 평균
        5: 1.3,  # 저녁: 외식, 쇼핑 증가
        6: 1.1,  # 밤: 여가 활동
    }
    return time_patterns.get(time_slot, 1.0) + np.random.uniform(-0.1, 0.1)

def generate_dates(start_date, end_date):
    """날짜 범위 생성"""
    start = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')
    dates = []
    current = start
    while current <= end:
        dates.append(int(current.strftime('%Y%m%d')))
        current += timedelta(days=1)
    return dates

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

def get_trend_multiplier(year, month, industry):
    """시기별 트렌드 배수 (2024 하반기 상승 트렌드 반영)"""
    # 2024 상반기 (1-6월) vs 하반기 (7-12월)
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
            # 하반기부터 점진적 증가
            base_mult = rising_industries[industry]
            if is_2025:
                # 2025년에는 더 증가
                return base_mult * 1.02
            return base_mult
    return 1.0

def process_file_1(input_file, output_file):
    """1.서울시민의 일별 소비지역별(행정동).csv 처리 (개선 버전)"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    # 날짜 범위 생성
    dates = generate_dates('20240101', '20250630')
    
    # 지역별 특성 정의
    region_chars = get_region_characteristics()
    
    # 고유한 조합 추출
    unique_combinations = df[['가맹점주소광역시도', '가맹점주소시군구', '고객행정동코드', '업종대분류']].drop_duplicates()
    
    # 서울시 구 리스트
    seoul_gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
                     '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
                     '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
                     '서초구', '강남구', '송파구', '강동구']
    
    result_rows = []
    
    for date in dates:
        year = int(str(date)[:4])
        month = int(str(date)[4:6])
        weekend_mult = get_weekend_multiplier(date)
        
        # 원본 데이터의 조합 처리
        for _, combo in unique_combinations.iterrows():
            region = combo['가맹점주소시군구']
            
            # 원본 데이터에서 유사한 패턴 찾기
            similar = df[
                (df['가맹점주소광역시도'] == combo['가맹점주소광역시도']) &
                (df['가맹점주소시군구'] == combo['가맹점주소시군구']) &
                (df['고객행정동코드'] == combo['고객행정동코드']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                # 계절별, 주말별, 시기별 트렌드 변동 적용
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                trend_mult = get_trend_multiplier(year, month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult * trend_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '가맹점주소광역시도': combo['가맹점주소광역시도'],
                    '가맹점주소시군구': combo['가맹점주소시군구'],
                    '고객행정동코드': combo['고객행정동코드'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
        
        # 지역별 특성 업종 추가 (원본에 없는 업종도 추가)
        for region in seoul_gu_list:
            if region not in region_chars:
                continue
            
            # 해당 지역의 원본 데이터 확인
            region_data = df[df['가맹점주소시군구'] == region]
            if len(region_data) == 0:
                continue
            
            # 지역의 행정동 코드들
            dong_codes = region_data['고객행정동코드'].unique()
            if len(dong_codes) == 0:
                continue
            
            chars = region_chars[region]
            all_industries = chars['주요'] + chars['보조']
            
            # 원본에 없는 업종 추가
            existing_industries = set(region_data['업종대분류'].unique())
            
            for industry in all_industries:
                if industry not in existing_industries:
                    # 원본 데이터의 평균 금액을 기준으로 생성
                    base_amount = region_data['카드이용금액계'].mean() if len(region_data) > 0 else 1000000
                    base_count = region_data['카드이용건수계'].mean() if len(region_data) > 0 else 100
                    
                    # 주요 업종은 더 높은 비율, 보조 업종은 낮은 비율
                    if industry in chars['주요']:
                        ratio = np.random.uniform(0.3, 0.6)  # 주요 업종: 30-60%
                    else:
                        ratio = np.random.uniform(0.05, 0.15)  # 보조 업종: 5-15%
                    
                    # 행정동별로 생성
                    for dong_code in dong_codes[:3]:  # 최대 3개 행정동
                        seasonal_mult = get_seasonal_multiplier(month, industry)
                        trend_mult = get_trend_multiplier(year, month, industry)
                        final_mult = weekend_mult * seasonal_mult * trend_mult * ratio
                        
                        new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                        new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                        
                        result_rows.append({
                            '기준일자': date,
                            '가맹점주소광역시도': '서울특별시',
                            '가맹점주소시군구': region,
                            '고객행정동코드': dong_code,
                            '업종대분류': industry,
                            '카드이용금액계': max(1, new_amount),
                            '카드이용건수계': max(1, new_count)
                        })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def process_file_2(input_file, output_file):
    """2.서울시민의 일별 시간대별(행정동).csv 처리"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    dates = generate_dates('20240101', '20250630')
    unique_combinations = df[['시간대', '고객행정동코드', '업종대분류']].drop_duplicates()
    
    result_rows = []
    for date in dates:
        month = int(str(date)[4:6])
        weekend_mult = get_weekend_multiplier(date)
        
        for _, combo in unique_combinations.iterrows():
            similar = df[
                (df['시간대'] == combo['시간대']) &
                (df['고객행정동코드'] == combo['고객행정동코드']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                time_mult = get_time_multiplier(combo['시간대'])
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult * time_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '시간대': combo['시간대'],
                    '고객행정동코드': combo['고객행정동코드'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def process_file_3(input_file, output_file):
    """3.서울시 내국인 성별 연령대별(격자별).csv 처리"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    dates = generate_dates('20240101', '20250630')
    unique_combinations = df[['격자_250', '개인법인구분', '성별', '연령대', '업종대분류']].drop_duplicates()
    
    result_rows = []
    for date in dates:
        month = int(str(date)[4:6])
        weekend_mult = get_weekend_multiplier(date)
        
        for _, combo in unique_combinations.iterrows():
            similar = df[
                (df['격자_250'] == combo['격자_250']) &
                (df['개인법인구분'] == combo['개인법인구분']) &
                (df['성별'] == combo['성별']) &
                (df['연령대'] == combo['연령대']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '격자_250': combo['격자_250'],
                    '개인법인구분': combo['개인법인구분'],
                    '성별': combo['성별'],
                    '연령대': combo['연령대'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def process_file_4(input_file, output_file):
    """4.서울시민의 시간대별(격자별).csv 처리"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    dates = generate_dates('20240101', '20250630')
    unique_combinations = df[['시간대', '격자_250', '업종대분류']].drop_duplicates()
    
    result_rows = []
    for date in dates:
        month = int(str(date)[4:6])
        weekend_mult = get_weekend_multiplier(date)
        
        for _, combo in unique_combinations.iterrows():
            similar = df[
                (df['시간대'] == combo['시간대']) &
                (df['격자_250'] == combo['격자_250']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                time_mult = get_time_multiplier(combo['시간대'])
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult * time_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '시간대': combo['시간대'],
                    '격자_250': combo['격자_250'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def process_file_5(input_file, output_file):
    """5.서울시 내국인 일자별 시간대별(격자별).csv 처리"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    dates = generate_dates('20240101', '20250630')
    unique_combinations = df[['요일', '시간대', '격자_50', '업종대분류']].drop_duplicates()
    
    result_rows = []
    for date in dates:
        month = int(str(date)[4:6])
        요일 = get_day_of_week(date)
        weekend_mult = get_weekend_multiplier(date)
        
        for _, combo in unique_combinations.iterrows():
            # 요일이 일치하는 경우만 처리
            if combo['요일'] != 요일:
                continue
                
            similar = df[
                (df['요일'] == combo['요일']) &
                (df['시간대'] == combo['시간대']) &
                (df['격자_50'] == combo['격자_50']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                time_mult = get_time_multiplier(combo['시간대'])
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult * time_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '요일': 요일,
                    '시간대': combo['시간대'],
                    '격자_50': combo['격자_50'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def process_file_6(input_file, output_file):
    """6.서울시 내국인 성별 연령대별(행정동별).csv 처리"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    # Unnamed: 8 컬럼 제거 (있는 경우)
    if 'Unnamed: 8' in df.columns:
        df = df.drop(columns=['Unnamed: 8'])
    
    dates = generate_dates('20240101', '20250630')
    unique_combinations = df[['가맹점행정동코드', '개인법인구분', '성별', '연령대', '업종대분류']].drop_duplicates()
    
    result_rows = []
    for date in dates:
        month = int(str(date)[4:6])
        weekend_mult = get_weekend_multiplier(date)
        
        for _, combo in unique_combinations.iterrows():
            similar = df[
                (df['가맹점행정동코드'] == combo['가맹점행정동코드']) &
                (df['개인법인구분'] == combo['개인법인구분']) &
                (df['성별'] == combo['성별']) &
                (df['연령대'] == combo['연령대']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '가맹점행정동코드': combo['가맹점행정동코드'],
                    '개인법인구분': combo['개인법인구분'],
                    '성별': combo['성별'],
                    '연령대': combo['연령대'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def process_file_7(input_file, output_file):
    """7.서울시민의 성별 연령대별(격자별).csv 처리"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    dates = generate_dates('20240101', '20250630')
    unique_combinations = df[['격자_250', '성별', '연령대', '업종대분류']].drop_duplicates()
    
    result_rows = []
    for date in dates:
        month = int(str(date)[4:6])
        weekend_mult = get_weekend_multiplier(date)
        
        for _, combo in unique_combinations.iterrows():
            similar = df[
                (df['격자_250'] == combo['격자_250']) &
                (df['성별'] == combo['성별']) &
                (df['연령대'] == combo['연령대']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '격자_250': combo['격자_250'],
                    '성별': combo['성별'],
                    '연령대': combo['연령대'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def process_file_8(input_file, output_file):
    """8.서울시 내국인의 개인카드 기준 유입지별(행정동별).csv 처리"""
    print(f"처리 중: {input_file}")
    df = pd.read_csv(input_file, encoding='cp949')
    
    dates = generate_dates('20240101', '20250630')
    unique_combinations = df[['가맹점행정동코드', '고객주소광역시도', '고객주소시군구', '업종대분류']].drop_duplicates()
    
    result_rows = []
    for date in dates:
        month = int(str(date)[4:6])
        weekend_mult = get_weekend_multiplier(date)
        
        for _, combo in unique_combinations.iterrows():
            similar = df[
                (df['가맹점행정동코드'] == combo['가맹점행정동코드']) &
                (df['고객주소광역시도'] == combo['고객주소광역시도']) &
                (df['고객주소시군구'] == combo['고객주소시군구']) &
                (df['업종대분류'] == combo['업종대분류'])
            ]
            
            if len(similar) > 0:
                base_amount = similar['카드이용금액계'].mean()
                base_count = similar['카드이용건수계'].mean()
                
                seasonal_mult = get_seasonal_multiplier(month, combo['업종대분류'])
                final_mult = weekend_mult * seasonal_mult
                
                new_amount = int(base_amount * final_mult * np.random.uniform(0.8, 1.2))
                new_count = int(base_count * final_mult * np.random.uniform(0.8, 1.2))
                
                result_rows.append({
                    '기준일자': date,
                    '가맹점행정동코드': combo['가맹점행정동코드'],
                    '고객주소광역시도': combo['고객주소광역시도'],
                    '고객주소시군구': combo['고객주소시군구'],
                    '업종대분류': combo['업종대분류'],
                    '카드이용금액계': max(1, new_amount),
                    '카드이용건수계': max(1, new_count)
                })
    
    result_df = pd.DataFrame(result_rows)
    result_df.to_csv(output_file, index=False, encoding='cp949')
    print(f"완료: {output_file} ({len(result_df)} 행)")

def main():
    # 출력 디렉토리 생성
    output_dir = 'data_2'
    os.makedirs(output_dir, exist_ok=True)
    
    # 파일 처리 매핑
    file_processors = {
        '1.서울시민의 일별 소비지역별(행정동).csv': process_file_1,
        '2.서울시민의 일별 시간대별(행정동).csv': process_file_2,
        '3.서울시 내국인 성별 연령대별(격자별).csv': process_file_3,
        '4.서울시민의 시간대별(격자별).csv': process_file_4,
        '5.서울시 내국인 일자별 시간대별(격자별).csv': process_file_5,
        '6.서울시 내국인 성별 연령대별(행정동별).csv': process_file_6,
        '7.서울시민의 성별 연령대별(격자별).csv': process_file_7,
        '8.서울시 내국인의 개인카드 기준 유입지별(행정동별).csv': process_file_8,
    }
    
    print("=" * 80)
    print("서울 시민 소비 데이터 생성 시작")
    print("기간: 2024년 1월 1일 ~ 2025년 6월 30일")
    print("=" * 80)
    
    for filename, processor in file_processors.items():
        input_path = f'data_1/{filename}'
        output_path = f'{output_dir}/{filename}'
        
        if os.path.exists(input_path):
            try:
                processor(input_path, output_path)
            except Exception as e:
                print(f"에러 발생 ({filename}): {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"파일을 찾을 수 없습니다: {input_path}")
    
    print("\n" + "=" * 80)
    print("모든 파일 처리 완료!")
    print("=" * 80)

if __name__ == '__main__':
    main()

