# 이중 매칭 알고리즘 API

## 개요
서울시 카드 데이터와 실시간 상권 활성화 데이터를 활용한 **이중 매칭 알고리즘** 기반 지역 추천 API입니다.

## 알고리즘 구조

### 6단계 추천 프로세스

```
01. 사용자 입력
02. 정적 프로필 매칭 (14개 세그먼트)
03. 실시간 지역 프로필 로드 (73개 핫스팟)
04. 이중 매칭 점수 계산
    ├─ 정적 매칭 (50%)
    └─ 실시간 매칭 (50%)
05. 최종 추천 점수 산출
06. 추천 결과 반환
```

### 정적 프로필 매칭 (50%)
- 업종 선호도 매칭 (40%)
- 인구통계 매칭 (30%)
- 소비 수준 매칭 (20%)
- 시간대 패턴 매칭 (10%)

### 실시간 프로필 매칭 (50%)
- 사용자 선호 업종 매칭 (35%)
- 실시간 종합 점수 (30%)
- 특화도 매칭 (20%)
- 시간대 적합도 (15%)

## API 엔드포인트

### POST /api/recommend
사용자 입력 기반 지역 추천

**요청:**
```json
{
  "age": 28,
  "gender": "남",
  "income_level": "중",
  "preferred_industries": ["한식", "카페", "영화관"],
  "time_period": "저녁",
  "is_weekend": false,
  "preference_type": "활발한"
}
```

**응답:**
```json
{
  "recommendations": [
    {
      "rank": 1,
      "region": "홍대 관광특구",
      "final_score": 85.32,
      "static_score": 82.5,
      "realtime_score": 88.2,
      "static_details": {
        "industry_match": 60.0,
        "demographic_match": 81.24,
        "spending_match": 59.35,
        "time_match": 65.0
      },
      "realtime_details": {
        "user_industry_match": 66.67,
        "comprehensive_score": 76.27,
        "specialization_match": 99.6,
        "time_match": 85.0
      },
      "comprehensive_score": 85.5,
      "grade": "매우 활성화 (Hot Zone)",
      "specialized_industries": ["음식·음료", "여가·오락"],
      "reasons": [
        "선호하시는 한식, 카페 업종이 특화된 지역",
        "20대 남성에게 인기",
        "현재 매우 활성화 (Hot Zone)",
        "저녁 시간대에 적합"
      ]
    }
  ],
  "user_profile": {
    "matched_segment": "20s_male",
    "segment_description": "20_29세 남",
    "top_segment_industries": ["기타요식", "편의점", "영화/공연"]
  }
}
```

### GET /api/regions
실시간 지역 정보 조회 (73개)

### GET /api/industries
사용 가능한 업종 목록 조회

### GET /api/segments
14개 세그먼트 정보 조회

## 실행 방법

```bash
cd api
uvicorn main:app --reload --port 8000
```

## 데이터 소스
- 정적 프로필: `outputs/step1_static_profiles.json` (547일 카드 데이터)
- 실시간 프로필: `outputs/realtime_area_profiles.json` (서울시 API)

