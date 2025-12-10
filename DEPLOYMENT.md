# 🚀 배포 가이드

## 📋 배포 개요

이 프로젝트는 **프론트엔드(Next.js)**와 **백엔드(FastAPI)**로 구성되어 있습니다.

---

## 🎨 프론트엔드 배포 (Vercel)

### 1️⃣ Vercel 배포 준비

```bash
# Vercel CLI 설치 (선택사항)
npm install -g vercel

# 프로젝트 루트에서 실행
vercel
```

### 2️⃣ GitHub 연동 배포 (권장)

1. **GitHub에 푸시**
   ```bash
   git add .
   git commit -m "feat: UI 개선 및 배포 준비"
   git push origin main
   ```

2. **Vercel 대시보드**
   - https://vercel.com 접속
   - "New Project" 클릭
   - GitHub 저장소 연결
   - 프로젝트 선택
   - "Deploy" 클릭

3. **환경 변수 설정**
   - Vercel 대시보드 → Settings → Environment Variables
   - 추가할 변수:
     ```
     NEXT_PUBLIC_API_URL=https://your-api-server.com
     ```

### 3️⃣ 자동 배포

- `main` 브랜치에 푸시하면 자동으로 배포됩니다
- PR을 생성하면 프리뷰 배포가 자동으로 생성됩니다

---

## 🔧 백엔드 배포 (Railway / Render / AWS)

### Option 1: Railway (권장)

1. **Railway 계정 생성**
   - https://railway.app 접속

2. **프로젝트 생성**
   ```bash
   # Railway CLI 설치
   npm install -g @railway/cli
   
   # 로그인
   railway login
   
   # 프로젝트 생성
   railway init
   ```

3. **배포 설정**
   - `api/` 폴더를 별도 저장소로 분리하거나
   - Railway에서 Root Directory를 `api`로 설정

4. **환경 변수 설정**
   ```
   PORT=8000
   ```

5. **배포 명령어**
   ```bash
   railway up
   ```

### Option 2: Render

1. **Render 계정 생성**
   - https://render.com 접속

2. **Web Service 생성**
   - "New +" → "Web Service"
   - GitHub 저장소 연결
   - Root Directory: `api`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **환경 변수 설정**
   - Render 대시보드에서 설정

### Option 3: AWS EC2

```bash
# EC2 인스턴스 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 프로젝트 클론
git clone https://github.com/your-repo.git
cd your-repo/api

# Python 환경 설정
sudo apt update
sudo apt install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 백그라운드 실행
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

---

## 🔗 배포 후 연결

### 프론트엔드 환경 변수 업데이트

Vercel 대시보드에서:
```
NEXT_PUBLIC_API_URL=https://your-api-server.railway.app
```

### CORS 설정 업데이트

`api/main.py`에서:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "http://localhost:3000"  # 개발용
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 배포 체크리스트

### 프론트엔드
- [ ] 환경 변수 설정 (`NEXT_PUBLIC_API_URL`)
- [ ] 빌드 테스트 (`npm run build`)
- [ ] Vercel 배포 완료
- [ ] 도메인 설정 (선택사항)

### 백엔드
- [ ] 의존성 파일 확인 (`requirements.txt`)
- [ ] 데이터 파일 업로드 (`outputs/*.json`)
- [ ] CORS 설정 업데이트
- [ ] API 서버 배포 완료
- [ ] Health check 확인 (`/` 엔드포인트)

### 연동 테스트
- [ ] API 연결 테스트
- [ ] 추천 기능 테스트
- [ ] 에러 처리 확인
- [ ] 모바일 반응형 확인

---

## 🐛 트러블슈팅

### 문제 1: API 연결 실패
```
해결: CORS 설정 확인 및 환경 변수 확인
```

### 문제 2: 데이터 파일 없음
```
해결: outputs/ 폴더의 JSON 파일들을 서버에 업로드
```

### 문제 3: 빌드 실패
```
해결: package.json의 의존성 버전 확인
```

---

## 📈 성능 최적화

### 프론트엔드
- [ ] 이미지 최적화 (Next.js Image)
- [ ] 코드 스플리팅
- [ ] CDN 활용 (Vercel 자동)

### 백엔드
- [ ] 데이터 캐싱
- [ ] 응답 압축
- [ ] 로드 밸런싱 (필요시)

---

## 🔒 보안 설정

### 환경 변수
- API 키는 절대 코드에 하드코딩하지 않기
- `.env.local`은 `.gitignore`에 포함

### CORS
- 프로덕션에서는 특정 도메인만 허용
- `allow_origins=["*"]`는 개발 환경에서만 사용

---

## 📞 지원

배포 관련 문제가 있으면:
1. GitHub Issues 확인
2. 문서 참조
3. 로그 확인

---

**작성일**: 2025-12-10
**버전**: 1.0.0

