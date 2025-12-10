#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실시간 상권현황데이터 처리 및 분석 모듈
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class CommercialAreaDataProcessor:
    """실시간 상권현황데이터 처리 클래스"""
    
    def __init__(self, df: pd.DataFrame):
        """
        데이터프로세서 초기화
        
        Args:
            df: 상권현황 데이터프레임
        """
        self.df = df.copy()
        self._preprocess()
    
    def _preprocess(self):
        """데이터 전처리"""
        # 컬럼명 정리 (이미지에서 본 컬럼명 기준)
        column_mapping = {
            # 핫스팟 관련
            'AREA_NM': '핫스팟장소명',
            'AREA_CD': '핫스팟코드',
            'LIVE_CMRCL_STTS': '실시간상권현황',
            'AREA_CMRCL_LVL': '장소실시간상권현황',
            'AREA_SH_PAYMENT_CNT': '장소신한카드결제건수',
            'AREA_SH_PAYMENT_AMT_MIN': '장소신한카드결제금액최소',
            'AREA_SH_PAYMENT_AMT_MAX': '장소신한카드결제금액최대',
            
            # 업종 관련
            'RSB_LRG_CTGR': '업종대분류',
            'RSB_MID_CTGR': '업종중분류',
            'RSB_PAYMENT_LVL': '업종실시간상권현황',
            'RSB_SH_PAYMENT_CNT': '업종신한카드결제건수',
            'RSB_SH_PAYMENT_AMT_MIN': '업종신한카드결제금액최소',
            'RSB_SH_PAYMENT_AMT_MAX': '업종신한카드결제금액최대',
            
            # 가맹점 관련
            'RSB_MCT_CNT': '업종가맹점수',
            'RSB_MCT_TIME': '업종가맹점수업데이트월',
            
            # 인구통계 관련
            'CMRCL_MALE_RATE': '남성소비비율',
            'CMRCL_FEMALE_RATE': '여성소비비율',
            'CMRCL_10_RATE': '10대이하소비비율',
            'CMRCL_20_RATE': '20대소비비율',
            'CMRCL_30_RATE': '30대소비비율',
            'CMRCL_40_RATE': '40대소비비율',
            'CMRCL_50_RATE': '50대소비비율',
            'CMRCL_60_RATE': '60대이상소비비율',
            'CMRCL_PERSONAL_RATE': '개인소비비율',
            'CMRCL_CORPORATION_RATE': '법인소비비율',
            'CMRCL_TIME': '실시간상권데이터업데이트시간'
        }
        
        # 컬럼명 매핑 (존재하는 컬럼만)
        for old_name, new_name in column_mapping.items():
            if old_name in self.df.columns:
                self.df.rename(columns={old_name: new_name}, inplace=True)
        
        # 날짜/시간 컬럼 변환
        if '실시간상권데이터업데이트시간' in self.df.columns:
            try:
                self.df['업데이트시간'] = pd.to_datetime(
                    self.df['실시간상권데이터업데이트시간'],
                    errors='coerce'
                )
            except:
                pass
        
        if '업종가맹점수업데이트월' in self.df.columns:
            try:
                self.df['업데이트월'] = pd.to_datetime(
                    self.df['업종가맹점수업데이트월'],
                    format='%Y%m',
                    errors='coerce'
                )
            except:
                pass
    
    def get_hotspots_by_industry(self, industry: str) -> pd.DataFrame:
        """
        업종별 핫스팟 조회
        
        Args:
            industry: 업종 대분류명
        
        Returns:
            해당 업종의 핫스팟 데이터프레임
        """
        if '업종대분류' not in self.df.columns:
            raise ValueError("업종대분류 컬럼이 없습니다.")
        
        result = self.df[self.df['업종대분류'] == industry].copy()
        return result.sort_values('장소신한카드결제건수', ascending=False)
    
    def get_industry_stats_by_area(self, area_cd: str = None, area_nm: str = None) -> pd.DataFrame:
        """
        지역별 업종 통계
        
        Args:
            area_cd: 핫스팟 코드
            area_nm: 핫스팟 장소명
        
        Returns:
            지역별 업종 통계 데이터프레임
        """
        if area_cd:
            filtered = self.df[self.df['핫스팟코드'] == area_cd].copy()
        elif area_nm:
            filtered = self.df[self.df['핫스팟장소명'] == area_nm].copy()
        else:
            filtered = self.df.copy()
        
        if '업종대분류' not in filtered.columns:
            return pd.DataFrame()
        
        stats = filtered.groupby('업종대분류').agg({
            '업종신한카드결제건수': 'sum',
            '업종신한카드결제금액최소': 'sum',
            '업종신한카드결제금액최대': 'sum',
            '업종가맹점수': 'sum'
        }).reset_index()
        
        stats = stats.sort_values('업종신한카드결제건수', ascending=False)
        return stats
    
    def get_demographic_analysis(self, area_cd: str = None) -> Dict:
        """
        인구통계 분석
        
        Args:
            area_cd: 핫스팟 코드
        
        Returns:
            인구통계 분석 결과 딕셔너리
        """
        if area_cd:
            filtered = self.df[self.df['핫스팟코드'] == area_cd].copy()
        else:
            filtered = self.df.copy()
        
        result = {}
        
        # 성별 비율
        if '남성소비비율' in filtered.columns and '여성소비비율' in filtered.columns:
            result['성별'] = {
                '남성': filtered['남성소비비율'].mean() if len(filtered) > 0 else 0,
                '여성': filtered['여성소비비율'].mean() if len(filtered) > 0 else 0
            }
        
        # 연령대별 비율
        age_columns = [
            '10대이하소비비율', '20대소비비율', '30대소비비율',
            '40대소비비율', '50대소비비율', '60대이상소비비율'
        ]
        age_data = {}
        for col in age_columns:
            if col in filtered.columns:
                age_key = col.replace('소비비율', '')
                age_data[age_key] = filtered[col].mean() if len(filtered) > 0 else 0
        result['연령대'] = age_data
        
        # 개인/법인 비율
        if '개인소비비율' in filtered.columns and '법인소비비율' in filtered.columns:
            result['소비자유형'] = {
                '개인': filtered['개인소비비율'].mean() if len(filtered) > 0 else 0,
                '법인': filtered['법인소비비율'].mean() if len(filtered) > 0 else 0
            }
        
        return result
    
    def merge_with_card_data(self, card_df: pd.DataFrame, 
                            merge_key: str = '가맹점주소시군구') -> pd.DataFrame:
        """
        카드 데이터와 병합
        
        Args:
            card_df: 카드 소비 데이터프레임
            merge_key: 병합 키 컬럼명
        
        Returns:
            병합된 데이터프레임
        """
        # TODO: 실제 병합 로직 구현 필요
        # 핫스팟 코드나 장소명을 기준으로 카드 데이터와 매칭
        # 예: 핫스팟 장소명에서 구 정보 추출하여 카드 데이터의 가맹점주소시군구와 매칭
        
        return pd.merge(
            self.df,
            card_df,
            left_on='핫스팟장소명',  # 실제 매칭 키는 데이터 구조에 따라 수정 필요
            right_on=merge_key,
            how='inner'
        )


def main():
    """테스트용 메인 함수"""
    print("="*80)
    print("실시간 상권현황데이터 처리 모듈 테스트")
    print("="*80)
    
    # 샘플 데이터 생성 (실제로는 API에서 가져온 데이터 사용)
    sample_data = {
        '핫스팟코드': ['A001', 'A002', 'A003'],
        '핫스팟장소명': ['강남역', '홍대입구', '명동'],
        '업종대분류': ['한식', '카페', '쇼핑'],
        '업종신한카드결제건수': [1000, 800, 1200],
        '남성소비비율': [0.6, 0.4, 0.5],
        '여성소비비율': [0.4, 0.6, 0.5]
    }
    
    df = pd.DataFrame(sample_data)
    processor = CommercialAreaDataProcessor(df)
    
    print("\n업종별 핫스팟:")
    print(processor.get_hotspots_by_industry('한식'))
    
    print("\n지역별 업종 통계:")
    print(processor.get_industry_stats_by_area(area_nm='강남역'))
    
    print("\n인구통계 분석:")
    print(processor.get_demographic_analysis())


if __name__ == '__main__':
    main()

