#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실시간 지역 프로필 생성 분석 스크립트
실시간 상권 데이터를 활용하여 지역 점수 및 프로필을 산출합니다.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

# API 클라이언트 import (상대 경로 처리)
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_api'))

from data_api.api_client import SeoulCommercialAreaAPI
from data_api.data_processor import CommercialAreaDataProcessor
from data_api.config import SEOUL_OPEN_DATA_API_KEY


def calculate_commercial_activity_score(df, area_nm):
    """
    상권 활성도 점수 계산
    상권활성도 = 정규화(결제건수) × 0.4 + 정규화(결제금액) × 0.3 + 정규화(업종다양성) × 0.3
    """
    area_data = df[df['AREA_NM'] == area_nm].copy()
    
    if len(area_data) == 0:
        return None
    
    # 결제건수 (지역 전체)
    payment_cnt = area_data['AREA_SH_PAYMENT_CNT'].iloc[0] if 'AREA_SH_PAYMENT_CNT' in area_data.columns else 0
    
    # 결제금액 (평균)
    if 'AREA_SH_PAYMENT_AMT_MIN' in area_data.columns and 'AREA_SH_PAYMENT_AMT_MAX' in area_data.columns:
        amt_min = area_data['AREA_SH_PAYMENT_AMT_MIN'].iloc[0] if pd.notna(area_data['AREA_SH_PAYMENT_AMT_MIN'].iloc[0]) else 0
        amt_max = area_data['AREA_SH_PAYMENT_AMT_MAX'].iloc[0] if pd.notna(area_data['AREA_SH_PAYMENT_AMT_MAX'].iloc[0]) else 0
        payment_amt = (amt_min + amt_max) / 2
    else:
        payment_amt = 0
    
    # 업종 다양성
    industry_diversity = area_data['RSB_LRG_CTGR'].nunique() if 'RSB_LRG_CTGR' in area_data.columns else 0
    
    # 정규화 (전체 데이터 기준)
    all_areas = df.groupby('AREA_NM').agg({
        'AREA_SH_PAYMENT_CNT': 'first',
        'AREA_SH_PAYMENT_AMT_MIN': 'first',
        'AREA_SH_PAYMENT_AMT_MAX': 'first',
        'RSB_LRG_CTGR': 'nunique'
    }).reset_index()
    
    max_cnt = all_areas['AREA_SH_PAYMENT_CNT'].max() if len(all_areas) > 0 else 1
    max_amt = ((all_areas['AREA_SH_PAYMENT_AMT_MIN'] + all_areas['AREA_SH_PAYMENT_AMT_MAX']) / 2).max() if len(all_areas) > 0 else 1
    max_diversity = all_areas['RSB_LRG_CTGR'].max() if len(all_areas) > 0 else 1
    
    # 정규화 점수 (0-100)
    cnt_score = (payment_cnt / max_cnt * 100) if max_cnt > 0 else 0
    amt_score = (payment_amt / max_amt * 100) if max_amt > 0 else 0
    div_score = (industry_diversity / max_diversity * 100) if max_diversity > 0 else 0
    
    # 최종 점수
    activity_score = (cnt_score * 0.4) + (amt_score * 0.3) + (div_score * 0.3)
    
    return {
        'payment_cnt': payment_cnt,
        'payment_amt': payment_amt,
        'industry_diversity': industry_diversity,
        'cnt_score': cnt_score,
        'amt_score': amt_score,
        'div_score': div_score,
        'activity_score': activity_score
    }


