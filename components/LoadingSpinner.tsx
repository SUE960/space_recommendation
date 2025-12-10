'use client'

import styles from './LoadingSpinner.module.css'

export function LoadingSpinner() {
  return (
    <div className={styles.loadingContainer}>
      <div className={styles.spinner}>
        <div className={styles.spinnerRing}></div>
        <div className={styles.spinnerRing}></div>
        <div className={styles.spinnerRing}></div>
      </div>
      <div className={styles.loadingText}>
        <h3>🔍 73개 지역 분석 중...</h3>
        <p>이중 매칭 알고리즘으로 최적의 지역을 찾고 있습니다</p>
        <div className={styles.steps}>
          <div className={styles.step}>✓ 정적 프로필 매칭</div>
          <div className={styles.step}>✓ 실시간 프로필 로드</div>
          <div className={styles.step}>⟳ 이중 매칭 점수 계산</div>
        </div>
      </div>
    </div>
  )
}

