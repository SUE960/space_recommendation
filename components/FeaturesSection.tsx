'use client'

import styles from './FeaturesSection.module.css'

export function FeaturesSection() {
  const features = [
    {
      icon: '📊',
      title: '트렌드 지역 탐지',
      description: '업종별·시간대별 지역별 소비 데이터를 분석하여 트렌드 지역 자동 탐지',
    },
    {
      icon: '🎯',
      title: '개인 맞춤 매칭',
      description: '간단한 정보 입력으로 당신과 가장 유사한 소비 패턴을 가진 지역 발견',
    },
    {
      icon: '📍',
      title: '지역 기반 분석',
      description: '서울 각 구별 소비 특성과 성장률을 시각화하여 제공',
    },
    {
      icon: '✨',
      title: '실시간 추천',
      description: '집단 패턴과 실시간 데이터를 결합하여 최적의 지역 추천',
    },
  ]

  return (
    <section className={styles.featuresSection}>
      <div className={styles.sectionHeader}>
        <span className={styles.sectionTag}>FEATURES</span>
        <h2 className={styles.sectionTitle}>주요 기능</h2>
      </div>
      <div className={styles.featuresGrid}>
        {features.map((feature, index) => (
          <div key={index} className={styles.featureCard}>
            <div className={styles.featureIcon}>{feature.icon}</div>
            <h3 className={styles.featureTitle}>{feature.title}</h3>
            <p className={styles.featureDescription}>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

