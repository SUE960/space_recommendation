'use client'

import { useRouter } from 'next/navigation'
import styles from './page.module.css'

export default function ResultPage() {
  const router = useRouter()

  return (
    <div className={styles.container}>
      <div className={styles.resultCard}>
        <h1 className={styles.title}>질문이 완료되었습니다!</h1>
        <p className={styles.description}>
          입력하신 정보를 바탕으로 지역을 추천해드리겠습니다.
        </p>
        <button
          onClick={() => router.push('/')}
          className={styles.button}
        >
          추천 결과 보기 →
        </button>
      </div>
    </div>
  )
}

