'use client'

import styles from './RecommendationResults.module.css'

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

interface RecommendationResultsProps {
  recommendations: RecommendationResponse
}

export function RecommendationResults({ recommendations }: RecommendationResultsProps) {
  const { recommendations: recs, user_profile } = recommendations
  
  // 디버깅: 받은 데이터 확인
  console.log('🔍 RecommendationResults received:', { 
    recsCount: recs?.length, 
    recs: recs,
    firstRec: recs?.[0],
    allRegions: recs?.map(r => r?.region),
    fullResponse: recommendations
  })
  
  // 데이터 검증 및 필터링
  let topRecs: Recommendation[] = []
  
  if (recs && Array.isArray(recs) && recs.length > 0) {
    // 유효한 추천만 필터링
    const validRecs = recs.filter(rec => {
      if (!rec) return false
      if (!rec.region || typeof rec.region !== 'string' || rec.region.trim() === '') {
        console.warn('❌ Invalid rec (no region):', rec)
        return false
      }
      return true
    })
    
    console.log(`✅ Valid recs: ${validRecs.length} out of ${recs.length}`)
    
    if (validRecs.length > 0) {
      topRecs = validRecs.slice(0, 3)
      console.log('✅ Top 3 recs:', topRecs.map(r => ({ region: r.region, score: r.score })))
    } else {
      console.error('❌ No valid recommendations after filtering!')
    }
  } else {
    console.error('❌ No recommendations array or empty array!', { recs, type: typeof recs })
  }
  
  console.log('📊 Final topRecs:', {
    count: topRecs.length,
    regions: topRecs.map(r => r.region)
  })
  
  // 추천 결과가 없으면 에러 메시지 표시 (구글 애드센스 정책: 빈 페이지에 광고 금지)
  if (!topRecs || topRecs.length === 0) {
    return (
      <div className={styles.results}>
        <div className={styles.profileSection}>
          <h3 className={styles.profileTitle}>입력하신 정보</h3>
          <div className={styles.profileInfo}>
            <div className={styles.profileItem}>
              <span className={styles.profileLabel}>연령대:</span>
              <span className={styles.profileValue}>{user_profile.age_group}</span>
            </div>
            <div className={styles.profileItem}>
              <span className={styles.profileLabel}>성별:</span>
              <span className={styles.profileValue}>{user_profile.gender}</span>
            </div>
            {user_profile.preferred_industry && (
              <div className={styles.profileItem}>
                <span className={styles.profileLabel}>선호 업종:</span>
                <span className={styles.profileValue}>{user_profile.preferred_industry}</span>
              </div>
            )}
            {user_profile.time_period && (
              <div className={styles.profileItem}>
                <span className={styles.profileLabel}>시간대:</span>
                <span className={styles.profileValue}>{user_profile.time_period}</span>
              </div>
            )}
            <div className={styles.profileItem}>
              <span className={styles.profileLabel}>주말 여부:</span>
              <span className={styles.profileValue}>{user_profile.is_weekend ? '주말' : '평일'}</span>
            </div>
          </div>
        </div>
        <div className={styles.recommendationsSection}>
          <h3 className={styles.recommendationsTitle}>추천 지역 Top 3</h3>
          <div style={{ 
            textAlign: 'center', 
            padding: '60px 40px', 
            background: '#fff',
            borderRadius: '16px',
            border: '2px solid #f0f0f0'
          }}>
            <p style={{ fontSize: '18px', color: '#333', marginBottom: '10px', fontWeight: '600' }}>
              추천 결과를 불러올 수 없습니다
            </p>
            <p style={{ fontSize: '14px', color: '#666', marginBottom: '20px' }}>
              데이터를 다시 불러오는 중입니다. 잠시만 기다려주세요.
            </p>
            <button 
              onClick={() => window.location.reload()} 
              style={{
                padding: '12px 24px',
                background: '#FF7426',
                color: '#fff',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              새로고침
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.results}>
      <div className={styles.profileSection}>
        <h3 className={styles.profileTitle}>입력하신 정보</h3>
        <div className={styles.profileInfo}>
          <div className={styles.profileItem}>
            <span className={styles.profileLabel}>연령대:</span>
            <span className={styles.profileValue}>{user_profile.age_group}</span>
          </div>
          <div className={styles.profileItem}>
            <span className={styles.profileLabel}>성별:</span>
            <span className={styles.profileValue}>{user_profile.gender}</span>
          </div>
          {user_profile.preferred_industry && (
            <div className={styles.profileItem}>
              <span className={styles.profileLabel}>선호 업종:</span>
              <span className={styles.profileValue}>{user_profile.preferred_industry}</span>
            </div>
          )}
          {user_profile.time_period && (
            <div className={styles.profileItem}>
              <span className={styles.profileLabel}>시간대:</span>
              <span className={styles.profileValue}>{user_profile.time_period}</span>
            </div>
          )}
          <div className={styles.profileItem}>
            <span className={styles.profileLabel}>주말 여부:</span>
            <span className={styles.profileValue}>{user_profile.is_weekend ? '주말' : '평일'}</span>
          </div>
        </div>
      </div>

      <div className={styles.recommendationsSection}>
        <h3 className={styles.recommendationsTitle}>추천 지역 Top 3</h3>
        <div className={styles.recommendationsList}>
          {topRecs.map((rec, index) => {
            // 지역 이름이 없으면 렌더링하지 않음
            if (!rec.region || rec.region.trim() === '') {
              console.error('Recommendation without region name:', rec)
              return null
            }
            
            return (
            <div key={rec.region || index} className={styles.recommendationCard}>
              <div className={styles.rankBadge}>
                {index + 1}
              </div>
              <div className={styles.cardContent}>
                <div className={styles.regionHeader}>
                  <h4 className={styles.regionName}>{rec.region}</h4>
                </div>
                <div className={styles.scoreBar}>
                  <div className={styles.scoreLabel}>추천 점수</div>
                  <div className={styles.scoreValue}>{rec.score.toFixed(2)}</div>
                  <div className={styles.scoreBarContainer}>
                    <div
                      className={styles.scoreBarFill}
                      style={{ width: `${(rec.score / topRecs[0].score) * 100}%` }}
                    />
                  </div>
                </div>
                <div className={styles.reason}>
                  <span className={styles.reasonLabel}>💡 추천 이유:</span>
                  <span className={styles.reasonText}>{rec.reason}</span>
                </div>
              </div>
            </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

