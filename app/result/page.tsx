'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { RecommendationResults } from '@/components/RecommendationResults'
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

export default function ResultPage() {
  const router = useRouter()
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showResults, setShowResults] = useState(false)

  const handleGetRecommendations = async () => {
    // localStorage에서 데이터 불러오기
    const savedData = localStorage.getItem('recommendationData')
    if (!savedData) {
      alert('추천 데이터를 찾을 수 없습니다. 다시 질문에 답해주세요.')
      router.push('/question')
      return
    }

    try {
      const data = JSON.parse(savedData)
      setLoading(true)
      setError(null)

      // API 호출
      const response = await fetch('http://localhost:8000/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          age_group: data.ageGroup,
          gender: data.gender,
          preferred_industry: data.preferredIndustry || null,
          time_period: data.currentTime || null,
          is_weekend: data.isWeekend || false,
        }),
      })

      if (!response.ok) {
        throw new Error('추천 요청에 실패했습니다')
      }

      const result: RecommendationResponse = await response.json()
      setRecommendations(result)
      setShowResults(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }

  // 이미 결과가 있으면 바로 표시
  useEffect(() => {
    const savedResults = localStorage.getItem('recommendationResults')
    if (savedResults) {
      try {
        const parsed = JSON.parse(savedResults)
        setRecommendations(parsed)
        setShowResults(true)
      } catch (e) {
        console.error('Failed to load saved results:', e)
      }
    }
  }, [])

  if (showResults && recommendations) {
    return (
      <div className={styles.container}>
        <div className={styles.resultsContainer}>
          <RecommendationResults recommendations={recommendations} />
          <button
            onClick={() => router.push('/')}
            className={styles.backButton}
          >
            ← 홈으로
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <div className={styles.resultCard}>
        <h1 className={styles.title}>질문이 완료되었습니다!</h1>
        <p className={styles.description}>
          입력하신 정보를 바탕으로 지역을 추천해드리겠습니다.
        </p>
        {error && (
          <div className={styles.error}>
            <p>❌ {error}</p>
          </div>
        )}
        <button
          onClick={handleGetRecommendations}
          className={styles.button}
          disabled={loading}
        >
          {loading ? '추천 중...' : '추천 결과 보기 →'}
        </button>
      </div>
    </div>
  )
}

