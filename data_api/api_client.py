#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울 열린데이터광장 실시간 상권현황데이터 API 클라이언트
API URL: http://openapi.seoul.go.kr:8088/{API_KEY}/xml/citydata_cmrcl/{START}/{END}/{AREA_NM}/
"""

import requests
import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import time
import urllib.parse


class SeoulCommercialAreaAPI:
    """서울시 실시간 상권현황데이터 API 클라이언트"""
    
    def __init__(self, api_key: str = None):
        """
        API 클라이언트 초기화
        
        Args:
            api_key: API 인증 키 (서울 열린데이터광장에서 발급)
        """
        self.api_key = api_key or "YOUR_API_KEY_HERE"
        self.base_url = "http://openapi.seoul.go.kr:8088"
        self.service_name = "citydata_cmrcl"
        
        # API 요청을 위한 기본 헤더
        self.headers = {
            'Accept': 'application/xml, application/json'
        }
        
        # 세션 생성 (연결 재사용)
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _parse_xml_response(self, xml_text: str) -> List[Dict]:
        """
        XML 응답을 파싱하여 딕셔너리 리스트로 변환
        
        Args:
            xml_text: XML 응답 텍스트
        
        Returns:
            파싱된 데이터 리스트
        """
        try:
            root = ET.fromstring(xml_text)
            
            # 결과 코드 확인
            result_code = root.find('.//resultCode')
            result_msg = root.find('.//resultMsg')
            
            if result_code is not None and result_code.text != 'INFO-000':
                error_msg = result_msg.text if result_msg is not None else '알 수 없는 오류'
                raise ValueError(f"API 오류: {error_msg} (코드: {result_code.text})")
            
            # LIVE_CMRCL_STTS 데이터 추출
            live_stts = root.find('.//LIVE_CMRCL_STTS')
            if live_stts is None:
                return []
            
            # 기본 지역 정보
            area_nm = root.find('.//AREA_NM')
            area_cd = root.find('.//AREA_CD')
            
            area_name = area_nm.text if area_nm is not None else None
            area_code = area_cd.text if area_cd is not None else None
            
            # 지역 레벨 데이터
            area_cmrcl_lvl = live_stts.find('AREA_CMRCL_LVL')
            area_sh_payment_cnt = live_stts.find('AREA_SH_PAYMENT_CNT')
            area_sh_payment_amt_min = live_stts.find('AREA_SH_PAYMENT_AMT_MIN')
            area_sh_payment_amt_max = live_stts.find('AREA_SH_PAYMENT_AMT_MAX')
            
            # 인구통계 데이터
            male_rate = live_stts.find('CMRCL_MALE_RATE')
            female_rate = live_stts.find('CMRCL_FEMALE_RATE')
            age_10_rate = live_stts.find('CMRCL_10_RATE')
            age_20_rate = live_stts.find('CMRCL_20_RATE')
            age_30_rate = live_stts.find('CMRCL_30_RATE')
            age_40_rate = live_stts.find('CMRCL_40_RATE')
            age_50_rate = live_stts.find('CMRCL_50_RATE')
            age_60_rate = live_stts.find('CMRCL_60_RATE')
            personal_rate = live_stts.find('CMRCL_PERSONAL_RATE')
            corporation_rate = live_stts.find('CMRCL_CORPORATION_RATE')
            cmrcl_time = live_stts.find('CMRCL_TIME')
            
            # 업종별 데이터 (CMRCL_RSB)
            cmrcl_rsb = live_stts.find('CMRCL_RSB')
            industry_data = []
            
            if cmrcl_rsb is not None:
                for rsb in cmrcl_rsb.findall('CMRCL_RSB'):
                    industry_item = {
                        'AREA_NM': area_name,
                        'AREA_CD': area_code,
                        'AREA_CMRCL_LVL': area_cmrcl_lvl.text if area_cmrcl_lvl is not None else None,
                        'AREA_SH_PAYMENT_CNT': int(area_sh_payment_cnt.text) if area_sh_payment_cnt is not None and area_sh_payment_cnt.text else None,
                        'AREA_SH_PAYMENT_AMT_MIN': int(area_sh_payment_amt_min.text) if area_sh_payment_amt_min is not None and area_sh_payment_amt_min.text else None,
                        'AREA_SH_PAYMENT_AMT_MAX': int(area_sh_payment_amt_max.text) if area_sh_payment_amt_max is not None and area_sh_payment_amt_max.text else None,
                        'RSB_LRG_CTGR': rsb.find('RSB_LRG_CTGR').text if rsb.find('RSB_LRG_CTGR') is not None else None,
                        'RSB_MID_CTGR': rsb.find('RSB_MID_CTGR').text if rsb.find('RSB_MID_CTGR') is not None else None,
                        'RSB_PAYMENT_LVL': rsb.find('RSB_PAYMENT_LVL').text if rsb.find('RSB_PAYMENT_LVL') is not None else None,
                        'RSB_SH_PAYMENT_CNT': int(rsb.find('RSB_SH_PAYMENT_CNT').text) if rsb.find('RSB_SH_PAYMENT_CNT') is not None and rsb.find('RSB_SH_PAYMENT_CNT').text else None,
                        'RSB_SH_PAYMENT_AMT_MIN': int(rsb.find('RSB_SH_PAYMENT_AMT_MIN').text) if rsb.find('RSB_SH_PAYMENT_AMT_MIN') is not None and rsb.find('RSB_SH_PAYMENT_AMT_MIN').text else None,
                        'RSB_SH_PAYMENT_AMT_MAX': int(rsb.find('RSB_SH_PAYMENT_AMT_MAX').text) if rsb.find('RSB_SH_PAYMENT_AMT_MAX') is not None and rsb.find('RSB_SH_PAYMENT_AMT_MAX').text else None,
                        'RSB_MCT_CNT': int(rsb.find('RSB_MCT_CNT').text) if rsb.find('RSB_MCT_CNT') is not None and rsb.find('RSB_MCT_CNT').text else None,
                        'RSB_MCT_TIME': rsb.find('RSB_MCT_TIME').text if rsb.find('RSB_MCT_TIME') is not None else None,
                        'CMRCL_MALE_RATE': float(male_rate.text) if male_rate is not None and male_rate.text else None,
                        'CMRCL_FEMALE_RATE': float(female_rate.text) if female_rate is not None and female_rate.text else None,
                        'CMRCL_10_RATE': float(age_10_rate.text) if age_10_rate is not None and age_10_rate.text else None,
                        'CMRCL_20_RATE': float(age_20_rate.text) if age_20_rate is not None and age_20_rate.text else None,
                        'CMRCL_30_RATE': float(age_30_rate.text) if age_30_rate is not None and age_30_rate.text else None,
                        'CMRCL_40_RATE': float(age_40_rate.text) if age_40_rate is not None and age_40_rate.text else None,
                        'CMRCL_50_RATE': float(age_50_rate.text) if age_50_rate is not None and age_50_rate.text else None,
                        'CMRCL_60_RATE': float(age_60_rate.text) if age_60_rate is not None and age_60_rate.text else None,
                        'CMRCL_PERSONAL_RATE': float(personal_rate.text) if personal_rate is not None and personal_rate.text else None,
                        'CMRCL_CORPORATION_RATE': float(corporation_rate.text) if corporation_rate is not None and corporation_rate.text else None,
                        'CMRCL_TIME': cmrcl_time.text if cmrcl_time is not None else None
                    }
                    industry_data.append(industry_item)
            
            return industry_data
        
        except ET.ParseError as e:
            print(f"XML 파싱 오류: {e}")
            return []
    
    def _make_request(self, area_nm: str, start: int = 1, end: int = 5) -> List[Dict]:
        """
        API 요청 실행
        
        Args:
            area_nm: 핫스팟 장소명 (필수)
            start: 시작 인덱스
            end: 종료 인덱스
        
        Returns:
            파싱된 데이터 리스트
        """
        # URL 인코딩
        area_nm_encoded = urllib.parse.quote(area_nm)
        
        # API URL 구성: http://openapi.seoul.go.kr:8088/{API_KEY}/xml/citydata_cmrcl/{START}/{END}/{AREA_NM}/
        url = f"{self.base_url}/{self.api_key}/xml/{self.service_name}/{start}/{end}/{area_nm_encoded}/"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # XML 응답 파싱
            return self._parse_xml_response(response.text)
        
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"응답 내용: {e.response.text[:500]}")
            raise
    
    def get_commercial_area_status(self, area_nm: str) -> pd.DataFrame:
        """
        실시간 상권현황데이터 조회
        
        Args:
            area_nm: 핫스팟 장소명 (필수) - 예: "광화문·덕수궁", "강남역" 등
        
        Returns:
            상권현황 데이터프레임
        """
        if not area_nm:
            raise ValueError("핫스팟 장소명(area_nm)은 필수입니다.")
        
        # API 요청 (한 번에 최대 5개까지 조회 가능)
        data = self._make_request(area_nm, start=1, end=5)
        
        if not data:
            return pd.DataFrame()
        
        # DataFrame으로 변환
        df = pd.DataFrame(data)
        return df
    
    def get_all_data(self, area_nm_list: List[str]) -> pd.DataFrame:
        """
        여러 핫스팟의 상권현황데이터 조회
        
        Args:
            area_nm_list: 조회할 핫스팟 장소명 리스트
        
        Returns:
            전체 상권현황 데이터프레임
        """
        if not area_nm_list:
            raise ValueError("핫스팟 장소명 리스트가 필요합니다.")
        
        all_data = []
        
        for idx, area_nm in enumerate(area_nm_list, 1):
            print(f"데이터 수집 중... ({idx}/{len(area_nm_list)}) {area_nm}")
            
            try:
                df = self.get_commercial_area_status(area_nm)
                if len(df) > 0:
                    all_data.append(df)
                    print(f"  ✓ {len(df)}개 업종 데이터 수집 완료")
                else:
                    print(f"  ⚠️  데이터 없음")
            except Exception as e:
                print(f"  ❌ 오류 발생: {e}")
                continue
            
            # API 호출 제한 방지
            time.sleep(0.5)
        
        if all_data:
            result_df = pd.concat(all_data, ignore_index=True)
            return result_df
        else:
            return pd.DataFrame()
    
    def save_to_csv(self, df: pd.DataFrame, filepath: str):
        """
        데이터프레임을 CSV 파일로 저장
        
        Args:
            df: 저장할 데이터프레임
            filepath: 저장할 파일 경로
        """
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"✓ 데이터 저장 완료: {filepath} ({len(df):,}행)")


def main():
    """테스트용 메인 함수"""
    print("="*80)
    print("서울시 실시간 상권현황데이터 API 클라이언트 테스트")
    print("="*80)
    
    # TODO: 실제 API 키를 입력하세요
    api_key = "YOUR_API_KEY_HERE"
    
    # API 클라이언트 생성
    client = SeoulCommercialAreaAPI(api_key=api_key)
    
    # 데이터 조회 예시 (광화문·덕수궁)
    try:
        area_name = "광화문·덕수궁"
        print(f"\n핫스팟 조회: {area_name}")
        df = client.get_commercial_area_status(area_name)
        
        print(f"\n조회된 데이터: {len(df)}행")
        print(f"\n컬럼: {list(df.columns)}")
        print(f"\n샘플 데이터:")
        print(df.head())
        
        # CSV 저장
        output_file = 'outputs/seoul_commercial_area_status.csv'
        import os
        os.makedirs('outputs', exist_ok=True)
        client.save_to_csv(df, output_file)
    
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
        print("\nAPI 키를 확인하고 다시 시도하세요.")


if __name__ == '__main__':
    main()

