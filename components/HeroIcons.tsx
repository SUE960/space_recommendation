'use client'

import styles from './HeroIcons.module.css'

export function HeroIcons() {
  return (
    <div className={styles.iconsContainer}>
      {/* 노란색 레고 블록 (좌상단) - 큰 블록 */}
      <div className={styles.legoBlock} style={{ top: '-30px', left: '3%', animationDelay: '0s', transform: 'rotate(-15deg)' }}>
        <div className={styles.blockTop} style={{ background: '#FFD700', width: '280px', height: '280px' }}>
          <div className={styles.stud} style={{ left: '20%', top: '20%', width: '48px', height: '48px' }} />
          <div className={styles.stud} style={{ left: '50%', top: '20%', width: '48px', height: '48px' }} />
          <div className={styles.stud} style={{ left: '80%', top: '20%', width: '48px', height: '48px' }} />
          <div className={styles.stud} style={{ left: '20%', top: '50%', width: '48px', height: '48px' }} />
          <div className={styles.stud} style={{ left: '50%', top: '50%', width: '48px', height: '48px' }} />
          <div className={styles.stud} style={{ left: '80%', top: '50%', width: '48px', height: '48px' }} />
        </div>
        <div className={styles.blockSide} style={{ background: '#FFC107', width: '280px', height: '80px', top: '280px' }} />
      </div>

      {/* 주황색 레고 블록 (우상단) */}
      <div className={styles.legoBlock} style={{ top: '8%', right: '5%', animationDelay: '0.5s', transform: 'rotate(12deg)' }}>
        <div className={styles.blockTop} style={{ background: '#FF8C42', width: '240px', height: '240px' }}>
          <div className={styles.stud} style={{ left: '25%', top: '25%', width: '42px', height: '42px' }} />
          <div className={styles.stud} style={{ left: '75%', top: '25%', width: '42px', height: '42px' }} />
          <div className={styles.stud} style={{ left: '25%', top: '75%', width: '42px', height: '42px' }} />
          <div className={styles.stud} style={{ left: '75%', top: '75%', width: '42px', height: '42px' }} />
        </div>
        <div className={styles.blockSide} style={{ background: '#FF6B35', width: '240px', height: '70px', top: '240px' }} />
      </div>

      {/* 파란색 레고 블록 (중앙 좌측) - 세로 블록 */}
      <div className={styles.legoBlock} style={{ top: '40%', left: '5%', animationDelay: '1s', transform: 'rotate(-12deg)' }}>
        <div className={styles.blockTop} style={{ background: '#3B82F6', width: '160px', height: '320px' }}>
          <div className={styles.stud} style={{ left: '30%', top: '15%', width: '36px', height: '36px' }} />
          <div className={styles.stud} style={{ left: '30%', top: '40%', width: '36px', height: '36px' }} />
          <div className={styles.stud} style={{ left: '30%', top: '65%', width: '36px', height: '36px' }} />
          <div className={styles.stud} style={{ left: '30%', top: '90%', width: '36px', height: '36px' }} />
        </div>
        <div className={styles.blockSide} style={{ background: '#2563EB', width: '160px', height: '80px', top: '320px' }} />
      </div>

      {/* 빨간색 레고 블록 (우하단) */}
      <div className={styles.legoBlock} style={{ bottom: '5%', right: '8%', animationDelay: '1.5s', transform: 'rotate(-8deg)' }}>
        <div className={styles.blockTop} style={{ background: '#EF4444', width: '200px', height: '120px' }}>
          <div className={styles.stud} style={{ left: '30%', top: '30%', width: '38px', height: '38px' }} />
          <div className={styles.stud} style={{ left: '70%', top: '30%', width: '38px', height: '38px' }} />
        </div>
        <div className={styles.blockSide} style={{ background: '#DC2626', width: '200px', height: '60px', top: '120px' }} />
      </div>

      {/* 초록색 스프링 (중앙 우측) - 큰 스프링 */}
      <div className={styles.spring} style={{ top: '35%', right: '10%', animationDelay: '2s' }}>
        <div className={styles.springCoil} style={{ color: '#10B981', width: '240px', height: '360px' }} />
      </div>

      {/* 파란색 스프링 (좌하단) */}
      <div className={styles.spring} style={{ bottom: '8%', left: '8%', animationDelay: '2.5s' }}>
        <div className={styles.springCoil} style={{ color: '#3B82F6', width: '200px', height: '300px' }} />
      </div>
    </div>
  )
}
