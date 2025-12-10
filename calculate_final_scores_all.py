#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

# 기존 CSV 로드
df = pd.read_csv('outputs/api_all_73_hotspots_scores.csv', encoding='utf-8-sig')

print("="*80)
print("72개 핫스팟 실시간 지역 프로필 점수 재계산")
print("="*80)
print("\n공식: 상권활성도(40%) + 특화점수(30%) + 인구통계(30%)")
print("="*80)

# 실시간 지역 프로필 점수 계산
df['실시간지역프로필점수'] = (
    df['상권활성도'] * 0.4 + 
    df['특화점수'] * 0.3 + 
    df['인구통계'] * 0.3
).round(2)

# 실시간 점수 기준으로 재정렬
df = df.sort_values('실시간지역프로필점수', ascending=False).reset_index(drop=True)
df['순위'] = range(1, len(df) + 1)

# 등급 재부여 (실시간 점수 기준)
def assign_realtime_grade(score):
    if score >= 80:
        return "매우 활성화 (Hot Zone)"
    elif score >= 60:
        return "활성화 (Active Zone)"
    elif score >= 40:
        return "보통 (Normal Zone)"
    else:
        return "비활성 (Low Activity Zone)"

df['실시간등급'] = df['실시간지역프로필점수'].apply(assign_realtime_grade)

# 컬럼 순서 재정렬
columns_order = ['순위', '핫스팟명', '핫스팟코드', '실시간지역프로필점수', '실시간등급',
                 '상권활성도', '특화점수', '인구통계', 
                 '특화업종', '결제건수', '결제금액', '업종수']
df = df[columns_order]

# 저장
df.to_csv('outputs/api_all_72_hotspots_realtime_scores.csv', index=False, encoding='utf-8-sig')
print(f"\n✓ CSV 저장: outputs/api_all_72_hotspots_realtime_scores.csv")

# 전체 순위표 출력
print("\n" + "="*80)
print("전체 72개 핫스팟 실시간 점수 순위표")
print("="*80)
print(f"\n{'순위':<4} {'핫스팟명':<25} {'실시간점수':<10} {'활성도':<8} {'특화':<8} {'인구':<8} {'등급':<25}")
print("-" * 100)

for _, row in df.iterrows():
    print(f"{row['순위']:<4} {row['핫스팟명']:<25} {row['실시간지역프로필점수']:>8.2f}  "
          f"{row['상권활성도']:>6.2f}  {row['특화점수']:>6.2f}  {row['인구통계']:>6.2f}  "
          f"{row['실시간등급']:<25}")

# 통계
print("\n" + "="*80)
print("통계 요약")
print("="*80)

print(f"\n등급별 분포:")
grade_counts = df['실시간등급'].value_counts()
for grade, count in grade_counts.items():
    pct = (count / len(df) * 100)
    print(f"  {grade}: {count}개 ({pct:.1f}%)")

print(f"\n점수 통계:")
print(f"  평균: {df['실시간지역프로필점수'].mean():.2f}점")
print(f"  중앙값: {df['실시간지역프로필점수'].median():.2f}점")
print(f"  최고: {df['실시간지역프로필점수'].max():.2f}점 ({df.iloc[0]['핫스팟명']})")
print(f"  최저: {df['실시간지역프로필점수'].min():.2f}점 ({df.iloc[-1]['핫스팟명']})")
print(f"  표준편차: {df['실시간지역프로필점수'].std():.2f}점")

print("\n" + "="*80)
print("완료!")
print("="*80)
