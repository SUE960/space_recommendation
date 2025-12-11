#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 전체 구(區) 지역 품질 점수 산출
Level 1: 지역 객관적 평가
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime


def load_card_data():
    """카드 데이터 로드"""
    file_path = 'data/card_data_2024.csv'
    
    if not os.path.exists(file_path):
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return None
    
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # 날짜 컬럼 변환
    if '이용일자' in df.columns:
        df['이용일자'] = pd.to_datetime(df['이용일자'], format='%Y%m%d')
    
    return df


def calculate_commercial_activity_score(df):
    """상업활동 점수 계산 (0-100)"""
    
    # 구별 집계
    gu_stats = df.groupby('시군구명').agg({
        '이용건수': 'sum',
        '이용금액': 'sum',
        '업종명': 'nunique'  # 업종 다양성
    }).reset_index()
    
    gu_stats.columns = ['구', '총_결제건수', '총_결제금액', '업종수']
    
    # 정규화 (0-100)
    max_count = gu_stats['총_결제건수'].max()
    max_amount = gu_stats['총_결제금액'].max()
    max_industry = gu_stats['업종수'].max()
    
    gu_stats['결제건수_점수'] = (gu_stats['총_결제건수'] / max_count) * 100
    gu_stats['결제금액_점수'] = (gu_stats['총_결제금액'] / max_amount) * 100
    gu_stats['업종다양성_점수'] = (gu_stats['업종수'] / max_industry) * 100
    
    # 가중 평균
    gu_stats['상업활동점수'] = (
        gu_stats['결제건수_점수'] * 0.4 +
        gu_stats['결제금액_점수'] * 0.4 +
        gu_stats['업종다양성_점수'] * 0.2
    ).round(1)
    
    return gu_stats[['구', '상업활동점수', '총_결제건수', '총_결제금액', '업종수']]


def calculate_specialization_score(df):
    """특화도 점수 계산 (0-100)"""
    
    results = []
    
    for gu in df['시군구명'].unique():
        gu_data = df[df['시군구명'] == gu]
        
        # 업종별 결제액
        industry_amounts = gu_data.groupby('업종명')['이용금액'].sum().sort_values(ascending=False)
        
        if len(industry_amounts) == 0:
            results.append({
                '구': gu,
                '특화도점수': 0,
                '1위업종': 'N/A',
                '1위비율': 0
            })
            continue
        
        total = industry_amounts.sum()
        
        # 1위 업종 비율
        top1_ratio = (industry_amounts.iloc[0] / total) * 100
        
        # 상위 3개 업종 집중도
        top3_ratio = (industry_amounts.head(3).sum() / total) * 100
        
        # 특화도 점수 = 1위 비율 60% + 상위3 집중도 40%
        specialization_score = (top1_ratio * 0.6) + (top3_ratio * 0.4)
        
        results.append({
            '구': gu,
            '특화도점수': round(specialization_score, 1),
            '1위업종': industry_amounts.index[0],
            '1위비율': round(top1_ratio, 1)
        })
    
    return pd.DataFrame(results)


def calculate_demographic_score(df):
    """인구통계 점수 계산 (0-100)"""
    
    # 인구 데이터가 없으므로 거래 패턴으로 대체
    # 성별/연령대 데이터가 있다면 활용
    
    results = []
    
    for gu in df['시군구명'].unique():
        gu_data = df[df['시군구명'] == gu]
        
        # 일평균 거래건수 (인구 활동성 대리 지표)
        daily_transactions = gu_data.groupby('이용일자')['이용건수'].sum()
        avg_daily = daily_transactions.mean()
        
        # 거래 안정성 (변동계수의 역수)
        std_daily = daily_transactions.std()
        cv = (std_daily / avg_daily) if avg_daily > 0 else 0
        stability_score = max(0, 100 - (cv * 100))  # 변동이 적을수록 높은 점수
        
        # 주중/주말 균형도
        df_temp = gu_data.copy()
        df_temp['요일'] = pd.to_datetime(df_temp['이용일자']).dt.dayofweek
        weekday = df_temp[df_temp['요일'] < 5]['이용건수'].sum()
        weekend = df_temp[df_temp['요일'] >= 5]['이용건수'].sum()
        total = weekday + weekend
        
        if total > 0:
            balance = 1 - abs((weekday/total) - 0.7)  # 주중 70% 정도가 이상적
            balance_score = balance * 100
        else:
            balance_score = 50
        
        # 종합
        demographic_score = (stability_score * 0.6 + balance_score * 0.4)
        
        results.append({
            '구': gu,
            '인구통계점수': round(demographic_score, 1)
        })
    
    return pd.DataFrame(results)


