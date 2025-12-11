'use client'

import { useRouter } from 'next/navigation'
import Image from 'next/image'
import styles from './Header.module.css'

export function Header() {
  const router = useRouter()

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logo} onClick={() => router.push('/')}>
          <Image
            src="/logo.png"
            alt="서울 추천 서비스"
            width={180}
            height={40}
            className={styles.logoImage}
            priority
          />
        </div>

        <nav className={styles.nav}>
          <button
            onClick={() => {
              router.push('/')
              setTimeout(() => {
                const section = document.getElementById('recommendation-section')
                if (section) {
                  section.scrollIntoView({ behavior: 'smooth' })
                }
              }, 100)
            }}
            className={styles.navButton}
          >
            기본 세팅하기
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