def calculate_specialization_score(df, area_nm):
    """
    업종별 특화 점수 계산
    특화점수 = (해당업종결제건수 / 전체결제건수) × 100
    """
    area_data = df[df['AREA_NM'] == area_nm].copy()
    
    if len(area_data) == 0 or 'RSB_SH_PAYMENT_CNT' not in area_data.columns:
        return None
    
    # 업종별 결제 건수
    industry_payments = area_data.groupby('RSB_LRG_CTGR')['RSB_SH_PAYMENT_CNT'].sum()
    total_payments = industry_payments.sum()
    
    if total_payments == 0:
        return None
    
    # 특화 점수 계산
    specialization_scores = {}
    for industry, count in industry_payments.items():
        score = (count / total_payments) * 100
        specialization_scores[industry] = {
            'payment_cnt': count,
            'specialization_score': score,
            'grade': '강한트렌드' if score >= 50 else ('중간트렌드' if score >= 30 else '일반지역')
        }
    
    # 최고 특화 업종
    top_industry = max(specialization_scores.items(), key=lambda x: x[1]['specialization_score'])
    
    return {
        'all_scores': specialization_scores,
        'top_industry': top_industry[0],
        'top_score': top_industry[1]['specialization_score'],
        'top_grade': top_industry[1]['grade']
    }


def calculate_demographic_score(df, area_nm):
    """
    인구통계 점수 계산
    인구통계점수 = Σ(연령대별비율 × 가중치)
    """
    area_data = df[df['AREA_NM'] == area_nm].copy()
    
    if len(area_data) == 0:
        return None
    
    # 연령대별 비율
    age_columns = {
        'CMRCL_10_RATE': ('10대이하', 1.0),
        'CMRCL_20_RATE': ('20대', 1.5),
        'CMRCL_30_RATE': ('30대', 1.5),
        'CMRCL_40_RATE': ('40대', 1.2),
        'CMRCL_50_RATE': ('50대', 1.2),
        'CMRCL_60_RATE': ('60대이상', 1.0)
    }
    
    demographic_score = 0
    age_details = {}
    
    for col, (label, weight) in age_columns.items():
        if col in area_data.columns:
            rate = area_data[col].iloc[0] if pd.notna(area_data[col].iloc[0]) else 0
            weighted_score = rate * weight
            demographic_score += weighted_score
            age_details[label] = {
                'rate': rate,
                'weight': weight,
                'weighted_score': weighted_score
            }
    
    # 성별 비율
    gender_info = {}
    if 'CMRCL_MALE_RATE' in area_data.columns:
        gender_info['male'] = area_data['CMRCL_MALE_RATE'].iloc[0] if pd.notna(area_data['CMRCL_MALE_RATE'].iloc[0]) else 0
    if 'CMRCL_FEMALE_RATE' in area_data.columns:
        gender_info['female'] = area_data['CMRCL_FEMALE_RATE'].iloc[0] if pd.notna(area_data['CMRCL_FEMALE_RATE'].iloc[0]) else 0
    
    return {
        'demographic_score': demographic_score,
        'age_details': age_details,
        'gender_info': gender_info
    }


def calculate_comprehensive_score(activity_score, specialization_score, demographic_score):
    """
    종합 지역 점수 계산
    종합점수 = (상권활성도 × 0.4) + (특화점수 × 0.3) + (인구통계점수 × 0.3)
    """
    if not all([activity_score, specialization_score, demographic_score]):
        return None
    
    # 정규화 (인구통계 점수는 이미 가중치 적용됨, 0-200 범위로 가정)
    norm_demo = (demographic_score['demographic_score'] / 200 * 100) if demographic_score['demographic_score'] > 0 else 0
    
    # 특화 점수 정규화 (0-100)
    norm_spec = specialization_score['top_score']
    
    # 상권 활성도 점수 (이미 0-100 범위)
    norm_activity = activity_score['activity_score']
    
    # 종합 점수
    comprehensive_score = (norm_activity * 0.4) + (norm_spec * 0.3) + (norm_demo * 0.3)
    
    # 등급 판정
    if comprehensive_score >= 80:
        grade = "매우 활성화 (Hot Zone)"
    elif comprehensive_score >= 60:
        grade = "활성화 (Active Zone)"
    elif comprehensive_score >= 40:
        grade = "보통 (Normal Zone)"
    else:
        grade = "비활성 (Low Activity Zone)"
    
    return {
        'comprehensive_score': comprehensive_score,
        'grade': grade,
        'components': {
            'activity': norm_activity,
            'specialization': norm_spec,
            'demographic': norm_demo
        }
    }


