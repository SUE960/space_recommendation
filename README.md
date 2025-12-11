# 서울 카드 데이터 기반 추천 서비스

서울 카드 데이터를 활용한 트렌드 지역 분석 및 개인 맞춤 추천 서비스입니다.

## 프로젝트 구조

```
fin-project/
├── api/                    # 백엔드 API 서버
│   ├── main.py            # FastAPI 서버
│   └── requirements.txt   # Python 의존성
├── app/                   # Next.js 프론트엔드
│   ├── layout.tsx
│   ├── page.tsx          # 메인 페이지
│   └── globals.css
├── components/            # React 컴포넌트
│   ├── ProcessFlow.tsx   # 프로세스 플로우 시각화
│   ├── RecommendationForm.tsx    # 사용자 입력 폼
│   └── RecommendationResults.tsx # 추천 결과 표시
├── outputs/               # 분석 결과 데이터
│   ├── seoul_all_gu_characteristics.csv
│   └── seoul_all_gu_with_growth.csv
└── package.json
```

## 설치 및 실행

### 1. 프론트엔드 의존성 설치

```bash
npm install
```

### 2. 백엔드 의존성 설치

```bash
cd api
pip install -r requirements.txt
```

### 3. 백엔드 API 서버 실행

```bash
# 터미널 1
cd api
python main.py
# 또는
uvicorn main:app --reload --port 8000
```

API 서버는 `http://localhost:8000`에서 실행됩니다.

### 4. 프론트엔드 개발 서버 실행

```bash
# 터미널 2
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

## 서비스 기능

### 1. 정적 집단 프로필 생성
- 서울 시민 카드 데이터를 활용하여 연령대·성별·업종·지역 단위의 집단 소비 성향 추출
- 페르소나 기반 선호 업종 매칭

### 2. 실시간 지역 프로필 산출
- 지역별 특화 업종 및 특화 비율 분석
- 지역별 소비 안정성 (변동계수) 계산
- 지역별 성장률 분석

### 3. 사용자 입력 기반 매칭
- 사용자가 입력한 정보 (연령대, 성별, 선호 업종, 시간대, 주말 여부)
- 집단 패턴과 매칭하여 개인화된 추천 점수 계산

### 4. 최종 추천
- 집단 패턴 + 실시간 데이터 + 사용자 입력 정보를 결합
- 추천 점수 기반으로 상위 10개 지역 추천
- 각 지역의 특화 업종, 안정성, 성장률 정보 제공

## 추천 알고리즘

추천 점수는 다음 요소들을 종합하여 계산됩니다:

1. **페르소나 매칭 점수 (40%)**
   - 연령대별, 성별 선호 업종과 지역 특화 업종 매칭
   - 특화 비율에 따라 점수 부여

2. **시간대 적합도 (30%)**
   - 현재 시간대에 적합한 업종이 특화된 지역 우선 추천

3. **지역 특화도 (30%)**
   - 특화 비율 50% 이상: 높은 점수
   - 특화 비율 30-50%: 중간 점수
   - 특화 비율 30% 미만: 낮은 점수

4. **보너스 점수**
   - 주말 여부: +20% 보너스
   - 성장률 > 1.5%: +10% 보너스
   - 변동계수 < 15%: +10% 보너스 (안정성 높음)

## API 엔드포인트

### GET `/api/regions`
모든 지역 정보 조회

### POST `/api/recommend`
사용자 입력 기반 지역 추천

**요청 본문:**
```json
{
  "age_group": "30-39세",
  "gender": "남성",
  "preferred_industry": "한식",
  "time_period": "점심(12-18시)",
  "is_weekend": false
}
```

**응답:**
```json
{
  "recommendations": [
    {
      "region": "서초구",
      "score": 0.85,
      "specialization": "한식",
      "specialization_ratio": 90.5,
      "stability": "안정적(19.9%)",
      "growth_rate": 0.68,
      "reason": "한식 특화 지역(특화비율 90.5%), 현재 시간대에 적합한 업종, 안정적인 소비 패턴"
    }
  ],
  "user_profile": {
    "age_group": "30-39세",
    "gender": "남성",
    "preferred_industry": "한식",
    "time_period": "점심(12-18시)",
    "is_weekend": false,
    "matched_preferences": ["한식", "보험", "안마/마사지", "대형마트", "기타식품"]
  }
}
```

### GET `/api/industries`
사용 가능한 업종 목록 조회

## Vercel 배포

### 프론트엔드 배포

1. GitHub에 프로젝트 푸시
2. [Vercel](https://vercel.com)에 로그인
3. "New Project" 클릭
4. GitHub 저장소 선택
5. 자동으로 빌드 및 배포됨

### 백엔드 배포

Vercel은 Python 백엔드를 직접 지원하지 않으므로, 다음 옵션을 고려하세요:

1. **Railway** 또는 **Render** 사용
2. **Vercel Serverless Functions**로 변환
3. 별도 서버에 배포 (AWS, GCP 등)

## 기술 스택

- **Frontend**: Next.js 14, React, TypeScript, CSS Modules
- **Backend**: FastAPI, Python, Pandas, NumPy
- **Deployment**: Vercel (Frontend)

## 데이터 소스

- 서울시민 카드 소비 데이터
- 지역별 특화 업종 분석 결과
- 지역별 성장률 분석 결과
