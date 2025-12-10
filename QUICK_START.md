# 🚀 빠른 시작 가이드

## 📌 이중 매칭 알고리즘 기반 지역 추천 서비스

---

## 🎯 주요 기능

### 6단계 추천 프로세스
1. **사용자 입력**: 나이, 성별, 소득, 선호 업종, 시간대 등
2. **정적 프로필 매칭**: 14개 세그먼트 중 매칭 (547일 카드 데이터 기반)
3. **실시간 프로필 로드**: 73개 핫스팟 실시간 상권 데이터
4. **이중 매칭 점수 계산**: 정적(50%) + 실시간(50%)
5. **최종 점수 산출**: 보정 및 정규화
6. **추천 결과 반환**: 상위 10개 지역

---

## 🏃 실행 방법

### 1️⃣ API 서버 실행

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**확인**: http://localhost:8000/docs

### 2️⃣ 프론트엔드 실행

```bash
npm install
npm run dev
```

**확인**: http://localhost:3000

---

## 📊 API 테스트

### cURL 예시

```bash
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 28,
    "gender": "남",
    "income_level": "중",
    "preferred_industries": ["한식", "카페", "영화관"],
    "time_period": "저녁",
    "is_weekend": false,
    "preference_type": "활발한"
  }'
```

### Python 예시

```python
import requests

response = requests.post(
    "http://localhost:8000/api/recommend",
    json={
        "age": 28,
        "gender": "남",
        "income_level": "중",
        "preferred_industries": ["한식", "카페", "영화관"],
        "time_period": "저녁",
        "is_weekend": False,
        "preference_type": "활발한"
    }
)

print(response.json())
```

---

## 📁 주요 파일

```
/api
  └── main.py              # 이중 매칭 알고리즘 구현

/components
  ├── RecommendationForm.tsx     # 입력 폼
  └── RecommendationResults.tsx  # 결과 표시

/outputs
  ├── step1_static_profiles.json    # 14개 세그먼트
  └── realtime_area_profiles.json   # 73개 핫스팟

/
  ├── step1_user_matcher.py         # 정적 프로필 매처
  ├── 추천시스템_설계문서.md          # 설계 문서
  └── 이중_매칭_알고리즘_구현완료.md   # 구현 보고서
```

---

## 🎓 알고리즘 핵심

### 정적 매칭 (50%)
- 업종 선호도 (40%)
- 인구통계 (30%)
- 소비 수준 (20%)
- 시간대 패턴 (10%)

### 실시간 매칭 (50%)
- 선호 업종 (35%)
- 종합 점수 (30%)
- 특화도 (20%)
- 시간대 (15%)

---

## 📊 예시 결과

**입력:**
- 28세 남성, 중소득
- 선호: 한식, 카페, 영화관
- 저녁, 평일, 활발한 지역

**출력:**
```
1위. 홍대 관광특구 (85.32점)
     정적: 82.5 | 실시간: 88.2
     이유: 선호 업종 특화, 20대 인기, 활성화

2위. 신촌·이대역 (78.45점)
     정적: 75.1 | 실시간: 81.8
     이유: 다양한 업종, 젊은 층, 저녁 활성화
```

---

## 🔍 문서

- **설계**: `추천시스템_설계문서.md`
- **구현**: `이중_매칭_알고리즘_구현완료.md`
- **API**: `api/README.md`

---

## 💡 팁

1. **데이터 업데이트**: `outputs/` 폴더의 JSON 파일 교체
2. **가중치 조정**: `api/main.py`의 가중치 상수 수정
3. **업종 매핑**: `INDUSTRY_MAPPING` 딕셔너리 확장

---

**작성일**: 2025-12-10

