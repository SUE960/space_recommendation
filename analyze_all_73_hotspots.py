#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'data_api')
from api_client import SeoulCommercialAreaAPI
sys.path.insert(0, '.')
from analyze_realtime_profiles import analyze_all_areas
import pandas as pd

api_key = "6863727948726b6436345862527950"
client = SeoulCommercialAreaAPI(api_key=api_key)

# 전체 73개 핫스팟 (POI 코드로 접근)
all_pois = []
for i in [1,2,3,4,5,6,7,9,10,13,14,15,16,17,18,19,20,21,23,24,25,26,27,29,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,63,64,66,67,68,70,71,72,73,74,76,77,78,79,80,81,82,83,84]:
    all_pois.append(f"POI{i:03d}")

print("="*80)
print(f"서울시 전체 73개 핫스팟 실시간 점수 계산")
print("="*80)

# 데이터 수집 (모든 POI 코드 시도)
all_data = []
successful_pois = []

for idx, poi in enumerate(all_pois, 1):
    try:
        df = client.get_commercial_area_status(poi)
        if len(df) > 0:
            all_data.append(df)
            area_name = df['AREA_NM'].iloc[0] if 'AREA_NM' in df.columns else poi
            successful_pois.append((poi, area_name, len(df)))
            print(f"  ✓ [{idx}/73] {poi} ({area_name}): {len(df)}개 업종")
        else:
            print(f"  ✗ [{idx}/73] {poi}: 데이터 없음")
    except Exception as e:
        print(f"  ✗ [{idx}/73] {poi}: 오류")
    
    if idx % 10 == 0:
        print(f"  ... {idx}/73 진행 ({len(successful_pois)}개 성공)")

# 전체 데이터 병합
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\n✓ 총 {len(combined_df)}행 데이터 수집 완료 ({len(successful_pois)}개 지역)")
    
    # 프로필 생성
    profiles = analyze_all_areas(combined_df)
    
    # 점수별 정렬
    profiles_sorted = sorted(profiles, key=lambda x: x['scores']['comprehensive']['comprehensive_score'], reverse=True)
    
    # CSV 저장
    summary_data = []
    for profile in profiles_sorted:
        basic = profile['basic_info']
        comp = profile['scores']['comprehensive']
        activity = profile['scores']['activity']
        spec = profile['scores']['specialization']
        demo = profile['scores']['demographic']
        
        summary_data.append({
            '순위': 0,  # 나중에 채움
            '핫스팟명': basic['area_nm'],
            '핫스팟코드': basic['area_cd'],
            '종합점수': round(comp['comprehensive_score'], 2),
            '상권활성도': round(activity['activity_score'], 2),
            '특화점수': round(spec['top_score'], 2),
            '인구통계': round(demo['demographic_score']/2, 2),
            '등급': comp['grade'],
            '특화업종': f"{spec['top_industry']} {spec['top_score']:.1f}%",
            '결제건수': activity['payment_cnt'],
            '결제금액': int(activity['payment_amt']),
            '업종수': activity['industry_diversity']
        })
    
    # 순위 부여
    for idx, row in enumerate(summary_data, 1):
        row['순위'] = idx
    
    df_result = pd.DataFrame(summary_data)
    df_result.to_csv('outputs/api_all_73_hotspots_scores.csv', index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV 저장: outputs/api_all_73_hotspots_scores.csv")
    
    # TOP 20 출력
    print("\n" + "="*80)
    print("TOP 20 핫스팟 순위표")
    print("="*80)
    print(f"\n{'순위':<4} {'핫스팟명':<25} {'종합':<8} {'활성도':<8} {'특화':<8} {'등급':<20}")
    print("-" * 80)
    for _, row in df_result.head(20).iterrows():
        print(f"{row['순위']:<4} {row['핫스팟명']:<25} {row['종합점수']:>6.2f}  {row['상권활성도']:>6.2f}  {row['특화점수']:>6.2f}  {row['등급']:<20}")
    
    print(f"\n✓ 전체 {len(profiles)}개 지역 분석 완료!")
else:
    print("\n❌ 수집된 데이터가 없습니다.")

