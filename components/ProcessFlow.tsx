'use client'

import styles from './ProcessFlow.module.css'

export function ProcessFlow() {
  const steps = [
    {
      id: 1,
      title: '정적 집단 프로필 생성',
      logo: '서울특별시 빅데이터 캠퍼스',
      dataSource: '서울 시민 카드 데이터 활용',
      description: '연령대·성별·업종·지역 단위의 집단 소비 성향 추출',
      logoColor: '#e74c3c',
    },
    {
      id: 2,
      title: '실시간 지역 프로필 산출',
      logo: '서울 열린데이터 광장',
      dataSource: '실시간 상권 데이터 활용',
      description: '실시간 지역 점수 산출\n방문자 특성에 지역 프로필 도출',
      logoColor: '#f39c12',
    },
    {
      id: 3,
      title: '사용자 입력 기반 매칭',
      logo: null,
      dataSource: null,
      description: '사용자 → 집단 → 지역\n개인 데이터가 없으므로\n사용자 입력한 정보를 집단 패턴과 매칭',
      logoColor: null,
    },
    {
      id: 4,
      title: '최종 추천',
      logo: null,
      dataSource: null,
      description: '집단 패턴 & 현 실시간 데이터\n& 사용자 입력 정보 결합해 추천 생성',
      logoColor: null,
      isFinal: true,
    },
  ]

  return (
    <div className={styles.processFlow}>
      {steps.map((step, index) => (
        <div key={step.id} className={styles.stepContainer}>
          <div
            className={`${styles.step} ${step.isFinal ? styles.finalStep : ''}`}
          >
            {step.logo && (
              <div className={styles.logoContainer}>
                <div
                  className={styles.logo}
                  style={{ color: step.logoColor }}
                >
                  {step.logo === '서울특별시 빅데이터 캠퍼스' ? (
                    <BigDataLogo />
                  ) : (
                    <OpenDataLogo />
                  )}
                </div>
                <p className={styles.logoText}>{step.logo}</p>
              </div>
            )}

            {step.dataSource && (
              <p className={styles.dataSource}>{step.dataSource}</p>
            )}

            <h3 className={styles.stepTitle}>{step.title}</h3>

            <div className={styles.description}>
              {step.description.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
            </div>
          </div>

          {index < steps.length - 1 && (
            <div className={styles.arrow}>
              <svg
                width="40"
                height="40"
                viewBox="0 0 40 40"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M15 10L25 20L15 30"
                  stroke="#667eea"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

// 서울특별시 빅데이터 캠퍼스 로고 (점들로 표현)
function BigDataLogo() {
  return (
    <svg width="80" height="80" viewBox="0 0 80 80" fill="currentColor">
      {/* 빨간색 점들 */}
      <circle cx="20" cy="20" r="6" fill="#e74c3c" />
      <circle cx="40" cy="15" r="5" fill="#e74c3c" />
      <circle cx="60" cy="25" r="7" fill="#e74c3c" />
      <circle cx="25" cy="40" r="5" fill="#e74c3c" />
      <circle cx="50" cy="35" r="6" fill="#e74c3c" />
      {/* 파란색 점들 */}
      <circle cx="30" cy="30" r="5" fill="#3498db" />
      <circle cx="55" cy="20" r="6" fill="#3498db" />
      <circle cx="15" cy="50" r="5" fill="#3498db" />
      <circle cx="45" cy="50" r="6" fill="#3498db" />
      <circle cx="65" cy="45" r="5" fill="#3498db" />
    </svg>
  )
}

// 서울 열린데이터 광장 로고 (8자 모양)
function OpenDataLogo() {
  return (
    <svg width="80" height="80" viewBox="0 0 80 80" fill="currentColor">
      <path
        d="M 20 10 Q 10 10 10 20 Q 10 30 20 30 Q 30 30 30 20 Q 30 10 20 10 Z M 20 50 Q 10 50 10 60 Q 10 70 20 70 Q 30 70 30 60 Q 30 50 20 50 Z"
        fill="#f39c12"
        stroke="#f39c12"
        strokeWidth="2"
      />
      <path
        d="M 60 10 Q 50 10 50 20 Q 50 30 60 30 Q 70 30 70 20 Q 70 10 60 10 Z M 60 50 Q 50 50 50 60 Q 50 70 60 70 Q 70 70 70 60 Q 70 50 60 50 Z"
        fill="#f39c12"
        stroke="#f39c12"
        strokeWidth="2"
      />
    </svg>
  )
}

