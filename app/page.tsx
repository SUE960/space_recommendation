'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { RecommendationForm } from '@/components/RecommendationForm'
import { RecommendationResults } from '@/components/RecommendationResults'
import { Footer } from '@/components/Footer'
import Image from 'next/image'
import styles from './page.module.css'

interface Recommendation {
  region: string
  score: number
  specialization: string | null
  specialization_ratio: number | null
  stability: string
  growth_rate: number | null
  reason: string
}

interface RecommendationResponse {
  recommendations: Recommendation[]
  user_profile: {
    age_group: string
    gender: string
    preferred_industry: string | null
    time_period: string | null
    is_weekend: boolean
    matched_preferences: string[]
  }
}

export default function Home() {
  const router = useRouter()
  const [showForm, setShowForm] = useState(false)
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleRecommend = async (formData: {
    ageGroup: string
    gender: string
    preferredIndustry: string
    timePeriod: string
    isWeekend: boolean
  }) => {
    setLoading(true)
    setError(null)
    setRecommendations(null)

    try {
      const response = await fetch('http://localhost:8000/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          age_group: formData.ageGroup,
          gender: formData.gender,
          preferred_industry: formData.preferredIndustry || null,
          time_period: formData.timePeriod || null,
          is_weekend: formData.isWeekend,
        }),
      })

      if (!response.ok) {
        throw new Error('추천 요청에 실패했습니다')
      }

      const data: RecommendationResponse = await response.json()
      setRecommendations(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className={styles.container}>
      {/* Banner Section */}
      <section className={styles.banner}>
        <Image
          src="/banner.png"
          alt="Banner"
          fill
          priority
          className={styles.bannerImage}
          style={{ objectFit: 'cover' }}
        />
        <div className={styles.bannerContent}>
          <span className={styles.bannerTag}>AI 기반 소비 패턴 분석</span>
          <h1 className={styles.bannerTitle}>
            <span className={styles.bannerTitleHighlight}>당신의 지역을 찾아드립니다</span>
          </h1>
          <p className={styles.bannerDescription}>
            서울시민 카드 소비 데이터 분석. 유사한 소비 패턴을 가진 그룹을 찾고,
            <br />
            맞춤형 장소와 업종을 추천합니다.
          </p>
          <div className={styles.bannerButtons}>
            <button
              onClick={() => router.push('/question')}
              className={styles.primaryButton}
            >
              지금 시작하기 →
            </button>
            <button className={styles.secondaryButton}>
              ⊙ 트렌드 맵 둘러보기
            </button>
          </div>
        </div>
      </section>

      {/* Recommendation Section */}
      <section id="recommendation-section" className={styles.serviceSection}>
        {!showForm ? (
          <div className={styles.formTrigger}>
            <div className={styles.welcomeMessage}>
              <h2>🎯 나에게 맞는 지역을 찾아보세요</h2>
              <p>상단 헤더의 "기본 세팅하기" 버튼을 눌러 시작하세요</p>
            </div>
          </div>
        ) : (
          <>
            <RecommendationForm onSubmit={handleRecommend} loading={loading} />

            {error && (
              <div className={styles.error}>
                <p>❌ {error}</p>
              </div>
            )}

            {recommendations && (
              <RecommendationResults recommendations={recommendations} />
            )}
          </>
        )}
      </section>

      {/* Footer */}
      <Footer />
    </main>
  )
}
