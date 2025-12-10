#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
지역별 특화 비율을 현실적으로 조정하는 스크립트
"""

import pandas as pd
import numpy as np

np.random.seed(42)

def get_region_specialization_targets():
    """지역별 목표 특화 비율 정의 (20% 이상이 특화, 특화 지역은 정확히 8-10개만)"""
    return {
        # 특화 지역 (20-30% 범위로 현실적으로, 정확히 8-10개만)
        '강남구': {
            '학원/학습지': 0.25,  # 25%
            '백화점': 0.18,
            '카페': 0.15,
            '결제대행(PG)': 0.12,
            '기타': 0.30
        },
        '서초구': {
            '한식': 0.22,  # 22%
            '의료기관': 0.18,
            '카페': 0.15,
            '결제대행(PG)': 0.12,
            '기타': 0.33
        },
        '중구': {
            '결제대행(PG)': 0.25,  # 25%
            '카페': 0.18,
            '편의점': 0.15,
            '호텔/콘도': 0.12,
            '기타': 0.30
        },
        '은평구': {
            '대형마트': 0.28,  # 28%
            '한식': 0.18,
            '카페': 0.15,
            '편의점': 0.12,
            '기타': 0.27
        },
        '구로구': {
            '결제대행(PG)': 0.25,  # 25%
            '한식': 0.18,
            '카페': 0.15,
            '편의점': 0.12,
            '기타': 0.30
        },
        '영등포구': {
            '주유소': 0.25,  # 25%
            '편의점': 0.18,
            '한식': 0.15,
            '카페': 0.12,
            '기타': 0.30
        },
        '중랑구': {
            '대형마트': 0.28,  # 28%
            '한식': 0.18,
            '카페': 0.15,
            '편의점': 0.12,
            '기타': 0.27
        },
        '송파구': {
            '일식': 0.25,  # 25%
            '의료기관': 0.18,
            '카페': 0.15,
            '편의점': 0.12,
            '기타': 0.30
        },
        '용산구': {
            '주유소': 0.25,  # 25%
            '의료기관': 0.20,
            '호텔/콘도': 0.15,
            '결제대행(PG)': 0.12,
            '기타': 0.28
        },
        # 비특화 지역 (모든 업종이 18% 이하로 균등 분포)
        '강동구': {
            '대형마트': 0.12,
            '한식': 0.12,
            '카페': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        },
        '강북구': {
            '한식': 0.12,
            '대형마트': 0.12,
            '카페': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        },
        '관악구': {
            '일식': 0.12,
            '카페': 0.12,
            '한식': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        },
        '마포구': {
            '일식': 0.12,
            '카페': 0.12,
            '한식': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        },
        '서대문구': {
            '백화점': 0.12,
            '의료기관': 0.12,
            '주유소': 0.12,
            '한식': 0.12,
            '기타': 0.52
        },
        '성북구': {
            '주유소': 0.12,
            '미용실': 0.12,
            '한식': 0.12,
            '카페': 0.12,
            '기타': 0.52
        },
        '광진구': {
            '일식': 0.12,
            '카페': 0.12,
            '한식': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        },
        '동작구': {
            '일식': 0.12,
            '카페': 0.12,
            '한식': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        },
        '강서구': {
            '미용실': 0.12,
            '일식': 0.12,
            '카페': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        },
        '성동구': {
            '미용실': 0.12,
            '의료기관': 0.12,
            '대형마트': 0.12,
            '한식': 0.12,
            '기타': 0.52
        },
        '동대문구': {
            '일식': 0.12,
            '생활잡화/수입상품점': 0.12,
            '한식': 0.12,
            '카페': 0.12,
            '기타': 0.52
        },
        '도봉구': {
            '미용실': 0.12,
            '실내/실외골프장': 0.12,
            '한식': 0.12,
            '카페': 0.12,
            '기타': 0.52
        },
        '노원구': {
            '미용실': 0.12,
            '기타식품': 0.12,
            '한식': 0.12,
            '카페': 0.12,
            '기타': 0.52
        },
        '종로구': {
            '미용실': 0.12,
            '한식': 0.12,
            '일식': 0.12,
            '카페': 0.12,
            '기타': 0.52
        },
        '금천구': {
            '주유소': 0.12,
            '대형마트': 0.12,
            '한식': 0.12,
            '편의점': 0.12,
            '기타': 0.52
        }
    }

def adjust_specialization():
    """지역별 특화 비율 조정"""
    input_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    output_file = 'data_2/1.서울시민의 일별 소비지역별(행정동).csv'
    
    print("="*80)
    print("지역별 특화 비율 조정")
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
    
    specialization_targets = get_region_specialization_targets()
    
    # 특화 지역 목록 (9개만)
    specialized_regions = ['강남구', '서초구', '중구', '은평구', '구로구', '영등포구', '중랑구', '송파구', '용산구']
    
    # 각 지역별로 조정 (특화 지역만 - 비특화 지역은 force_non_specialized_direct.py에서 처리)
    for region in specialized_regions:
        if region not in specialization_targets:
            continue
        # 비특화 지역은 건너뛰기 (specialization_targets에 비특화 지역이 포함되어 있을 수 있으므로)
        if region not in specialized_regions:
            continue
            
        df_region = df[df['가맹점주소시군구'] == region].copy()
        
        if len(df_region) == 0:
            continue
        
        # 현재 업종별 총액 계산
        current_totals = df_region.groupby('업종대분류')['카드이용금액계'].sum()
        total_amount = df_region['카드이용금액계'].sum()
        
        if total_amount == 0:
            continue
        
        # 목표 비율
        targets = specialization_targets[region]
        
        # 전체 금액 합계 유지하면서 비율만 조정
        # 1단계: 각 업종별 목표 금액 계산
        target_amounts = {}
        for industry, target_ratio in targets.items():
            if industry == '기타':
                continue
            target_amounts[industry] = total_amount * target_ratio
        
        # 기타 업종 목표 금액
        major_target_total = sum(target_amounts.values())
        others_target = total_amount - major_target_total
        
        # 2단계: 각 업종별 조정 배수 계산 (전체 합계 유지)
        adjustments = {}
        for industry, target_amount in target_amounts.items():
            if industry in current_totals.index:
                current_amount = current_totals[industry]
                if current_amount > 0:
                    adjustments[industry] = target_amount / current_amount
                else:
                    adjustments[industry] = 1.0
            else:
                adjustments[industry] = 1.0
        
        # 기타 업종 조정
        major_industries = [ind for ind in targets.keys() if ind != '기타']
        other_industries = df_region[~df_region['업종대분류'].isin(major_industries)]['업종대분류'].unique()
        other_current_total = df_region[df_region['업종대분류'].isin(other_industries)]['카드이용금액계'].sum()
        
        if other_current_total > 0:
            others_adjustment = others_target / other_current_total
        else:
            others_adjustment = 1.0
        
        # 3단계: 조정 적용 (더 적극적으로 - 50% 반영)
        for industry, adjustment in adjustments.items():
            # 조정 범위 제한
            # 목표와 현재의 차이를 50% 반영
            if adjustment > 1.0:
                adjustment = 1.0 + (adjustment - 1.0) * 0.5  # 50% 반영
            else:
                adjustment = 1.0 - (1.0 - adjustment) * 0.5  # 50% 반영
            
            adjustment = min(adjustment, 1.3)  # 최대 1.3배
            adjustment = max(adjustment, 0.8)  # 최소 0.8배
            
            industry_mask = (df['가맹점주소시군구'] == region) & (df['업종대분류'] == industry)
            df.loc[industry_mask, '카드이용금액계'] = (df.loc[industry_mask, '카드이용금액계'] * adjustment).astype(int)
            df.loc[industry_mask, '카드이용건수계'] = (df.loc[industry_mask, '카드이용건수계'] * adjustment).astype(int)
        
        # 기타 업종 조정
        if others_adjustment > 1.0:
            others_adjustment = 1.0 + (others_adjustment - 1.0) * 0.5
        else:
            others_adjustment = 1.0 - (1.0 - others_adjustment) * 0.5
        
        others_adjustment = min(others_adjustment, 1.15)
        others_adjustment = max(others_adjustment, 0.9)
        
        for other_ind in other_industries:
            other_mask = (df['가맹점주소시군구'] == region) & (df['업종대분류'] == other_ind)
            df.loc[other_mask, '카드이용금액계'] = (df.loc[other_mask, '카드이용금액계'] * others_adjustment).astype(int)
            df.loc[other_mask, '카드이용건수계'] = (df.loc[other_mask, '카드이용건수계'] * others_adjustment).astype(int)
        
        # 비특화 지역은 force_non_specialized.py에서 처리하므로 여기서는 처리하지 않음
    
    # 기준일자를 다시 정수형으로 변환
    if df['기준일자'].dtype == 'datetime64[ns]':
        df['기준일자'] = df['기준일자'].dt.strftime('%Y%m%d').astype(int)
    
    # 저장
    df.to_csv(output_file, index=False, encoding='cp949')
    print(f"조정 완료: {output_file} ({len(df):,} 행)")

if __name__ == '__main__':
    adjust_specialization()

