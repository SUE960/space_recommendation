'use client'

import { useState } from 'react'
import styles from './RecommendationForm.module.css'

interface RecommendationFormProps {
  onSubmit: (formData: {
    age: number
    gender: string
    incomeLevel: string
    preferredIndustries: string[]
    timePeriod: string
    isWeekend: boolean
    preferenceType: string
  }) => void
  loading: boolean
}

export function RecommendationForm({ onSubmit, loading }: RecommendationFormProps) {
  const [age, setAge] = useState(28)
  const [gender, setGender] = useState('남')
  const [incomeLevel, setIncomeLevel] = useState('중')
  const [preferredIndustries, setPreferredIndustries] = useState<string[]>(['한식', '카페'])
  const [industryInput, setIndustryInput] = useState('')
  const [timePeriod, setTimePeriod] = useState('저녁')
  const [isWeekend, setIsWeekend] = useState(false)
  const [preferenceType, setPreferenceType] = useState('활발한')

  const handleAddIndustry = () => {
    if (industryInput && !preferredIndustries.includes(industryInput)) {
      setPreferredIndustries([...preferredIndustries, industryInput])
      setIndustryInput('')
    }
  }

  const handleRemoveIndustry = (industry: string) => {
    setPreferredIndustries(preferredIndustries.filter(i => i !== industry))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      age,
      gender,
      incomeLevel,
      preferredIndustries,
      timePeriod,
      isWeekend,
      preferenceType,
    })
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <h3 className={styles.formTitle}>🎯 이중 매칭 알고리즘 기반 추천</h3>
      
      <div className={styles.formSection}>
        <h4>기본 정보 (정적 프로필 매칭용)</h4>
        
        <div className={styles.formGroup}>
          <label htmlFor="age">나이</label>
          <input
            id="age"
            type="number"
            value={age}
            onChange={(e) => setAge(Number(e.target.value))}
            min={10}
            max={100}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="gender">성별</label>
          <select
            id="gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            required
          >
            <option value="남">남성</option>
            <option value="여">여성</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="incomeLevel">소득 수준</label>
          <select
            id="incomeLevel"
            value={incomeLevel}
            onChange={(e) => setIncomeLevel(e.target.value)}
            required
          >
            <option value="저">저소득</option>
            <option value="중">중소득</option>
            <option value="고">고소득</option>
          </select>
        </div>
      </div>

      <div className={styles.formSection}>
        <h4>선호 사항 (실시간 매칭용)</h4>
        
        <div className={styles.formGroup}>
          <label htmlFor="industryInput">선호 업종</label>
          <div className={styles.industryInput}>
            <input
              id="industryInput"
              type="text"
              value={industryInput}
              onChange={(e) => setIndustryInput(e.target.value)}
              placeholder="예: 영화관, 노래방 등"
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddIndustry())}
            />
            <button type="button" onClick={handleAddIndustry} className={styles.addButton}>
              추가
            </button>
          </div>
          <div className={styles.industryTags}>
            {preferredIndustries.map((industry) => (
              <span key={industry} className={styles.tag}>
                {industry}
                <button type="button" onClick={() => handleRemoveIndustry(industry)}>×</button>
              </span>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="timePeriod">시간대</label>
          <select
            id="timePeriod"
            value={timePeriod}
            onChange={(e) => setTimePeriod(e.target.value)}
            required
          >
            <option value="새벽">새벽 (0-6시)</option>
            <option value="오전">오전 (6-12시)</option>
            <option value="오후">오후 (12-18시)</option>
            <option value="저녁">저녁 (18-24시)</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="preferenceType">선호 지역 특성</label>
          <select
            id="preferenceType"
            value={preferenceType}
            onChange={(e) => setPreferenceType(e.target.value)}
            required
          >
            <option value="활발한">활발한 (다양한 업종)</option>
            <option value="특화된">특화된 (특정 업종 집중)</option>
            <option value="안정적인">안정적인 (중간 수준)</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={isWeekend}
              onChange={(e) => setIsWeekend(e.target.checked)}
            />
            <span>주말 방문 예정</span>
          </label>
        </div>
      </div>

      <button type="submit" className={styles.submitButton} disabled={loading}>
        {loading ? '🔍 73개 지역 분석 중...' : '🎯 맞춤 지역 추천 받기'}
      </button>
    </form>
  )
}

