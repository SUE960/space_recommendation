'use client'

import { useState, useEffect } from 'react'
import TrendMap from '@/components/TrendMap'
import styles from './page.module.css'

interface Hotspot {
  순위: number
  핫스팟명: string
  핫스팟코드: string
  실시간지역프로필점수: number
  실시간등급: string
  상권활성도: number
  특화점수: number
  인구통계: number
  특화업종: string
  결제건수: number
  결제금액: number
  업종수: number
}

export default function TrendMapPage() {
  const [hotspots, setHotspots] = useState<Hotspot[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<'all' | 'active' | 'normal'>('all')

  useEffect(() => {
    // 72개 핫스팟 데이터 로드
    fetch('/api/hotspots')
      .then((res) => {
        if (!res.ok) throw new Error('데이터 로드 실패')
        return res.json()
      })
      .then((hotspotData) => {
        if (hotspotData && hotspotData.length > 0) {
          setHotspots(hotspotData)
        } else {
          setError('데이터가 없습니다.')
        }
        setLoading(false)
      })
      .catch((err) => {
        setError('데이터를 불러오는데 실패했습니다.')
        setLoading(false)
        console.error(err)
      })
  }, [])

  const filteredHotspots = hotspots.filter((hotspot) => {
    if (filter === 'all') return true
    if (filter === 'active') {
      return hotspot.실시간등급.includes('활성화')
    }
    return hotspot.실시간등급.includes('보통')
  })

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>지도 데이터를 불러오는 중...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>서울 트렌드 맵</h1>
        <p className={styles.description}>
          72개 핫스팟의 실시간 지역 프로필 점수를 지도에서 확인하세요
        </p>
      </div>

      <div className={styles.filters}>
        <button
          className={`${styles.filterButton} ${filter === 'all' ? styles.active : ''}`}
          onClick={() => setFilter('all')}
        >
          전체 ({hotspots.length})
        </button>
        <button
          className={`${styles.filterButton} ${filter === 'active' ? styles.active : ''}`}
          onClick={() => setFilter('active')}
        >
          활성화 지역 ({hotspots.filter((h) => h.실시간등급.includes('활성화')).length})
        </button>
        <button
          className={`${styles.filterButton} ${filter === 'normal' ? styles.active : ''}`}
          onClick={() => setFilter('normal')}
        >
          보통 지역 ({hotspots.filter((h) => h.실시간등급.includes('보통')).length})
        </button>
      </div>

      <div className={styles.legend}>
        <div className={styles.legendItem}>
          <div className={styles.legendColor} style={{ backgroundColor: '#FF6B6B' }}></div>
          <span>70점 이상 (활성화)</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.legendColor} style={{ backgroundColor: '#FFA500' }}></div>
          <span>60-69점</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.legendColor} style={{ backgroundColor: '#FFD700' }}></div>
          <span>50-59점</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.legendColor} style={{ backgroundColor: '#90EE90' }}></div>
          <span>50점 미만</span>
        </div>
      </div>

      <TrendMap hotspots={filteredHotspots} />

      <div className={styles.stats}>
        <div className={styles.statCard}>
          <div className={styles.statValue}>{hotspots.length}</div>
          <div className={styles.statLabel}>전체 핫스팟</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statValue}>
            {hotspots.filter((h) => h.실시간등급.includes('활성화')).length}
          </div>
          <div className={styles.statLabel}>활성화 지역</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statValue}>
            {hotspots.length > 0
              ? (hotspots.reduce((sum, h) => sum + h.실시간지역프로필점수, 0) / hotspots.length).toFixed(1)
              : 0}
          </div>
          <div className={styles.statLabel}>평균 점수</div>
        </div>
      </div>
    </div>
  )
}
