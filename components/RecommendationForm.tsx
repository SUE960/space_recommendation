'use client'

import { useState, useRef, useEffect } from 'react'
import styles from './RecommendationForm.module.css'

interface RecommendationFormProps {
  onSubmit: (formData: {
    ageGroup: string
    gender: string
    preferredIndustry: string
    timePeriod: string
    isWeekend: boolean
  }) => void
  loading: boolean
}

const INDUSTRIES = [
  '한식',
  '일식',
  '양식',
  '중식',
  '카페/디저트',
  '패스트푸드',
  '대형마트',
  '편의점',
  '의류/패션',
  '화장품/뷰티',
  '문화/여가',
  '스포츠',
  '병원/약국',
  '학원/교육',
]

export function RecommendationForm({ onSubmit, loading }: RecommendationFormProps) {
  const [ageGroup, setAgeGroup] = useState('30-39세')
  const [gender, setGender] = useState('남성')
  const [selectedIndustries, setSelectedIndustries] = useState<string[]>([])
  const [isIndustryDropdownOpen, setIsIndustryDropdownOpen] = useState(false)
  const [timePeriod, setTimePeriod] = useState('')
  const [isWeekend, setIsWeekend] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsIndustryDropdownOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const toggleIndustry = (industry: string) => {
    setSelectedIndustries(prev =>
      prev.includes(industry)
        ? prev.filter(i => i !== industry)
        : [...prev, industry]
    )
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      ageGroup,
      gender,
      preferredIndustry: selectedIndustries.join(', '),
      timePeriod,
      isWeekend,
    })
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.formGroup}>
        <label htmlFor="ageGroup">연령대</label>
        <select
          id="ageGroup"
          value={ageGroup}
          onChange={(e) => setAgeGroup(e.target.value)}
          required
        >
          <option value="20세미만">20세 미만</option>
          <option value="20-29세">20-29세</option>
          <option value="30-39세">30-39세</option>
          <option value="40-49세">40-49세</option>
          <option value="50-59세">50-59세</option>
          <option value="60-69세">60-69세</option>
          <option value="70세이상">70세 이상</option>
        </select>
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="gender">성별</label>
        <select
          id="gender"
          value={gender}
          onChange={(e) => setGender(e.target.value)}
          required
        >
          <option value="남성">남성</option>
          <option value="여성">여성</option>
        </select>
      </div>

      <div className={styles.formGroup} ref={dropdownRef}>
        <label>선호 업종 (선택)</label>
        <div
          className={styles.multiSelectTrigger}
          onClick={() => setIsIndustryDropdownOpen(!isIndustryDropdownOpen)}
        >
          <span className={styles.multiSelectText}>
            {selectedIndustries.length === 0
              ? '예: 한식, 대형마트, 일식 등'
              : selectedIndustries.join(', ')}
          </span>
          <svg
            className={styles.multiSelectArrow}
            width="18"
            height="18"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            style={{
              transform: isIndustryDropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            }}
          >
            <path
              d="M4 6L8 10L12 6"
              stroke="#666666"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        {isIndustryDropdownOpen && (
          <div className={styles.multiSelectDropdown}>
            {INDUSTRIES.map((industry) => (
              <label key={industry} className={styles.multiSelectOption}>
                <input
                  type="checkbox"
                  checked={selectedIndustries.includes(industry)}
                  onChange={() => toggleIndustry(industry)}
                  className={styles.multiSelectCheckbox}
                />
                <span>{industry}</span>
              </label>
            ))}
          </div>
        )}
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="timePeriod">시간대 (선택)</label>
        <select
          id="timePeriod"
          value={timePeriod}
          onChange={(e) => setTimePeriod(e.target.value)}
        >
          <option value="">선택 안함</option>
          <option value="점심(12-18시)">점심 (12-18시)</option>
          <option value="오후(18-24시)">오후 (18-24시)</option>
          <option value="저녁">저녁</option>
        </select>
      </div>

      <div className={styles.formGroup}>
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            checked={isWeekend}
            onChange={(e) => setIsWeekend(e.target.checked)}
          />
          <span>주말 여부</span>
        </label>
      </div>

      <button type="submit" className={styles.submitButton} disabled={loading}>
        {loading ? '추천 중...' : '지역 추천 받기'}
      </button>
    </form>
  )
}

