import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

interface RecommendationRequest {
  age_group: string
  gender: string
  preferred_industry: string | null
  time_period: string | null
  is_weekend: boolean
  purpose?: string | null // 방문 목적 (식사, 카페/디저트, 쇼핑, 문화/여가, 운동/스포츠, 기타)
  budget?: string | null // 예산 (5만원 미만, 5만원 ~ 10만원, 10만원 ~ 20만원, 20만원 이상)
  priority?: string | null // 우선순위 (접근성, 트렌드, 가격, 다양성)
}

// 서울 25개 구 데이터
const SEOUL_GUS = [
  '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구',
  '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구',
  '성동구', '성북구', '송파구', '영등포구', '용산구', '은평구', '종로구',
  '중구', '중랑구', '강서구'
]

// 연령대별 선호 지역 매핑 (실제 핫스팟 데이터 기반)
const AGE_PREFERENCE_MAP: Record<string, string[]> = {
  '10-19': ['홍대 관광특구', '강남역', '이태원 관광특구', '명동 관광특구', '건대입구역'],
  '20-29': ['홍대 관광특구', '강남역', '이태원 관광특구', '명동 관광특구', '신촌·이대역', '건대입구역', '잠실 관광특구', '용리단길'],
  '30-39': ['강남역', '서초구', '송파구', '잠실 관광특구', '압구정로데오거리', '여의도'],
  '40-49': ['서초구', '강남역', '송파구', '잠실 관광특구', '종로·청계 관광특구'],
  '50-59': ['종로·청계 관광특구', '서초구', '송파구', '잠실 관광특구', '광화문·덕수궁'],
  '60+': ['종로·청계 관광특구', '서초구', '송파구', '잠실 관광특구', '인사동']
}

// 목적(purpose)에 따른 업종 매핑
const PURPOSE_INDUSTRY_MAP: Record<string, string[]> = {
  '식사': ['한식', '중식', '일식', '양식', '기타요식'],
  '카페/디저트': ['커피전문점', '제과점'],
  '쇼핑': ['대형마트', '편의점', '슈퍼마켓일반형', '슈퍼마켓기업형', '백화점', '패션잡화'],
  '문화/여가': ['영화/공연', '게임방/오락실', '노래방', '스포츠', '서점'],
  '운동/스포츠': ['스포츠', '실내/실외골프장'],
  '기타': []
}

// 업종 매칭 점수 계산 (개선된 버전 - purpose 반영)
function calculateIndustryMatch(
  preferredIndustry: string | null,
  regionSpecialization: string,
  specializationRatio: number,
  purpose: string | null = null
): number {
  if (!regionSpecialization) return 0.3 // 기본 점수
  
  const specialization = regionSpecialization.toLowerCase()
  
  // 1. purpose 기반 업종 매칭 (우선순위 높음)
  if (purpose && PURPOSE_INDUSTRY_MAP[purpose]) {
    const purposeIndustries = PURPOSE_INDUSTRY_MAP[purpose]
    for (const industry of purposeIndustries) {
      if (specialization.includes(industry.toLowerCase())) {
        // purpose와 일치하면 높은 점수
        return 0.7 + (specializationRatio / 100) * 0.3 // 0.7 ~ 1.0
      }
    }
  }
  
  // 2. 사용자 선호 업종 매칭
  if (preferredIndustry) {
    const industries = preferredIndustry.split(',').map(i => i.trim().toLowerCase())
    
    // 정확한 매칭
    for (const industry of industries) {
      if (specialization.includes(industry)) {
        // 특화 비율이 높을수록 더 높은 점수
        return 0.5 + (specializationRatio / 100) * 0.5 // 0.5 ~ 1.0
      }
    }
    
    // 부분 매칭 (업종 키워드 포함)
    const industryKeywords: Record<string, string[]> = {
      '화장품': ['화장품', '뷰티', '미용'],
      '의류': ['의류', '패션', '잡화'],
      '음식': ['한식', '중식', '일식', '양식', '기타요식', '커피'],
      '쇼핑': ['대형마트', '편의점', '슈퍼마켓', '백화점'],
      '문화': ['영화', '공연', '게임', '노래방', '스포츠']
    }
    
    for (const [category, keywords] of Object.entries(industryKeywords)) {
      if (industries.some(ind => keywords.some(kw => ind.includes(kw)))) {
        if (keywords.some(kw => specialization.includes(kw))) {
          return 0.4 + (specializationRatio / 100) * 0.3 // 0.4 ~ 0.7
        }
      }
    }
  }
  
  return 0.2 // 낮은 매칭
}

