# 🎯 서울 카드 데이터 기반 AI 추천 시스템

서울 카드 데이터와 실시간 지역 분석을 활용한 **개인 맞춤형 지역 추천 서비스**입니다.

## 🌟 주요 특징

- ✅ **14개 세그먼트** 정적 집단 프로필 (연령대 × 성별)
- ✅ **서울시 25개 구** 실시간 지역 점수 분석
- ✅ **AI 기반 매칭 알고리즘** (사용자 선호도 + 지역 특성)
- ✅ **웹 인터페이스** (Next.js + FastAPI)
- ✅ **실시간 추천 API**

---

## 📊 시스템 아키텍처

```
┌─────────────────┐
│   사용자 입력    │  나이, 성별, 소득, 선호 업종
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    STEP 1       │  정적 집단 프로필 생성
│  카드 데이터    │  - 14개 세그먼트 분석
│  분석 시스템    │  - 업종별 선호도
└────────┬────────┘  - 지역별 방문 패턴
         │
         ▼
┌─────────────────┐
│    STEP 2       │  실시간 지역 프로필
│ 지역 점수 계산   │  - 25개 구 분석
└────────┬────────┘  - 업종 다양성/안정성/성장률
         │
         ▼
┌─────────────────┐
│    STEP 3       │  사용자-지역 매칭
│  통합 추천      │  - 선호도 점수 계산
│    시스템       │  - 지역 점수 반영
└────────┬────────┘  - 최종 TOP 5 추천
         │
         ▼
┌─────────────────┐
│  추천 결과 제공  │  웹/API를 통한 결과 제공
└─────────────────┘
```

---

## 📁 프로젝트 구조

```
fin-project/
├── 🎯 STEP 1: 정적 집단 프로필 생성
│   ├── step1_static_profile_generation.py   # 카드 데이터 분석
│   ├── step1_user_matcher.py                # 사용자-세그먼트 매칭
│   └── STEP1_가이드.md                      # STEP 1 상세 가이드
│
├── 🔄 STEP 2: 실시간 지역 프로필 (다른 에이전트 담당)
│   └── outputs/seoul_all_gu_final.csv       # 25개 구 점수 데이터
│
├── 🎁 STEP 3: 통합 추천 시스템
│   ├── step3_integrated_recommendation.py   # 통합 추천 엔진
│   └── STEP1_STEP2_통합가이드.md            # 통합 가이드
│
├── 🌐 웹 서비스
│   ├── api/                                 # FastAPI 백엔드
│   │   ├── main.py                         # API 서버
│   │   └── requirements.txt                # Python 의존성
│   ├── app/                                 # Next.js 프론트엔드
│   │   ├── page.tsx                        # 메인 페이지
│   │   ├── question/page.tsx               # 질문 페이지
│   │   └── result/page.tsx                 # 결과 페이지
│   └── components/                          # React 컴포넌트
│       ├── RecommendationForm.tsx          # 입력 폼
│       └── RecommendationResults.tsx       # 결과 표시
│
├── 📊 데이터 및 결과
│   ├── data_2/                             # 서울시 카드 데이터
│   │   ├── 6.서울시 내국인 성별 연령대별(행정동별).csv  ⭐ 주요
│   │   └── 2.서울시민의 일별 시간대별(행정동).csv
│   └── outputs/                            # 분석 결과
│       ├── step1_static_profiles.json      # STEP 1 프로필
│       ├── step1_segment_matcher.json      # 매칭 테이블
│       └── seoul_all_gu_final.csv          # STEP 2 지역 점수
│
└── 📚 문서
    ├── README.md                            # 이 파일
    ├── STEP1_가이드.md                      # STEP 1 가이드
    ├── STEP1_STEP2_통합가이드.md            # 통합 시스템 가이드
    └── 프로젝트_전체정리.md                  # 전체 프로젝트 정리
```

---

## 🚀 빠른 시작

### Step 1: STEP 1 정적 프로필 생성

```bash
# 카드 데이터 기반 집단 프로필 생성
python3 step1_static_profile_generation.py
```

**생성 파일**:
- `outputs/step1_static_profiles.json` - 14개 세그먼트 프로필
- `outputs/step1_segment_matcher.json` - 매칭 테이블
- `outputs/step1_summary_report.md` - 요약 리포트

### Step 2: 통합 추천 시스템 사용

```python
from step3_integrated_recommendation import IntegratedRecommendationSystem

# 시스템 초기화
system = IntegratedRecommendationSystem(
    step1_dir='outputs',
    step2_file='outputs/seoul_all_gu_final.csv'  # STEP 2 결과
)

# 사용자 맞춤 추천
result = system.recommend_regions(
    age=28,
    gender='남',
    income_level='중',
    preferences={
        'preferred_industries': ['한식', '커피전문점', '영화/공연'],
        'priorities': {'preference_match': 0.6, 'score': 0.4}
    },
    top_n=5
)

# 결과 출력
system.print_recommendations(result)
```

