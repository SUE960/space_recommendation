#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사용자 피드백 및 품질 관리 시스템
================================================
추천 품질을 지속적으로 개선하기 위한 피드백 수집 및 분석 시스템

핵심 기능:
1. 사용자 만족도 수집
2. 추천 품질 메트릭 정의
3. A/B 테스트 지원
4. 지속적 개선을 위한 분석
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import sqlite3


class FeedbackQualitySystem:
    """사용자 피드백 및 품질 관리 시스템"""
    
    def __init__(self, db_path: str = "outputs/feedback.db"):
        """
        초기화
        
        Args:
            db_path: SQLite 데이터베이스 경로
        """
        self.db_path = db_path
        self._init_database()
        
        # 품질 메트릭 정의
        self.quality_metrics = self._define_quality_metrics()
    
    def _init_database(self):
        """피드백 데이터베이스 초기화"""
        Path(self.db_path).parent.mkdir(exist_ok=True, parents=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 피드백 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                recommendation_id TEXT,
                timestamp TEXT,
                rating INTEGER,
                visited BOOLEAN,
                satisfaction_score INTEGER,
                relevance_score INTEGER,
                diversity_score INTEGER,
                comment TEXT,
                user_age INTEGER,
                user_gender TEXT,
                recommended_region TEXT,
                recommendation_rank INTEGER
            )
        ''')
        
        # 추천 로그 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendation_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_id TEXT UNIQUE,
                user_id TEXT,
                timestamp TEXT,
                user_age INTEGER,
                user_gender TEXT,
                input_preferences TEXT,
                recommendations TEXT,
                algorithm_version TEXT
            )
        ''')
        
        # A/B 테스트 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id TEXT,
                user_id TEXT,
                variant TEXT,
                timestamp TEXT,
                conversion BOOLEAN,
                metrics TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _define_quality_metrics(self) -> Dict:
        """
        품질 메트릭 정의
        
        Returns:
            품질 메트릭 딕셔너리
        """
        return {
            'relevance': {
                'name': '적합성',
                'description': '추천된 지역이 사용자 선호도와 얼마나 잘 맞는가',
                'measurement': 'rating_avg',
                'target': 4.0,  # 5점 만점 중 4.0 이상
                'weight': 0.35
            },
            'satisfaction': {
                'name': '만족도',
                'description': '사용자가 추천 결과에 얼마나 만족하는가',
                'measurement': 'satisfaction_score_avg',
                'target': 4.0,
                'weight': 0.30
            },
            'visit_rate': {
                'name': '방문율',
                'description': '추천된 지역을 실제로 방문한 비율',
                'measurement': 'visited_ratio',
                'target': 0.50,  # 50% 이상
                'weight': 0.20
            },
            'diversity': {
                'name': '다양성',
                'description': '추천 결과가 얼마나 다양한가',
                'measurement': 'diversity_score_avg',
                'target': 3.5,
                'weight': 0.15
            }
        }
    
    def collect_feedback(
        self,
        user_id: str,
        recommendation_id: str,
        rating: int,
        visited: bool,
        user_age: int,
        user_gender: str,
        recommended_region: str,
        recommendation_rank: int,
        satisfaction_score: Optional[int] = None,
        relevance_score: Optional[int] = None,
        diversity_score: Optional[int] = None,
        comment: Optional[str] = None
    ) -> Dict:
        """
        사용자 피드백 수집
        
        Args:
            user_id: 사용자 ID
            recommendation_id: 추천 ID
            rating: 전체 평점 (1-5)
            visited: 실제 방문 여부
            user_age: 사용자 나이
            user_gender: 사용자 성별
            recommended_region: 추천된 지역
            recommendation_rank: 추천 순위
            satisfaction_score: 만족도 점수 (1-5)
            relevance_score: 적합성 점수 (1-5)
            diversity_score: 다양성 점수 (1-5)
            comment: 자유 코멘트
            
        Returns:
            피드백 ID 및 결과
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 기본값 설정
        if satisfaction_score is None:
            satisfaction_score = rating
        if relevance_score is None:
            relevance_score = rating
        if diversity_score is None:
            diversity_score = rating
        
        cursor.execute('''
            INSERT INTO feedback (
                user_id, recommendation_id, timestamp, rating, visited,
                satisfaction_score, relevance_score, diversity_score, comment,
                user_age, user_gender, recommended_region, recommendation_rank
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, recommendation_id, datetime.now().isoformat(),
            rating, visited, satisfaction_score, relevance_score, diversity_score,
            comment, user_age, user_gender, recommended_region, recommendation_rank
        ))
        
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'feedback_id': feedback_id,
            'status': 'success',
            'message': '피드백이 성공적으로 저장되었습니다.'
        }
    
    def log_recommendation(
        self,
        recommendation_id: str,
        user_id: str,
        user_age: int,
        user_gender: str,
        input_preferences: Dict,
        recommendations: List[Dict],
        algorithm_version: str = 'v1.0'
    ):
        """
        추천 로그 기록
        
        Args:
            recommendation_id: 추천 ID (고유)
            user_id: 사용자 ID
            user_age: 사용자 나이
            user_gender: 사용자 성별
            input_preferences: 사용자 입력 선호도
            recommendations: 추천 결과 리스트
            algorithm_version: 알고리즘 버전
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO recommendation_log (
                recommendation_id, user_id, timestamp, user_age, user_gender,
                input_preferences, recommendations, algorithm_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recommendation_id, user_id, datetime.now().isoformat(),
            user_age, user_gender,
            json.dumps(input_preferences, ensure_ascii=False),
            json.dumps(recommendations, ensure_ascii=False),
            algorithm_version
        ))
        
        conn.commit()
        conn.close()
    
    def calculate_quality_score(self, period_days: int = 30) -> Dict:
        """
        품질 점수 계산
        
        Args:
            period_days: 분석 기간 (일)
            
        Returns:
            품질 점수 및 세부 메트릭
        """
        conn = sqlite3.connect(self.db_path)
        
        # 기간 필터
        start_date = (datetime.now() - timedelta(days=period_days)).isoformat()
        
        # 피드백 데이터 로드
        df = pd.read_sql_query('''
            SELECT * FROM feedback
            WHERE timestamp >= ?
        ''', conn, params=(start_date,))
        
        conn.close()
        
        if df.empty:
            return {
                'overall_score': 0,
                'metrics': {},
                'status': 'no_data',
                'message': f'최근 {period_days}일간 피드백 데이터가 없습니다.'
            }
        
        # 메트릭별 계산
        metrics_scores = {}
        
        for metric_key, metric_info in self.quality_metrics.items():
            if metric_info['measurement'] == 'rating_avg':
                score = df['rating'].mean()
            elif metric_info['measurement'] == 'satisfaction_score_avg':
                score = df['satisfaction_score'].mean()
            elif metric_info['measurement'] == 'visited_ratio':
                score = df['visited'].mean()
            elif metric_info['measurement'] == 'diversity_score_avg':
                score = df['diversity_score'].mean()
            else:
                score = 0
            
            # 정규화 (0-100)
            if metric_info['measurement'] in ['rating_avg', 'satisfaction_score_avg', 'diversity_score_avg']:
                normalized_score = (score / 5.0) * 100
            else:  # visited_ratio
                normalized_score = score * 100
            
            # 목표 달성률
            achievement = (score / metric_info['target']) * 100 if metric_info['target'] > 0 else 0
            
            metrics_scores[metric_key] = {
                'name': metric_info['name'],
                'score': score,
                'normalized_score': normalized_score,
                'target': metric_info['target'],
                'achievement': achievement,
                'weight': metric_info['weight']
            }
        
        # 전체 품질 점수 (가중 평균)
        overall_score = sum(
            m['normalized_score'] * m['weight'] 
            for m in metrics_scores.values()
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'metrics': metrics_scores,
            'sample_size': len(df),
            'period_days': period_days,
            'status': 'success'
        }
    
    def analyze_feedback_by_segment(self, period_days: int = 30) -> Dict:
        """
        세그먼트별 피드백 분석
        
        Args:
            period_days: 분석 기간
            
        Returns:
            세그먼트별 분석 결과
        """
        conn = sqlite3.connect(self.db_path)
        start_date = (datetime.now() - timedelta(days=period_days)).isoformat()
        
        df = pd.read_sql_query('''
            SELECT * FROM feedback
            WHERE timestamp >= ?
        ''', conn, params=(start_date,))
        
        conn.close()
        
        if df.empty:
            return {'status': 'no_data'}
        
        # 연령대 추가
        df['age_group'] = df['user_age'].apply(self._get_age_group)
        
        # 세그먼트별 분석
        segments = {}
        
        # 연령대별
        for age_group in df['age_group'].unique():
            segment_df = df[df['age_group'] == age_group]
            segments[f'age_{age_group}'] = {
                'sample_size': len(segment_df),
                'avg_rating': segment_df['rating'].mean(),
                'visit_rate': segment_df['visited'].mean(),
                'avg_satisfaction': segment_df['satisfaction_score'].mean()
            }
        
        # 성별별
        for gender in df['user_gender'].unique():
            segment_df = df[df['user_gender'] == gender]
            segments[f'gender_{gender}'] = {
                'sample_size': len(segment_df),
                'avg_rating': segment_df['rating'].mean(),
                'visit_rate': segment_df['visited'].mean(),
                'avg_satisfaction': segment_df['satisfaction_score'].mean()
            }
        
        # 추천 순위별
        rank_analysis = df.groupby('recommendation_rank').agg({
            'rating': 'mean',
            'visited': 'mean',
            'satisfaction_score': 'mean'
        }).to_dict('index')
        
        return {
            'segments': segments,
            'rank_analysis': rank_analysis,
            'status': 'success'
        }
    
    def identify_improvement_areas(self, period_days: int = 30) -> List[Dict]:
        """
        개선 필요 영역 식별
        
        Args:
            period_days: 분석 기간
            
        Returns:
            개선 제안 리스트
        """
        quality_score = self.calculate_quality_score(period_days)
        
        if quality_score['status'] == 'no_data':
            return []
        
        improvements = []
        
        for metric_key, metric_data in quality_score['metrics'].items():
            if metric_data['achievement'] < 80:  # 목표의 80% 미달
                improvements.append({
                    'metric': metric_data['name'],
                    'current_score': metric_data['score'],
                    'target': metric_data['target'],
                    'achievement': metric_data['achievement'],
                    'priority': 'high' if metric_data['achievement'] < 60 else 'medium',
                    'suggestions': self._get_improvement_suggestions(metric_key, metric_data)
                })
        
        # 우선순위 정렬
        improvements.sort(key=lambda x: x['achievement'])
        
        return improvements
    
    def _get_improvement_suggestions(self, metric_key: str, metric_data: Dict) -> List[str]:
        """개선 제안 생성"""
        suggestions = []
        
        if metric_key == 'relevance':
            suggestions.extend([
                "사용자 선호도 가중치 재조정",
                "업종 매칭 알고리즘 개선",
                "연령대별 선호도 반영 강화"
            ])
        elif metric_key == 'satisfaction':
            suggestions.extend([
                "추천 설명의 명확성 향상",
                "사용자 입력 항목 최적화",
                "추천 다양성 증대"
            ])
        elif metric_key == 'visit_rate':
            suggestions.extend([
                "접근성 정보 추가 (교통편)",
                "실시간 혼잡도 정보 제공",
                "방문 인센티브 제공 검토"
            ])
        elif metric_key == 'diversity':
            suggestions.extend([
                "추천 알고리즘에 다양성 패널티 추가",
                "비슷한 지역 필터링 강화",
                "사용자 탐색 성향 반영"
            ])
        
        return suggestions
    
    def _get_age_group(self, age: int) -> str:
        """연령대 변환"""
        if age < 20:
            return '10대'
        elif age < 30:
            return '20대'
        elif age < 40:
            return '30대'
        elif age < 50:
            return '40대'
        elif age < 60:
            return '50대'
        else:
            return '60대이상'
    
    def run_ab_test(
        self,
        test_id: str,
        user_id: str,
        variant: str,
        conversion: bool,
        metrics: Dict
    ):
        """
        A/B 테스트 기록
        
        Args:
            test_id: 테스트 ID
            user_id: 사용자 ID
            variant: 변형 (A, B, ...)
            conversion: 전환 여부
            metrics: 추가 메트릭
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ab_test (test_id, user_id, variant, timestamp, conversion, metrics)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            test_id, user_id, variant, datetime.now().isoformat(),
            conversion, json.dumps(metrics, ensure_ascii=False)
        ))
        
        conn.commit()
        conn.close()
    
    def analyze_ab_test(self, test_id: str) -> Dict:
        """
        A/B 테스트 결과 분석
        
        Args:
            test_id: 테스트 ID
            
        Returns:
            분석 결과
        """
        conn = sqlite3.connect(self.db_path)
        
        df = pd.read_sql_query('''
            SELECT * FROM ab_test WHERE test_id = ?
        ''', conn, params=(test_id,))
        
        conn.close()
        
        if df.empty:
            return {'status': 'no_data'}
        
        results = {}
        
        for variant in df['variant'].unique():
            variant_df = df[df['variant'] == variant]
            results[variant] = {
                'sample_size': len(variant_df),
                'conversion_rate': variant_df['conversion'].mean(),
                'conversions': variant_df['conversion'].sum()
            }
        
        # 승자 결정
        winner = max(results.items(), key=lambda x: x[1]['conversion_rate'])
        
        return {
            'test_id': test_id,
            'results': results,
            'winner': winner[0],
            'status': 'success'
        }
    
    def generate_quality_report(self, period_days: int = 30) -> str:
        """
        품질 보고서 생성
        
        Args:
            period_days: 분석 기간
            
        Returns:
            마크다운 형식 보고서
        """
        quality = self.calculate_quality_score(period_days)
        segment_analysis = self.analyze_feedback_by_segment(period_days)
        improvements = self.identify_improvement_areas(period_days)
        
        report = f"""# 추천 시스템 품질 보고서
        