// 업종 다양성 점수 계산
function calculateDiversityScore(diversityText: string): number {
  if (!diversityText) return 0.5
  
  if (diversityText.includes('높음')) return 0.9
  if (diversityText.includes('보통')) return 0.7
  if (diversityText.includes('낮음')) return 0.4
  
  // 업종 수 추출
  const match = diversityText.match(/(\d+)개/)
  if (match) {
    const count = parseInt(match[1])
    return Math.min(count / 15, 1.0) // 15개 이상이면 1.0
  }
  
  return 0.5
}

// 안정성 점수 계산
function calculateStabilityScore(cv: number): number {
  if (cv < 16) return 1.0 // 매우 안정적
  if (cv < 18) return 0.9 // 안정적
  if (cv < 20) return 0.7 // 보통
  if (cv < 22) return 0.5 // 불안정
  return 0.3 // 매우 불안정
}

// 연령대별 지역 선호도 점수
function calculateAgePreferenceScore(
  ageGroup: string,
  regionName: string
): number {
  const preferredRegions = AGE_PREFERENCE_MAP[ageGroup] || []
  
  // 정확한 매칭
  if (preferredRegions.includes(regionName)) {
    const index = preferredRegions.indexOf(regionName)
    return 1.0 - (index * 0.1) // 1위: 1.0, 2위: 0.9, ...
  }
  
  // 부분 매칭 (핫스팟명 포함 체크)
  for (const pref of preferredRegions) {
    // 정확한 매칭
    if (regionName === pref) {
      return 0.8
    }
    // 부분 매칭 (홍대, 강남역 등 키워드 포함)
    if (regionName.includes(pref) || pref.includes(regionName)) {
      return 0.7
    }
    // 키워드 매칭 (홍대 관광특구 -> 홍대)
    const prefKeyword = pref.split(' ')[0].split('·')[0].split('관광특구')[0]
    const regionKeyword = regionName.split(' ')[0].split('·')[0].split('관광특구')[0]
    if (prefKeyword === regionKeyword || regionName.includes(prefKeyword)) {
      return 0.6
    }
  }
  
  return 0.5 // 기본 점수
}

// 우선순위(priority)에 따른 가중치 조정
function getPriorityWeights(priority: string | null): {
  industry: number
  age: number
  stability: number
  diversity: number
} {
  const defaultWeights = {
    industry: 35,
    age: 25,
    stability: 20,
    diversity: 15
  }
  
  if (!priority) return defaultWeights
  
  switch (priority) {
    case '접근성':
      // 접근성은 안정성과 다양성에 가중치
      return { industry: 30, age: 20, stability: 30, diversity: 20 }
    case '트렌드':
      // 트렌드는 연령대 선호도와 다양성에 가중치
      return { industry: 30, age: 35, stability: 15, diversity: 20 }
    case '가격':
      // 가격은 안정성에 가중치
      return { industry: 30, age: 25, stability: 35, diversity: 10 }
    case '다양성':
      // 다양성은 다양성 점수에 가중치
      return { industry: 25, age: 20, stability: 15, diversity: 40 }
    default:
      return defaultWeights
  }
}

