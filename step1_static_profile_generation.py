"""
STEP 1: 정적 집단 프로필 생성 시스템
================================================
서울 카드 데이터를 활용하여 나이/성별/소득 기반 소비 패턴 프로필을 생성합니다.

주요 기능:
1. 연령대별 소비 패턴 분석
2. 성별 소비 패턴 분석  
3. 업종별 선호도 분석
4. 시간대별 소비 패턴 분석
5. 지역별 방문 선호도 분석
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict

class StaticProfileGenerator:
    """정적 집단 프로필 생성 클래스"""
    
    def __init__(self, data_dir: str = "data_2"):
        """
        초기화
        
        Args:
            data_dir: 카드 데이터가 있는 디렉토리
        """
        self.data_dir = Path(data_dir)
        self.profiles = {}
        
        # 연령대 매핑
        self.age_groups = {
            '20세미만': 'teen',
            '20_29세': '20s',
            '30_39세': '30s', 
            '40_49세': '40s',
            '50_59세': '50s',
            '60_69세': '60s',
            '70세이상': '70plus'
        }
        
        # 성별 매핑
        self.gender_map = {'남': 'male', '여': 'female'}
        
    def load_card_data(self) -> pd.DataFrame:
        """
        카드 데이터 로드 (성별/연령대별 행정동별 데이터)
        
        Returns:
            카드 데이터 DataFrame
        """
        print("📊 카드 데이터 로딩 중...")
        
        file_path = self.data_dir / "6.서울시 내국인 성별 연령대별(행정동별).csv"
        df = pd.read_csv(file_path, encoding='cp949')
        
        print(f"✅ 총 {len(df):,}개 레코드 로드 완료")
        print(f"   - 기간: {df['기준일자'].min()} ~ {df['기준일자'].max()}")
        print(f"   - 연령대: {df['연령대'].nunique()}개")
        print(f"   - 업종: {df['업종대분류'].nunique()}개")
        
        return df
        
    def load_time_data(self) -> pd.DataFrame:
        """
        시간대별 소비 데이터 로드
        
        Returns:
            시간대별 데이터 DataFrame
        """
        print("⏰ 시간대별 데이터 로딩 중...")
        
        file_path = self.data_dir / "2.서울시민의 일별 시간대별(행정동).csv"
        df = pd.read_csv(file_path, encoding='cp949')
        
        print(f"✅ 총 {len(df):,}개 레코드 로드 완료")
        
        return df
    
    def analyze_age_gender_profiles(self, df: pd.DataFrame) -> Dict:
        """
        연령대/성별별 소비 패턴 프로필 생성
        
        Args:
            df: 카드 데이터 DataFrame
            
        Returns:
            연령대/성별별 프로필 딕셔너리
        """
        print("\n👥 연령대/성별별 프로필 생성 중...")
        
        profiles = {}
        
        for age_kr, age_en in self.age_groups.items():
            for gender_kr, gender_en in self.gender_map.items():
                # 해당 집단 데이터 필터링
                mask = (df['연령대'] == age_kr) & (df['성별'] == gender_kr)
                group_data = df[mask]
                
                if len(group_data) == 0:
                    continue
                
                profile_key = f"{age_en}_{gender_en}"
                
                # 1. 업종별 소비 패턴
                industry_spending = group_data.groupby('업종대분류').agg({
                    '카드이용금액계': 'sum',
                    '카드이용건수계': 'sum'
                }).reset_index()
                
                industry_spending['평균거래금액'] = (
                    industry_spending['카드이용금액계'] / 
                    industry_spending['카드이용건수계']
                )
                
                # 업종별 선호도 (총 소비 금액 기준 비율)
                total_spending = industry_spending['카드이용금액계'].sum()
                industry_spending['선호도비율'] = (
                    industry_spending['카드이용금액계'] / total_spending * 100
                )
                
                # 상위 10개 업종
                top_industries = industry_spending.nlargest(10, '카드이용금액계')
                
                # 2. 지역별 방문 패턴
                region_pattern = group_data.groupby('가맹점행정동코드').agg({
                    '카드이용금액계': 'sum',
                    '카드이용건수계': 'sum'
                }).reset_index()
                
                region_pattern['방문빈도'] = region_pattern['카드이용건수계']
                top_regions = region_pattern.nlargest(10, '카드이용금액계')
                
                # 3. 소비 특성 지표
                total_transactions = group_data['카드이용건수계'].sum()
                avg_transaction = group_data['카드이용금액계'].sum() / total_transactions
                
                # 프로필 생성
                profile = {
                    'segment_info': {
                        'age_group': age_en,
                        'age_group_kr': age_kr,
                        'gender': gender_en,
                        'gender_kr': gender_kr,
                        'profile_id': profile_key
                    },
                    'spending_characteristics': {
                        'total_spending': int(group_data['카드이용금액계'].sum()),
                        'total_transactions': int(total_transactions),
                        'avg_transaction_amount': int(avg_transaction),
                        'active_days': int(group_data['기준일자'].nunique())
                    },
                    'industry_preferences': [
                        {
                            'industry': row['업종대분류'],
                            'spending_amount': int(row['카드이용금액계']),
                            'transaction_count': int(row['카드이용건수계']),
                            'avg_amount': int(row['평균거래금액']),
                            'preference_ratio': round(row['선호도비율'], 2),
                            'rank': idx + 1
                        }
                        for idx, (_, row) in enumerate(top_industries.iterrows())
                    ],
                    'region_preferences': [
                        {
                            'region_code': str(row['가맹점행정동코드']),
                            'spending_amount': int(row['카드이용금액계']),
                            'visit_count': int(row['카드이용건수계']),
                            'rank': idx + 1
                        }
                        for idx, (_, row) in enumerate(top_regions.iterrows())
                    ]
                }
                
                profiles[profile_key] = profile
                
                print(f"✓ {age_kr} {gender_kr}: {len(group_data):,}건 분석 완료")
        
        print(f"\n✅ 총 {len(profiles)}개 세그먼트 프로필 생성 완료")
        
        return profiles
    
    def analyze_time_patterns(self, df: pd.DataFrame, profiles: Dict) -> Dict:
        """
        시간대별 소비 패턴 분석 (프로필에 추가)
        
        Args:
            df: 시간대별 데이터 DataFrame
            profiles: 기존 프로필 딕셔너리
            
        Returns:
            시간대 패턴이 추가된 프로필
        """
        print("\n⏰ 시간대별 소비 패턴 분석 중...")
        
        # 시간대별 집계
        time_pattern = df.groupby('시간대').agg({
            '카드이용금액계': 'sum',
            '카드이용건수계': 'sum'
        }).reset_index()
        
        # 시간대 구분
        def categorize_time(hour):
            if 6 <= hour < 12:
                return '오전'
            elif 12 <= hour < 18:
                return '오후'
            elif 18 <= hour < 24:
                return '저녁'
            else:
                return '새벽'
        
        time_pattern['시간대구분'] = time_pattern['시간대'].apply(categorize_time)
        
        # 시간대별 비율 계산
        total_spending = time_pattern['카드이용금액계'].sum()
        time_pattern['비율'] = time_pattern['카드이용금액계'] / total_spending * 100
        
        # 전체 프로필에 시간대 패턴 추가 (공통 패턴)
        time_patterns = [
            {
                'hour': int(row['시간대']),
                'time_category': row['시간대구분'],
                'spending_amount': int(row['카드이용금액계']),
                'transaction_count': int(row['카드이용건수계']),
                'ratio': round(row['비율'], 2)
            }
            for _, row in time_pattern.iterrows()
        ]
        
        # 시간대별 집계
        time_summary = time_pattern.groupby('시간대구분').agg({
            '카드이용금액계': 'sum',
            '비율': 'sum'
        }).reset_index()
        
        time_summary_list = [
            {
                'period': row['시간대구분'],
                'spending_ratio': round(row['비율'], 2)
            }
            for _, row in time_summary.iterrows()
        ]
        
        print(f"✅ 시간대 패턴 분석 완료")
        
        return {
            'hourly_patterns': time_patterns,
            'period_summary': time_summary_list
        }
    
    def create_user_segment_matcher(self, profiles: Dict) -> Dict:
        """
        사용자 입력을 세그먼트에 매칭하는 룩업 테이블 생성
        
        Args:
            profiles: 생성된 프로필 딕셔너리
            
        Returns:
            매칭 룩업 테이블
        """
        print("\n🔗 사용자-세그먼트 매칭 테이블 생성 중...")
        
        matcher = {
            'age_mapping': self.age_groups,
            'gender_mapping': self.gender_map,
            'available_segments': list(profiles.keys()),
            'segment_descriptions': {}
        }
        
        # 각 세그먼트 설명 추가
        for segment_id, profile in profiles.items():
            info = profile['segment_info']
            spending = profile['spending_characteristics']
            top_industry = profile['industry_preferences'][0] if profile['industry_preferences'] else None
            
            description = {
                'segment_id': segment_id,
                'description_kr': f"{info['age_group_kr']} {info['gender_kr']}",
                'total_spending': spending['total_spending'],
                'avg_transaction': spending['avg_transaction_amount'],
                'primary_interest': top_industry['industry'] if top_industry else 'N/A'
            }
            
            matcher['segment_descriptions'][segment_id] = description
        
        print(f"✅ {len(matcher['available_segments'])}개 세그먼트 매칭 테이블 생성 완료")
        
        return matcher
    
    def generate_all_profiles(self) -> Tuple[Dict, Dict, Dict]:
        """
        전체 프로필 생성 프로세스 실행
        
        Returns:
            (프로필, 시간패턴, 매칭테이블) 튜플
        """
        print("=" * 70)
        print("🚀 STEP 1: 정적 집단 프로필 생성 시작")
        print("=" * 70)
        
        # 1. 카드 데이터 로드
        card_df = self.load_card_data()
        
        # 2. 연령대/성별 프로필 생성
        profiles = self.analyze_age_gender_profiles(card_df)
        
        # 3. 시간대별 패턴 분석
        time_df = self.load_time_data()
        time_patterns = self.analyze_time_patterns(time_df, profiles)
        
        # 4. 사용자 매칭 테이블 생성
        matcher = self.create_user_segment_matcher(profiles)
        
        print("\n" + "=" * 70)
        print("✅ STEP 1 완료!")
        print("=" * 70)
        
        return profiles, time_patterns, matcher
    
    def save_profiles(self, profiles: Dict, time_patterns: Dict, matcher: Dict, output_dir: str = "outputs"):
        """
        생성된 프로필을 파일로 저장
        
        Args:
            profiles: 프로필 딕셔너리
            time_patterns: 시간 패턴 딕셔너리
            matcher: 매칭 테이블
            output_dir: 출력 디렉토리
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print("\n💾 프로필 저장 중...")
        
        # 1. 전체 프로필 저장
        profile_file = output_path / "step1_static_profiles.json"
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
        print(f"✓ 프로필 저장: {profile_file}")
        
        # 2. 시간 패턴 저장
        time_file = output_path / "step1_time_patterns.json"
        with open(time_file, 'w', encoding='utf-8') as f:
            json.dump(time_patterns, f, ensure_ascii=False, indent=2)
        print(f"✓ 시간 패턴 저장: {time_file}")
        
        # 3. 매칭 테이블 저장
        matcher_file = output_path / "step1_segment_matcher.json"
        with open(matcher_file, 'w', encoding='utf-8') as f:
            json.dump(matcher, f, ensure_ascii=False, indent=2)
        print(f"✓ 매칭 테이블 저장: {matcher_file}")
        
        # 4. 요약 리포트 생성
        self._create_summary_report(profiles, time_patterns, matcher, output_path)
        
        print("\n✅ 모든 파일 저장 완료!")
    
    def _create_summary_report(self, profiles: Dict, time_patterns: Dict, matcher: Dict, output_path: Path):
        """요약 리포트 생성"""
        
        report_file = output_path / "step1_summary_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# STEP 1: 정적 집단 프로필 생성 결과 리포트\n\n")
            f.write(f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 프로필 생성 요약\n\n")
            f.write(f"- **총 세그먼트 수**: {len(profiles)}개\n")
            f.write(f"- **연령대**: {len(self.age_groups)}개\n")
            f.write(f"- **성별**: {len(self.gender_map)}개\n\n")
            
            f.write("## 🎯 세그먼트별 주요 특징\n\n")
            f.write("| 세그먼트 | 총 소비액 | 평균 거래액 | 주요 관심사 |\n")
            f.write("|---------|-----------|------------|------------|\n")
            
            for segment_id in sorted(profiles.keys()):
                profile = profiles[segment_id]
                info = profile['segment_info']
                spending = profile['spending_characteristics']
                top_industry = profile['industry_preferences'][0] if profile['industry_preferences'] else None
                
                f.write(f"| {info['age_group_kr']} {info['gender_kr']} | "
                       f"{spending['total_spending']:,}원 | "
                       f"{spending['avg_transaction_amount']:,}원 | "
                       f"{top_industry['industry'] if top_industry else 'N/A'} |\n")
            
            f.write("\n## ⏰ 시간대별 소비 패턴\n\n")
            f.write("| 시간대 | 소비 비율 |\n")
            f.write("|--------|----------|\n")
            
            for period in time_patterns['period_summary']:
                f.write(f"| {period['period']} | {period['spending_ratio']:.1f}% |\n")
            
            f.write("\n## 📈 세그먼트별 TOP 3 업종\n\n")
            
            for segment_id in sorted(profiles.keys()):
                profile = profiles[segment_id]
                info = profile['segment_info']
                
                f.write(f"### {info['age_group_kr']} {info['gender_kr']}\n\n")
                
                for idx, industry in enumerate(profile['industry_preferences'][:3], 1):
                    f.write(f"{idx}. **{industry['industry']}** - "
                           f"{industry['preference_ratio']:.1f}% "
                           f"(평균 {industry['avg_amount']:,}원)\n")
                
                f.write("\n")
        
        print(f"✓ 요약 리포트 저장: {report_file}")


def main():
    """메인 실행 함수"""
    
    # 프로필 생성기 초기화
    generator = StaticProfileGenerator(data_dir="data_2")
    
    # 프로필 생성
    profiles, time_patterns, matcher = generator.generate_all_profiles()
    
    # 결과 저장
    generator.save_profiles(profiles, time_patterns, matcher)
    
    print("\n" + "=" * 70)
    print("🎉 STEP 1 정적 집단 프로필 생성 완료!")
    print("=" * 70)
    print("\n생성된 파일:")
    print("  - outputs/step1_static_profiles.json")
    print("  - outputs/step1_time_patterns.json")
    print("  - outputs/step1_segment_matcher.json")
    print("  - outputs/step1_summary_report.md")
    print("\n이제 이 프로필을 사용하여 사용자를 세그먼트에 매칭할 수 있습니다.")


if __name__ == "__main__":
    main()





