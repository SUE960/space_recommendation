#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인구 데이터 처리 및 분석 모듈
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class PopulationDataProcessor:
    """인구 데이터 처리 클래스"""
    
    def __init__(self, df: pd.DataFrame):
        """
        데이터프로세서 초기화
        
        Args:
            df: 인구 데이터프레임
        """
        self.df = df.copy()
        self._preprocess()
    
    def _preprocess(self):
        """데이터 전처리"""
        # 기준연도분기코드를 연도와 분기로 분리
        if '기준연도분기코드' in self.df.columns:
            self.df['연도'] = self.df['기준연도분기코드'].astype(str).str[:4].astype(int)
            self.df['분기'] = self.df['기준연도분기코드'].astype(str).str[4].astype(int)
            self.df['연도분기'] = self.df['연도'].astype(str) + 'Q' + self.df['분기'].astype(str)
        
        # 인구 비율 계산
        if '총인구수' in self.df.columns:
            if '남성인구수' in self.df.columns:
                self.df['남성비율'] = (self.df['남성인구수'] / self.df['총인구수'] * 100).round(2)
            if '여성인구수' in self.df.columns:
                self.df['여성비율'] = (self.df['여성인구수'] / self.df['총인구수'] * 100).round(2)
            
            # 연령대별 비율 계산
            age_columns = ['10대인구수', '20대인구수', '30대인구수', 
                          '40대인구수', '50대인구수', '60대이상인구수']
            for col in age_columns:
                if col in self.df.columns:
                    ratio_col = col.replace('인구수', '비율')
                    self.df[ratio_col] = (self.df[col] / self.df['총인구수'] * 100).round(2)
    
    def get_population_by_period(self, year: int = None, quarter: int = None) -> pd.DataFrame:
        """
        기간별 인구 데이터 조회
        
        Args:
            year: 연도 (선택)
            quarter: 분기 (선택)
        
        Returns:
            필터링된 인구 데이터프레임
        """
        filtered = self.df.copy()
        
        if year:
            filtered = filtered[filtered['연도'] == year]
        if quarter:
            filtered = filtered[filtered['분기'] == quarter]
        
        return filtered.sort_values('기준연도분기코드')
    
    def get_population_trend(self) -> pd.DataFrame:
        """
        인구 추이 분석
        
        Returns:
            연도분기별 인구 추이 데이터프레임
        """
        if '기준연도분기코드' not in self.df.columns or '총인구수' not in self.df.columns:
            return pd.DataFrame()
        
        trend = self.df[['기준연도분기코드', '연도', '분기', '총인구수', 
                         '남성인구수', '여성인구수', '총가구수']].copy()
        trend = trend.sort_values('기준연도분기코드')
        
        # 전분기 대비 증감률 계산
        if len(trend) > 1:
            trend['인구증감'] = trend['총인구수'].diff()
            trend['인구증감률'] = (trend['총인구수'].pct_change() * 100).round(2)
            trend['가구증감'] = trend['총가구수'].diff()
            trend['가구증감률'] = (trend['총가구수'].pct_change() * 100).round(2)
        
        return trend
    
    def get_age_distribution(self, year: int = None, quarter: int = None) -> Dict:
        """
        연령대별 인구 분포 분석
        
        Args:
            year: 연도 (선택)
            quarter: 분기 (선택)
        
        Returns:
            연령대별 인구 분포 딕셔너리
        """
        filtered = self.get_population_by_period(year, quarter)
        
        if len(filtered) == 0:
            return {}
        
        # 가장 최근 데이터 사용
        latest = filtered.iloc[-1]
        
        age_dist = {}
        age_columns = {
            '10대인구수': '10대',
            '20대인구수': '20대',
            '30대인구수': '30대',
            '40대인구수': '40대',
            '50대인구수': '50대',
            '60대이상인구수': '60대이상'
        }
        
        for col, label in age_columns.items():
            if col in latest:
                age_dist[label] = {
                    '인구수': int(latest[col]) if pd.notna(latest[col]) else 0,
                    '비율': float(latest[col.replace('인구수', '비율')]) if col.replace('인구수', '비율') in latest else None
                }
        
        return age_dist
    
    def get_gender_distribution(self, year: int = None, quarter: int = None) -> Dict:
        """
        성별 인구 분포 분석
        
        Args:
            year: 연도 (선택)
            quarter: 분기 (선택)
        
        Returns:
            성별 인구 분포 딕셔너리
        """
        filtered = self.get_population_by_period(year, quarter)
        
        if len(filtered) == 0:
            return {}
        
        latest = filtered.iloc[-1]
        
        result = {}
        if '남성인구수' in latest and '여성인구수' in latest:
            result = {
                '남성': {
                    '인구수': int(latest['남성인구수']) if pd.notna(latest['남성인구수']) else 0,
                    '비율': float(latest['남성비율']) if '남성비율' in latest and pd.notna(latest['남성비율']) else None
                },
                '여성': {
                    '인구수': int(latest['여성인구수']) if pd.notna(latest['여성인구수']) else 0,
                    '비율': float(latest['여성비율']) if '여성비율' in latest and pd.notna(latest['여성비율']) else None
                }
            }
        
        return result
    
    def get_household_statistics(self, year: int = None, quarter: int = None) -> Dict:
        """
        가구 통계 분석
        
        Args:
            year: 연도 (선택)
            quarter: 분기 (선택)
        
        Returns:
            가구 통계 딕셔너리
        """
        filtered = self.get_population_by_period(year, quarter)
        
        if len(filtered) == 0:
            return {}
        
        latest = filtered.iloc[-1]
        
        result = {}
        if '총가구수' in latest:
            result['총가구수'] = int(latest['총가구수']) if pd.notna(latest['총가구수']) else 0
        if '아파트가구수' in latest:
            result['아파트가구수'] = int(latest['아파트가구수']) if pd.notna(latest['아파트가구수']) else 0
        if '비아파트가구수' in latest:
            result['비아파트가구수'] = int(latest['비아파트가구수']) if pd.notna(latest['비아파트가구수']) else 0
        
        # 가구당 인구수 계산
        if '총가구수' in result and '총인구수' in latest and result['총가구수'] > 0:
            result['가구당인구수'] = round(latest['총인구수'] / result['총가구수'], 2)
        
        return result
    
    def merge_with_card_data(self, card_df: pd.DataFrame) -> pd.DataFrame:
        """
        카드 데이터와 병합 (인구 데이터를 기준으로)
        
        Args:
            card_df: 카드 소비 데이터프레임
        
        Returns:
            병합된 데이터프레임
        """
        # TODO: 실제 병합 로직 구현 필요
        # 인구 데이터의 연도/분기 정보를 카드 데이터와 매칭
        # 예: 카드 데이터의 기준일자를 연도/분기로 변환하여 매칭
        
        return self.df


def main():
    """테스트용 메인 함수"""
    print("="*80)
    print("인구 데이터 처리 모듈 테스트")
    print("="*80)
    
    # 샘플 데이터 생성
    sample_data = {
        '기준연도분기코드': [20214, 20244, 20251],
        '총인구수': [9664310, 9360421, 9360421],
        '남성인구수': [4699535, 4527676, 4527676],
        '여성인구수': [4964775, 4832745, 4832745],
        '10대인구수': [1405211, 1243704, 1243704],
        '20대인구수': [1459649, 1350090, 1350090],
        '30대인구수': [1474993, 1421660, 1421660],
        '총가구수': [4413371, 4453816, 4453816]
    }
    
    df = pd.DataFrame(sample_data)
    processor = PopulationDataProcessor(df)
    
    print("\n인구 추이:")
    print(processor.get_population_trend())
    
    print("\n연령대별 분포:")
    print(processor.get_age_distribution())
    
    print("\n성별 분포:")
    print(processor.get_gender_distribution())
    
    print("\n가구 통계:")
    print(processor.get_household_statistics())


if __name__ == '__main__':
    main()

