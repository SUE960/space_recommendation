#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 인구 데이터 수집 스크립트
API에서 인구 및 가구 통계 데이터를 가져와서 저장합니다.
"""

import os
import sys
from datetime import datetime
from population_api_client import SeoulPopulationAPI
from config import (
    SEOUL_OPEN_DATA_API_KEY,
    OUTPUT_DIR
)


def main():
    """메인 실행 함수"""
    print("="*80)
    print("서울시 인구 데이터 수집")
    print("="*80)
    
    # API 키 확인
    if SEOUL_OPEN_DATA_API_KEY == "YOUR_API_KEY_HERE":
        print("\n⚠️  경고: API 키가 설정되지 않았습니다!")
        print("data_api/config.py 파일에서 SEOUL_OPEN_DATA_API_KEY를 설정하세요.")
        return
    
    # 출력 디렉토리 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # API 클라이언트 생성
    print("\nAPI 클라이언트 초기화 중...")
    client = SeoulPopulationAPI(api_key=SEOUL_OPEN_DATA_API_KEY)
    
    # 데이터 수집
    print("\n데이터 수집 시작...")
    try:
        # 전체 인구 데이터 조회 (서울시)
        df = client.get_all_population_data(mega_cd="11")
        
        if len(df) == 0:
            print("\n⚠️  조회된 데이터가 없습니다.")
            print("API 키와 URL을 확인하세요.")
            return
        
        print(f"\n✓ 데이터 수집 완료: {len(df):,}행")
        print(f"\n컬럼 목록:")
        for col in df.columns:
            print(f"  - {col}")
        
        # 통계 정보 출력
        print("\n" + "="*80)
        print("데이터 통계")
        print("="*80)
        
        if '기준연도분기코드' in df.columns:
            print(f"\n기준연도분기별 데이터 수:")
            period_counts = df['기준연도분기코드'].value_counts().sort_index()
            for period, count in period_counts.items():
                yyyyq = str(period)
                year = yyyyq[:4]
                quarter = yyyyq[4]
                print(f"  - {year}년 {quarter}분기: {count}건")
        
        if '총인구수' in df.columns:
            print(f"\n인구수 통계:")
            print(f"  최소: {df['총인구수'].min():,}명")
            print(f"  최대: {df['총인구수'].max():,}명")
            print(f"  평균: {df['총인구수'].mean():,.0f}명")
        
        if '총가구수' in df.columns:
            print(f"\n가구수 통계:")
            print(f"  최소: {df['총가구수'].min():,}가구")
            print(f"  최대: {df['총가구수'].max():,}가구")
            print(f"  평균: {df['총가구수'].mean():,.0f}가구")
        
        # CSV 저장
        output_file = os.path.join(OUTPUT_DIR, "seoul_population_data.csv")
        client.save_to_csv(df, output_file)
        
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