// 예산(budget)에 따른 지역 필터링 점수
function calculateBudgetScore(budget: string | null, region: string): number {
  if (!budget) return 1.0 // 기본 점수
  
  // 프리미엄 지역 (20만원 이상)
  const premiumRegions = ['강남구', '서초구', '송파구', '용산구']
  // 합리적 지역 (5만원 미만)
  const affordableRegions = ['강북구', '도봉구', '은평구', '금천구', '구로구']
  
  if (budget.includes('20만원 이상')) {
    return premiumRegions.some(r => region.includes(r)) ? 1.2 : 0.9
  } else if (budget.includes('5만원 미만')) {
    return affordableRegions.some(r => region.includes(r)) ? 1.2 : 0.9
  }
  
  return 1.0 // 중간 예산은 모든 지역 동일
}

// 추천 점수 계산 (실제 데이터 기반 - purpose, budget, priority 반영)
function calculateRecommendationScore(
  region: string,
  data: any,
  request: RecommendationRequest
): number {
  let score = 0 // 0부터 시작하여 가중치 합산
  
  // 우선순위에 따른 가중치 조정
  const weights = getPriorityWeights(request.priority || null)
  
  // 핫스팟 데이터와 구 데이터의 필드명이 다를 수 있으므로 처리
  let specializationRatio = parseFloat(data.특화비율 || data['특화비율'] || '0')
  const specializationScore = parseFloat(data.특화점수 || data['특화점수'] || '0')
  
  // 특화점수는 0-100 범위이므로 그대로 사용 가능
  if (specializationScore > 0 && specializationRatio === 0) {
    specializationRatio = specializationScore
  }
  
  const specializationIndustry = (data.특화업종 || data['특화업종'] || '').trim()
  
  // 1. 업종 매칭 (purpose 반영)
  const industryMatch = calculateIndustryMatch(
    request.preferred_industry,
    specializationIndustry,
    specializationRatio,
    request.purpose || null
  )
  score += industryMatch * weights.industry
  
  // 2. 연령대별 선호도
  const agePreference = calculateAgePreferenceScore(
    request.age_group,
    region
  )
  score += agePreference * weights.age
  
  // 3. 안정성 (핫스팟 데이터는 상권활성도 기반)
  const cv = parseFloat(data.변동계수 || data['변동계수'] || '0')
  const activity = parseFloat(data.상권활성도 || data['상권활성도'] || '0')
  let stability = 0.5
  if (cv > 0) {
    // 구 데이터인 경우
    stability = calculateStabilityScore(cv)
  } else if (activity > 0) {
    // 핫스팟 데이터인 경우 (상권활성도 기반)
    stability = activity >= 70 ? 0.9 : activity >= 50 ? 0.7 : activity >= 30 ? 0.5 : 0.3
  }
  score += stability * weights.stability
  
  // 4. 업종 다양성
  const diversityText = data.업종다양성 || data['업종다양성'] || ''
  const industryCount = parseFloat(data.업종수 || data['업종수'] || '0')
  let diversity = 0.5
  if (diversityText) {
    diversity = calculateDiversityScore(diversityText)
  } else if (industryCount > 0) {
    // 핫스팟 데이터는 업종수로 다양성 계산
    // 업종수가 많을수록 다양성 높음
    diversity = Math.min(industryCount / 5, 1.0) // 5개 이상이면 1.0
  }
  score += diversity * weights.diversity
  
  // 5. 특화 비율 보너스
  const specializationBonus = Math.min(specializationRatio / 100, 1.0) * 5
  score += specializationBonus
  
  // 6. 예산 점수 적용
  const budgetMultiplier = calculateBudgetScore(request.budget || null, region)
  score *= budgetMultiplier
  
  // 7. 시간대/주말 보너스
  if (request.is_weekend) {
    // 주말에는 다양성이 높은 지역에 보너스
    if (diversity > 0.7) {
      score += 3
    }
  } else {
    // 평일에는 안정적인 지역에 보너스
    if (stability > 0.8) {
      score += 3
    }
  }
  
  // 점수 정규화 (0-100)
  return Math.min(Math.max(score, 20), 100) // 최소 20점, 최대 100점
}

