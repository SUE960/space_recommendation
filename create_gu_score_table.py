#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 전체 25개 구 지역 품질 점수표 생성
기존 분석 데이터 활용
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime


def load_existing_data():
    """기존 분석 데이터 로드"""
    
    # 1. 기본 특성 데이터
    final_df = pd.read_csv('outputs/seoul_all_gu_final.csv', encoding='utf-8-sig')
    
    # 2. CV 데이터
    cv_df = pd.read_csv('outputs/seoul_all_gu_cv.csv', encoding='utf-8-sig')
    
    # 3. 성장률 데이터  
    growth_df = pd.read_csv('outputs/seoul_all_gu_with_growth.csv', encoding='utf-8-sig')
    
    return final_df, cv_df, growth_df


def calculate_scores():
    """25개 구 점수 계산"""
    
    print("="*100)
    print("서울시 25개 구 Level 1 지역 품질 점수 산출")
    print("="*100)
    
    # 데이터 로드
    final_df, cv_df, growth_df = load_existing_data()
    
    # 결과 DataFrame 초기화
    results = []
    
    for idx, row in final_df.iterrows():
        gu_name = row['구']
        
        # ===== 1. 상업활동 점수 (30%) =====
        # 업종 다양성 기준
        diversity_text = row['업종다양성']
        if '높음' in diversity_text:
            diversity_count = int(diversity_text.split('(')[1].split('개')[0])
            diversity_score = min(diversity_count * 6.67, 100)  # 15개면 100점
        elif '보통' in diversity_text:
            diversity_count = int(diversity_text.split('(')[1].split('개')[0])
            diversity_score = min(diversity_count * 7.14, 85)  # 14개면 100점
        else:  # 낮음
            diversity_count = int(diversity_text.split('(')[1].split('개')[0])
            diversity_score = diversity_count * 8  # 최대 80점
        
        # CV(변동계수)로 안정성 점수 (낮을수록 좋음)
        cv_value = cv_df[cv_df['구'] == gu_name]['변동계수(%)'].values[0] if gu_name in cv_df['구'].values else 20.0
        stability_score = max(0, 100 - (cv_value * 3))  # CV 20% 이하가 좋음
        
        # 상업활동 점수 = 다양성 60% + 안정성 40%
        commercial_score = (diversity_score * 0.6 + stability_score * 0.4)
        
        # ===== 2. 특화도 점수 (25%) =====
        feature_text = row['특징']
        
        if '데이터 부족' in feature_text:
            specialization_score = 30
            main_industry = '데이터 부족'
            spec_ratio = 0
        else:
            # 특화 비율 추출
            if '%' in feature_text:
                try:
                    spec_ratio = float(feature_text.split('(')[1].split('%')[0])
                    main_industry = feature_text.split(' 특화')[0]
                except:
                    spec_ratio = 50
                    main_industry = feature_text[:20]
            else:
                spec_ratio = 50
                main_industry = feature_text[:20]
            
            # 특화도 점수 = 특화 비율 기반
            # 30-50%: 중간 특화, 50-70%: 높은 특화, 70%+: 매우 높은 특화
            if spec_ratio >= 70:
                specialization_score = 90 + (min(spec_ratio - 70, 30) * 0.33)
            elif spec_ratio >= 50:
                specialization_score = 70 + ((spec_ratio - 50) * 1.0)
            elif spec_ratio >= 30:
                specialization_score = 50 + ((spec_ratio - 30) * 1.0)
            else:
                specialization_score = spec_ratio * 1.67
        
        # ===== 3. 인구통계 점수 (20%) =====
        # 안정성(CV)을 인구활동성으로 해석
        demographic_score = stability_score  # 재사용
        
        # ===== 4. 경제력 점수 (25%) =====
        # 성장률 기반
        growth_text = row['성장률']
        
        if '↑상승' in growth_text:
            growth_value = float(growth_text.split('%')[0].replace('+', ''))
            economic_score = 70 + min(growth_value * 5, 30)  # 최대 100점
        elif '↓하락' in growth_text:
            growth_value = float(growth_text.split('%')[0])
            economic_score = 50 + max(growth_value * 10, -30)  # 최소 20점
        else:  # 유지
            growth_value = float(growth_text.split('%')[0].replace('+', ''))
            economic_score = 60 + (abs(growth_value) * 2)  # 60-70점
        
        # ===== 종합 점수 =====
        total_score = (
            commercial_score * 0.30 +
            specialization_score * 0.25 +
            demographic_score * 0.20 +
            economic_score * 0.25
        )
        
        # 등급 부여
        if total_score >= 80:
            grade = 'S급'
            grade_desc = '초우량 상권'
        elif total_score >= 70:
            grade = 'A급'
            grade_desc = '우량 상권'
        elif total_score >= 60:
            grade = 'B급'
            grade_desc = '보통 상권'
        elif total_score >= 50:
            grade = 'C급'
            grade_desc = '개선 필요'
        else:
            grade = 'D급'
            grade_desc = '저활성 지역'
        
        results.append({
            '구': gu_name,
            '종합점수': round(total_score, 1),
            '상업활동점수': round(commercial_score, 1),
            '특화도점수': round(specialization_score, 1),
            '인구통계점수': round(demographic_score, 1),
            '경제력점수': round(economic_score, 1),
            '등급': grade,
            '등급설명': grade_desc,
            '주요특화업종': main_industry,
            '특화비율': round(spec_ratio, 1),
            '업종수': diversity_count,
            'CV': round(cv_value, 1),
            '성장률': growth_text
        })
    
    # DataFrame 생성 및 정렬
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values('종합점수', ascending=False).reset_index(drop=True)
    result_df['순위'] = range(1, len(result_df) + 1)
    
    return result_df