def calculate_economic_power_score():
    """경제력 점수 계산 (0-100)"""
    
    # 소득·소비 데이터 로드
    if os.path.exists('outputs/seoul_income_consumption_data.csv'):
        income_df = pd.read_csv('outputs/seoul_income_consumption_data.csv')
        
        # 구별 평균 계산 (상권명에서 구 추출 필요)
        # 일단 전체 평균 사용
        avg_income = income_df['MT_AVRG_INCOME_AMT'].mean()
        avg_spending = income_df['EXPNDTR_TOTAMT'].mean()
        
        # 모든 구에 동일 점수 (데이터 부족으로)
        # 실제로는 구별로 매핑 필요
        economic_score = 50  # 기본 점수
        
    else:
        economic_score = 50  # 기본 점수
    
    return economic_score


def calculate_all_regional_scores(df):
    """전체 구의 종합 점수 계산"""
    
    print("="*80)
    print("서울시 전체 구 지역 품질 점수 산출")
    print("="*80)
    
    # 1. 상업활동 점수
    print("\n[1/4] 상업활동 점수 계산 중...")
    commercial_df = calculate_commercial_activity_score(df)
    
    # 2. 특화도 점수
    print("[2/4] 특화도 점수 계산 중...")
    specialization_df = calculate_specialization_score(df)
    
    # 3. 인구통계 점수
    print("[3/4] 인구통계 점수 계산 중...")
    demographic_df = calculate_demographic_score(df)
    
    # 4. 경제력 점수
    print("[4/4] 경제력 점수 계산 중...")
    economic_score = calculate_economic_power_score()
    
    # 통합
    result = commercial_df.merge(specialization_df, on='구')
    result = result.merge(demographic_df, on='구')
    result['경제력점수'] = economic_score  # 일단 동일값
    
    # 종합 점수 계산
    result['종합점수'] = (
        result['상업활동점수'] * 0.30 +
        result['특화도점수'] * 0.25 +
        result['인구통계점수'] * 0.20 +
        result['경제력점수'] * 0.25
    ).round(1)
    
    # 순위
    result = result.sort_values('종합점수', ascending=False).reset_index(drop=True)
    result['순위'] = range(1, len(result) + 1)
    
    # 등급 부여
    def assign_grade(score):
        if score >= 80:
            return 'S급 (초우량)'
        elif score >= 70:
            return 'A급 (우량)'
        elif score >= 60:
            return 'B급 (보통)'
        elif score >= 50:
            return 'C급 (개선필요)'
        else:
            return 'D급 (저활성)'
    
    result['등급'] = result['종합점수'].apply(assign_grade)
    
    return result


def print_results(df):
    """결과 출력"""
    
    print("\n" + "="*80)
    print("서울시 25개 구 지역 품질 점수표")
    print("="*80)
    
    print(f"\n{'순위':<6} {'구':<12} {'종합':<8} {'상업':<8} {'특화':<8} {'인구':<8} {'경제':<8} {'등급':<15} {'특화업종':<20}")
    print("-" * 120)
    
    for _, row in df.iterrows():
        print(f"{row['순위']:<6} {row['구']:<12} "
              f"{row['종합점수']:>6.1f}  "
              f"{row['상업활동점수']:>6.1f}  "
              f"{row['특화도점수']:>6.1f}  "
              f"{row['인구통계점수']:>6.1f}  "
              f"{row['경제력점수']:>6.1f}  "
              f"{row['등급']:<15} "
              f"{row['1위업종']:<20}")
    
    # 통계 요약
    print("\n" + "="*80)
    print("통계 요약")
    print("="*80)
    
    print(f"\n등급별 분포:")
    grade_counts = df['등급'].value_counts().sort_index()
    for grade, count in grade_counts.items():
        print(f"  {grade}: {count}개 구")
    
    print(f"\n점수 통계:")
    print(f"  평균: {df['종합점수'].mean():.1f}점")
    print(f"  중앙값: {df['종합점수'].median():.1f}점")
    print(f"  최고: {df['종합점수'].max():.1f}점 ({df.iloc[0]['구']})")
    print(f"  최저: {df['종합점수'].min():.1f}점 ({df.iloc[-1]['구']})")
    print(f"  표준편차: {df['종합점수'].std():.1f}점")


