import { NextRequest, NextResponse } from 'next/server'

// 간단한 추천 알고리즘 (TypeScript로 구현)
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { age, gender, preferred_industries, time_period, is_weekend } = body

    // 나이대 결정
    let ageGroup = '20-29세'
    if (age < 20) ageGroup = '10대'
    else if (age < 30) ageGroup = '20-29세'
    else if (age < 40) ageGroup = '30-39세'
    else if (age < 50) ageGroup = '40-49세'
    else if (age < 60) ageGroup = '50-59세'
    else if (age < 70) ageGroup = '60-69세'
    else ageGroup = '70세 이상'

    // 추천 지역 (샘플 데이터)
    const recommendations = [
      {
        rank: 1,
        region: '홍대 관광특구',
        final_score: 85.32,
        static_score: 82.5,
        realtime_score: 88.2,
        static_details: {
          industry_match: 60.0,
          demographic_match: 81.24,
          spending_match: 59.35,
          time_match: 65.0
        },
        realtime_details: {
          user_industry_match: 66.67,
          comprehensive_score: 76.27,
          specialization_match: 99.6,
          time_match: 85.0
        },
        comprehensive_score: 85.5,
        grade: '매우 활성화 (Hot Zone)',
        specialized_industries: ['음식·음료', '여가·오락'],
        reasons: [
          `선호하시는 ${preferred_industries[0] || '맛집'} 업종이 특화된 지역`,
          `${ageGroup} ${gender}에게 인기`,
          '현재 매우 활성화 (Hot Zone)',
          `${time_period} 시간대에 적합`
        ]
      },
      {
        rank: 2,
        region: '강남역',
        final_score: 78.45,
        static_score: 75.1,
        realtime_score: 81.8,
        static_details: {
          industry_match: 55.0,
          demographic_match: 85.0,
          spending_match: 70.0,
          time_match: 60.0
        },
        realtime_details: {
          user_industry_match: 60.0,
          comprehensive_score: 82.0,
          specialization_match: 88.0,
          time_match: 80.0
        },
        comprehensive_score: 82.0,
        grade: '활성화',
        specialized_industries: ['음식·음료', '쇼핑'],
        reasons: [
          '다양한 업종이 밀집',
          '직장인들에게 인기',
          '높은 접근성',
          '트렌디한 지역'
        ]
      },
      {
        rank: 3,
        region: '명동',
        final_score: 76.23,
        static_score: 72.0,
        realtime_score: 80.5,
        static_details: {
          industry_match: 58.0,
          demographic_match: 75.0,
          spending_match: 65.0,
          time_match: 70.0
        },
        realtime_details: {
          user_industry_match: 65.0,
          comprehensive_score: 78.0,
          specialization_match: 85.0,
          time_match: 82.0
        },
        comprehensive_score: 78.0,
        grade: '활성화',
        specialized_industries: ['쇼핑', '음식·음료'],
        reasons: [
          '관광 명소',
          '쇼핑 천국',
          '다양한 음식점',
          '주말 방문 추천'
        ]
      }
    ]

    // 주말 보너스
    if (is_weekend) {
      recommendations.forEach(rec => {
        rec.final_score = Math.min(rec.final_score * 1.1, 100)
      })
    }

    return NextResponse.json({
      recommendations,
      user_profile: {
        age,
        gender,
        income_level: '중',
        matched_segment: `${ageGroup}_${gender}`,
        segment_description: `${ageGroup} ${gender}`,
        preferred_industries,
        time_period,
        is_weekend,
        preference_type: '활발한',
        top_segment_industries: ['한식', '카페', '영화관']
      }
    })
  } catch (error) {
    console.error('추천 오류:', error)
    return NextResponse.json(
      { error: '추천 처리 중 오류가 발생했습니다' },
      { status: 500 }
    )
  }
}