### Step 3: 웹 서비스 실행

#### 3-1. 프론트엔드 의존성 설치

```bash
npm install
```

#### 3-2. 백엔드 API 서버 실행

```bash
cd api
pip install -r requirements.txt
python main.py
# 또는
uvicorn main:app --reload --port 8000
```

API 서버: `http://localhost:8000`

#### 3-3. 프론트엔드 개발 서버 실행

```bash
npm run dev
```

웹 서비스: `http://localhost:3000`

---

## 🎯 핵심 기능

### 1. STEP 1: 정적 집단 프로필 생성

**서울시 카드 데이터를 분석하여 14개 세그먼트 프로필 생성**

| 세그먼트 | 총 소비액 | 평균 거래액 | 주요 관심사 |
|---------|-----------|------------|------------|
| 30대 남성 | 738억원 | 33,687원 | 한식 (38.3%) |
| 40대 남성 | 671억원 | 30,956원 | 대형마트 (55.1%) |
| 30대 여성 | 276억원 | 20,453원 | 컴퓨터/SW (38.5%) |
| 20대 여성 | 224억원 | 30,072원 | 기타 (46.4%) |

- **연령대**: 7개 (20세미만 ~ 70세이상)
- **성별**: 2개 (남/여)
- **분석 항목**: 업종별 선호도, 지역별 방문 패턴, 시간대별 소비

### 2. STEP 2: 실시간 지역 프로필 (다른 에이전트 담당)

**서울시 25개 구의 특성 분석**

| 항목 | 설명 | 예시 |
|------|------|------|
| **특화 업종** | 지역의 대표 업종 | 강남구: 학원/학습지 (31.4%) |
| **업종 다양성** | 업종 수 | 강남구: 보통(14개) |
| **소비 안정성** | 변동계수 | 강남구: 안정적(16.8%) |
| **성장률** | 전월 대비 증감 | 관악구: +2.00% (↑상승) |

### 3. STEP 3: 통합 추천 시스템

**사용자 선호도 + 지역 특성을 결합한 AI 매칭**

```python
최종 점수 = (선호도 점수 × 0.6) + (지역 점수 × 0.4)
```

#### 선호도 점수 계산 요소:
- ✅ 업종 매칭 (사용자 선호 vs 지역 특화)
- ✅ 연령대별 가중치 (20-30대는 성장 지역 선호)
- ✅ 다양성 선호도 (관심 업종 수에 따라)
- ✅ 소득 수준 반영

#### 지역 점수 계산 요소:
- ✅ 업종 다양성 (최대 +20점)
- ✅ 소비 안정성 (최대 +10점)
- ✅ 성장률 (-10 ~ +15점)

### 4. 웹 인터페이스

- 📝 **질문 페이지**: 나이, 성별, 소득, 선호 업종 입력
- 🎁 **결과 페이지**: TOP 5 지역 추천 + 상세 정보
- 📊 **프로세스 시각화**: 추천 과정 단계별 표시

---

## 📊 추천 예시

### 시나리오 1: 20대 남성 직장인

**입력**:
- 나이: 28세
- 성별: 남
- 소득: 중
- 선호 업종: 한식, 커피전문점, 영화/공연

**추천 결과**:
```
1위. 마포구 (75.8점)
   - 선호도: 65.0점 | 지역 점수: 82.0점
   - 이유: ZZ_나머지 특화, 성장하는 지역 (+1.67%), 20대에게 인기

2위. 관악구 (73.4점)
   - 선호도: 60.0점 | 지역 점수: 76.0점
   - 이유: 일식 특화, 젊은 층 방문 많음

3위. 영등포구 (71.6점)
   - 선호도: 55.0점 | 지역 점수: 79.0점
   - 이유: 다양한 업종, 성장세 양호
```

### 시나리오 2: 40대 남성 가장

**입력**:
- 나이: 45세
- 성별: 남
- 소득: 중
- 선호 업종: 대형마트, 한식, 주유소

**추천 결과**:
```
1위. 금천구 (79.3점)
   - 선호도: 92.6점 | 지역 점수: 66.0점
   - 이유: 대형마트 특화 (47.7%), 안정적 소비

2위. 강동구 (77.8점)
   - 선호도: 92.6점 | 지역 점수: 63.0점
   - 이유: 대형마트 특화 (87.1%), 가족 단위 방문 많음

3위. 은평구 (78.5점)
   - 선호도: 92.6점 | 지역 점수: 64.5점
   - 이유: 실용적 소비 지역, 안정적 패턴
```

---

## 🔌 API 엔드포인트

### GET `/api/regions`
모든 지역 정보 조회

