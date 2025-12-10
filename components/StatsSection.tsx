'use client'

import styles from './StatsSection.module.css'

export function StatsSection() {
  const stats = [
    {
      number: '25개',
      label: '서울시 구',
      description: '전체 구 분석',
    },
    {
      number: '547일',
      label: '분석 기간',
      description: '카드 소비 데이터',
    },
    {
      number: '89%',
      label: '평균 정확도',
      description: '추천 만족도',
    },
  ]

  return (
    <section className={styles.statsSection}>
      <div className={styles.statsContainer}>
        {stats.map((stat, index) => (
          <div key={index} className={styles.statCard}>
            <div className={styles.statNumber}>{stat.number}</div>
            <div className={styles.statLabel}>{stat.label}</div>
            <div className={styles.statDescription}>{stat.description}</div>
          </div>
        ))}
      </div>
    </section>
  )
}

