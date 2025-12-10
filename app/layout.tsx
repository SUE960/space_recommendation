import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '플레이스메이트 - AI 기반 지역 추천',
  description: '트렌드 지역이 핫하다고 해도, 나한테 맞는 곳인지 고민되시나요? 서울시민 소비 데이터로 분석한 나이대별 트렌드 지역을 추천해드립니다.',
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

