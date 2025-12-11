# Vercel 배포 가이드

## 🚀 빠른 배포 (자동)

GitHub와 연동되어 있다면 **자동 배포**됩니다!

1. GitHub에 푸시 완료 ✅
2. Vercel이 자동으로 감지하여 배포 시작

배포 상태 확인: https://vercel.com/dashboard

---

## 📦 수동 배포 (첫 배포 시)

### 1. Vercel CLI 설치 (필요 시)

```bash
npm install -g vercel
```

### 2. 로그인

```bash
vercel login
```

### 3. 배포

```bash
cd /Volumes/T7/class/2025-FALL/AI_RS/fin-project
vercel
```

첫 배포 시 질문에 답변:
- **Set up and deploy?** → Yes
- **Which scope?** → 본인 계정 선택
- **Link to existing project?** → No
- **Project name?** → space-recommendation (또는 원하는 이름)
- **Directory?** → ./ (엔터)
- **Override settings?** → No

### 4. 프로덕션 배포

```bash
vercel --prod
```

---

## 🔗 배포 후 확인 사항

### 배포 URL
배포가 완료되면 다음과 같은 URL을 받습니다:
```
https://space-recommendation-xxx.vercel.app
```

### 테스트 체크리스트

✅ **1. 메인 페이지 로드**
- URL에 접속하여 메인 페이지가 정상적으로 표시되는지 확인

✅ **2. 질문 페이지 이동**
- "지금 시작하기" 버튼 클릭
- `/question` 페이지로 이동되는지 확인

✅ **3. 추천 받기**
- 나이, 성별, 선호 업종 입력
- "추천 받기" 버튼 클릭
- 추천 결과가 나오는지 확인

✅ **4. 연령대별 추천 확인**
- 50세로 입력 시 홍대가 하위 순위인지 확인
- 20대로 입력 시 홍대가 상위 순위인지 확인

---

## ⚙️ 환경 변수 설정 (필요 시)

### Vercel 대시보드에서 설정

1. https://vercel.com/dashboard 접속
2. 프로젝트 선택
3. **Settings** → **Environment Variables**
4. 필요한 환경 변수 추가:

```
NEXT_PUBLIC_API_URL=https://your-api-url.com
SEOUL_API_KEY=your-seoul-api-key
```

---

## 🔄 자동 배포 설정

### GitHub 연동 (권장)

1. Vercel 대시보드에서 **Import Project**
2. **Import Git Repository** 선택
3. GitHub 저장소 선택: `SUE960/space_recommendation`
4. 프로젝트 설정:
   - **Framework Preset**: Next.js
   - **Root Directory**: ./
   - **Build Command**: `npm run build` (자동 감지)
   - **Output Directory**: `.next` (자동 감지)

5. **Deploy** 클릭

### 자동 배포 동작

```
main 브랜치에 푸시 → Vercel이 자동 빌드 → 자동 배포
```

---

## 🐛 문제 해결

### 빌드 실패 시

#### 1. 로그 확인
```bash
vercel logs
```

#### 2. 로컬에서 빌드 테스트
```bash
npm run build
```

#### 3. 자주 발생하는 문제

**문제**: `Module not found`
- **해결**: `package.json`의 dependencies 확인
- 누락된 패키지 추가:
  ```bash
  npm install [패키지명]
  git add package.json package-lock.json
  git commit -m "fix: add missing dependencies"
  git push
  ```

**문제**: TypeScript 에러
- **해결**: 타입 체크 통과 확인
  ```bash
  npm run type-check
  ```

**문제**: 환경 변수 접근 실패
- **해결**: Vercel 대시보드에서 환경 변수 설정

---

## 📊 배포 상태 확인

### Vercel 대시보드
- 빌드 로그 확인
- 배포 히스토리
- 성능 메트릭
- 에러 로그

### CLI로 확인
```bash
# 최근 배포 목록
vercel ls

# 배포 상태
vercel inspect [deployment-url]

# 로그 확인
vercel logs [deployment-url]
```

---

## 🎯 프로덕션 체크리스트

배포 전 확인사항:

- [ ] 로컬에서 `npm run build` 성공
- [ ] 로컬에서 `npm run start` 정상 동작
- [ ] `.gitignore`에 민감한 파일 제외
- [ ] 환경 변수 Vercel에 설정
- [ ] README.md 업데이트
- [ ] 라이선스 확인

---

## 🔗 유용한 링크

- **Vercel 대시보드**: https://vercel.com/dashboard
- **Next.js 배포 문서**: https://nextjs.org/docs/deployment
- **Vercel CLI 문서**: https://vercel.com/docs/cli

---

## 💡 팁

### 1. 프리뷰 배포
모든 브랜치 푸시는 프리뷰 URL을 생성합니다:
```
feature/new-feature 브랜치 → https://space-recommendation-git-feature-xxx.vercel.app
```

### 2. 배포 롤백
```bash
# 이전 배포로 롤백
vercel rollback [previous-deployment-url]
```

### 3. 커스텀 도메인
Vercel 대시보드 → Settings → Domains에서 설정 가능

---

## 📞 배포 후 공유

배포가 완료되면 다음 정보를 공유하세요:

**배포 URL**: https://space-recommendation-xxx.vercel.app
**GitHub**: https://github.com/SUE960/space_recommendation

---

**배포 완료!** 🎉