**분석 기간**: 최근 {period_days}일  
**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. 전체 품질 점수

**종합 점수**: {quality['overall_score']:.2f}점 / 100점

"""
        
        if quality['status'] == 'success':
            report += "### 메트릭별 세부 점수\n\n"
            for metric_key, metric_data in quality['metrics'].items():
                report += f"#### {metric_data['name']}\n"
                report += f"- 현재 점수: {metric_data['score']:.2f}\n"
                report += f"- 정규화 점수: {metric_data['normalized_score']:.2f}/100\n"
                report += f"- 목표: {metric_data['target']}\n"
                report += f"- 목표 달성률: {metric_data['achievement']:.1f}%\n"
                report += f"- 가중치: {metric_data['weight']*100:.0f}%\n\n"
        
        report += "\n---\n\n## 2. 세그먼트별 분석\n\n"
        
        if segment_analysis['status'] == 'success':
            report += "### 연령대별 성과\n\n"
            for key, data in segment_analysis['segments'].items():
                if key.startswith('age_'):
                    age_group = key.replace('age_', '')
                    report += f"- **{age_group}**: 평점 {data['avg_rating']:.2f}, 방문율 {data['visit_rate']*100:.1f}%\n"
            
            report += "\n### 추천 순위별 성과\n\n"
            for rank, data in segment_analysis['rank_analysis'].items():
                report += f"- **{rank}위**: 평점 {data['rating']:.2f}, 방문율 {data['visited']*100:.1f}%\n"
        
        report += "\n---\n\n## 3. 개선 필요 영역\n\n"
        
        if improvements:
            for imp in improvements:
                report += f"### [{imp['priority'].upper()}] {imp['metric']}\n"
                report += f"- 현재: {imp['current_score']:.2f}\n"
                report += f"- 목표: {imp['target']}\n"
                report += f"- 달성률: {imp['achievement']:.1f}%\n"
                report += f"**개선 제안**:\n"
                for sug in imp['suggestions']:
                    report += f"  - {sug}\n"
                report += "\n"
        else:
            report += "모든 메트릭이 목표를 달성했습니다! 🎉\n"
        
        return report


def demo_feedback_system():
    """피드백 시스템 데모"""
    
    print("=" * 80)
    print("사용자 피드백 및 품질 관리 시스템 데모")
    print("=" * 80)
    
    system = FeedbackQualitySystem()
    
    # 샘플 데이터 생성
    print("\n[1단계] 샘플 피드백 데이터 생성 중...")
    
    import uuid
    
    sample_data = [
        # 20대
        {'age': 22, 'gender': '남', 'region': '홍대', 'rank': 1, 'rating': 5, 'visited': True, 'satisfaction': 5},
        {'age': 25, 'gender': '여', 'region': '강남역', 'rank': 1, 'rating': 4, 'visited': True, 'satisfaction': 4},
        {'age': 28, 'gender': '남', 'region': '홍대', 'rank': 2, 'rating': 4, 'visited': False, 'satisfaction': 3},
        # 30대
        {'age': 32, 'gender': '여', 'region': '강남역', 'rank': 1, 'rating': 5, 'visited': True, 'satisfaction': 5},
        {'age': 35, 'gender': '남', 'region': '서초', 'rank': 1, 'rating': 4, 'visited': True, 'satisfaction': 4},
        # 50대
        {'age': 50, 'gender': '남', 'region': '홍대', 'rank': 1, 'rating': 2, 'visited': False, 'satisfaction': 2, 'comment': '너무 시끄러워요'},
        {'age': 52, 'gender': '여', 'region': '종로', 'rank': 1, 'rating': 5, 'visited': True, 'satisfaction': 5},
        {'age': 55, 'gender': '남', 'region': '잠실', 'rank': 1, 'rating': 5, 'visited': True, 'satisfaction': 5},
    ]
    
    for data in sample_data:
        rec_id = str(uuid.uuid4())
        user_id = f"user_{data['age']}_{data['gender']}"
        
        system.collect_feedback(
            user_id=user_id,
            recommendation_id=rec_id,
            rating=data['rating'],
            visited=data['visited'],
            user_age=data['age'],
            user_gender=data['gender'],
            recommended_region=data['region'],
            recommendation_rank=data['rank'],
            satisfaction_score=data['satisfaction'],
            comment=data.get('comment')
        )
    
    print(f"  ✓ {len(sample_data)}개 피드백 데이터 생성 완료")
    
    # 품질 점수 계산
    print("\n[2단계] 품질 점수 계산 중...")
    quality = system.calculate_quality_score(period_days=30)
    
    print(f"\n  📊 종합 품질 점수: {quality['overall_score']:.2f}점")
    print(f"  📈 분석 샘플 수: {quality['sample_size']}개\n")
    
    for metric_key, metric_data in quality['metrics'].items():
        status = "✅" if metric_data['achievement'] >= 80 else "⚠️"
        print(f"  {status} {metric_data['name']}: {metric_data['normalized_score']:.1f}점 "
              f"(목표 달성률: {metric_data['achievement']:.1f}%)")
    
    # 세그먼트별 분석
    print("\n[3단계] 세그먼트별 분석...")
    segment = system.analyze_feedback_by_segment(period_days=30)
    
    if segment['status'] == 'success':
        print("\n  📍 연령대별 성과:")
        for key, data in segment['segments'].items():
            if key.startswith('age_'):
                age_group = key.replace('age_', '')
                print(f"    • {age_group}: 평점 {data['avg_rating']:.2f}, "
                      f"방문율 {data['visit_rate']*100:.0f}%")
    
    # 개선 영역 식별
    print("\n[4단계] 개선 필요 영역 식별...")
    improvements = system.identify_improvement_areas(period_days=30)
    
    if improvements:
        print(f"\n  ⚠️  {len(improvements)}개 개선 필요 영역 발견\n")
        for imp in improvements[:2]:  # 상위 2개만 표시
            print(f"  [{imp['priority'].upper()}] {imp['metric']}")
            print(f"    - 달성률: {imp['achievement']:.1f}%")
            print(f"    - 개선 제안: {imp['suggestions'][0]}")
    else:
        print("\n  ✅ 모든 메트릭이 목표를 달성했습니다!")
    
    # 보고서 생성
    print("\n[5단계] 품질 보고서 생성...")
    report = system.generate_quality_report(period_days=30)
    
    report_path = Path("outputs/quality_report.md")
    report_path.write_text(report, encoding='utf-8')
    
    print(f"  ✓ 보고서 저장: {report_path}")
    
    print("\n" + "=" * 80)
    print("✅ 데모 완료!")
    print("=" * 80)


if __name__ == '__main__':
    demo_feedback_system()

