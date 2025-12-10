#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 실시간 상권현황데이터 수집 스크립트
API에서 데이터를 가져와서 저장합니다.
"""

import os
import sys
from datetime import datetime

# 현재 디렉토리를 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from api_client import SeoulCommercialAreaAPI
from data_processor import CommercialAreaDataProcessor
from config import (
    SEOUL_OPEN_DATA_API_KEY,
    OUTPUT_DIR,
    COMMERCIAL_AREA_DATA_FILE
)


def main():
    """메인 실행 함수"""
    print("="*80)
    print("서울시 실시간 상권현황데이터 수집")
    print("="*80)
    
    # API 키 확인
    if SEOUL_OPEN_DATA_API_KEY == "YOUR_API_KEY_HERE":
        print("\n⚠️  경고: API 키가 설정되지 않았습니다!")
        print("data_api/config.py 파일에서 SEOUL_OPEN_DATA_API_KEY를 설정하세요.")
        print("\n서울 열린데이터광장에서 API 키를 발급받으세요:")
        print("https://data.seoul.go.kr/dataList/OA-22385/F/1/datasetView.do")
        return
    
    # 출력 디렉토리 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # API 클라이언트 생성
    print("\nAPI 클라이언트 초기화 중...")
    client = SeoulCommercialAreaAPI(api_key=SEOUL_OPEN_DATA_API_KEY)
    
    # 데이터 수집
    print("\n데이터 수집 시작...")
    print("\n⚠️  참고: 이 API는 핫스팟 장소명을 필수로 입력해야 합니다.")
    print("예시: '광화문·덕수궁', '강남역', '홍대입구' 등")
    
    # 조회할 핫스팟 리스트 (사용자가 수정 가능)
    # TODO: 실제 조회할 핫스팟 목록을 입력하세요
    hotspot_list = [
        "광화문·덕수궁",
        # "강남역",
        # "홍대입구",
        # "명동",
        # 추가 핫스팟을 여기에 입력하세요
    ]
    
    if not hotspot_list or hotspot_list == ["광화문·덕수궁"]:
        print("\n⚠️  경고: 기본 테스트 핫스팟만 조회합니다.")
        print("fetch_commercial_area_data.py 파일에서 hotspot_list를 수정하세요.")
    
    try:
        # 여러 핫스팟 데이터 조회
        df = client.get_all_data(hotspot_list)
        
        if len(df) == 0:
            print("\n⚠️  조회된 데이터가 없습니다.")
            print("API 키와 URL을 확인하세요.")
            return
        
        print(f"\n✓ 데이터 수집 완료: {len(df):,}행")
        print(f"\n컬럼 목록:")
        for col in df.columns:
            print(f"  - {col}")
        
        # 데이터 전처리
        print("\n데이터 전처리 중...")
        processor = CommercialAreaDataProcessor(df)
        
        # CSV 저장
        output_file = os.path.join(OUTPUT_DIR, COMMERCIAL_AREA_DATA_FILE)
        client.save_to_csv(df, output_file)
        
        # 통계 정보 출력
        print("\n" + "="*80)
        print("데이터 통계")
        print("="*80)
        
        if '업종대분류' in df.columns:
            industry_counts = df['업종대분류'].value_counts()
            print(f"\n업종별 데이터 수:")
            for industry, count in industry_counts.head(10).items():
                print(f"  - {industry}: {count:,}건")
        
        if '핫스팟장소명' in df.columns:
            hotspot_counts = df['핫스팟장소명'].nunique()
            print(f"\n고유 핫스팟 수: {hotspot_counts:,}개")
        
        print("\n" + "="*80)
        print("데이터 수집 완료!")
        print("="*80)
        print(f"\n저장 위치: {output_file}")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        print("\nAPI 연결 정보를 확인하고 다시 시도하세요.")


if __name__ == '__main__':
    main()

