'use client'

import styles from './CTASection.module.css'

interface CTASectionProps {
  onStartClick?: () => void
}

export function CTASection({ onStartClick }: CTASectionProps) {
  const handleScrollToForm = () => {
    if (onStartClick) {
      onStartClick()
    } else {
      const formSection = document.getElementById('recommendation-section')
      if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth' })
      }
    }
  }

  return (
    <section className={styles.ctaSection}>
      <div className={styles.ctaContainer}>
        <div className={styles.ctaContent}>
          <div className={styles.ctaVisual}>
            <div className={styles.visualCircle}></div>
            <div className={styles.visualCircle}></div>
            <div className={styles.visualCircle}></div>
          </div>
          <div className={styles.ctaText}>
            <span className={styles.ctaTag}>무료 체험</span>
            <h2 className={styles.ctaTitle}>지금 바로 시작하세요</h2>
            <p className={styles.ctaDescription}>
              간단한 정보 입력으로 당신에게 최적화된 지역을 추천받아보세요.
            </p>
            <button onClick={handleScrollToForm} className={styles.ctaButton}>
              지역 추천 시작하기 →
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}

