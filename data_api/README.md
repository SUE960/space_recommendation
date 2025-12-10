# 서울시 실시간 상권현황데이터 API 연결 가이드

## 개요
서울 열린데이터광장의 실시간 상권현황데이터 API를 연결하여 데이터를 수집하는 모듈입니다.

## API 정보
- **API URL**: `http://openapi.seoul.go.kr:8088/{API_KEY}/xml/citydata_cmrcl/{START}/{END}/{AREA_NM}/`
- **응답 형식**: XML
- **필수 파라미터**: 핫스팟 장소명 (AREA_NM)

## 설치 및 설정

### 1. API 키 발급
서울 열린데이터광장에서 API 키를 발급받으세요:
- https://data.seoul.go.kr/dataList/OA-22385/F/1/datasetView.do

### 2. 설정 파일 수정
`data_api/config.py` 파일을 열어서 API 키를 입력하세요:

```python
SEOUL_OPEN_DATA_API_KEY = "발급받은_API_키"
```

### 3. 조회할 핫스팟 목록 설정
`data_api/fetch_commercial_area_data.py` 파일에서 조회할 핫스팟 목록을 설정하세요:

```python
hotspot_list = [
    "광화문·덕수궁",
    "강남역",
    "홍대입구",
    "명동",
    # 추가 핫스팟을 여기에 입력
]
```

## 사용 방법

### 기본 사용법

```python
from data_api.api_client import SeoulCommercialAreaAPI

# API 클라이언트 생성
client = SeoulCommercialAreaAPI(api_key="YOUR_API_KEY")

# 단일 핫스팟 조회
df = client.get_commercial_area_status("광화문·덕수궁")
print(df)

# 여러 핫스팟 조회
hotspot_list = ["광화문·덕수궁", "강남역", "홍대입구"]
df = client.get_all_data(hotspot_list)

# CSV 저장
client.save_to_csv(df, "outputs/commercial_area_data.csv")
```

### 스크립트 실행

```bash
cd data_api
python fetch_commercial_area_data.py
```

## 데이터 구조

API 응답에서 추출되는 주요 컬럼:

- **지역 정보**: `AREA_NM` (핫스팟장소명), `AREA_CD` (핫스팟코드)
- **지역 상권 현황**: `AREA_CMRCL_LVL`, `AREA_SH_PAYMENT_CNT`, `AREA_SH_PAYMENT_AMT_MIN/MAX`
- **업종 정보**: `RSB_LRG_CTGR` (업종대분류), `RSB_MID_CTGR` (업종중분류)
- **업종 상권 현황**: `RSB_PAYMENT_LVL`, `RSB_SH_PAYMENT_CNT`, `RSB_SH_PAYMENT_AMT_MIN/MAX`
- **가맹점 정보**: `RSB_MCT_CNT` (업종가맹점수), `RSB_MCT_TIME` (업데이트월)
- **인구통계**: `CMRCL_MALE_RATE`, `CMRCL_FEMALE_RATE`, `CMRCL_10_RATE` ~ `CMRCL_60_RATE`
- **소비자 유형**: `CMRCL_PERSONAL_RATE`, `CMRCL_CORPORATION_RATE`
- **업데이트 시간**: `CMRCL_TIME`

## 데이터 처리

`data_api/data_processor.py` 모듈을 사용하여 데이터를 분석할 수 있습니다:

```python
from data_api.data_processor import CommercialAreaDataProcessor

processor = CommercialAreaDataProcessor(df)

# 업종별 핫스팟 조회
result = processor.get_hotspots_by_industry("음식·음료")

# 지역별 업종 통계
stats = processor.get_industry_stats_by_area(area_nm="광화문·덕수궁")

# 인구통계 분석
demographic = processor.get_demographic_analysis(area_cd="POI009")
```

## 주의사항

1. API 호출 제한: API 호출 간 0.5초 지연이 자동으로 설정되어 있습니다.
2. 핫스팟 장소명: 정확한 핫스팟 장소명을 입력해야 합니다. (예: "광화문·덕수궁")
3. 데이터 범위: 한 번에 최대 5개까지 조회 가능합니다.

## 문제 해결

### API 키 오류
- `config.py`에서 API 키가 올바르게 설정되었는지 확인하세요.

### 데이터 없음
- 핫스팟 장소명이 정확한지 확인하세요.
- API 서버 상태를 확인하세요.

### XML 파싱 오류
- API 응답 형식이 변경되었을 수 있습니다. `api_client.py`의 `_parse_xml_response` 메서드를 확인하세요.