export async function POST(request: NextRequest) {
  try {
    const body: RecommendationRequest = await request.json()
    
    // 핫스팟 데이터 읽기 (강남역, 홍대 등 실제 지역명 포함)
    let csvPath = path.join(process.cwd(), 'public', 'api_all_72_hotspots_realtime_scores.csv')
    if (!fs.existsSync(csvPath)) {
      csvPath = path.join(process.cwd(), 'outputs', 'api_all_72_hotspots_realtime_scores.csv')
    }
    
    if (!fs.existsSync(csvPath)) {
      console.error('Hotspot CSV file not found, falling back to gu data')
      // 폴백: 구 데이터 사용
      csvPath = path.join(process.cwd(), 'public', 'seoul_all_gu_characteristics.csv')
      if (!fs.existsSync(csvPath)) {
        csvPath = path.join(process.cwd(), 'outputs', 'seoul_all_gu_characteristics.csv')
      }
    }
    
    const csvContent = fs.readFileSync(csvPath, 'utf-8')
    const lines = csvContent.split('\n').filter(line => line.trim())
    const headers = lines[0].split(',').map(h => h.trim())
    
    console.log('CSV Headers:', headers)
    console.log('Total lines:', lines.length)
    console.log('Using data file:', csvPath)
    
    // CSV 파싱 (간단하고 확실한 방법)
    const regions: any[] = []
    const hotspotNameIndex = headers.indexOf('핫스팟명')
    const guIndex = headers.indexOf('구')
    
    console.log(`핫스팟명 인덱스: ${hotspotNameIndex}, 구 인덱스: ${guIndex}`)
    
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim()
      if (!line) continue
      
      // 쉼표로 split하되, 따옴표 안의 쉼표는 무시
      const values: string[] = []
      let current = ''
      let inQuotes = false
      
      for (let j = 0; j < line.length; j++) {
        const char = line[j]
        if (char === '"') {
          inQuotes = !inQuotes
        } else if (char === ',' && !inQuotes) {
          values.push(current.trim())
          current = ''
        } else {
          current += char
        }
      }
      values.push(current.trim()) // 마지막 값
      
      // region 객체 생성
      const region: any = {}
      headers.forEach((header, index) => {
        const value = values[index] || ''
        // 따옴표 제거
        region[header] = value.replace(/^"|"$/g, '').trim()
      })
      
      // 지역 이름 추출 - 핫스팟명 우선, 없으면 구
      let regionName = ''
      
      if (hotspotNameIndex >= 0 && hotspotNameIndex < values.length) {
        regionName = String(values[hotspotNameIndex] || '').trim()
      }
      
      if (!regionName && guIndex >= 0 && guIndex < values.length) {
        regionName = String(values[guIndex] || '').trim()
      }
      
      // 지역 이름이 유효한 경우만 추가
      if (regionName && regionName !== '' && regionName.length >= 2) {
        region.regionName = regionName
        regions.push(region)
        if (i <= 5) { // 처음 5개만 로그
          console.log(`✅ Added region: ${regionName} (line ${i})`)
        }
      }
    }
    
    console.log(`Total valid regions: ${regions.length}`)
    
    // 지역 이름이 있는 데이터만 추천 후보로 사용
    if (regions.length === 0) {
      console.error('No regions with valid names found in CSV')
      return NextResponse.json(
        { error: '유효한 지역 데이터를 찾을 수 없습니다' },
        { status: 500 }
      )
    }
    
    // 각 지역에 대해 추천 점수 계산 (지역 이름이 있는 데이터만)
    const recommendations = regions
      .map(region => {
        // 지역 이름 추출 - regionName이 명시적으로 저장되어 있음
        const regionName = region.regionName || ''
        const finalRegionName = String(regionName).trim()
        
        // 지역 이름이 없으면 null 반환
        if (!finalRegionName || finalRegionName === '') {
          console.error('❌ Region without name found. region.regionName:', region.regionName, 'Available keys:', Object.keys(region))
          return null
        }
        
        // 핫스팟 데이터와 구 데이터의 필드명이 다를 수 있으므로 처리
        let specializationRatio = parseFloat(region.특화비율 || region['특화비율'] || '0')
        const specializationScore = parseFloat(region.특화점수 || region['특화점수'] || '0')
        
        // 특화점수가 있으면 사용 (핫스팟 데이터는 특화점수 사용)
        if (specializationScore > 0 && specializationRatio === 0) {
          specializationRatio = specializationScore
        }
        
        // 변동계수는 구 데이터에만 있으므로, 핫스팟 데이터는 상권활성도로 대체
        const cv = parseFloat(region.변동계수 || region['변동계수'] || '0')
        const activity = parseFloat(region.상권활성도 || region['상권활성도'] || '0')
        
        // 안정성 계산 (핫스팟 데이터는 상권활성도 기반)
        let stability = '보통'
        if (cv > 0 && cv < 100) {
          // 구 데이터인 경우 (변동계수는 보통 10-30 범위)
          stability = cv < 16 ? '매우 안정적' : cv < 18 ? '안정적' : cv < 20 ? '보통' : '불안정'
        } else if (activity > 0) {
          // 핫스팟 데이터인 경우 (상권활성도 기반, 0-100 범위)
          stability = activity >= 70 ? '매우 안정적' : activity >= 50 ? '안정적' : activity >= 30 ? '보통' : '불안정'
        }
        
        const score = calculateRecommendationScore(finalRegionName, region, body)
        
        console.log(`📊 ${finalRegionName}: score=${score.toFixed(2)}, activity=${activity}, specialization=${specializationRatio.toFixed(1)}`)
        
        const recommendation = {
          region: finalRegionName, // 반드시 지역 이름 포함 (홍대 관광특구, 강남역, 강남구 등)
          score: Math.round(score * 10) / 10,
          specialization: (region.특화업종 || region['특화업종'] || '').trim() || null,
          specialization_ratio: specializationRatio || null,
          stability: stability,
          growth_rate: null,
          reason: generateReason(region, body, score)
        }
        
        console.log(`✅ Recommendation created: ${finalRegionName} (score: ${recommendation.score})`)
        return recommendation
      })
      .filter((rec): rec is NonNullable<typeof rec> => {
        // 지역 이름이 있는 추천만 통과
        if (!rec || !rec.region || rec.region.trim() === '') {
          return false
        }
        return true
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 3) // 상위 3개
    
    // 사용자 프로필 구성 (먼저 선언)
    const userProfile = {
      age_group: body.age_group,
      gender: body.gender,
      preferred_industry: body.preferred_industry,
      time_period: body.time_period,
      is_weekend: body.is_weekend,
      matched_preferences: body.preferred_industry 
        ? body.preferred_industry.split(',').map(i => i.trim())
        : []
    }
    
    // 최종 필터링: null 제거 및 지역 이름 검증
    const validRecommendations = recommendations
      .filter((rec): rec is NonNullable<typeof rec> => {
        if (!rec) return false
        if (!rec.region || rec.region.trim() === '') {
          console.error('Found recommendation without region name:', rec)
          return false
        }
        return true
      })
    
    console.log(`Final recommendations count: ${validRecommendations.length}`)
    validRecommendations.forEach((rec, idx) => {
      console.log(`Recommendation ${idx + 1}: ${rec.region} (score: ${rec.score})`)
    })
    
    // 추천 결과가 없거나 지역 이름이 없는 경우 에러
    if (validRecommendations.length === 0) {
      console.error('No valid recommendations with region names found')
      return NextResponse.json(
        { error: '추천할 지역 데이터를 찾을 수 없습니다' },
        { status: 500 }
      )
    }
    
    // 최종 응답 (지역 이름이 반드시 포함된 추천만 반환)
    const finalResponse = {
      recommendations: validRecommendations,
      user_profile: userProfile
    }
    
    console.log('Final response:', JSON.stringify(finalResponse, null, 2))
    
    return NextResponse.json(finalResponse)
  } catch (error) {
    console.error('Recommendation error:', error)
    return NextResponse.json(
      { error: '추천 요청 처리 중 오류가 발생했습니다' },
      { status: 500 }
    )
  }
}