def save_results(df):
    """결과 저장"""
    
    os.makedirs('outputs', exist_ok=True)
    
    # CSV 저장
    output_file = 'outputs/seoul_25gu_quality_scores.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV 저장: {output_file}")
    
    # JSON 저장
    json_data = {
        '생성일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '분석대상': '서울시 25개 구',
        '평가기준': {
            'Level': 1,
            '유형': '지역 객관적 품질 평가',
            '점수범위': '0-100점',
            '가중치': {
                '상업활동': '30%',
                '특화도': '25%',
                '인구통계': '20%',
                '경제력': '25%'
            }
        },
        '구별점수': df.to_dict('records')
    }
    
    json_file = 'outputs/seoul_25gu_quality_scores.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 저장: {json_file}")
    
    # Markdown 표 생성
    md_file = 'outputs/서울시_25개구_지역점수표.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 서울시 25개 구 지역 품질 점수표\n\n")
        f.write(f"**생성일시:** {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}\n\n")
        f.write("**평가 기준:** Level 1 - 지역 객관적 품질 평가\n\n")
        f.write("---\n\n")
        f.write("## 전체 순위표\n\n")
        f.write("| 순위 | 구 | 종합점수 | 상업활동 | 특화도 | 인구통계 | 경제력 | 등급 | 주요 특화업종 |\n")
        f.write("|:----:|:-----|:--------:|:--------:|:------:|:--------:|:------:|:-----|:--------------|\n")
        
        for _, row in df.iterrows():
            f.write(f"| {row['순위']} | {row['구']} | {row['종합점수']:.1f} | "
                   f"{row['상업활동점수']:.1f} | {row['특화도점수']:.1f} | "
                   f"{row['인구통계점수']:.1f} | {row['경제력점수']:.1f} | "
                   f"{row['등급']} | {row['1위업종']} |\n")
        
        f.write("\n---\n\n")
        f.write("## 등급별 분류\n\n")
        
        for grade in ['S급 (초우량)', 'A급 (우량)', 'B급 (보통)', 'C급 (개선필요)', 'D급 (저활성)']:
            grade_df = df[df['등급'] == grade]
            if len(grade_df) > 0:
                f.write(f"### {grade}\n\n")
                for _, row in grade_df.iterrows():
                    f.write(f"- **{row['구']}** ({row['종합점수']:.1f}점) - {row['1위업종']} 특화\n")
                f.write("\n")
        
        f.write("---\n\n")
        f.write("## 점수 상세 분석\n\n")
        
        # TOP 3
        f.write("### 🥇 TOP 3 구\n\n")
        for i in range(min(3, len(df))):
            row = df.iloc[i]
            f.write(f"#### {i+1}위: {row['구']} ({row['종합점수']:.1f}점)\n\n")
            f.write(f"- **상업활동**: {row['상업활동점수']:.1f}점\n")
            f.write(f"- **특화도**: {row['특화도점수']:.1f}점 ({row['1위업종']})\n")
            f.write(f"- **인구통계**: {row['인구통계점수']:.1f}점\n")
            f.write(f"- **경제력**: {row['경제력점수']:.1f}점\n")
            f.write(f"- **총 거래**: {int(row['총_결제건수']):,}건, {int(row['총_결제금액']):,}원\n")
            f.write(f"- **업종수**: {int(row['업종수'])}개\n\n")
    
    print(f"✓ Markdown 저장: {md_file}")


def main():
    """메인 실행 함수"""
    
    # 데이터 로드
    print("데이터 로드 중...")
    df = load_card_data()
    
    if df is None:
        print("❌ 데이터를 로드할 수 없습니다.")
        return
    
    print(f"✓ 데이터 로드 완료: {len(df):,}건")
    print(f"  기간: {df['이용일자'].min()} ~ {df['이용일자'].max()}")
    print(f"  대상: {df['시군구명'].nunique()}개 구")
    
    # 점수 계산
    result_df = calculate_all_regional_scores(df)
    
    # 결과 출력
    print_results(result_df)
    
    # 결과 저장
    save_results(result_df)
    
    print("\n" + "="*80)
    print("분석 완료!")
    print("="*80)
    
    return result_df


if __name__ == '__main__':
    result = main()





