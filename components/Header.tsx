'use client'

import { useRouter } from 'next/navigation'
import styles from './Header.module.css'

export function Header() {
  const router = useRouter()

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logo} onClick={() => router.push('/')}>
          <span className={styles.logoText}>서울 추천 서비스</span>
        </div>

        <nav className={styles.nav}>
          <button
            onClick={() => router.push('/question')}
            className={styles.navButton}
          >
            개인정보 입력하기
          </button>
          <button
            onClick={() => {
              const section = document.getElementById('recommendation-section')
              if (section) {
                section.scrollIntoView({ behavior: 'smooth' })
              }
            }}
            className={styles.navButtonSecondary}
          >
            추천받기
          </button>
        </nav>
      </div>
    </header>
  )
}


