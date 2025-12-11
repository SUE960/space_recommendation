# Mapbox 설정 가이드

## 📍 트렌드 맵 기능 사용을 위한 Mapbox 설정

### 1. Mapbox 계정 생성 및 API 토큰 발급

1. [Mapbox 공식 웹사이트](https://www.mapbox.com/) 접속
2. 무료 계정 생성 (월 50,000회 무료 요청)
3. 대시보드에서 **Access Token** 복사

### 2. 환경 변수 설정

#### 로컬 개발 환경

`.env.local` 파일 생성 (프로젝트 루트):

```env
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
```

#### Vercel 배포 환경

1. Vercel 대시보드 접속
2. 프로젝트 선택 → Settings → Environment Variables
3. 다음 추가:
   - **Name**: `NEXT_PUBLIC_MAPBOX_TOKEN`
   - **Value**: Mapbox Access Token
   - **Environment**: Production, Preview, Development 모두 선택

### 3. 확인

설정 완료 후 `/trend-map` 페이지에서 지도가 정상적으로 표시됩니다.

### 4. Mapbox 무료 티어 제한

- **월 50,000회** 무료 요청
- 초과 시 $5/1,000회 요청
- 대부분의 경우 무료 티어로 충분합니다

### 5. 대안 (Mapbox 없이 사용)

Mapbox 토큰이 없어도 페이지는 표시되지만 지도는 보이지 않습니다.
대안으로 다음을 고려할 수 있습니다:

- **Naver Maps API** (한국 서비스에 적합)
- **Kakao Maps API** (한국 서비스에 적합)
- **Google Maps API** (유료)

현재는 Mapbox를 기본으로 사용하며, 필요시 다른 지도 API로 전환 가능합니다.
