#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 상권별 소득·소비 데이터(trdarNcmCnsmp) 분석
상권별 월평균 소득 및 카테고리별 지출액 분석
"""

import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import os
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False


# 실제 제공된 상권별 소득·소비 데이터 XML
INCOME_CONSUMPTION_XML = """<?xml version="1.0" encoding="UTF-8"?>
<trdarNcmCnsmp>
<list_total_count>42346</list_total_count>
<RESULT>
<CODE>INFO-000</CODE>
<MESSAGE>정상 처리되었습니다</MESSAGE>
</RESULT>
<row>
<STDR_YYQU_CD>20191</STDR_YYQU_CD>
<TRDAR_SE_CD>A</TRDAR_SE_CD>
<TRDAR_SE_CD_NM>골목상권</TRDAR_SE_CD_NM>
<TRDAR_CD>3110020</TRDAR_CD>
<TRDAR_CD_NM>서울국제고등학교</TRDAR_CD_NM>
<MT_AVRG_INCOME_AMT>2838790</MT_AVRG_INCOME_AMT>
<INCOME_SCTN_CD>06</INCOME_SCTN_CD>
<EXPNDTR_TOTAMT>1893277180</EXPNDTR_TOTAMT>
<FDSTFFS_EXPNDTR_TOTAMT>452132567</FDSTFFS_EXPNDTR_TOTAMT>
<CLTHS_FTWR_EXPNDTR_TOTAMT>252800465</CLTHS_FTWR_EXPNDTR_TOTAMT>
<LVSPL_EXPNDTR_TOTAMT>124254004</LVSPL_EXPNDTR_TOTAMT>
<MCP_EXPNDTR_TOTAMT>230932468</MCP_EXPNDTR_TOTAMT>
<TRNSPORT_EXPNDTR_TOTAMT>243437040</TRNSPORT_EXPNDTR_TOTAMT>
<LSR_EXPNDTR_TOTAMT>68238981</LSR_EXPNDTR_TOTAMT>
<CLTUR_EXPNDTR_TOTAMT>71326707</CLTUR_EXPNDTR_TOTAMT>
<EDC_EXPNDTR_TOTAMT>354675459</EDC_EXPNDTR_TOTAMT>
<PLESR_EXPNDTR_TOTAMT>95479489</PLESR_EXPNDTR_TOTAMT>
</row>
<row>
<STDR_YYQU_CD>20191</STDR_YYQU_CD>
<TRDAR_SE_CD>A</TRDAR_SE_CD>
<TRDAR_SE_CD_NM>골목상권</TRDAR_SE_CD_NM>
<TRDAR_CD>3110021</TRDAR_CD>
<TRDAR_CD_NM>성균관대학교</TRDAR_CD_NM>
<MT_AVRG_INCOME_AMT>3094492</MT_AVRG_INCOME_AMT>
<INCOME_SCTN_CD>07</INCOME_SCTN_CD>
<EXPNDTR_TOTAMT>1062083531</EXPNDTR_TOTAMT>
<FDSTFFS_EXPNDTR_TOTAMT>242915806</FDSTFFS_EXPNDTR_TOTAMT>
<CLTHS_FTWR_EXPNDTR_TOTAMT>149142873</CLTHS_FTWR_EXPNDTR_TOTAMT>
<LVSPL_EXPNDTR_TOTAMT>64336647</LVSPL_EXPNDTR_TOTAMT>
<MCP_EXPNDTR_TOTAMT>128741468</MCP_EXPNDTR_TOTAMT>
<TRNSPORT_EXPNDTR_TOTAMT>119906366</TRNSPORT_EXPNDTR_TOTAMT>
<LSR_EXPNDTR_TOTAMT>38074560</LSR_EXPNDTR_TOTAMT>
<CLTUR_EXPNDTR_TOTAMT>43410868</CLTUR_EXPNDTR_TOTAMT>
<EDC_EXPNDTR_TOTAMT>217013206</EDC_EXPNDTR_TOTAMT>
<PLESR_EXPNDTR_TOTAMT>58541737</PLESR_EXPNDTR_TOTAMT>
</row>
<row>
<STDR_YYQU_CD>20191</STDR_YYQU_CD>
<TRDAR_SE_CD>A</TRDAR_SE_CD>
<TRDAR_SE_CD_NM>골목상권</TRDAR_SE_CD_NM>
<TRDAR_CD>3110022</TRDAR_CD>
<TRDAR_CD_NM>경신고등학교</TRDAR_CD_NM>
<MT_AVRG_INCOME_AMT>3727474</MT_AVRG_INCOME_AMT>
<INCOME_SCTN_CD>07</INCOME_SCTN_CD>
<EXPNDTR_TOTAMT>879563907</EXPNDTR_TOTAMT>
<FDSTFFS_EXPNDTR_TOTAMT>213067686</FDSTFFS_EXPNDTR_TOTAMT>
<CLTHS_FTWR_EXPNDTR_TOTAMT>112630640</CLTHS_FTWR_EXPNDTR_TOTAMT>
<LVSPL_EXPNDTR_TOTAMT>67054373</LVSPL_EXPNDTR_TOTAMT>
<MCP_EXPNDTR_TOTAMT>103617117</MCP_EXPNDTR_TOTAMT>
<TRNSPORT_EXPNDTR_TOTAMT>141197378</TRNSPORT_EXPNDTR_TOTAMT>
<LSR_EXPNDTR_TOTAMT>35771940</LSR_EXPNDTR_TOTAMT>
<CLTUR_EXPNDTR_TOTAMT>28983203</CLTUR_EXPNDTR_TOTAMT>
<EDC_EXPNDTR_TOTAMT>137249616</EDC_EXPNDTR_TOTAMT>
<PLESR_EXPNDTR_TOTAMT>39991954</PLESR_EXPNDTR_TOTAMT>
</row>
<row>
<STDR_YYQU_CD>20191</STDR_YYQU_CD>
<TRDAR_SE_CD>A</TRDAR_SE_CD>
<TRDAR_SE_CD_NM>골목상권</TRDAR_SE_CD_NM>
<TRDAR_CD>3110023</TRDAR_CD>
<TRDAR_CD_NM>서울대병원</TRDAR_CD_NM>
<MT_AVRG_INCOME_AMT>3583075</MT_AVRG_INCOME_AMT>
<INCOME_SCTN_CD>07</INCOME_SCTN_CD>
<EXPNDTR_TOTAMT>430124011</EXPNDTR_TOTAMT>
<FDSTFFS_EXPNDTR_TOTAMT>108261409</FDSTFFS_EXPNDTR_TOTAMT>
<CLTHS_FTWR_EXPNDTR_TOTAMT>56900899</CLTHS_FTWR_EXPNDTR_TOTAMT>
<LVSPL_EXPNDTR_TOTAMT>32354969</LVSPL_EXPNDTR_TOTAMT>
<MCP_EXPNDTR_TOTAMT>52009106</MCP_EXPNDTR_TOTAMT>
<TRNSPORT_EXPNDTR_TOTAMT>63413630</TRNSPORT_EXPNDTR_TOTAMT>
<LSR_EXPNDTR_TOTAMT>16013724</LSR_EXPNDTR_TOTAMT>
<CLTUR_EXPNDTR_TOTAMT>16065073</CLTUR_EXPNDTR_TOTAMT>
<EDC_EXPNDTR_TOTAMT>63589499</EDC_EXPNDTR_TOTAMT>
<PLESR_EXPNDTR_TOTAMT>21515702</PLESR_EXPNDTR_TOTAMT>
</row>
<row>
<STDR_YYQU_CD>20191</STDR_YYQU_CD>
<TRDAR_SE_CD>A</TRDAR_SE_CD>
<TRDAR_SE_CD_NM>골목상권</TRDAR_SE_CD_NM>
<TRDAR_CD>3110024</TRDAR_CD>
<TRDAR_CD_NM>혜회동주민센터</TRDAR_CD_NM>
<MT_AVRG_INCOME_AMT>3680918</MT_AVRG_INCOME_AMT>
<INCOME_SCTN_CD>07</INCOME_SCTN_CD>
<EXPNDTR_TOTAMT>526235130</EXPNDTR_TOTAMT>
<FDSTFFS_EXPNDTR_TOTAMT>139291704</FDSTFFS_EXPNDTR_TOTAMT>
<CLTHS_FTWR_EXPNDTR_TOTAMT>65438122</CLTHS_FTWR_EXPNDTR_TOTAMT>
<LVSPL_EXPNDTR_TOTAMT>42020919</LVSPL_EXPNDTR_TOTAMT>
<MCP_EXPNDTR_TOTAMT>64590263</MCP_EXPNDTR_TOTAMT>
<TRNSPORT_EXPNDTR_TOTAMT>87008490</TRNSPORT_EXPNDTR_TOTAMT>
<LSR_EXPNDTR_TOTAMT>19119069</LSR_EXPNDTR_TOTAMT>
<CLTUR_EXPNDTR_TOTAMT>17469686</CLTUR_EXPNDTR_TOTAMT>
<EDC_EXPNDTR_TOTAMT>67542127</EDC_EXPNDTR_TOTAMT>
<PLESR_EXPNDTR_TOTAMT>23754750</PLESR_EXPNDTR_TOTAMT>
</row>
</trdarNcmCnsmp>
"""


# 컬럼명 매핑
COLUMN_MAPPING = {
    'STDR_YYQU_CD': '기준연도분기코드',
    'TRDAR_SE_CD': '상권구분코드',
    'TRDAR_SE_CD_NM': '상권구분명',
    'TRDAR_CD': '상권코드',
    'TRDAR_CD_NM': '상권명',
    'MT_AVRG_INCOME_AMT': '월평균소득',
    'INCOME_SCTN_CD': '소득구간코드',
    'EXPNDTR_TOTAMT': '지출총액',
    'FDSTFFS_EXPNDTR_TOTAMT': '식료품비',
    'CLTHS_FTWR_EXPNDTR_TOTAMT': '의류신발비',
    'LVSPL_EXPNDTR_TOTAMT': '생활용품비',
    'MCP_EXPNDTR_TOTAMT': '의료비',
    'TRNSPORT_EXPNDTR_TOTAMT': '교통비',
    'LSR_EXPNDTR_TOTAMT': '여가비',
    'CLTUR_EXPNDTR_TOTAMT': '문화비',
    'EDC_EXPNDTR_TOTAMT': '교육비',
    'PLESR_EXPNDTR_TOTAMT': '오락비'
}

# 지출 카테고리
EXPENDITURE_CATEGORIES = {
    '식료품비': 'FDSTFFS_EXPNDTR_TOTAMT',
    '의류신발비': 'CLTHS_FTWR_EXPNDTR_TOTAMT',
    '생활용품비': 'LVSPL_EXPNDTR_TOTAMT',
    '의료비': 'MCP_EXPNDTR_TOTAMT',
    '교통비': 'TRNSPORT_EXPNDTR_TOTAMT',
    '여가비': 'LSR_EXPNDTR_TOTAMT',
    '문화비': 'CLTUR_EXPNDTR_TOTAMT',
    '교육비': 'EDC_EXPNDTR_TOTAMT',
    '오락비': 'PLESR_EXPNDTR_TOTAMT'
}


def parse_income_consumption_data(xml_text):
    """소득·소비 데이터 XML 파싱"""
    root = ET.fromstring(xml_text)
    
    data_rows = []
    for row in root.findall('.//row'):
        row_data = {}
        for child in row:
            tag = child.tag
            text = child.text
            
            if text and text.strip():
                # 숫자 필드는 int로 변환
                if 'AMT' in tag or 'CD' in tag:
                    try:
                        row_data[tag] = int(text)
                    except ValueError:
                        row_data[tag] = text
                else:
                    row_data[tag] = text
            else:
                row_data[tag] = None
        
        data_rows.append(row_data)
    
    df = pd.DataFrame(data_rows)
    
    # 연도/분기 추출
    df['연도'] = df['STDR_YYQU_CD'].astype(str).str[:4]
    df['분기'] = df['STDR_YYQU_CD'].astype(str).str[4]
    df['연도분기'] = df['연도'] + 'Q' + df['분기']
    
    return df


def analyze_basic_info(df):
    """기본 정보 분석"""
    print("\n" + "="*80)
    print("데이터 기본 정보")
    print("="*80)
    
    print(f"\n총 데이터 수: {len(df):,}개 상권")
    print(f"데이터 기간: {df['연도분기'].min()} ~ {df['연도분기'].max()}")
    print(f"상권 구분: {df['TRDAR_SE_CD_NM'].unique()}")
    
    print(f"\n[샘플 데이터 - 상위 5개 상권]")
    print(f"\n{'상권명':<20} {'월평균소득':<15} {'지출총액':<15} {'소득대비지출율':<12}")
    print("-" * 70)
    
    for _, row in df.head().iterrows():
        spending_ratio = (row['EXPNDTR_TOTAMT'] / row['MT_AVRG_INCOME_AMT']) if row['MT_AVRG_INCOME_AMT'] > 0 else 0
        print(f"{row['TRDAR_CD_NM']:<20} {row['MT_AVRG_INCOME_AMT']:>13,}원  {row['EXPNDTR_TOTAMT']:>13,}원  {spending_ratio:>10.1f}배")


def analyze_income_distribution(df):
    """소득 분포 분석"""
    print("\n" + "="*80)
    print("상권별 소득 분포 분석")
    print("="*80)
    
    income_stats = df['MT_AVRG_INCOME_AMT'].describe()
    
    print(f"\n[월평균 소득 통계]")
    print(f"평균: {income_stats['mean']:,.0f}원")
    print(f"중앙값: {income_stats['50%']:,.0f}원")
    print(f"최소: {income_stats['min']:,.0f}원")
    print(f"최대: {income_stats['max']:,.0f}원")
    print(f"표준편차: {income_stats['std']:,.0f}원")
    
    # 소득 구간별 분석
    print(f"\n[소득구간별 상권 수]")
    income_section_counts = df['INCOME_SCTN_CD'].value_counts().sort_index()
    
    for section, count in income_section_counts.items():
        pct = (count / len(df) * 100)
        print(f"소득구간 {section:02d}: {count:>5}개 ({pct:>5.1f}%)")


def analyze_expenditure_patterns(df):
    """지출 패턴 분석"""
    print("\n" + "="*80)
    print("카테고리별 지출 패턴 분석")
    print("="*80)
    
    # 전체 평균 지출액
    print(f"\n[카테고리별 평균 지출액]")
    print(f"\n{'카테고리':<12} {'평균 지출액':<18} {'총지출 대비':<12}")
    print("-" * 50)
    
    avg_total = df['EXPNDTR_TOTAMT'].mean()
    
    for category_kr, category_en in EXPENDITURE_CATEGORIES.items():
        avg_amount = df[category_en].mean()
        ratio = (avg_amount / avg_total * 100) if avg_total > 0 else 0
        print(f"{category_kr:<12} {avg_amount:>15,.0f}원  {ratio:>9.1f}%")
    
    print(f"\n{'전체':<12} {avg_total:>15,.0f}원  {100.0:>9.1f}%")


def analyze_top_areas(df):
    """상위 상권 분석"""
    print("\n" + "="*80)
    print("주요 지표별 상위 상권")
    print("="*80)
    
    # 1. 월평균 소득 상위
    print(f"\n[월평균 소득 TOP 10]")
    print(f"\n{'순위':<6} {'상권명':<25} {'월평균소득':<18}")
    print("-" * 55)
    
    top_income = df.nlargest(10, 'MT_AVRG_INCOME_AMT')
    for idx, (_, row) in enumerate(top_income.iterrows(), 1):
        print(f"{idx:<6} {row['TRDAR_CD_NM']:<25} {row['MT_AVRG_INCOME_AMT']:>15,}원")
    
    # 2. 지출총액 상위
    print(f"\n[지출총액 TOP 10]")
    print(f"\n{'순위':<6} {'상권명':<25} {'지출총액':<18}")
    print("-" * 55)
    
    top_spending = df.nlargest(10, 'EXPNDTR_TOTAMT')
    for idx, (_, row) in enumerate(top_spending.iterrows(), 1):
        print(f"{idx:<6} {row['TRDAR_CD_NM']:<25} {row['EXPNDTR_TOTAMT']:>15,}원")


def analyze_category_leaders(df):
    """카테고리별 최고 지출 상권"""
    print("\n" + "="*80)
    print("카테고리별 최고 지출 상권")
    print("="*80)
    
    print(f"\n{'카테고리':<12} {'상권명':<25} {'지출액':<18}")
    print("-" * 60)
    
    for category_kr, category_en in EXPENDITURE_CATEGORIES.items():
        top_row = df.nlargest(1, category_en).iloc[0]
        print(f"{category_kr:<12} {top_row['TRDAR_CD_NM']:<25} {top_row[category_en]:>15,}원")


def calculate_spending_efficiency(df):
    """소비 효율성 분석"""
    print("\n" + "="*80)
    print("소비 효율성 분석 (소득 대비 지출 비율)")
    print("="*80)
    
    df['지출비율'] = df['EXPNDTR_TOTAMT'] / df['MT_AVRG_INCOME_AMT']
    
    # 효율성 통계
    efficiency_stats = df['지출비율'].describe()
    
    print(f"\n[소득 대비 지출 비율 통계]")
    print(f"평균: {efficiency_stats['mean']:.2f}배")
    print(f"중앙값: {efficiency_stats['50%']:.2f}배")
    print(f"최소: {efficiency_stats['min']:.2f}배")
    print(f"최대: {efficiency_stats['max']:.2f}배")
    
    # 고소비 상권 (지출비율 높은 상위 10개)
    print(f"\n[고소비 상권 TOP 10 (지출/소득 비율)]")
    print(f"\n{'순위':<6} {'상권명':<25} {'월소득':<15} {'지출액':<15} {'비율':<10}")
    print("-" * 75)
    
    high_spenders = df.nlargest(10, '지출비율')
    for idx, (_, row) in enumerate(high_spenders.iterrows(), 1):
        print(f"{idx:<6} {row['TRDAR_CD_NM']:<25} {row['MT_AVRG_INCOME_AMT']:>12,}원  {row['EXPNDTR_TOTAMT']:>12,}원  {row['지출비율']:>8.1f}배")


def save_analysis_results(df):
    """분석 결과 저장"""
    os.makedirs('outputs', exist_ok=True)
    
    # 1. 전체 데이터 저장
    output_file = 'outputs/seoul_income_consumption_data.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ 전체 데이터 저장: {output_file}")
    
    # 2. 요약 통계 저장
    summary = {
        '총_상권수': len(df),
        '평균_월소득': int(df['MT_AVRG_INCOME_AMT'].mean()),
        '평균_지출총액': int(df['EXPNDTR_TOTAMT'].mean()),
        '평균_식료품비': int(df['FDSTFFS_EXPNDTR_TOTAMT'].mean()),
        '평균_의류신발비': int(df['CLTHS_FTWR_EXPNDTR_TOTAMT'].mean()),
        '평균_생활용품비': int(df['LVSPL_EXPNDTR_TOTAMT'].mean()),
        '평균_의료비': int(df['MCP_EXPNDTR_TOTAMT'].mean()),
        '평균_교통비': int(df['TRNSPORT_EXPNDTR_TOTAMT'].mean()),
        '평균_여가비': int(df['LSR_EXPNDTR_TOTAMT'].mean()),
        '평균_문화비': int(df['CLTUR_EXPNDTR_TOTAMT'].mean()),
        '평균_교육비': int(df['EDC_EXPNDTR_TOTAMT'].mean()),
        '평균_오락비': int(df['PLESR_EXPNDTR_TOTAMT'].mean()),
        '평균_지출비율': round(df['EXPNDTR_TOTAMT'].mean() / df['MT_AVRG_INCOME_AMT'].mean(), 2)
    }
    
    summary_df = pd.DataFrame([summary])
    summary_file = 'outputs/income_consumption_summary.csv'
    summary_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
    print(f"✓ 요약 통계 저장: {summary_file}")
    
    # 3. 상위 상권 저장
    top_areas = df.nlargest(50, 'EXPNDTR_TOTAMT')[['TRDAR_CD_NM', 'MT_AVRG_INCOME_AMT', 'EXPNDTR_TOTAMT'] + list(EXPENDITURE_CATEGORIES.values())]
    top_file = 'outputs/top_commercial_areas_by_spending.csv'
    top_areas.to_csv(top_file, index=False, encoding='utf-8-sig')
    print(f"✓ 상위 상권 저장: {top_file}")


def suggest_integration():
    """데이터 통합 활용 방안"""
    print("\n" + "="*80)
    print("💡 프로젝트 통합 활용 방안")
    print("="*80)
    
    suggestions = [
        "1. 카드 소비 데이터와 결합",
        "   → 상권별 실제 카드 사용 패턴과 소득/지출 데이터 비교",
        "   → 소득 수준별 결제 선호도 분석",
        "",
        "2. 인구 데이터와 결합",
        "   → 연령대별 소비 패턴 예측",
        "   → 인구 구조에 따른 상권 특성 분석",
        "",
        "3. GIS 데이터와 결합",
        "   → 지역별 소득 밀집도 시각화",
        "   → 고소득/고지출 상권 지도 매핑",
        "",
        "4. 실시간 지역 프로필 강화",
        "   → 경제력 점수 추가 (소득/지출 수준)",
        "   → 소비성향 지표 (카테고리별 지출 비율)",
        "   → 타겟 고객층 매칭 (소득 구간별)",
        "",
        "5. 추천 시스템 개인화",
        "   → 사용자 소득/지출 패턴 기반 상권 추천",
        "   → 비슷한 경제 수준의 이용자가 선호하는 지역 추천"
    ]
    
    for suggestion in suggestions:
        print(suggestion)


def main():
    """메인 실행 함수"""
    print("="*80)
    print("서울시 상권별 소득·소비 데이터 분석")
    print("="*80)
    
    # XML 데이터 파싱
    print("\n[1단계] XML 데이터 파싱")
    print("-" * 80)
    df = parse_income_consumption_data(INCOME_CONSUMPTION_XML)
    print(f"✓ 데이터 파싱 완료: 샘플 {len(df)}개 상권")
    print(f"✓ 전체 데이터: 42,346개 상권 (API에서 확인)")
    
    # 기본 정보 분석
    analyze_basic_info(df)
    
    # 소득 분포 분석
    analyze_income_distribution(df)
    
    # 지출 패턴 분석
    analyze_expenditure_patterns(df)
    
    # 상위 상권 분석
    analyze_top_areas(df)
    
    # 카테고리별 리더
    analyze_category_leaders(df)
    
    # 소비 효율성
    calculate_spending_efficiency(df)
    
    # 결과 저장
    print("\n[최종 단계] 결과 저장")
    print("-" * 80)
    save_analysis_results(df)
    
    # 통합 활용 방안
    suggest_integration()
    
    print("\n" + "="*80)
    print("분석 완료!")
    print("="*80)
    print("\n🎯 이 데이터는 프로젝트의 핵심 경제 지표로 활용 가능합니다!")
    
    return df


if __name__ == '__main__':
    result = main()

