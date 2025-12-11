'use client'

import { useState } from 'react'
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

export function RecommendationForm({ onSubmit, loading }: RecommendationFormProps) {
  const [ageGroup, setAgeGroup] = useState('30-39세')
  const [gender, setGender] = useState('남성')
  const [preferredIndustry, setPreferredIndustry] = useState('')
  const [timePeriod, setTimePeriod] = useState('')
  const [isWeekend, setIsWeekend] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      ageGroup,
      gender,
      preferredIndustry,
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

      <div className={styles.formGroup}>
        <label htmlFor="preferredIndustry">선호 업종 (선택)</label>
        <input
          id="preferredIndustry"
          type="text"
          value={preferredIndustry}
          onChange={(e) => setPreferredIndustry(e.target.value)}
          placeholder="예: 한식, 대형마트, 일식 등"
        />
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