function generateReason(region: any, request: RecommendationRequest, score: number): string {
  const reasons: string[] = []
  
  // 목적(purpose) 기반 추천 이유
  if (request.purpose) {
    const purposeIndustries = PURPOSE_INDUSTRY_MAP[request.purpose] || []
    const specialization = (region.특화업종 || '').toLowerCase()
    
    if (purposeIndustries.some(ind => specialization.includes(ind.toLowerCase()))) {
      reasons.push(`${request.purpose}에 최적화된 지역`)
    }
  }
  
  // 업종 매칭
  if (region.특화업종) {
    const specializationRatio = parseFloat(region.특화비율 || '0')
    
    if (request.purpose && PURPOSE_INDUSTRY_MAP[request.purpose]) {
      const purposeIndustries = PURPOSE_INDUSTRY_MAP[request.purpose]
      if (purposeIndustries.some(ind => region.특화업종.includes(ind))) {
        if (specializationRatio > 50) {
          reasons.push(`${region.특화업종} 강력 특화 (${specializationRatio}%)`)
        } else {
          reasons.push(`${region.특화업종} 특화 지역`)
        }
      }
    } else if (request.preferred_industry) {
      const industries = request.preferred_industry.split(',').map(i => i.trim())
      if (industries.some(ind => region.특화업종.toLowerCase().includes(ind.toLowerCase()))) {
        if (specializationRatio > 50) {
          reasons.push(`${region.특화업종} 강력 특화 지역 (${specializationRatio}%)`)
        } else {
          reasons.push(`${region.특화업종} 특화 지역`)
        }
      }
    }
  }
  
  // 연령대 적합도 (핫스팟명 또는 구 컬럼 사용)
  const agePrefRegions = AGE_PREFERENCE_MAP[request.age_group] || []
  const regionName = region.regionName || region.핫스팟명 || region.구 || ''
  if (regionName && agePrefRegions.some(pref => regionName.includes(pref) || pref.includes(regionName))) {
    reasons.push(`${request.age_group} 연령대 선호 지역`)
  }
  
  // 우선순위 기반 이유
  if (request.priority === '접근성') {
    reasons.push('교통 편리한 지역')
  } else if (request.priority === '트렌드') {
    reasons.push('인기 상권 지역')
  } else if (request.priority === '가격') {
    const cv = parseFloat(region.변동계수 || '20')
    if (cv < 18) {
      reasons.push('합리적인 가격대')
    }
  } else if (request.priority === '다양성') {
    const diversity = region.업종다양성 || ''
    if (diversity.includes('높음') || diversity.includes('15개')) {
      reasons.push('다양한 업종 선택 가능')
    }
  }
  
  // 안정성
  const cv = parseFloat(region.변동계수 || '20')
  if (cv < 16) {
    reasons.push('매우 안정적인 소비 패턴')
  } else if (cv < 18) {
    reasons.push('안정적인 소비 패턴')
  }
  
  // 시간대 적합도
  if (request.is_weekend) {
    const diversity = region.업종다양성 || ''
    if (diversity.includes('높음')) {
      reasons.push('주말 다양한 활동에 적합')
    } else {
      reasons.push('주말 방문에 적합')
    }
  } else {
    if (cv < 18) {
      reasons.push('평일 안정적인 소비 환경')
    }
  }
  
  if (reasons.length === 0) {
    reasons.push('균형잡힌 상권과 안정적인 지역')
  }
  
  return reasons.join(', ')
}