def generate_area_profile(df, area_nm):
    """지역 프로필 생성"""
    area_data = df[df['AREA_NM'] == area_nm].copy()
    
    if len(area_data) == 0:
        return None
    
    # 기본 정보
    area_cd = area_data['AREA_CD'].iloc[0] if 'AREA_CD' in area_data.columns else None
    area_level = area_data['AREA_CMRCL_LVL'].iloc[0] if 'AREA_CMRCL_LVL' in area_data.columns else None
    update_time = area_data['CMRCL_TIME'].iloc[0] if 'CMRCL_TIME' in area_data.columns else None
    
    # 점수 계산
    activity_score = calculate_commercial_activity_score(df, area_nm)
    specialization_score = calculate_specialization_score(df, area_nm)
    demographic_score = calculate_demographic_score(df, area_nm)
    comprehensive_score = calculate_comprehensive_score(activity_score, specialization_score, demographic_score)
    
    # 업종 정보
    industry_info = []
    if 'RSB_LRG_CTGR' in area_data.columns:
        industry_stats = area_data.groupby(['RSB_LRG_CTGR', 'RSB_MID_CTGR']).agg({
            'RSB_SH_PAYMENT_CNT': 'sum',
            'RSB_SH_PAYMENT_AMT_MIN': 'first',
            'RSB_SH_PAYMENT_AMT_MAX': 'first',
            'RSB_PAYMENT_LVL': 'first',
            'RSB_MCT_CNT': 'first'
        }).reset_index()
        
        industry_stats = industry_stats.sort_values('RSB_SH_PAYMENT_CNT', ascending=False)
        
        for _, row in industry_stats.head(5).iterrows():
            industry_info.append({
                'large_category': row['RSB_LRG_CTGR'],
                'mid_category': row['RSB_MID_CTGR'],
                'payment_cnt': int(row['RSB_SH_PAYMENT_CNT']),
                'amt_min': int(row['RSB_SH_PAYMENT_AMT_MIN']) if pd.notna(row['RSB_SH_PAYMENT_AMT_MIN']) else 0,
                'amt_max': int(row['RSB_SH_PAYMENT_AMT_MAX']) if pd.notna(row['RSB_SH_PAYMENT_AMT_MAX']) else 0,
                'payment_level': row['RSB_PAYMENT_LVL'] if pd.notna(row['RSB_PAYMENT_LVL']) else None,
                'merchant_cnt': int(row['RSB_MCT_CNT']) if pd.notna(row['RSB_MCT_CNT']) else 0
            })
    
    profile = {
        'basic_info': {
            'area_nm': area_nm,
            'area_cd': area_cd,
            'area_level': area_level,
            'update_time': update_time
        },
        'scores': {
            'activity': activity_score,
            'specialization': specialization_score,
            'demographic': demographic_score,
            'comprehensive': comprehensive_score
        },
        'industry_info': industry_info
    }
    
    return profile


def analyze_all_areas(df):
    """모든 지역 분석"""
    if len(df) == 0:
        return []
    
    unique_areas = df['AREA_NM'].unique() if 'AREA_NM' in df.columns else []
    
    profiles = []
    for area_nm in unique_areas:
        profile = generate_area_profile(df, area_nm)
        if profile:
            profiles.append(profile)
    
    return profiles


def convert_to_serializable(obj):
    """JSON 직렬화 가능한 형태로 변환"""
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj


