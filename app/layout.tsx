import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '서울 카드 데이터 기반 추천 서비스',
  description: '트렌드 지역 분석 및 개인 맞춤 추천 서비스',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}

