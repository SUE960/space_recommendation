'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { RecommendationResults } from '@/components/RecommendationResults'
import styles from './page.module.css'

interface RecommendationResponse {
  recommendations: Array<{
    region: string
    score: number
    specialization: string | null
    specialization_ratio: number | null
    stability: string
    growth_rate: number | null
    reason: string
  }>
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