def save_analysis_results(profiles, output_dir='outputs'):
    """분석 결과 저장"""
    os.makedirs(output_dir, exist_ok=True)
    
    # JSON 저장 (직렬화 가능한 형태로 변환)
    json_file = os.path.join(output_dir, 'realtime_area_profiles.json')
    serializable_profiles = convert_to_serializable(profiles)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_profiles, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 저장: {json_file}")
    
    # CSV 저장 (요약)
    summary_data = []
    for profile in profiles:
        basic = profile['basic_info']
        comp = profile['scores']['comprehensive']
        spec = profile['scores']['specialization']
        
        summary_data.append({
            '핫스팟명': basic['area_nm'],
            '핫스팟코드': basic['area_cd'],
            '상권레벨': basic['area_level'],
            '종합점수': round(comp['comprehensive_score'], 2) if comp else None,
            '등급': comp['grade'] if comp else None,
            '상권활성도점수': round(profile['scores']['activity']['activity_score'], 2) if profile['scores']['activity'] else None,
            '최고특화업종': spec['top_industry'] if spec else None,
            '특화점수': round(spec['top_score'], 2) if spec else None,
            '인구통계점수': round(profile['scores']['demographic']['demographic_score'], 2) if profile['scores']['demographic'] else None,
            '업데이트시간': basic['update_time']
        })
    
    summary_df = pd.DataFrame(summary_data)
    csv_file = os.path.join(output_dir, 'realtime_area_profiles_summary.csv')
    summary_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"✓ CSV 저장: {csv_file}")
    
    return summary_df


def print_analysis_results(profiles):
    """분석 결과 출력"""
    print("\n" + "="*80)
    print("실시간 지역 프로필 분석 결과")
    print("="*80)
    
    for profile in profiles:
        basic = profile['basic_info']
        comp = profile['scores']['comprehensive']
        activity = profile['scores']['activity']
        spec = profile['scores']['specialization']
        demo = profile['scores']['demographic']
        
        print(f"\n{'='*80}")
        print(f"핫스팟: {basic['area_nm']} ({basic['area_cd']})")
        print(f"{'='*80}")
        
        # 종합 점수
        if comp:
            print(f"\n[종합 지역 점수]")
            print(f"  종합 점수: {comp['comprehensive_score']:.2f}점")
            print(f"  등급: {comp['grade']}")
            print(f"  구성 요소:")
            print(f"    - 상권 활성도: {comp['components']['activity']:.2f}점")
            print(f"    - 특화 점수: {comp['components']['specialization']:.2f}점")
            print(f"    - 인구통계 점수: {comp['components']['demographic']:.2f}점")
        
        # 상권 활성도
        if activity:
            print(f"\n[상권 활성도 점수]")
            print(f"  최종 점수: {activity['activity_score']:.2f}점")
            print(f"  구성 요소:")
            print(f"    - 결제 건수: {activity['payment_cnt']}건 (점수: {activity['cnt_score']:.2f})")
            print(f"    - 결제 금액: {activity['payment_amt']:,.0f}원 (점수: {activity['amt_score']:.2f})")
            print(f"    - 업종 다양성: {activity['industry_diversity']}개 (점수: {activity['div_score']:.2f})")
        
        # 특화 점수
        if spec:
            print(f"\n[업종별 특화 점수]")
            print(f"  최고 특화 업종: {spec['top_industry']}")
            print(f"  특화 점수: {spec['top_score']:.2f}점 ({spec['top_grade']})")
            print(f"  업종별 상세:")
            for industry, info in list(spec['all_scores'].items())[:5]:
                print(f"    - {industry}: {info['specialization_score']:.2f}% ({info['grade']})")
        
        # 인구통계
        if demo:
            print(f"\n[인구통계 점수]")
            print(f"  최종 점수: {demo['demographic_score']:.2f}점")
            print(f"  성별 비율:")
            if 'male' in demo['gender_info']:
                print(f"    - 남성: {demo['gender_info']['male']:.1f}%")
            if 'female' in demo['gender_info']:
                print(f"    - 여성: {demo['gender_info']['female']:.1f}%")
            print(f"  연령대별 비율 (가중 점수):")
            for age, info in demo['age_details'].items():
                print(f"    - {age}: {info['rate']:.1f}% (가중치 {info['weight']}, 점수 {info['weighted_score']:.2f})")
        
        # 업종 정보
        if profile['industry_info']:
            print(f"\n[주요 업종 정보 (Top 5)]")
            for idx, industry in enumerate(profile['industry_info'], 1):
                print(f"  {idx}. {industry['large_category']} - {industry['mid_category']}")
                print(f"     결제 건수: {industry['payment_cnt']}건")
                print(f"     결제 금액: {industry['amt_min']:,} ~ {industry['amt_max']:,}원")
                print(f"     상권 현황: {industry['payment_level']}")
                print(f"     가맹점 수: {industry['merchant_cnt']}개")