def print_table(df):
    """표 형식으로 출력"""
    
    print("\n" + "="*100)
    print("서울시 25개 구 지역 품질 점수표 (Level 1: 객관적 평가)")
    print("="*100)
    
    print(f"\n{'순위':<4} {'구':<10} {'종합':<7} {'상업':<7} {'특화':<7} {'인구':<7} {'경제':<7} "
          f"{'등급':<8} {'주요 특화업종':<25} {'특화율':<8}")
    print("-" * 100)
    
    for _, row in df.iterrows():
        print(f"{row['순위']:<4} {row['구']:<10} "
              f"{row['종합점수']:>5.1f}  "
              f"{row['상업활동점수']:>5.1f}  "
              f"{row['특화도점수']:>5.1f}  "
              f"{row['인구통계점수']:>5.1f}  "
              f"{row['경제력점수']:>5.1f}  "
              f"{row['등급']:<8} "
              f"{row['주요특화업종'][:25]:<25} "
              f"{row['특화비율']:>6.1f}%")
    
    # 통계
    print("\n" + "="*100)
    print("통계 요약")
    print("="*100)
    
    print(f"\n[등급별 분포]")
    for grade in ['S급', 'A급', 'B급', 'C급', 'D급']:
        count = len(df[df['등급'] == grade])
        if count > 0:
            gus = ', '.join(df[df['등급'] == grade]['구'].tolist())
            print(f"  {grade}: {count}개 구 - {gus}")
    
    print(f"\n[점수 통계]")
    print(f"  평균: {df['종합점수'].mean():.1f}점")
    print(f"  중앙값: {df['종합점수'].median():.1f}점")
    print(f"  최고: {df['종합점수'].max():.1f}점 ({df.iloc[0]['구']})")
    print(f"  최저: {df['종합점수'].min():.1f}점 ({df.iloc[-1]['구']})")
    print(f"  표준편차: {df['종합점수'].std():.1f}점")
    
    print(f"\n[TOP 5 구]")
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        print(f"  {i+1}. {row['구']}: {row['종합점수']:.1f}점 "
              f"({row['주요특화업종']} {row['특화비율']:.1f}% 특화)")


