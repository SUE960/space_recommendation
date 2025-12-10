"""
데이터 API 연결 모듈
두 번째 데이터 소스와의 API 통신을 담당합니다.
"""

from .api_client import SeoulCommercialAreaAPI
from .population_api_client import SeoulPopulationAPI
from .data_processor import CommercialAreaDataProcessor

__all__ = ['SeoulCommercialAreaAPI', 'SeoulPopulationAPI', 'CommercialAreaDataProcessor']

