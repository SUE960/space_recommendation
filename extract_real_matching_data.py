#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시민 소비 데이터 구조 파악 및 Level 2 매칭용 데이터 추출
"""

import pandas as pd
import numpy as np


def check_data_structure():
    """데이터 구조 확인"""
    
    print("="*100)
    print("서울시민 소비 데이터 구조 파악")
    print("="*100)
    
    # 1. 성별 연령대별 데이터 (행정동별)
    print("\n[파일 6] 서울시 내국인 성별 연령대별(행정동별)")
    print("-" * 100)
    
    try:
        df6 = pd.read_csv('data_2/6.서울시 내국인 성별 연령대별(행정동별).csv', encoding='cp949')
        print(f"✓ 로드 성공: {len(df6):,}행")
        print(f"\n컬럼: {list(df6.columns)}")
        print(f"\n샘플 데이터:")
        print(df6.head(10))
        
        # 구별 집계
        if '시군구명' in df6.columns or '행정동명' in df6.columns:
            print(f"\n행정동 수: {df6['행정동명'].nunique() if '행정동명' in df6.columns else 'N/A'}")
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    # 2. 일별 소비 지역별 데이터
    print(f"\n{'='*100}")
    print("[파일 1] 서울시민의 일별 소비지역별(행정동)")
    print("-" * 100)
    
    try:
        df1 = pd.read_csv('data_2/1.서울시민의 일별 소비지역별(행정동).csv', encoding='cp949')
        print(f"✓ 로드 성공: {len(df1):,}행")
        print(f"\n컬럼: {list(df1.columns)}")
        print(f"\n샘플 데이터:")
        print(df1.head(10))
        
        # 업종 분류
        if '업종분류' in df1.columns:
            print(f"\n업종 종류: {df1['업종분류'].nunique()}개")
            print(f"업종 목록: {df1['업종분류'].unique()[:10]}")
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    return df6, df1


def extract_gu_demographics(df6):
    """구별 인구통계 추출"""
    
    print(f"\n{'='*100}")
    print("구별 인구통계 데이터 추출")
    print("="*100)
    
    # 행정동명에서 구 추출 (예: "종로구 청운동" → "종로구")
    df6['구'] = df6['행정동명'].str.split().str[0]
    
    # 구별 연령대별 집계
    gu_age_data = df6.groupby(['구', '연령대'])['카드이용건수'].sum().reset_index()
    
    # 피벗 (구 × 연령대)
    gu_age_pivot = gu_age_data.pivot(index='구', columns='연령대', values='카드이용건수')
    
    # 비율 계산
    gu_age_ratio = gu_age_pivot.div(gu_age_pivot.sum(axis=1), axis=0) * 100
    
    print("\n구별 연령대 비율:")
    print(gu_age_ratio.round(1))
    
    # 성별 비율
    gu_gender_data = df6.groupby(['구', '성별'])['카드이용건수'].sum().reset_index()
    gu_gender_pivot = gu_gender_data.pivot(index='구', columns='성별', values='카드이용건수')
    gu_gender_ratio = gu_gender_pivot.div(gu_gender_pivot.sum(axis=1), axis=0) * 100
    
    print("\n구별 성별 비율:")
    print(gu_gender_ratio.round(1))
    
    return gu_age_ratio, gu_gender_ratio


def extract_gu_consumption_pattern(df1):
    """구별 소비 패턴 추출"""
    
    print(f"\n{'='*100}")
    print("구별 소비 패턴 데이터 추출")
    print("="*100)
    
    # 행정동명에서 구 추출
    df1['구'] = df1['소비자주소시군구'].str.replace('서울특별시', '').str.strip()
    
    # 구별 업종별 소비액 집계
    gu_industry = df1.groupby(['구', '업종분류'])['카드이용금액'].sum().reset_index()
    
    # 피벗
    gu_industry_pivot = gu_industry.pivot(index='구', columns='업종분류', values='카드이용금액')
    
    # 비율 계산
    gu_industry_ratio = gu_industry_pivot.div(gu_industry_pivot.sum(axis=1), axis=0) * 100
    
    print("\n구별 업종별 소비 비율 (상위 5개 업종):")
    print(gu_industry_ratio.iloc[:, :5].round(1))
    
    return gu_industry_ratio


def map_to_consumption_categories(industry_ratio):
    """업종을 9개 소비 카테고리로 매핑"""
    
    # 업종 → 소비 카테고리 매핑
    category_mapping = {
        '식료품': ['음식', '제과', '주점', '커피', '편의점', '슈퍼마켓', '대형마트'],
        '의류신발': ['의류', '신발', '가방', '액세서리', '패션'],
        '생활용품': ['생활잡화', '화장품', '뷰티', '세탁'],
        '의료': ['약국', '의원', '병원', '한의원'],
        '교통': ['주유소', '자동차', '택시', '대중교통'],
        '여가': ['스포츠', '레저', '골프', '헬스'],
        '문화': ['서점', '문구', '영화', '공연', '음반'],
        '교육': ['학원', '학습지', '교육'],
        '오락': ['오락', '게임', '노래방']
    }
    
    # 실제 매핑 로직 구현
    print("\n업종 → 소비카테고리 매핑 필요")
    
    return None


if __name__ == '__main__':
    # 데이터 구조 확인
    df6, df1 = check_data_structure()
    
    print(f"\n{'='*100}")
    print("✅ 데이터 구조 파악 완료!")
    print("="*100)
    
    print("\n💡 다음 단계:")
    print("1. 구별 실제 인구통계 추출 (연령대, 성별 비율)")
    print("2. 구별 실제 소비 패턴 추출 (업종별 소비액)")
    print("3. 업종을 9개 카테고리로 매핑")
    print("4. Level 2 매칭에 실제 데이터 적용")





