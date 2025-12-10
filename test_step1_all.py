"""
STEP 1 시스템 전체 테스트 및 데모
====================================
모든 기능을 한 번에 테스트하고 결과를 확인합니다.
"""

from step1_user_matcher import UserSegmentMatcher
from step3_integrated_recommendation import IntegratedRecommendationSystem
import json
from pathlib import Path


def test_step1_profiles():
    """STEP 1 프로필 생성 확인"""
    print("=" * 70)
    print("📊 STEP 1: 정적 집단 프로필 확인")
    print("=" * 70)
    
    # 프로필 파일 확인
    profile_file = Path("outputs/step1_static_profiles.json")
    
    if not profile_file.exists():
        print("❌ 프로필 파일이 없습니다. 먼저 step1_static_profile_generation.py를 실행하세요.")
        return False
    
    with open(profile_file, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    print(f"✅ 총 {len(profiles)}개 세그먼트 프로필 로드 완료")
    
    # 각 세그먼트 요약 출력
    print("\n세그먼트별 요약:")
    print("-" * 70)
    
    for segment_id, profile in sorted(profiles.items()):
        info = profile['segment_info']
        spending = profile['spending_characteristics']
        top_ind = profile['industry_preferences'][0] if profile['industry_preferences'] else None
        
        print(f"• {info['age_group_kr']:8s} {info['gender_kr']:2s}: "
              f"총 {spending['total_spending']:>12,}원, "
              f"평균 {spending['avg_transaction_amount']:>7,}원, "
              f"관심: {top_ind['industry'] if top_ind else 'N/A'}")
    
    print("\n" + "=" * 70)
    return True


def test_user_matching():
    """사용자 매칭 테스트"""
    print("\n📍 STEP 1: 사용자 매칭 테스트")
    print("=" * 70)
    
    matcher = UserSegmentMatcher()
    
    # 테스트 케이스
    test_cases = [
        {'name': '20대 남성 대학생', 'age': 22, 'gender': '남', 'income': '저'},
        {'name': '30대 여성 직장인', 'age': 32, 'gender': '여', 'income': '중'},
        {'name': '40대 남성 가장', 'age': 45, 'gender': '남', 'income': '고'},
        {'name': '60대 여성 주부', 'age': 62, 'gender': '여', 'income': '중'},
    ]
    
    for case in test_cases:
        print(f"\n[{case['name']}] {case['age']}세 {case['gender']}, 소득 {case['income']}")
        
        profile = matcher.match_user(
            age=case['age'],
            gender=case['gender'],
            income_level=case['income']
        )
        
        info = profile['segment_info']
        spending = profile['spending_characteristics']
        
        print(f"  → 세그먼트: {info['age_group_kr']} {info['gender_kr']}")
        print(f"  → 평균 거래액: {spending['avg_transaction_amount']:,}원")
        
        if 'income_adjustment' in profile:
            adj = profile['income_adjustment']
            print(f"  → 소득 조정: {adj['adjusted_avg_transaction']:,}원 (×{adj['multiplier']})")
        
        print(f"  → 주요 관심 업종:")
        for idx, ind in enumerate(profile['industry_preferences'][:3], 1):
            print(f"     {idx}. {ind['industry']} ({ind['preference_ratio']:.1f}%)")
    
    print("\n" + "=" * 70)
    return True


def test_integrated_recommendation():
    """통합 추천 시스템 테스트"""
    print("\n🎁 STEP 3: 통합 추천 시스템 테스트")
    print("=" * 70)
    
    # STEP 2 파일 확인
    step2_file = Path("outputs/seoul_all_gu_final.csv")
    
    if not step2_file.exists():
        print("⚠️  STEP 2 파일이 없습니다. STEP 1 기반 추천만 수행합니다.")
        step2_file = None
    else:
        print(f"✅ STEP 2 파일 발견: {step2_file}")
    
    # 시스템 초기화
    system = IntegratedRecommendationSystem(
        step1_dir='outputs',
        step2_file=str(step2_file) if step2_file else None
    )
    
    # 테스트 사용자
    print("\n[테스트 사용자] 28세 남성, 소득 중, 한식/카페 선호")
    
    result = system.recommend_regions(
        age=28,
        gender='남',
        income_level='중',
        preferences={
            'preferred_industries': ['한식', '커피전문점', '영화/공연'],
            'priorities': {'preference_match': 0.6, 'score': 0.4}
        },
        top_n=5,
        use_step2=(step2_file is not None)
    )
    
    # 결과 출력
    print(f"\n✅ {len(result['recommendations'])}개 지역 추천 완료")
    print("-" * 70)
    
    for rec in result['recommendations']:
        print(f"\n{rec['rank']}위. {rec.get('region_name', rec.get('gu_name', 'Unknown'))}")
        print(f"   매칭 점수: {rec['match_score']:.1f}점")
        
        if 'preference_score' in rec:
            print(f"   - 선호도: {rec['preference_score']:.1f}점")
            print(f"   - 지역: {rec['step2_score']:.1f}점")
        
        print(f"   이유: {rec['reason']}")
    
    print("\n" + "=" * 70)
    return True


def test_segment_comparison():
    """세그먼트 비교 테스트"""
    print("\n📈 STEP 1: 세그먼트 비교")
    print("=" * 70)
    
    matcher = UserSegmentMatcher()
    
    # 같은 연령대, 다른 성별 비교
    print("\n[비교 1] 30대 남성 vs 30대 여성")
    comparison = matcher.compare_segments('30s_male', '30s_female')
    
    seg1 = comparison['segment1']
    seg2 = comparison['segment2']
    
    print(f"  {seg1['info']['gender_kr']}: 총 소비 {seg1['total_spending']:,}원, "
          f"평균 {seg1['avg_transaction']:,}원")
    print(f"  {seg2['info']['gender_kr']}: 총 소비 {seg2['total_spending']:,}원, "
          f"평균 {seg2['avg_transaction']:,}원")
    print(f"  → 소비액 비율: {comparison['spending_ratio']:.2f}배")
    print(f"  → 거래액 비율: {comparison['transaction_ratio']:.2f}배")
    
    # 다른 연령대 비교
    print("\n[비교 2] 20대 남성 vs 40대 남성")
    comparison = matcher.compare_segments('20s_male', '40s_male')
    
    seg1 = comparison['segment1']
    seg2 = comparison['segment2']
    
    print(f"  20대: 평균 {seg1['avg_transaction']:,}원, "
          f"관심: {seg1['top_industry']['industry']}")
    print(f"  40대: 평균 {seg2['avg_transaction']:,}원, "
          f"관심: {seg2['top_industry']['industry']}")
    print(f"  → 거래액 비율: {comparison['transaction_ratio']:.2f}배")
    
    print("\n" + "=" * 70)
    return True


def main():
    """전체 테스트 실행"""
    print("\n" + "🎯" * 35)
    print(" " * 20 + "STEP 1 시스템 전체 테스트")
    print("🎯" * 35 + "\n")
    
    results = []
    
    # 1. 프로필 확인
    results.append(("프로필 생성 확인", test_step1_profiles()))
    
    # 2. 사용자 매칭
    results.append(("사용자 매칭", test_user_matching()))
    
    # 3. 세그먼트 비교
    results.append(("세그먼트 비교", test_segment_comparison()))
    
    # 4. 통합 추천
    results.append(("통합 추천", test_integrated_recommendation()))
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("📋 테스트 결과 요약")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 모든 테스트 통과! STEP 1 시스템이 정상적으로 작동합니다.")
    else:
        print("⚠️  일부 테스트 실패. 위 내용을 확인하세요.")
    print("=" * 70)
    
    # 추가 정보
    print("\n📚 추가 정보:")
    print("  - 상세 가이드: STEP1_가이드.md")
    print("  - 통합 가이드: STEP1_STEP2_통합가이드.md")
    print("  - 구현 보고서: STEP1_구현완료보고서.md")
    print("  - 프로젝트 개요: README.md")
    
    print("\n💡 빠른 시작:")
    print("  python3 step1_static_profile_generation.py  # 프로필 생성")
    print("  python3 step1_user_matcher.py               # 매칭 데모")
    print("  python3 step3_integrated_recommendation.py  # 통합 추천 데모")
    print()


if __name__ == "__main__":
    main()