**응답 예시**:
```json
{
  "regions": [
    {
      "name": "강남구",
      "specialization": "학원/학습지",
      "diversity": "보통(14개)",
      "stability": "안정적(16.8%)",
      "growth_rate": "0.62%"
    }
  ]
}
```

### POST `/api/recommend`
사용자 입력 기반 지역 추천

**요청 본문**:
```json
{
  "age": 28,
  "gender": "남",
  "income_level": "중",
  "preferred_industries": ["한식", "커피전문점", "영화/공연"],
  "priorities": {
    "preference_match": 0.6,
    "score": 0.4
  }
}
```

**응답**:
```json
{
  "recommendations": [
    {
      "rank": 1,
      "region_name": "마포구",
      "match_score": 75.8,
      "preference_score": 65.0,
      "step2_score": 82.0,
      "reason": "20대 남성에게 인기, 기타요식 관심사에 적합, 성장하는 지역",
      "region_details": {
        "특징": "ZZ_나머지 특화 (52.7%)",
        "업종다양성": "낮음(8개)",
        "소비안정성": "안정적(17.1%)",
        "성장률": "+1.67% (↑상승)"
      }
    }
  ],
  "user_info": {
    "age": 28,
    "gender": "남",
    "matched_segment": "20_29세 남",
    "avg_budget": 9333
  }
}
```

### GET `/api/industries`
사용 가능한 업종 목록 조회

### GET `/api/segments`
모든 사용자 세그먼트 정보 조회

---

## 📚 상세 가이드

### 🎯 STEP 1 가이드
[STEP1_가이드.md](./STEP1_가이드.md)에서 다음 내용을 확인하세요:
- 정적 집단 프로필 생성 방법
- 사용자-세그먼트 매칭 방법
- 14개 세그먼트별 상세 특징
- API 사용 예시 및 커스터마이징

### 🔄 통합 시스템 가이드
[STEP1_STEP2_통합가이드.md](./STEP1_STEP2_통합가이드.md)에서 다음 내용을 확인하세요:
- STEP 1 + STEP 2 통합 방법
- 추천 알고리즘 상세 설명
- 다양한 사용 시나리오
- 가중치 조정 및 최적화
- 트러블슈팅

### 📊 프로젝트 전체 정리
[프로젝트_전체정리.md](./프로젝트_전체정리.md)에서 전체 프로젝트 개요를 확인하세요.

---

## 📊 데이터 출처

### STEP 1 데이터
- **서울시 빅데이터 캠퍼스**: 서울시민 카드 소비 데이터
  - `6.서울시 내국인 성별 연령대별(행정동별).csv` ⭐ 주요
  - `2.서울시민의 일별 시간대별(행정동).csv`
  - 기간: 2024.01.01 ~ 2025.06.30
  - 총 레코드: 100,101개
  - 분석 업종: 44개

### STEP 2 데이터
- 서울시 25개 구 실시간 특성 분석
- 업종 다양성, 소비 안정성, 성장률 계산

---

## 🛠️ 기술 스택

| 분야 | 기술 |
|------|------|
| **Frontend** | Next.js 14, React, TypeScript, CSS Modules |
| **Backend** | FastAPI, Python 3.9+ |
| **Data Analysis** | Pandas, NumPy |
| **AI/ML** | 커스텀 매칭 알고리즘 |
| **Deployment** | Vercel (Frontend), Railway/Render (Backend) |

---

## 🚀 배포

### 프론트엔드 배포 (Vercel)

1. GitHub에 프로젝트 푸시
2. [Vercel](https://vercel.com) 로그인
3. "New Project" 클릭
4. GitHub 저장소 선택
5. 자동 빌드 및 배포

### 백엔드 배포 옵션

1. **Railway** 또는 **Render** 사용 (추천)
   ```bash
   # requirements.txt 준비
   cd api
   # Railway CLI 사용
   railway login
   railway init
   railway up
   ```

2. **Vercel Serverless Functions**로 변환

3. **별도 서버** (AWS, GCP, Azure 등)

---

## 📈 성능 및 확장성

### 현재 성능
- ✅ 14개 세그먼트 프로필 (즉시 로드)
- ✅ 25개 구 분석 (< 1초)
- ✅ 추천 계산 (< 100ms)
- ✅ API 응답 시간 (< 200ms)

### 확장 가능성
- 🔄 실시간 데이터 업데이트 (일/주/월 단위)
- 📊 더 많은 세그먼트 추가 (소득 수준별 세분화)
- 🌏 다른 도시로 확장 가능
- 🤖 ML 모델 적용 가능 (협업 필터링, 딥러닝 등)

---

## 🤝 기여

프로젝트 개선을 위한 기여를 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

## 👥 팀

**인공지능과 추천시스템 기말 프로젝트**

---

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.

---

## 🎉 감사합니다!

이 프로젝트를 통해 서울시민들이 자신에게 맞는 최적의 지역을 찾을 수 있기를 바랍니다! 🚀