def save_results(df):
    """결과 저장"""
    
    os.makedirs('outputs', exist_ok=True)
    
    # CSV 저장
    csv_file = 'outputs/seoul_25gu_level1_scores.csv'
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV 저장: {csv_file}")
    
    # Markdown 표 생성
    md_file = 'outputs/서울시_25개구_지역점수표_Level1.md'
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 서울시 25개 구 지역 품질 점수표\n\n")
        f.write(f"**생성일시:** {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n\n")
        f.write("**평가 수준:** Level 1 - 지역 객관적 품질 평가\n\n")
        f.write("**평가 기준:**\n")
        f.write("- 상업활동 (30%): 업종 다양성 + 소비 안정성\n")
        f.write("- 특화도 (25%): 주요 업종 집중도\n")
        f.write("- 인구통계 (20%): 인구 활동 안정성\n")
        f.write("- 경제력 (25%): 성장률 및 발전 가능성\n\n")
        f.write("---\n\n")
        
        f.write("## 📊 전체 순위표\n\n")
        f.write("| 순위 | 구 | 종합점수 | 상업활동 | 특화도 | 인구통계 | 경제력 | 등급 | 주요 특화업종 | 특화비율 |\n")
        f.write("|:----:|:---|:--------:|:--------:|:------:|:--------:|:------:|:----:|:-------------|:--------:|\n")
        
        for _, row in df.iterrows():
            f.write(f"| {row['순위']} | {row['구']} | **{row['종합점수']:.1f}** | "
                   f"{row['상업활동점수']:.1f} | {row['특화도점수']:.1f} | "
                   f"{row['인구통계점수']:.1f} | {row['경제력점수']:.1f} | "
                   f"{row['등급']} | {row['주요특화업종']} | {row['특화비율']:.1f}% |\n")
        
        f.write("\n---\n\n")
        
        # 등급별 상세
        f.write("## 🏆 등급별 상세 분석\n\n")
        
        for grade in ['S급', 'A급', 'B급', 'C급', 'D급']:
            grade_df = df[df['등급'] == grade]
            if len(grade_df) == 0:
                continue
            
            f.write(f"### {grade} - {grade_df.iloc[0]['등급설명']}\n\n")
            
            for _, row in grade_df.iterrows():
                f.write(f"#### {row['순위']}위: {row['구']} ({row['종합점수']:.1f}점)\n\n")
                f.write(f"- **주요 특화:** {row['주요특화업종']} ({row['특화비율']:.1f}%)\n")
                f.write(f"- **업종 수:** {row['업종수']}개\n")
                f.write(f"- **성장률:** {row['성장률']}\n")
                f.write(f"- **점수 구성:**\n")
                f.write(f"  - 상업활동: {row['상업활동점수']:.1f}점\n")
                f.write(f"  - 특화도: {row['특화도점수']:.1f}점\n")
                f.write(f"  - 인구통계: {row['인구통계점수']:.1f}점\n")
                f.write(f"  - 경제력: {row['경제력점수']:.1f}점\n")
                f.write("\n")
        
        f.write("---\n\n")
        
        # 인사이트
        f.write("## 💡 주요 인사이트\n\n")
        
        top3 = df.head(3)
        f.write("### TOP 3 우수 지역\n\n")
        for i, (_, row) in enumerate(top3.iterrows(), 1):
            f.write(f"{i}. **{row['구']}** ({row['종합점수']:.1f}점) - "
                   f"{row['주요특화업종']} 특화, {row['성장률']}\n")
        
        f.write("\n### 특화 패턴\n\n")
        
        # 업종별 특화 구 분류
        industry_groups = {}
        for _, row in df.iterrows():
            industry = row['주요특화업종']
            if industry not in industry_groups:
                industry_groups[industry] = []
            industry_groups[industry].append(f"{row['구']}({row['종합점수']:.1f}점)")
        
        for industry, gus in sorted(industry_groups.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            f.write(f"- **{industry}**: {', '.join(gus)}\n")
        
        f.write("\n---\n\n")
        f.write("## 📌 참고사항\n\n")
        f.write("- 이 점수는 **지역의 객관적 품질**을 평가한 것입니다.\n")
        f.write("- **모든 사용자에게 동일한 점수**가 적용됩니다.\n")
        f.write("- **개인화 추천**을 위해서는 Level 2 (사용자-지역 매칭)가 필요합니다.\n")
        f.write("- 사용자의 연령, 소득, 선호도에 따라 최적 지역은 달라질 수 있습니다.\n")
    
    print(f"✓ Markdown 저장: {md_file}")


def main():
    """메인 실행"""
    
    # 점수 계산
    result_df = calculate_scores()
    
    # 출력
    print_table(result_df)
    
    # 저장
    save_results(result_df)
    
    print("\n" + "="*100)
    print("✅ 서울시 25개 구 Level 1 지역 품질 점수표 생성 완료!")
    print("="*100)
    
    return result_df


if __name__ == '__main__':
    result = main()

