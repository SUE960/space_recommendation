'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import styles from './page.module.css'

interface Question {
  id: number
  question: string
  options: { label: string; value: string }[]
  field: string
}

const questions: Question[] = [
  {
    id: 1,
    question: '연령대를 선택해주세요',
    options: [
      { label: '20세 미만', value: '20세미만' },
      { label: '20-29세', value: '20-29세' },
      { label: '30-39세', value: '30-39세' },
      { label: '40-49세', value: '40-49세' },
      { label: '50-59세', value: '50-59세' },
      { label: '60-69세', value: '60-69세' },
      { label: '70세 이상', value: '70세이상' },
    ],
    field: 'age_group',
  },
  {
    id: 2,
    question: '성별을 선택해주세요',
    options: [
      { label: '남성', value: '남성' },
      { label: '여성', value: '여성' },
    ],
    field: 'gender',
  },
  {
    id: 3,
    question: '주로 언제 소비하시나요?',
    options: [
      { label: '점심 (12-18시)', value: '점심(12-18시)' },
      { label: '오후 (18-24시)', value: '오후(18-24시)' },
      { label: '저녁', value: '저녁' },
    ],
    field: 'time_period',
  },
  {
    id: 4,
    question: '선호하는 업종을 선택해주세요 (선택사항)',
    options: [
      { label: '한식', value: '한식' },
      { label: '일식', value: '일식' },
      { label: '양식', value: '양식' },
      { label: '대형마트', value: '대형마트' },
      { label: '편의점', value: '편의점' },
      { label: '전자상거래', value: '전자상거래' },
      { label: '백화점', value: '백화점' },
      { label: '선택 안함', value: '' },
    ],
    field: 'preferred_industry',
  },
  {
    id: 5,
    question: '주말에 주로 소비하시나요?',
    options: [
      { label: '네, 주말에 주로 소비합니다', value: 'true' },
      { label: '아니요, 평일에 주로 소비합니다', value: 'false' },
    ],
    field: 'is_weekend',
  },
]

interface Answers {
  age_group?: string
  gender?: string
  time_period?: string
  preferred_industry?: string
  is_weekend?: boolean
}

export default function QuestionPage() {
  const router = useRouter()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Answers>({})
  const [selectedOption, setSelectedOption] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const progress = ((currentQuestion + 1) / questions.length) * 100
  const currentQ = questions[currentQuestion]

  // 현재 질문의 저장된 답변 불러오기
  useEffect(() => {
    const currentAnswer = answers[currentQ.field as keyof Answers]
    if (currentAnswer !== undefined) {
      setSelectedOption(
        typeof currentAnswer === 'boolean' ? String(currentAnswer) : currentAnswer
      )
    } else {
      setSelectedOption(null)
    }
  }, [currentQuestion, currentQ.field, answers])

  const handleNext = async () => {
    if (!selectedOption) return

    const newAnswers = { ...answers }
    const field = currentQ.field as keyof Answers
    
    // 값 변환
    if (field === 'is_weekend') {
      newAnswers[field] = selectedOption === 'true'
    } else if (field === 'preferred_industry') {
      newAnswers[field] = selectedOption === '' ? undefined : selectedOption
    } else {
      newAnswers[field] = selectedOption as any
    }
    
    setAnswers(newAnswers)

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedOption(null)
    } else {
      // 모든 질문 완료 - API 호출 후 결과 페이지로 이동
      await submitAnswers(newAnswers)
    }
  }

  const submitAnswers = async (finalAnswers: Answers) => {
    setLoading(true)
    try {
      // 연령대를 숫자로 변환 (예: "20-29세" -> 25)
      const ageGroupToNumber = (ageGroup: string): number => {
        if (ageGroup === '20세미만') return 18
        if (ageGroup === '70세이상') return 70
        const match = ageGroup.match(/(\d+)-(\d+)/)
        if (match) {
          const [, min, max] = match
          return Math.floor((parseInt(min) + parseInt(max)) / 2)
        }
        return 30 // 기본값
      }

      // 로컬 개발: http://localhost:8000
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          age: ageGroupToNumber(finalAnswers.age_group || '30-39세'),
          gender: finalAnswers.gender === '남성' ? '남' : '여',
          income_level: '중',
          preferred_industries: finalAnswers.preferred_industry ? [finalAnswers.preferred_industry] : ['한식'],
          time_period: finalAnswers.time_period || '저녁',
          is_weekend: finalAnswers.is_weekend || false,
          preference_type: '활발한',
        }),
      })

      if (!response.ok) {
        throw new Error('추천 요청에 실패했습니다')
      }

      const data = await response.json()
      sessionStorage.setItem('recommendations', JSON.stringify(data))
      router.push('/result')
    } catch (err) {
      console.error('Error:', err)
      alert('추천 요청 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
    }
  }

  const handleOptionSelect = (value: string) => {
    setSelectedOption(value)
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
                selectedOption === option.value ? styles.optionSelected : ''
              }`}
            >
              <input
                type="radio"
                name="option"
                value={option.value}
                checked={selectedOption === option.value}
                onChange={() => handleOptionSelect(option.value)}
                className={styles.radioInput}
              />
              <span className={styles.optionText}>{option.label}</span>
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
            disabled={!selectedOption || loading}
            className={`${styles.navButton} ${styles.nextButton} ${
              !selectedOption || loading ? styles.disabled : ''
            }`}
          >
            {loading ? '처리 중...' : currentQuestion === questions.length - 1 ? '결과 보기 →' : '다음 →'}
          </button>
        </div>
      </div>
    </div>
  )
}

