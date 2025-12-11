import type { Metadata } from 'next'
import Script from 'next/script'
import './globals.css'
import { Header } from '@/components/Header'

export const metadata: Metadata = {
  title: '서울 카드 데이터 기반 추천 서비스',
  description: '트렌드 지역 분석 및 개인 맞춤 추천 서비스',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const kakaoKey = process.env.NEXT_PUBLIC_KAKAO_MAP_KEY || 'c2e410bd46b3705d319f436284127360'
  
  return (
    <html lang="ko">
      <head>
        <Script
          src={`//dapi.kakao.com/v2/maps/sdk.js?appkey=${kakaoKey}&autoload=false`}
          strategy="beforeInteractive"
        />
      </head>
      <body>
        <Header />
        <div style={{ paddingTop: '80px' }}>
          {children}
        </div>
      </body>
    </html>
  )
}

