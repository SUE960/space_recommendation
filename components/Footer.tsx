'use client'

import styles from './Footer.module.css'

export function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContent}>
        <p className={styles.copyright}>
          © 2024 Seoul Card Pattern Analysis. AI 기반 소비 패턴 분석 서비스
        </p>
      </div>
    </footer>
  )
}

