'use client'

import { useState } from 'react'
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
    question: '평일 주로 언제 소비하시나요?',
    options: [
      '오전 (06:00-12:00)',
      '오후 (12:00-18:00)',
      '저녁 (18:00-23:00)',
      '심야 (23:00-06:00)',
    ],
  },
  {
    id: 2,
    question: '주말 주로 언제 소비하시나요?',
    options: [
      '오전 (06:00-12:00)',
      '오후 (12:00-18:00)',
      '저녁 (18:00-23:00)',
      '심야 (23:00-06:00)',
    ],
  },
  {
    id: 3,
    question: '선호하는 업종은 무엇인가요?',
    options: [
      '한식',
      '일식/양식',
      '카페/디저트',
      '쇼핑/백화점',
      '문화/여가',
      '기타',
    ],
  },
  {
    id: 4,
    question: '주로 소비하는 금액대는?',
    options: [
      '10만원 미만',
      '10만원 ~ 30만원',
      '30만원 ~ 50만원',
      '50만원 이상',
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
      // 모든 질문 완료 - 결과 페이지로 이동
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

