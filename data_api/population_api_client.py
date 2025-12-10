#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 인구 데이터 API 클라이언트
인구 및 가구 통계 데이터를 조회합니다.
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import time
import urllib.parse


class SeoulPopulationAPI:
    """서울시 인구 데이터 API 클라이언트"""
    
    def __init__(self, api_key: str = None):
        """
        API 클라이언트 초기화
        
        Args:
            api_key: API 인증 키 (서울 열린데이터광장에서 발급)
        """
        self.api_key = api_key or "YOUR_API_KEY_HERE"
        self.base_url = "http://openapi.seoul.go.kr:8088"
        self.service_name = "VwsmMegaRepopW"  # 인구 데이터 서비스명
        
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
            result_code = root.find('.//CODE')
            result_msg = root.find('.//MESSAGE')
            
            if result_code is not None and result_code.text != 'INFO-000':
                error_msg = result_msg.text if result_msg is not None else '알 수 없는 오류'
                raise ValueError(f"API 오류: {error_msg} (코드: {result_code.text})")
            
            # row 데이터 추출
            rows = root.findall('.//row')
            data_list = []
            
            for row in rows:
                row_data = {}
                for child in row:
                    tag = child.tag
                    text = child.text
                    
                    # 숫자 필드는 int로 변환
                    if text and text.strip():
                        if any(keyword in tag for keyword in ['_CO', '_CD']):
                            try:
                                row_data[tag] = int(text)
                            except ValueError:
                                row_data[tag] = text
                        else:
                            row_data[tag] = text
                    else:
                        row_data[tag] = None
                
                data_list.append(row_data)
            
            return data_list
        
        except ET.ParseError as e:
            print(f"XML 파싱 오류: {e}")
            return []
    
    def _make_request(self, start: int = 1, end: int = 1000, 
                     stdr_yyqu_cd: str = None, mega_cd: str = None) -> List[Dict]:
        """
        API 요청 실행
        
        Args:
            start: 시작 인덱스
            end: 종료 인덱스
            stdr_yyqu_cd: 기준 연도분기 코드 (선택, 예: "20214" = 2021년 4분기)
            mega_cd: 광역시도 코드 (선택, "11" = 서울시)
        
        Returns:
            파싱된 데이터 리스트
        """
        # API URL 구성: http://openapi.seoul.go.kr:8088/{API_KEY}/xml/{SERVICE_NAME}/{START}/{END}/
        url = f"{self.base_url}/{self.api_key}/xml/{self.service_name}/{start}/{end}/"
        
        # 파라미터 추가 (필요한 경우)
        params = {}
        if stdr_yyqu_cd:
            params['STDR_YYQU_CD'] = stdr_yyqu_cd
        if mega_cd:
            params['MEGA_CD'] = mega_cd
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # XML 응답 파싱
            return self._parse_xml_response(response.text)
        
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"응답 내용: {e.response.text[:500]}")
            raise
    
    def get_population_data(self, 
                           stdr_yyqu_cd: str = None,
                           mega_cd: str = "11",
                           start: int = 1,
                           end: int = 1000) -> pd.DataFrame:
        """
        인구 데이터 조회
        
        Args:
            stdr_yyqu_cd: 기준 연도분기 코드 (선택, 예: "20214" = 2021년 4분기)
            mega_cd: 광역시도 코드 (기본값: "11" = 서울시)
            start: 시작 인덱스
            end: 종료 인덱스
        
        Returns:
            인구 데이터프레임
        """
        data = self._make_request(start=start, end=end, 
                                 stdr_yyqu_cd=stdr_yyqu_cd, 
                                 mega_cd=mega_cd)
        
        if not data:
            return pd.DataFrame()
        
        # DataFrame으로 변환
        df = pd.DataFrame(data)
        
        # 컬럼명 한글 변환 (선택사항)
        column_mapping = {
            'STDR_YYQU_CD': '기준연도분기코드',
            'MEGA_CD': '광역시도코드',
            'MEGA_CD_NM': '광역시도명',
            'TOT_REPOP_CO': '총인구수',
            'ML_REPOP_CO': '남성인구수',
            'FML_REPOP_CO': '여성인구수',
            'AGRDE_10_REPOP_CO': '10대인구수',
            'AGRDE_20_REPOP_CO': '20대인구수',
            'AGRDE_30_REPOP_CO': '30대인구수',
            'AGRDE_40_REPOP_CO': '40대인구수',
            'AGRDE_50_REPOP_CO': '50대인구수',
            'AGRDE_60_ABOVE_REPOP_CO': '60대이상인구수',
            'MAG_10_REPOP_CO': '남성10대인구수',
            'MAG_20_REPOP_CO': '남성20대인구수',
            'MAG_30_REPOP_CO': '남성30대인구수',
            'MAG_40_REPOP_CO': '남성40대인구수',
            'MAG_50_REPOP_CO': '남성50대인구수',
            'MAG_60_ABOVE_REPOP_CO': '남성60대이상인구수',
            'FAG_10_REPOP_CO': '여성10대인구수',
            'FAG_20_REPOP_CO': '여성20대인구수',
            'FAG_30_REPOP_CO': '여성30대인구수',
            'FAG_40_REPOP_CO': '여성40대인구수',
            'FAG_50_REPOP_CO': '여성50대인구수',
            'FAG_60_ABOVE_REPOP_CO': '여성60대이상인구수',
            'TOT_HSHLD_CO': '총가구수',
            'APT_HSHLD_CO': '아파트가구수',
            'NON_APT_HSHLD_CO': '비아파트가구수'
        }
        
        # 컬럼명 매핑 (존재하는 컬럼만)
        df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns}, 
                 inplace=True)
        
        return df
    
    def get_all_population_data(self, 
                                stdr_yyqu_cd_list: List[str] = None,
                                mega_cd: str = "11") -> pd.DataFrame:
        """
        모든 인구 데이터 조회 (페이지네이션 처리)
        
        Args:
            stdr_yyqu_cd_list: 조회할 기준 연도분기 코드 리스트 (None이면 전체)
            mega_cd: 광역시도 코드 (기본값: "11" = 서울시)
        
        Returns:
            전체 인구 데이터프레임
        """
        all_data = []
        start = 1
        page_size = 1000
        
        if stdr_yyqu_cd_list:
            # 특정 연도분기만 조회
            for stdr_yyqu_cd in stdr_yyqu_cd_list:
                print(f"데이터 수집 중... 기준연도분기: {stdr_yyqu_cd}")
                df = self.get_population_data(stdr_yyqu_cd=stdr_yyqu_cd, 
                                              mega_cd=mega_cd,
                                              start=start, 
                                              end=start + page_size - 1)
                if len(df) > 0:
                    all_data.append(df)
                time.sleep(0.5)
        else:
            # 전체 데이터 조회
            while True:
                print(f"데이터 수집 중... {start}~{start + page_size - 1}")
                df = self.get_population_data(mega_cd=mega_cd,
                                             start=start, 
                                             end=start + page_size - 1)
                
                if len(df) == 0:
                    break
                
                all_data.append(df)
                
                # 다음 페이지가 없으면 종료
                if len(df) < page_size:
                    break
                
                start += page_size
                time.sleep(0.5)  # API 호출 제한 방지
        
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
    print("서울시 인구 데이터 API 클라이언트 테스트")
    print("="*80)
    
    # TODO: 실제 API 키를 입력하세요
    api_key = "YOUR_API_KEY_HERE"
    
    # API 클라이언트 생성
    client = SeoulPopulationAPI(api_key=api_key)
    
    # 데이터 조회 예시
    try:
        print("\n전체 인구 데이터 조회 중...")
        df = client.get_all_population_data(mega_cd="11")  # 서울시
        
        print(f"\n조회된 데이터: {len(df)}행")
        print(f"\n컬럼: {list(df.columns)}")
        print(f"\n샘플 데이터:")
        print(df.head())
        
        # 연도분기별 통계
        if '기준연도분기코드' in df.columns:
            print("\n" + "="*80)
            print("연도분기별 인구 통계")
            print("="*80)
            for _, row in df.iterrows():
                yyyyq = str(row['기준연도분기코드'])
                year = yyyyq[:4]
                quarter = yyyyq[4]
                print(f"\n{year}년 {quarter}분기:")
                if '총인구수' in df.columns:
                    print(f"  총인구수: {row['총인구수']:,}명")
                if '남성인구수' in df.columns and '여성인구수' in df.columns:
                    print(f"  남성: {row['남성인구수']:,}명, 여성: {row['여성인구수']:,}명")
                if '총가구수' in df.columns:
                    print(f"  총가구수: {row['총가구수']:,}가구")
        
        # CSV 저장
        output_file = 'outputs/seoul_population_data.csv'
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