def main():
    """메인 실행 함수"""
    print("="*80)
    print("실시간 지역 프로필 생성 분석")
    print("="*80)
    
    # 실시간 상권현황데이터 로드
    print("\n[1단계] 실시간 상권현황데이터 수집")
    print("-" * 80)
    
    if SEOUL_OPEN_DATA_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  API 키가 설정되지 않았습니다.")
        print("실제 데이터 대신 샘플 데이터를 사용합니다.")
        
        # 여러 핫스팟 샘플 데이터 생성 (실제 API 응답 구조 기반)
        sample_data_list = []
        
        # 1. 광화문·덕수궁
        sample_data_list.append({
            'AREA_NM': ['광화문·덕수궁'] * 8,
            'AREA_CD': ['POI009'] * 8,
            'AREA_CMRCL_LVL': ['보통'] * 8,
            'AREA_SH_PAYMENT_CNT': [92] * 8,
            'AREA_SH_PAYMENT_AMT_MIN': [3400000] * 8,
            'AREA_SH_PAYMENT_AMT_MAX': [3500000] * 8,
            'RSB_LRG_CTGR': ['음식·음료', '음식·음료', '음식·음료', '음식·음료', '유통', '유통', '패션·뷰티', '여가·오락'],
            'RSB_MID_CTGR': ['한식', '일식/중식/양식', '제과/커피/패스트푸드', '기타요식', '할인점/슈퍼마켓', '편의점', '의복/의류', '스포츠/문화/레저'],
            'RSB_PAYMENT_LVL': ['보통', '한산한', '한산한', '한산한', '분주한', '보통', '보통', '바쁜'],
            'RSB_SH_PAYMENT_CNT': [12, 4, 8, 7, 8, 13, 4, 36],
            'RSB_SH_PAYMENT_AMT_MIN': [800000, 450000, 100000, 150000, 100000, 100000, 300000, 1100000],
            'RSB_SH_PAYMENT_AMT_MAX': [850000, 500000, 150000, 200000, 150000, 150000, 350000, 1200000],
            'RSB_MCT_CNT': [374, 179, 107, 310, 12, 39, 27, 75],
            'RSB_MCT_TIME': ['202511'] * 8,
            'CMRCL_MALE_RATE': [38.3] * 8,
            'CMRCL_FEMALE_RATE': [61.7] * 8,
            'CMRCL_10_RATE': [0.3] * 8,
            'CMRCL_20_RATE': [15.9] * 8,
            'CMRCL_30_RATE': [32.0] * 8,
            'CMRCL_40_RATE': [31.9] * 8,
            'CMRCL_50_RATE': [8.5] * 8,
            'CMRCL_60_RATE': [11.4] * 8,
            'CMRCL_PERSONAL_RATE': [95.0] * 8,
            'CMRCL_CORPORATION_RATE': [5.0] * 8,
            'CMRCL_TIME': ['20251206 2100'] * 8
        })
        
        # 2. 강남역
        sample_data_list.append({
            'AREA_NM': ['강남역'] * 10,
            'AREA_CD': ['POI001'] * 10,
            'AREA_CMRCL_LVL': ['분주한'] * 10,
            'AREA_SH_PAYMENT_CNT': [156] * 10,
            'AREA_SH_PAYMENT_AMT_MIN': [4200000] * 10,
            'AREA_SH_PAYMENT_AMT_MAX': [4500000] * 10,
            'RSB_LRG_CTGR': ['음식·음료', '음식·음료', '음식·음료', '유통', '유통', '패션·뷰티', '패션·뷰티', '여가·오락', '서비스', '서비스'],
            'RSB_MID_CTGR': ['한식', '일식/중식/양식', '제과/커피/패스트푸드', '편의점', '할인점/슈퍼마켓', '의복/의류', '화장품', '스포츠/문화/레저', '미용실', '학원/학습지'],
            'RSB_PAYMENT_LVL': ['바쁜', '보통', '분주한', '바쁜', '보통', '분주한', '보통', '바쁜', '보통', '분주한'],
            'RSB_SH_PAYMENT_CNT': [28, 15, 22, 18, 12, 16, 14, 20, 8, 3],
            'RSB_SH_PAYMENT_AMT_MIN': [1200000, 800000, 200000, 150000, 200000, 500000, 400000, 1500000, 300000, 200000],
            'RSB_SH_PAYMENT_AMT_MAX': [1300000, 900000, 250000, 200000, 250000, 600000, 500000, 1600000, 400000, 300000],
            'RSB_MCT_CNT': [450, 220, 180, 85, 25, 120, 95, 110, 65, 45],
            'RSB_MCT_TIME': ['202511'] * 10,
            'CMRCL_MALE_RATE': [45.2] * 10,
            'CMRCL_FEMALE_RATE': [54.8] * 10,
            'CMRCL_10_RATE': [1.2] * 10,
            'CMRCL_20_RATE': [28.5] * 10,
            'CMRCL_30_RATE': [35.2] * 10,
            'CMRCL_40_RATE': [22.8] * 10,
            'CMRCL_50_RATE': [7.3] * 10,
            'CMRCL_60_RATE': [5.0] * 10,
            'CMRCL_PERSONAL_RATE': [88.5] * 10,
            'CMRCL_CORPORATION_RATE': [11.5] * 10,
            'CMRCL_TIME': ['20251206 2100'] * 10
        })
        
        # 3. 홍대입구
        sample_data_list.append({
            'AREA_NM': ['홍대입구'] * 9,
            'AREA_CD': ['POI003'] * 9,
            'AREA_CMRCL_LVL': ['바쁜'] * 9,
            'AREA_SH_PAYMENT_CNT': [128] * 9,
            'AREA_SH_PAYMENT_AMT_MIN': [2800000] * 9,
            'AREA_SH_PAYMENT_AMT_MAX': [3200000] * 9,
            'RSB_LRG_CTGR': ['음식·음료', '음식·음료', '음식·음료', '유통', '패션·뷰티', '패션·뷰티', '여가·오락', '여가·오락', '서비스'],
            'RSB_MID_CTGR': ['한식', '일식/중식/양식', '제과/커피/패스트푸드', '편의점', '의복/의류', '화장품', '스포츠/문화/레저', '노래방', '미용실'],
            'RSB_PAYMENT_LVL': ['바쁜', '보통', '바쁜', '바쁜', '분주한', '보통', '바쁜', '바쁜', '보통'],
            'RSB_SH_PAYMENT_CNT': [25, 18, 30, 15, 12, 8, 10, 8, 2],
            'RSB_SH_PAYMENT_AMT_MIN': [600000, 500000, 150000, 100000, 400000, 350000, 800000, 200000, 250000],
            'RSB_SH_PAYMENT_AMT_MAX': [700000, 600000, 200000, 150000, 500000, 450000, 900000, 250000, 300000],
            'RSB_MCT_CNT': [320, 180, 250, 60, 95, 70, 85, 45, 40],
            'RSB_MCT_TIME': ['202511'] * 9,
            'CMRCL_MALE_RATE': [48.5] * 9,
            'CMRCL_FEMALE_RATE': [51.5] * 9,
            'CMRCL_10_RATE': [0.8] * 9,
            'CMRCL_20_RATE': [42.3] * 9,
            'CMRCL_30_RATE': [38.5] * 9,
            'CMRCL_40_RATE': [12.5] * 9,
            'CMRCL_50_RATE': [4.2] * 9,
            'CMRCL_60_RATE': [1.7] * 9,
            'CMRCL_PERSONAL_RATE': [92.3] * 9,
            'CMRCL_CORPORATION_RATE': [7.7] * 9,
            'CMRCL_TIME': ['20251206 2100'] * 9
        })
        
        # 4. 명동
        sample_data_list.append({
            'AREA_NM': ['명동'] * 7,
            'AREA_CD': ['POI005'] * 7,
            'AREA_CMRCL_LVL': ['보통'] * 7,
            'AREA_SH_PAYMENT_CNT': [78] * 7,
            'AREA_SH_PAYMENT_AMT_MIN': [3100000] * 7,
            'AREA_SH_PAYMENT_AMT_MAX': [3400000] * 7,
            'RSB_LRG_CTGR': ['음식·음료', '유통', '패션·뷰티', '패션·뷰티', '여가·오락', '서비스', '서비스'],
            'RSB_MID_CTGR': ['한식', '편의점', '의복/의류', '화장품', '스포츠/문화/레저', '미용실', '안마/마사지'],
            'RSB_PAYMENT_LVL': ['보통', '보통', '보통', '보통', '한산한', '보통', '보통'],
            'RSB_SH_PAYMENT_CNT': [18, 12, 15, 10, 8, 9, 6],
            'RSB_SH_PAYMENT_AMT_MIN': [700000, 120000, 600000, 500000, 900000, 400000, 800000],
            'RSB_SH_PAYMENT_AMT_MAX': [800000, 150000, 700000, 600000, 1000000, 500000, 900000],
            'RSB_MCT_CNT': [280, 45, 150, 120, 65, 55, 40],
            'RSB_MCT_TIME': ['202511'] * 7,
            'CMRCL_MALE_RATE': [42.8] * 7,
            'CMRCL_FEMALE_RATE': [57.2] * 7,
            'CMRCL_10_RATE': [2.1] * 7,
            'CMRCL_20_RATE': [25.3] * 7,
            'CMRCL_30_RATE': [28.7] * 7,
            'CMRCL_40_RATE': [25.9] * 7,
            'CMRCL_50_RATE': [12.5] * 7,
            'CMRCL_60_RATE': [5.5] * 7,
            'CMRCL_PERSONAL_RATE': [90.2] * 7,
            'CMRCL_CORPORATION_RATE': [9.8] * 7,
            'CMRCL_TIME': ['20251206 2100'] * 7
        })
        
        # 모든 샘플 데이터 합치기
        dfs = [pd.DataFrame(data) for data in sample_data_list]
        df = pd.concat(dfs, ignore_index=True)
        print(f"✓ 샘플 데이터 생성: {len(df)}행 ({len(sample_data_list)}개 핫스팟)")
        print(f"  - 핫스팟 목록: {', '.join([data['AREA_NM'][0] for data in sample_data_list])}")
    else:
        try:
            client = SeoulCommercialAreaAPI(api_key=SEOUL_OPEN_DATA_API_KEY)
            area_list = ["광화문·덕수궁", "강남역", "홍대입구"]
            df = client.get_all_data(area_list)
            print(f"✓ 실시간 데이터 수집 완료: {len(df)}행")
        except Exception as e:
            print(f"⚠️  API 오류: {e}")
            print("샘플 데이터를 사용합니다.")
            return
    
    # 지역 프로필 생성
    print("\n[2단계] 지역 프로필 생성 및 점수 계산")
    print("-" * 80)
    profiles = analyze_all_areas(df)
    print(f"✓ {len(profiles)}개 지역 프로필 생성 완료")
    
    # 결과 출력
    print("\n[3단계] 분석 결과")
    print("-" * 80)
    print_analysis_results(profiles)
    
    # 결과 저장
    print("\n[4단계] 결과 저장")
    print("-" * 80)
    summary_df = save_analysis_results(profiles)
    
    print("\n" + "="*80)
    print("분석 완료!")
    print("="*80)
    print(f"\n생성된 프로필 수: {len(profiles)}개")
    print(f"결과 파일:")
    print(f"  - outputs/realtime_area_profiles.json")
    print(f"  - outputs/realtime_area_profiles_summary.csv")


if __name__ == '__main__':
    main()

