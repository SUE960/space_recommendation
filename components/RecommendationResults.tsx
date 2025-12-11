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
  console.log('RecommendationResults received:', { 
    recsCount: recs?.length, 
    recs: recs,
    firstRec: recs?.[0] 
  })
  
  // TOP 3로 제한
  const topRecs = (recs || []).slice(0, 3)
  
  // 추천 결과가 없으면 메시지 표시
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
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <p>추천 결과를 불러오는 중입니다...</p>
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
                <div className={styles.details}>
                  {rec.specialization && (
                    <div className={styles.detailItem}>
                      <span className={styles.detailLabel}>특화 업종:</span>
                      <span className={styles.detailValue}>
                        {rec.specialization}
                        {rec.specialization_ratio && ` (${rec.specialization_ratio}%)`}
                      </span>
                    </div>
                  )}
                  <div className={styles.detailItem}>
                    <span className={styles.detailLabel}>안정성:</span>
                    <span className={styles.detailValue}>{rec.stability}</span>
                  </div>
                  {rec.growth_rate !== null && rec.growth_rate > 0 && (
                    <div className={styles.detailItem}>
                      <span className={styles.detailLabel}>성장률:</span>
                      <span className={styles.detailValue}>
                        <span className={styles.growthPositive}>+{rec.growth_rate.toFixed(2)}%</span>
                      </span>
                    </div>
                  )}
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

