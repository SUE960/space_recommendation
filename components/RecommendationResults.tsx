'use client'

import styles from './RecommendationResults.module.css'

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

interface RecommendationResultsProps {
  recommendations: RecommendationResponse
}

export function RecommendationResults({ recommendations }: RecommendationResultsProps) {
  const { recommendations: recs, user_profile } = recommendations

  return (
    <div className={styles.results}>
      {/* 사용자 프로필 섹션 */}
      <div className={styles.profileSection}>
        <h3 className={styles.profileTitle}>🎯 이중 매칭 결과</h3>
        <div className={styles.profileGrid}>
          <div className={styles.profileCard}>
            <h4>정적 프로필 매칭</h4>
            <p className={styles.segmentInfo}>
              매칭 세그먼트: <strong>{user_profile.segment_description}</strong>
            </p>
            <p className={styles.industries}>
              집단 선호 업종: {user_profile.top_segment_industries.slice(0, 3).join(', ')}
            </p>
          </div>
          <div className={styles.profileCard}>
            <h4>실시간 선호도</h4>
            <p className={styles.userPrefs}>
              선호 업종: <strong>{user_profile.preferred_industries.join(', ')}</strong>
            </p>
            <p className={styles.userPrefs}>
              {user_profile.time_period} · {user_profile.is_weekend ? '주말' : '평일'} · {user_profile.preference_type}
            </p>
          </div>
        </div>
      </div>

      {/* 추천 결과 섹션 */}
      <div className={styles.recommendationsSection}>
        <h3 className={styles.recommendationsTitle}>
          📍 추천 지역 Top {recs.length}
        </h3>
        <div className={styles.recommendationsList}>
          {recs.map((rec) => (
            <div key={rec.region} className={styles.recommendationCard}>
              <div className={styles.cardHeader}>
                <div className={styles.rankBadge}>{rec.rank}위</div>
                <div className={styles.regionInfo}>
                  <h4 className={styles.regionName}>{rec.region}</h4>
                  <span className={styles.grade}>{rec.grade}</span>
                </div>
                <div className={styles.finalScore}>
                  <span className={styles.scoreValue}>{rec.final_score.toFixed(1)}</span>
                  <span className={styles.scoreLabel}>점</span>
                </div>
              </div>

              {/* 이중 매칭 점수 */}
              <div className={styles.dualScores}>
                <div className={styles.scoreBox}>
                  <div className={styles.scoreBoxHeader}>
                    <span>정적 매칭</span>
                    <span className={styles.scoreBoxValue}>{rec.static_score.toFixed(1)}</span>
                  </div>
                  <div className={styles.scoreDetails}>
                    <div className={styles.scoreDetail}>
                      <span>업종</span>
                      <span>{rec.static_details.industry_match.toFixed(0)}점</span>
                    </div>
                    <div className={styles.scoreDetail}>
                      <span>인구통계</span>
                      <span>{rec.static_details.demographic_match.toFixed(0)}점</span>
                    </div>
                    <div className={styles.scoreDetail}>
                      <span>소비수준</span>
                      <span>{rec.static_details.spending_match.toFixed(0)}점</span>
                    </div>
                    <div className={styles.scoreDetail}>
                      <span>시간대</span>
                      <span>{rec.static_details.time_match.toFixed(0)}점</span>
                    </div>
                  </div>
                </div>

                <div className={styles.scoreBox}>
                  <div className={styles.scoreBoxHeader}>
                    <span>실시간 매칭</span>
                    <span className={styles.scoreBoxValue}>{rec.realtime_score.toFixed(1)}</span>
                  </div>
                  <div className={styles.scoreDetails}>
                    <div className={styles.scoreDetail}>
                      <span>선호업종</span>
                      <span>{rec.realtime_details.user_industry_match.toFixed(0)}점</span>
                    </div>
                    <div className={styles.scoreDetail}>
                      <span>종합점수</span>
                      <span>{rec.realtime_details.comprehensive_score.toFixed(0)}점</span>
                    </div>
                    <div className={styles.scoreDetail}>
                      <span>특화도</span>
                      <span>{rec.realtime_details.specialization_match.toFixed(0)}점</span>
                    </div>
                    <div className={styles.scoreDetail}>
                      <span>시간대</span>
                      <span>{rec.realtime_details.time_match.toFixed(0)}점</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* 특화 업종 */}
              <div className={styles.industries}>
                <span className={styles.industriesLabel}>특화 업종:</span>
                <div className={styles.industryTags}>
                  {rec.specialized_industries.map((industry) => (
                    <span key={industry} className={styles.industryTag}>
                      {industry}
                    </span>
                  ))}
                </div>
              </div>

              {/* 추천 이유 */}
              <div className={styles.reasons}>
                <span className={styles.reasonsLabel}>추천 이유:</span>
                <ul className={styles.reasonsList}>
                  {rec.reasons.map((reason, idx) => (
                    <li key={idx}>{reason}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
