'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { RecommendationForm } from '@/components/RecommendationForm'
import { RecommendationResults } from '@/components/RecommendationResults'
import { LoadingSpinner } from '@/components/LoadingSpinner'
import { Footer } from '@/components/Footer'
import Image from 'next/image'
import styles from './page.module.css'

interface Recommendation {
  rank: number
  region: string
  final_score: number
  static_score: number
  realtime_score: number
  static_details: {
    industry_match: number
    demographic_match: number
    spending_match: number
    time_match: number
  }
  realtime_details: {
    user_industry_match: number
    comprehensive_score: number
    specialization_match: number
    time_match: number
  }
  comprehensive_score: number
  grade: string
  specialized_industries: string[]
  reasons: string[]
}

interface RecommendationResponse {
  recommendations: Recommendation[]
  user_profile: {
    age: number
    gender: string
    income_level: string
    matched_segment: string
    segment_description: string
    preferred_industries: string[]
    time_period: string
    is_weekend: boolean
    preference_type: string
    top_segment_industries: string[]
  }
}

export default function Home() {
  const router = useRouter()
  const [showForm, setShowForm] = useState(false)
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleShowForm = () => {
    setShowForm(true)
    // 폼으로 부드럽게 스크롤
    setTimeout(() => {
      const formSection = document.getElementById('recommendation-section')
      if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }, 100)
  }

  const handleRecommend = async (formData: {
    age: number
    gender: string
    incomeLevel: string
    preferredIndustries: string[]
    timePeriod: string
    isWeekend: boolean
    preferenceType: string
  }) => {
    setLoading(true)
    setError(null)
    setRecommendations(null)

    try {
      // Next.js API Routes 사용 (Vercel에서 완벽 작동!)
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          age: formData.age,
          gender: formData.gender,
          income_level: formData.incomeLevel,
          preferred_industries: formData.preferredIndustries,
          time_period: formData.timePeriod,
          is_weekend: formData.isWeekend,
          preference_type: formData.preferenceType,
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
        <div className={styles.bannerImageWrapper}>
          <Image
            src="/banner.png"
            alt="Banner"
            fill
            priority
            className={styles.bannerImage}
            style={{ objectFit: 'cover' }}
            sizes="100vw"
            quality={90}
          />
        </div>
        <div className={styles.bannerContent}>
          <span className={styles.bannerTag}>AI 기반 지역 추천</span>
          <h1 className={styles.bannerTitle}>
            <span className={styles.bannerTitleHighlight}>플레이스메이트 🤝</span>
          </h1>
          <p className={styles.bannerDescription}>
            트렌드 지역이 핫하다고 해도, 나한테 맞는 곳인지 고민되시나요?
            <br />
            서울시민 소비 데이터로 분석한 <strong>나이대별 트렌드 지역</strong>을 추천해드립니다.
          </p>
          <div className={styles.bannerButtons}>
            <button
              onClick={() => router.push('/question')}
              className={styles.primaryButton}
            >
              어디로 갈까? →
            </button>
            <button className={styles.secondaryButton}>
              ⊙ 트렌드 맵 둘러보기
            </button>
            <button
              onClick={handleShowForm}
              className={styles.triggerButton}
            >
              🎯 개인 정보 입력하기
            </button>
          </div>
        </div>
      </section>

      {/* Recommendation Section */}
      <section id="recommendation-section" className={styles.serviceSection}>
        {showForm && (
          <>
            <RecommendationForm onSubmit={handleRecommend} loading={loading} />

            {loading && <LoadingSpinner />}

            {error && (
              <div className={styles.errorContainer}>
                <div className={styles.errorIcon}>⚠️</div>
                <h3 className={styles.errorTitle}>오류가 발생했습니다</h3>
                <p className={styles.errorMessage}>{error}</p>
                <button 
                  onClick={() => setError(null)} 
                  className={styles.errorButton}
                >
                  다시 시도하기
                </button>
              </div>
            )}

            {recommendations && !loading && (
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
