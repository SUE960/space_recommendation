# 🚀 GitHub + Vercel 배포 가이드

## 📋 단계별 가이드

### 1️⃣ GitHub 저장소 생성

1. **GitHub 접속**
   - https://github.com 접속
   - 로그인

2. **새 저장소 만들기**
   - 우측 상단 "+" → "New repository" 클릭
   - Repository name: `fin-project` (또는 원하는 이름)
   - Description: `서울 카드 데이터 기반 AI 추천 시스템`
   - Public 또는 Private 선택
   - **❌ README, .gitignore, license 추가하지 마세요** (이미 있음)
   - "Create repository" 클릭

3. **저장소 URL 복사**
   ```
   https://github.com/YOUR_USERNAME/fin-project.git
   ```

---

### 2️⃣ 로컬 저장소 연결 및 푸시

터미널에서 다음 명령어를 실행하세요:

```bash
# 프로젝트 디렉토리로 이동
cd /Volumes/T7/class/2025-FALL/AI_RS/fin-project

# GitHub 저장소 연결 (YOUR_USERNAME을 본인 GitHub 아이디로 변경)
git remote add origin https://github.com/YOUR_USERNAME/fin-project.git

# 브랜치 이름 확인 (main이어야 함)
git branch

# GitHub에 푸시
git push -u origin main
```

**에러 발생 시:**

#### 에러 1: remote origin already exists
```bash
# 기존 원격 저장소 제거 후 재설정
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/fin-project.git
git push -u origin main
```

#### 에러 2: 인증 실패
```bash
# GitHub Personal Access Token 사용
# Settings → Developer settings → Personal access tokens → Generate new token
# repo 권한 체크 후 토큰 생성
# 푸시 시 Password에 토큰 입력
```

---

### 3️⃣ Vercel 배포

#### A. GitHub 연동 방식 (권장)

1. **Vercel 접속**
   - https://vercel.com 접속
   - "Sign Up" 또는 "Log In"
   - **"Continue with GitHub"** 선택

2. **새 프로젝트 생성**
   - 대시보드에서 "Add New..." → "Project" 클릭
   - GitHub 저장소 목록에서 `fin-project` 선택
   - "Import" 클릭

3. **프로젝트 설정**
   ```
   Framework Preset: Next.js (자동 감지됨)
   Root Directory: ./
   Build Command: npm run build (자동)
   Output Directory: .next (자동)
   Install Command: npm install (자동)
   ```

4. **환경 변수 설정**
   - "Environment Variables" 섹션 펼치기
   - 추가할 변수:
     ```
     Key: NEXT_PUBLIC_API_URL
     Value: http://localhost:8000
     ```
   - (나중에 백엔드 배포 후 실제 URL로 변경)

5. **배포 시작**
   - "Deploy" 버튼 클릭
   - 2-3분 대기
   - 완료! 🎉

6. **배포된 URL 확인**
   ```
   https://your-project-name.vercel.app
   ```

#### B. CLI 방식

```bash
# Vercel CLI 설치
npm install -g vercel

# 로그인
vercel login

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

---

### 4️⃣ 백엔드 API 배포 (선택사항)

#### Railway 배포

1. **Railway 접속**
   - https://railway.app 접속
   - "Start a New Project" 클릭
   - "Deploy from GitHub repo" 선택

2. **프로젝트 설정**
   - 저장소 선택: `fin-project`
   - Root Directory: `api`
   - Build Command: (비워두기)
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **환경 변수**
   ```
   PORT=8000
   ```

4. **배포 URL 복사**
   ```
   https://your-api.railway.app
   ```

5. **Vercel 환경 변수 업데이트**
   - Vercel 대시보드 → Settings → Environment Variables
   - `NEXT_PUBLIC_API_URL` 값을 Railway URL로 변경
   - Redeploy 클릭

---

## 🎯 빠른 참조

### GitHub 푸시 명령어
```bash
git remote add origin https://github.com/YOUR_USERNAME/fin-project.git
git push -u origin main
```

### Vercel 배포
1. https://vercel.com
2. Import Project
3. 저장소 선택
4. Deploy

### 자동 배포
- `main` 브랜치에 푸시하면 자동으로 Vercel 재배포됨
- PR 생성 시 프리뷰 배포 자동 생성

---

## ✅ 체크리스트

### GitHub 푸시 전
- [x] 로컬 커밋 완료
- [x] .gitignore 설정
- [ ] GitHub 저장소 생성
- [ ] 원격 저장소 연결
- [ ] 푸시 완료

### Vercel 배포
- [ ] Vercel 계정 생성
- [ ] GitHub 연동
- [ ] 프로젝트 Import
- [ ] 환경 변수 설정
- [ ] 배포 완료

### 배포 확인
- [ ] 프론트엔드 접속 확인
- [ ] API 연결 확인
- [ ] 추천 기능 테스트
- [ ] 모바일 반응형 확인

---

## 🐛 트러블슈팅

### 문제 1: GitHub 푸시 실패
```bash
# SSH 키 설정 또는 Personal Access Token 사용
# Settings → Developer settings → Tokens
```

### 문제 2: Vercel 빌드 실패
```bash
# package.json 확인
# node_modules 삭제 후 재설치
npm install
```

### 문제 3: API 연결 안 됨
```bash
# CORS 설정 확인 (api/main.py)
# 환경 변수 확인 (Vercel 대시보드)
```

---

## 📞 다음 단계

1. **지금 바로 실행**: 위의 명령어 복사해서 실행
2. **GitHub 저장소 URL**: 생성 후 명령어의 URL 부분 수정
3. **Vercel 배포**: GitHub 푸시 완료 후 Vercel 접속

---

**작성일**: 2025-12-10

