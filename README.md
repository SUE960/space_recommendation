# 🤝 플레이스메이트 (PlaceMate)

**이중 매칭 알고리즘**을 활용한 AI 기반 지역 추천 서비스입니다.

> 트렌드 지역이 핫하다고 해도, 나한테 맞는 곳인지 고민되시나요?  
> 서울시민 소비 데이터로 분석한 나이대별 트렌드 지역을 추천해드립니다.

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6)](https://www.typescriptlang.org/)

---

## 🌟 주요 특징

- ✅ **이중 매칭 알고리즘** - 정적(50%) + 실시간(50%) 프로필 결합
- ✅ **14개 세그먼트** - 547일 서울시민 카드 데이터 기반
- ✅ **73개 핫스팟** - 서울시 실시간 상권 활성화 정보
- ✅ **6단계 추천 프로세스** - 입력부터 결과까지 체계적 분석
- ✅ **현대적 UI/UX** - 반응형 디자인, 실시간 피드백

---

## 🚀 빠른 시작

### 📋 사전 요구사항

- Node.js 18+
- Python 3.9+
- npm 또는 yarn

### 1️⃣ 프로젝트 클론

```bash
git clone https://github.com/your-repo/fin-project.git
cd fin-project
```

### 2️⃣ 프론트엔드 실행

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

**접속**: http://localhost:3000

### 3️⃣ 백엔드 API 실행

```bash
# API 디렉토리로 이동
cd api

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload --port 8000
```

**API 문서**: http://localhost:8000/docs

---

## 📊 시스템 아키텍처

### 6단계 추천 프로세스

```
01. 사용자 입력
    ↓ 나이, 성별, 소득, 선호 업종, 시간대 등
    
02. 정적 프로필 매칭
    ↓ 14개 세그먼트 중 매칭 (547일 카드 데이터)
    
03. 실시간 프로필 로드
    ↓ 73개 핫스팟 실시간 상권 데이터
    
04. 이중 매칭 점수 계산
    ├─ 정적 매칭 (50%): 업종 40% + 인구 30% + 소비 20% + 시간 10%
    └─ 실시간 매칭 (50%): 선호 35% + 종합 30% + 특화 20% + 시간 15%
    
05. 최종 점수 산출
    ↓ 통합 + 보정 (주말, 예산, 위치)
    
06. 추천 결과 반환
    ↓ 상위 10개 지역
```

---

## 🎯 핵심 알고리즘

### 정적 프로필 매칭 (50%)

```python
정적 점수 = 업종 선호도 매칭 (40%)
          + 인구통계 매칭 (30%)
          + 소비 수준 매칭 (20%)
          + 시간대 패턴 매칭 (10%)
```

**데이터 소스**: 547일 서울시민 카드 소비 데이터
**세그먼트**: 14개 (7개 연령대 × 2개 성별)

### 실시간 프로필 매칭 (50%)

```python
실시간 점수 = 사용자 선호 업종 매칭 (35%)
            + 실시간 종합 점수 (30%)
            + 특화도 매칭 (20%)
            + 시간대 적합도 (15%)
```

**데이터 소스**: 서울시 상권 활성화 정보 API
**지역**: 73개 핫스팟

### 최종 통합

```python
최종 점수 = (정적 점수 × 0.5) + (실시간 점수 × 0.5)
         + 주말 보너스 (×1.1)
         + 예산 매칭 보정
         + 위치 선호도 보정
```

---

## 📁 프로젝트 구조

```
fin-project/
├── 🎨 프론트엔드
│   ├── app/                    # Next.js 페이지
│   │   ├── page.tsx           # 메인 페이지
│   │   ├── question/          # 질문 페이지
│   │   └── result/            # 결과 페이지
│   └── components/            # React 컴포넌트
│       ├── RecommendationForm.tsx
│       ├── RecommendationResults.tsx
│       └── LoadingSpinner.tsx
│
├── 🔧 백엔드
│   └── api/
│       ├── main.py            # FastAPI 서버 (이중 매칭 알고리즘)
│       ├── requirements.txt   # Python 의존성
│       └── README.md          # API 문서
│
├── 📊 데이터
│   ├── outputs/
│   │   ├── step1_static_profiles.json      # 14개 세그먼트
│   │   └── realtime_area_profiles.json     # 73개 핫스팟
│   └── data_2/                # 원본 카드 데이터
│
├── 🔬 알고리즘
│   ├── step1_user_matcher.py              # 정적 프로필 매처
│   └── step3_integrated_recommendation.py # 통합 추천
│
└── 📚 문서
    ├── README.md                          # 이 파일
    ├── QUICK_START.md                     # 빠른 시작 가이드
    ├── DEPLOYMENT.md                      # 배포 가이드
    ├── 추천시스템_설계문서.md               # 상세 설계
    └── 이중_매칭_알고리즘_구현완료.md        # 구현 보고서
```

---

## 🎬 사용 예시

### 입력

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

### 출력

```
🏆 추천 결과

1위. 홍대 관광특구 (85.32점)
     ├─ 정적 매칭: 82.5점
     │  ├─ 업종: 60.0점
     │  ├─ 인구: 81.2점
     │  ├─ 소비: 59.4점
     │  └─ 시간: 65.0점
     │
     ├─ 실시간 매칭: 88.2점
     │  ├─ 선호: 66.7점
     │  ├─ 종합: 76.3점
     │  ├─ 특화: 99.6점
     │  └─ 시간: 85.0점
     │
     └─ 추천 이유
        • 선호하시는 한식, 카페 업종이 특화된 지역
        • 20대 남성에게 인기
        • 현재 매우 활성화 (Hot Zone)
        • 저녁 시간대에 적합
```

---

## 🔌 API 엔드포인트

### POST `/api/recommend`
사용자 입력 기반 지역 추천

### GET `/api/regions`
73개 실시간 지역 정보 조회

### GET `/api/industries`
사용 가능한 업종 목록 조회

### GET `/api/segments`
14개 세그먼트 정보 조회

**상세 API 문서**: [api/README.md](./api/README.md)

---

## 🚀 배포

### 프론트엔드 (Vercel)

```bash
# Vercel CLI 설치
npm install -g vercel

# 배포
vercel
```

또는 GitHub 연동으로 자동 배포

### 백엔드 (Railway / Render)

```bash
# Railway 배포
railway login
railway init
railway up
```

**상세 배포 가이드**: [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 📊 데이터 소스

### 정적 프로필
- **출처**: 서울시 빅데이터 캠퍼스
- **기간**: 2024.01.01 ~ 2025.06.30 (547일)
- **레코드**: 100,101개
- **업종**: 44개
- **세그먼트**: 14개 (7개 연령대 × 2개 성별)

### 실시간 프로필
- **출처**: 서울시 상권 활성화 정보 API
- **지역**: 73개 핫스팟
- **데이터**: 상권 활성도, 특화 점수, 인구통계, 종합 점수

---

## 🛠️ 기술 스택

| 분야 | 기술 |
|------|------|
| **Frontend** | Next.js 14, React, TypeScript, CSS Modules |
| **Backend** | FastAPI, Python 3.9+, Uvicorn |
| **Data** | Pandas, NumPy |
| **Algorithm** | 이중 매칭 알고리즘 (커스텀) |
| **Deployment** | Vercel, Railway, Render |

---

## 📈 성능

- ⚡ 정적 프로필 로드: < 100ms
- ⚡ 실시간 프로필 로드: < 200ms
- ⚡ 73개 지역 매칭 계산: < 500ms
- ⚡ 전체 추천 프로세스: < 1초

---

## 📚 문서

- 📖 [빠른 시작 가이드](./QUICK_START.md)
- 📖 [배포 가이드](./DEPLOYMENT.md)
- 📖 [API 문서](./api/README.md)
- 📖 [설계 문서](./추천시스템_설계문서.md)
- 📖 [구현 보고서](./이중_매칭_알고리즘_구현완료.md)

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

## 🎉 감사합니다!

이 프로젝트를 통해 서울시민들이 자신에게 맞는 최적의 지역을 찾을 수 있기를 바랍니다! 🚀

---

**Last Updated**: 2025-12-10
