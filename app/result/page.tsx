'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { RecommendationResults } from '@/components/RecommendationResults'
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

export default function ResultPage() {
  const router = useRouter()
  const [data, setData] = useState<RecommendationResponse | null>(null)

  useEffect(() => {
    const stored = sessionStorage.getItem('recommendations')
    if (stored) {
      try {
        const parsed = JSON.parse(stored)
        setData(parsed)
      } catch (err) {
        console.error('Failed to parse recommendations:', err)
        router.push('/')
      }
    } else {
      router.push('/')
    }
  }, [router])

  if (!data) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>로딩 중...</div>
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <button onClick={() => router.push('/')} className={styles.homeButton}>
          ← 홈으로
        </button>
        <h1 className={styles.title}>추천 결과</h1>
      </div>
      <RecommendationResults recommendations={data} />
    </div>
  )
}

