#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 설정 파일
실제 API 키와 URL을 여기에 입력하세요.
"""

# 서울 열린데이터광장 API 설정
# API URL 형식: http://openapi.seoul.go.kr:8088/{API_KEY}/xml/citydata_cmrcl/{START}/{END}/{AREA_NM}/
SEOUL_OPEN_DATA_API_KEY = "6863727948726b6436345862527950"  # TODO: 실제 API 키 입력

# API 요청 설정
API_REQUEST_TIMEOUT = 30  # 초
API_REQUEST_DELAY = 0.5  # API 호출 간 지연 시간 (초)

# 데이터 저장 경로
OUTPUT_DIR = "outputs"
COMMERCIAL_AREA_DATA_FILE = "seoul_commercial_area_status.csv"

