'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import styles from './page.module.css'

interface Question {
  id: number
  question: string
  options: string[]
}

const questions: Question[] = [
  {
    id: 1,
    question: '지금 몇 시인가요?',
    options: [
      '오전 (06:00-12:00)',
      '오후 (12:00-18:00)',
      '저녁 (18:00-23:00)',
      '심야 (23:00-06:00)',
    ],
  },
  {
    id: 2,
    question: '방문하는 날은 주말인가요?',
    options: [
      '평일',
      '주말',
    ],
  },
  {
    id: 3,
    question: '지금 가고 싶은 목적은 무엇인가요?',
    options: [
      '식사',
      '카페/디저트',
      '쇼핑',
      '문화/여가',
      '운동/스포츠',
      '기타',
    ],
  },
  {
    id: 4,
    question: '예산은 어느 정도인가요?',
    options: [
      '5만원 미만',
      '5만원 ~ 10만원',
      '10만원 ~ 20만원',
      '20만원 이상',
    ],
  },
  {
    id: 5,
    question: '가장 중요하게 생각하는 것은?',
    options: [
      '접근성 (교통 편리)',
      '트렌드 (인기 지역)',
      '가격 (합리적)',
      '다양성 (다양한 옵션)',
    ],
  },
]

export default function QuestionPage() {
  const router = useRouter()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<string[]>([])
  const [selectedOption, setSelectedOption] = useState<string | null>(null)
  const [userPreferences, setUserPreferences] = useState<any>(null)

  // localStorage에서 기본 세팅 불러오기
  useEffect(() => {
    const savedData = localStorage.getItem('userPreferences')
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData)
        setUserPreferences(parsed)
      } catch (e) {
        console.error('Failed to load saved preferences:', e)
      }
    } else {
      // 기본 세팅이 없으면 홈으로 리다이렉트
      alert('먼저 기본 세팅을 완료해주세요!')
      router.push('/')
    }
  }, [router])

  const progress = ((currentQuestion + 1) / questions.length) * 100
  const currentQ = questions[currentQuestion]

  const handleNext = () => {
    if (!selectedOption) return

    const newAnswers = [...answers]
    newAnswers[currentQuestion] = selectedOption
    setAnswers(newAnswers)

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedOption(null)
    } else {
      // 모든 질문 완료 - 기본 세팅과 함께 추천 요청
      const allData = {
        // 기본 세팅 (localStorage에서 가져온 값)
        ageGroup: userPreferences?.ageGroup || '30-39세',
        gender: userPreferences?.gender || '남성',
        preferredIndustry: userPreferences?.selectedIndustries?.join(', ') || '',
        // 추가 질문 답변
        currentTime: answers[0] || '',
        isWeekend: answers[1] === '주말',
        purpose: answers[2] || '',
        budget: answers[3] || '',
        priority: answers[4] || '',
      }
      
      // localStorage에 임시 저장 (결과 페이지에서 사용)
      localStorage.setItem('recommendationData', JSON.stringify(allData))
      
      // 결과 페이지로 이동
      router.push('/result')
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
      setSelectedOption(answers[currentQuestion - 1] || null)
    }
  }

  const handleOptionSelect = (option: string) => {
    setSelectedOption(option)
  }

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className={styles.header}>
        <button onClick={() => router.push('/')} className={styles.homeButton}>
          ← 홈으로
        </button>
        <div className={styles.progressInfo}>
          <div className={styles.progressText}>{Math.round(progress)}%</div>
          <div className={styles.progressBar}>
            <div
              className={styles.progressFill}
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className={styles.questionNumber}>
            질문 {currentQuestion + 1}/{questions.length}
          </div>
        </div>
      </div>

      {/* Title Section */}
      {currentQuestion === 0 && (
        <div className={styles.titleSection}>
          <h1 className={styles.title}>지금 당장 갈 곳 추천</h1>
          <p className={styles.subtitle}>
            몇 가지 질문에 답하시면 지금 당장 가기 좋은 서울 지역을 추천해드립니다
          </p>
          {userPreferences && (
            <div className={styles.savedInfo}>
              <p className={styles.savedInfoText}>
                기본 세팅: {userPreferences.ageGroup} {userPreferences.gender}
                {userPreferences.selectedIndustries?.length > 0 && ` · ${userPreferences.selectedIndustries.join(', ')}`}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Question Card */}
      <div className={styles.questionCard}>
        <h2 className={styles.question}>{currentQ.question}</h2>

        <div className={styles.options}>
          {currentQ.options.map((option, index) => (
            <label
              key={index}
              className={`${styles.option} ${
                selectedOption === option ? styles.optionSelected : ''
              }`}
            >
              <input
                type="radio"
                name="option"
                value={option}
                checked={selectedOption === option}
                onChange={() => handleOptionSelect(option)}
                className={styles.radioInput}
              />
              <span className={styles.optionText}>{option}</span>
            </label>
          ))}
        </div>

        {/* Navigation Buttons */}
        <div className={styles.navigation}>
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className={`${styles.navButton} ${styles.prevButton} ${
              currentQuestion === 0 ? styles.disabled : ''
            }`}
          >
            ← 이전
          </button>
          <button
            onClick={handleNext}
            disabled={!selectedOption}
            className={`${styles.navButton} ${styles.nextButton} ${
              !selectedOption ? styles.disabled : ''
            }`}
          >
            다음 →
          </button>
        </div>
      </div>
    </div>
  )
}

