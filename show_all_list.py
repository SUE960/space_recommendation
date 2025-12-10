#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_csv('outputs/api_all_72_hotspots_realtime_scores.csv', encoding='utf-8-sig')

print("="*80)
print("서울시 전체 72개 핫스팟 리스트 (실시간 점수 순)")
print("="*80)

print("\n✅ 활성화 등급 (3개)")
print("-" * 80)
active = df[df['실시간등급'].str.contains('Active')]
for idx, row in active.iterrows():
    print(f"{row['순위']:2d}. {row['핫스팟명']:<30} {row['실시간지역프로필점수']:6.2f}점")

print("\n⚪ 보통 등급 (69개)")
print("-" * 80)
normal = df[df['실시간등급'].str.contains('Normal')]
for idx, row in normal.iterrows():
    print(f"{row['순위']:2d}. {row['핫스팟명']:<30} {row['실시간지역프로필점수']:6.2f}점")

print("\n" + "="*80)
print("카테고리별 분류")
print("="*80)

# 관광특구
print("\n【관광특구 7개】")
tourist = df[df['핫스팟명'].str.contains('관광특구')]
for _, row in tourist.iterrows():
    print(f"  {row['순위']:2d}위. {row['핫스팟명']:<30} {row['실시간지역프로필점수']:6.2f}점")

# 지하철역
print("\n【지하철역 43개】")
subway = df[df['핫스팟명'].str.contains('역')]
for _, row in subway.iterrows():
    print(f"  {row['순위']:2d}위. {row['핫스팟명']:<30} {row['실시간지역프로필점수']:6.2f}점")

# 거리/동네
print("\n【핫플레이스/거리 22개】")
place = df[~df['핫스팟명'].str.contains('역|관광특구')]
for _, row in place.iterrows():
    print(f"  {row['순위']:2d}위. {row['핫스팟명']:<30} {row['실시간지역프로필점수']:6.2f}점")

