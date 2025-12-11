import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

interface RecommendationRequest {
  age_group: string
  gender: string
  preferred_industry: string | null
  time_period: string | null
  is_weekend: boolean
}

// 서울 25개 구 데이터
const SEOUL_GUS = [
  '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구',
  '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구',
  '성동구', '성북구', '송파구', '영등포구', '용산구', '은평구', '종로구',
  '중구', '중랑구', '강서구'
]

// 업종 매칭 점수 계산
function calculateIndustryMatch(
  preferredIndustry: string | null,
  regionSpecialization: string
): number {
  if (!preferredIndustry) return 0.5 // 기본 점수
  
  const industries = preferredIndustry.split(',').map(i => i.trim())
  const specialization = regionSpecialization.toLowerCase()
  
  for (const industry of industries) {
    if (specialization.includes(industry.toLowerCase())) {
      return 0.9 // 높은 매칭
    }
  }
  
  return 0.3 // 낮은 매칭
}

// 추천 점수 계산
function calculateRecommendationScore(
  region: string,
  data: any,
  request: RecommendationRequest
): number {
  let score = 30 // 기본 점수 (30점부터 시작)
  
  // 업종 매칭 (40%)
  const industryMatch = calculateIndustryMatch(
    request.preferred_industry,
    data.특화업종 || ''
  )
  score += industryMatch * 40
  
  // 특화 비율 (20%)
  const specializationRatio = parseFloat(data.특화비율 || '0') / 100
  score += specializationRatio * 20
  
  // 안정성 (10%)
  const cv = parseFloat(data.변동계수 || '20')
  const stability = cv < 18 ? 0.9 : cv < 20 ? 0.7 : 0.5
  score += stability * 10
  
  // 주말 보너스 (최대 5점)
  if (request.is_weekend) {
    score += 5
  }
  
  // 점수 차별화를 위한 랜덤 요소 제거하고, 실제 데이터 기반으로만 계산
  // 최대 100점이지만, 실제로는 30-100 사이의 점수가 나오도록 조정
  return Math.min(Math.max(score, 30), 100) // 30-100 점수 범위
}

export async function POST(request: NextRequest) {
  try {
    const body: RecommendationRequest = await request.json()
    
    // CSV 데이터 읽기 (public 폴더 또는 outputs 폴더)
    let csvPath = path.join(process.cwd(), 'public', 'seoul_all_gu_characteristics.csv')
    if (!fs.existsSync(csvPath)) {
      csvPath = path.join(process.cwd(), 'outputs', 'seoul_all_gu_characteristics.csv')
    }
    const csvContent = fs.readFileSync(csvPath, 'utf-8')
    const lines = csvContent.split('\n').filter(line => line.trim())
    const headers = lines[0].split(',')
    
    // CSV 파싱
    const regions: any[] = []
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',')
      const region: any = {}
      headers.forEach((header, index) => {
        region[header] = values[index] || ''
      })
      regions.push(region)
    }
    
    // 각 지역에 대해 추천 점수 계산
    const recommendations = regions
      .map(region => {
        // 지역 이름 추출 (여러 가능한 컬럼명 시도)
        const regionName = region.구 || region['구'] || region.region || region.Region || '알 수 없는 지역'
        const score = calculateRecommendationScore(regionName, region, body)
        const specializationRatio = parseFloat(region.특화비율 || region['특화비율'] || '0')
        const cv = parseFloat(region.변동계수 || region['변동계수'] || '20')
        
        return {
          region: regionName,
          score: Math.round(score * 10) / 10,
          specialization: region.특화업종 || region['특화업종'] || null,
          specialization_ratio: specializationRatio || null,
          stability: cv < 18 ? '매우 안정적' : cv < 20 ? '안정적' : '보통',
          growth_rate: null,
          reason: generateReason(region, body, score)
        }
      })
      .filter(rec => rec.region && rec.region !== '알 수 없는 지역') // 유효한 지역만 필터링
      .sort((a, b) => b.score - a.score)
      .slice(0, 3) // 상위 3개
    
    // 사용자 프로필 구성
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
    
    return NextResponse.json({
      recommendations,
      user_profile: userProfile
    })
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
  
  if (region.특화업종 && request.preferred_industry) {
    const industries = request.preferred_industry.split(',').map(i => i.trim())
    if (industries.some(ind => region.특화업종.includes(ind))) {
      reasons.push(`${region.특화업종} 특화 지역`)
    }
  }
  
  const cv = parseFloat(region.변동계수 || '20')
  if (cv < 18) {
    reasons.push('안정적인 소비 패턴')
  }
  
  if (request.is_weekend) {
    reasons.push('주말 방문에 적합')
  }
  
  if (reasons.length === 0) {
    reasons.push('다양한 업종과 안정적인 지역')
  }
  
  return reasons.join(', ')
}
