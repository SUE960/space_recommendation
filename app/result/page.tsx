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

      // API 호출 - 질문에서 수집한 모든 정보를 실제 데이터 기반 추천에 활용
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '/api'
      const response = await fetch(`${apiUrl}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          age_group: data.ageGroup?.replace('세', '') || '20-29',
          gender: data.gender,
          preferred_industry: data.preferredIndustry || null,
          time_period: data.currentTime || null,
          is_weekend: data.isWeekend || false,
          purpose: data.purpose || null, // 방문 목적
          budget: data.budget || null, // 예산
          priority: data.priority || null, // 우선순위
        }),
      })

      if (!response.ok) {
        throw new Error('추천 요청에 실패했습니다')
      }

      const result: RecommendationResponse = await response.json()
      setRecommendations(result)
      setShowResults(true)
      
      // 결과를 localStorage에 저장
      localStorage.setItem('recommendationResults', JSON.stringify(result))
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }

  // 페이지 로드 시 자동으로 추천 요청 (실제 데이터와 로직 기반)
  useEffect(() => {
    const fetchRecommendations = async () => {
      // localStorage에서 데이터 불러오기
      const savedData = localStorage.getItem('recommendationData')
      if (!savedData) {
        // 저장된 데이터가 없으면 질문 페이지로 리다이렉트
        router.push('/question')
        return
      }

      // 이미 결과가 있으면 바로 표시 (하지만 새로고침해서 최신 데이터 가져오기)
      const savedResults = localStorage.getItem('recommendationResults')
      if (savedResults) {
        try {
          const parsed = JSON.parse(savedResults)
          console.log('Loading saved results:', {
            count: parsed.recommendations?.length,
            regions: parsed.recommendations?.map((r: any) => r.region)
          })
          // 저장된 결과가 유효한지 확인
          if (parsed.recommendations && parsed.recommendations.length > 0) {
            setRecommendations(parsed)
            setShowResults(true)
            // 저장된 결과를 사용하되, 백그라운드에서 새로고침
            // return // 일단 새로고침하도록 주석 처리
          }
        } catch (e) {
          console.error('Failed to load saved results:', e)
          localStorage.removeItem('recommendationResults')
        }
      }

      // 새로 추천 요청
      try {
        const data = JSON.parse(savedData)
        setLoading(true)
        setError(null)

        // ageGroup 형식 변환 (예: '20-29세' -> '20-29')
        const ageGroup = data.ageGroup?.replace('세', '') || '20-29'
        
        // API 호출 - 질문에서 수집한 모든 정보를 실제 데이터 기반 추천에 활용
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || '/api'
        const response = await fetch(`${apiUrl}/recommend`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            age_group: ageGroup,
            gender: data.gender,
            preferred_industry: data.preferredIndustry || null,
            time_period: data.currentTime || null,
            is_weekend: data.isWeekend || false,
            purpose: data.purpose || null, // 방문 목적
            budget: data.budget || null, // 예산
            priority: data.priority || null, // 우선순위
          }),
        })

        const resultData = await response.json()
        
        console.log('📡 API Response status:', response.status)
        console.log('📡 API Response data:', resultData)
        console.log('📡 Response keys:', Object.keys(resultData))
        console.log('📡 Recommendations type:', typeof resultData.recommendations)
        console.log('📡 Recommendations is array:', Array.isArray(resultData.recommendations))
        
        if (!response.ok) {
          console.error('❌ API Error:', resultData)
          throw new Error(resultData.error || '추천 요청에 실패했습니다')
        }

        // 추천 결과가 비어있는지 확인
        if (!resultData.recommendations) {
          console.error('❌ No recommendations property in response!', resultData)
          throw new Error('추천 결과 형식이 올바르지 않습니다.')
        }
        
        if (!Array.isArray(resultData.recommendations)) {
          console.error('❌ Recommendations is not an array!', typeof resultData.recommendations, resultData.recommendations)
          throw new Error('추천 결과 형식이 올바르지 않습니다.')
        }
        
        if (resultData.recommendations.length === 0) {
          console.error('❌ Empty recommendations array:', resultData)
          throw new Error('추천 결과를 찾을 수 없습니다. 다시 시도해주세요.')
        }

        const result: RecommendationResponse = resultData
        console.log('✅ Received recommendations:', {
          count: result.recommendations.length,
          regions: result.recommendations.map(r => r?.region),
          firstRec: result.recommendations[0],
          allRecs: result.recommendations
        })
        
        setRecommendations(result)
        setShowResults(true)
        
        // 결과를 localStorage에 저장
        localStorage.setItem('recommendationResults', JSON.stringify(result))
      } catch (err) {
        setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다')
      } finally {
        setLoading(false)
      }
    }

    fetchRecommendations()
  }, [router])

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

  // 로딩 중이거나 에러가 있을 때만 표시
  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.resultCard}>
          <h1 className={styles.title}>추천 중...</h1>
          <p className={styles.description}>
            입력하신 정보를 바탕으로 실제 데이터와 로직을 활용하여 최적의 지역을 찾고 있습니다.
          </p>
          <div className={styles.loadingSpinner}>⏳</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.resultCard}>
          <h1 className={styles.title}>오류가 발생했습니다</h1>
          <div className={styles.error}>
            <p>❌ {error}</p>
            <p style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
              문제가 지속되면 질문 페이지로 돌아가 다시 시도해주세요.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
            <button
              onClick={handleGetRecommendations}
              className={styles.button}
            >
              다시 시도
            </button>
            <button
              onClick={() => router.push('/question')}
              className={styles.button}
              style={{ background: '#666' }}
            >
              질문 다시하기
            </button>
          </div>
        </div>
      </div>
    )
  }

  // 결과가 아직 없으면 (로딩 완료 전)
  return null
}

