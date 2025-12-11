#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실시간 데이터 업데이트 시스템
================================================
API 데이터를 주기적으로 갱신하여 항상 최신 정보를 제공

핵심 기능:
1. 서울시 API에서 실시간 데이터 수집
2. 주기적 자동 업데이트
3. 데이터 버전 관리
4. 변경 사항 추적 및 알림
"""

import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import time
import threading
import logging
from collections import defaultdict


class RealtimeDataUpdater:
    """실시간 데이터 업데이트 시스템"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        data_dir: str = "outputs/realtime_data",
        update_interval_hours: int = 6
    ):
        """
        초기화
        
        Args:
            api_key: 서울시 API 키 (선택)
            data_dir: 데이터 저장 디렉토리
            update_interval_hours: 업데이트 간격 (시간)
        """
        self.api_key = api_key
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True, parents=True)
        
        self.update_interval_hours = update_interval_hours
        
        # 로깅 설정
        self._setup_logging()
        
        # 데이터 버전 관리
        self.version_file = self.data_dir / "version.json"
        self.current_version = self._load_version()
        
        # API 엔드포인트 정의
        self.api_endpoints = self._define_api_endpoints()
    
    def _setup_logging(self):
        """로깅 설정"""
        log_file = self.data_dir / "update.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _define_api_endpoints(self) -> Dict:
        """
        API 엔드포인트 정의
        
        Returns:
            API 엔드포인트 딕셔너리
        """
        return {
            'commercial_area': {
                'name': '서울시 우리마을가게 상권분석서비스',
                'url': 'http://openapi.seoul.go.kr:8088/{api_key}/json/VwsmSignguStorW/',
                'description': '상권 활성화 지수 및 업종 정보',
                'update_frequency': 'daily'
            },
            'population': {
                'name': '서울시 우리마을가게 상권분석서비스(업종별 상주인구)',
                'url': 'http://openapi.seoul.go.kr:8088/{api_key}/json/VwsmSignguStorW2/',
                'description': '업종별 상주인구 정보',
                'update_frequency': 'weekly'
            },
            'card_usage': {
                'name': '서울시 빅데이터캠퍼스 카드 사용 데이터',
                'description': '카드 사용 트렌드 분석',
                'update_frequency': 'monthly',
                'simulated': True  # 실제 API 없음, 시뮬레이션
            }
        }
    
    def _load_version(self) -> Dict:
        """현재 데이터 버전 로드"""
        if self.version_file.exists():
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'version': '0.0.0',
                'last_update': None,
                'datasets': {}
            }
    
    def _save_version(self):
        """데이터 버전 저장"""
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_version, f, ensure_ascii=False, indent=2)
    
    def fetch_commercial_area_data(self) -> Optional[pd.DataFrame]:
        """
        상권 데이터 수집
        
        Returns:
            상권 데이터 DataFrame
        """
        self.logger.info("상권 데이터 수집 시작...")
        
        # 실제 API 호출 (API 키가 있는 경우)
        if self.api_key:
            try:
                url = self.api_endpoints['commercial_area']['url'].format(api_key=self.api_key)
                url += '1/1000/'  # 페이징
                
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                # 데이터 파싱
                if 'VwsmSignguStorW' in data and 'row' in data['VwsmSignguStorW']:
                    df = pd.DataFrame(data['VwsmSignguStorW']['row'])
                    self.logger.info(f"  ✓ {len(df)}개 상권 데이터 수집 완료")
                    return df
                else:
                    self.logger.warning("  ⚠️  API 응답에 데이터가 없습니다")
                    return None
                    
            except Exception as e:
                self.logger.error(f"  ❌ API 호출 실패: {str(e)}")
                return None
        
        # API 키가 없으면 시뮬레이션 데이터 생성
        else:
            self.logger.info("  ⚙️  시뮬레이션 데이터 생성 중...")
            return self._generate_simulated_commercial_data()
    
    def _generate_simulated_commercial_data(self) -> pd.DataFrame:
        """시뮬레이션 상권 데이터 생성"""
        
        regions = [
            '강남구', '강동구', '강북구', '강서구', '관악구', '광진구',
            '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구',
            '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구',
            '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'
        ]
        
        # 시간에 따라 변하는 값 생성 (시뮬레이션)
        current_hour = datetime.now().hour
        time_factor = 1.0 + 0.1 * np.sin(current_hour * np.pi / 12)  # 시간대별 변동
        
        data = []
        for region in regions:
            base_activity = np.random.uniform(60, 95)
            base_specialization = np.random.uniform(50, 90)
            
            data.append({
                'region': region,
                'commercial_activity': base_activity * time_factor,
                'specialization_score': base_specialization,
                'population': np.random.randint(200000, 600000),
                'store_count': np.random.randint(5000, 15000),
                'timestamp': datetime.now().isoformat()
            })
        
        return pd.DataFrame(data)
    
    def update_all_datasets(self) -> Dict:
        """
        모든 데이터셋 업데이트
        
        Returns:
            업데이트 결과
        """
        self.logger.info("=" * 80)
        self.logger.info("전체 데이터 업데이트 시작")
        self.logger.info("=" * 80)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'success': [],
            'failed': [],
            'skipped': []
        }
        
        # 상권 데이터 업데이트
        try:
            commercial_df = self.fetch_commercial_area_data()
            
            if commercial_df is not None:
                # 데이터 저장
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_path = self.data_dir / f"commercial_area_{timestamp}.csv"
                commercial_df.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                # 최신 버전으로 심볼릭 링크 (또는 복사)
                latest_path = self.data_dir / "commercial_area_latest.csv"
                commercial_df.to_csv(latest_path, index=False, encoding='utf-8-sig')
                
                # 버전 정보 업데이트
                self.current_version['datasets']['commercial_area'] = {
                    'last_update': timestamp,
                    'file': str(file_path),
                    'records': len(commercial_df)
                }
                
                results['success'].append('commercial_area')
                self.logger.info(f"✅ 상권 데이터 업데이트 완료: {len(commercial_df)}개 레코드")
            else:
                results['failed'].append('commercial_area')
                self.logger.warning("⚠️  상권 데이터 업데이트 실패")
                
        except Exception as e:
            results['failed'].append('commercial_area')
            self.logger.error(f"❌ 상권 데이터 업데이트 오류: {str(e)}")
        
        # 기타 데이터셋도 유사하게 처리...
        
        # 버전 정보 저장
        self.current_version['last_update'] = results['timestamp']
        self.current_version['version'] = self._increment_version(self.current_version['version'])
        self._save_version()
        
        self.logger.info("=" * 80)
        self.logger.info(f"업데이트 완료: 성공 {len(results['success'])}, 실패 {len(results['failed'])}")
        self.logger.info(f"새 버전: {self.current_version['version']}")
        self.logger.info("=" * 80)
        
        return results
    
    def _increment_version(self, version: str) -> str:
        """버전 번호 증가"""
        parts = version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)
    
    def get_latest_data(self, dataset_name: str = 'commercial_area') -> Optional[pd.DataFrame]:
        """
        최신 데이터 로드
        
        Args:
            dataset_name: 데이터셋 이름
            
        Returns:
            최신 데이터 DataFrame
        """
        latest_path = self.data_dir / f"{dataset_name}_latest.csv"
        
        if latest_path.exists():
            return pd.read_csv(latest_path, encoding='utf-8-sig')
        else:
            self.logger.warning(f"최신 데이터 파일이 없습니다: {latest_path}")
            return None
    
    def get_data_freshness(self) -> Dict:
        """
        데이터 신선도 확인
        
        Returns:
            데이터셋별 신선도 정보
        """
        freshness = {}
        
        for dataset_name, dataset_info in self.current_version['datasets'].items():
            last_update = datetime.fromisoformat(dataset_info['last_update'])
            age_hours = (datetime.now() - last_update).total_seconds() / 3600
            
            if age_hours < 1:
                status = 'very_fresh'
                description = '매우 신선'
            elif age_hours < 6:
                status = 'fresh'
                description = '신선'
            elif age_hours < 24:
                status = 'acceptable'
                description = '보통'
            else:
                status = 'stale'
                description = '업데이트 필요'
            
            freshness[dataset_name] = {
                'last_update': dataset_info['last_update'],
                'age_hours': age_hours,
                'status': status,
                'description': description
            }
        
        return freshness
    
    def compare_data_versions(
        self,
        old_version: str,
        new_version: str
    ) -> Dict:
        """
        데이터 버전 비교
        
        Args:
            old_version: 이전 버전 타임스탬프
            new_version: 새 버전 타임스탬프
            
        Returns:
            변경 사항 딕셔너리
        """
        old_file = self.data_dir / f"commercial_area_{old_version}.csv"
        new_file = self.data_dir / f"commercial_area_{new_version}.csv"
        
        if not old_file.exists() or not new_file.exists():
            return {'error': '파일을 찾을 수 없습니다'}
        
        old_df = pd.read_csv(old_file, encoding='utf-8-sig')
        new_df = pd.read_csv(new_file, encoding='utf-8-sig')
        
        changes = {
            'added_regions': [],
            'removed_regions': [],
            'significant_changes': []
        }
        
        # 추가된 지역
        if 'region' in old_df.columns and 'region' in new_df.columns:
            old_regions = set(old_df['region'].unique())
            new_regions = set(new_df['region'].unique())
            
            changes['added_regions'] = list(new_regions - old_regions)
            changes['removed_regions'] = list(old_regions - new_regions)
        
        # 주요 변경 사항 (활성도 10% 이상 변화)
        if 'commercial_activity' in old_df.columns and 'commercial_activity' in new_df.columns:
            merged = old_df.merge(new_df, on='region', suffixes=('_old', '_new'))
            
            for _, row in merged.iterrows():
                old_val = row.get('commercial_activity_old', 0)
                new_val = row.get('commercial_activity_new', 0)
                
                if old_val > 0:
                    change_pct = abs((new_val - old_val) / old_val * 100)
                    
                    if change_pct > 10:
                        changes['significant_changes'].append({
                            'region': row['region'],
                            'old_value': old_val,
                            'new_value': new_val,
                            'change_percent': change_pct
                        })
        
        return changes
    
    def start_auto_update(self):
        """자동 업데이트 시작 (백그라운드)"""
        
        self.logger.info(f"자동 업데이트 시작: {self.update_interval_hours}시간 간격")
        
        # 백그라운드 스레드에서 실행
        def run_scheduler():
            while True:
                try:
                    self.update_all_datasets()
                except Exception as e:
                    self.logger.error(f"자동 업데이트 오류: {str(e)}")
                
                # 다음 업데이트까지 대기
                time.sleep(self.update_interval_hours * 3600)
        
        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()
        
        self.logger.info("자동 업데이트 스레드 시작 완료")
    
    def generate_update_report(self) -> str:
        """
        업데이트 보고서 생성
        
        Returns:
            마크다운 형식 보고서
        """
        freshness = self.get_data_freshness()
        
        report = f"""# 실시간 데이터 업데이트 보고서

**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**현재 버전**: {self.current_version['version']}  
**마지막 업데이트**: {self.current_version['last_update']}

---

## 데이터 신선도

"""
        
        for dataset_name, info in freshness.items():
            status_emoji = {
                'very_fresh': '🟢',
                'fresh': '🟢',
                'acceptable': '🟡',
                'stale': '🔴'
            }.get(info['status'], '⚪')
            
            report += f"### {status_emoji} {dataset_name}\n"
            report += f"- 상태: {info['description']}\n"
            report += f"- 마지막 업데이트: {info['last_update']}\n"
            report += f"- 경과 시간: {info['age_hours']:.1f}시간\n\n"
        
        report += "\n---\n\n## 업데이트 설정\n\n"
        report += f"- 업데이트 간격: {self.update_interval_hours}시간\n"
        report += f"- 데이터 저장 위치: {self.data_dir}\n"
        
        report += "\n---\n\n## API 엔드포인트\n\n"
        
        for endpoint_name, endpoint_info in self.api_endpoints.items():
            report += f"### {endpoint_info['name']}\n"
            report += f"- 설명: {endpoint_info['description']}\n"
            report += f"- 업데이트 주기: {endpoint_info['update_frequency']}\n\n"
        
        return report


def demo_realtime_updater():
    """실시간 업데이트 시스템 데모"""
    
    print("=" * 80)
    print("실시간 데이터 업데이트 시스템 데모")
    print("=" * 80)
    
    # 시스템 초기화 (API 키 없이 시뮬레이션 모드)
    updater = RealtimeDataUpdater(
        api_key=None,  # 실제 사용 시 API 키 입력
        data_dir="outputs/realtime_data",
        update_interval_hours=6
    )
    
    print("\n[1단계] 데이터 업데이트 실행...")
    results = updater.update_all_datasets()
    
    print(f"\n  ✅ 성공: {len(results['success'])}개")
    print(f"  ❌ 실패: {len(results['failed'])}개")
    print(f"  ⏭️  건너뜀: {len(results['skipped'])}개")
    
    # 최신 데이터 로드
    print("\n[2단계] 최신 데이터 확인...")
    latest_data = updater.get_latest_data('commercial_area')
    
    if latest_data is not None:
        print(f"\n  📊 데이터 샘플 (상위 5개 지역):")
        print(latest_data.head().to_string(index=False))
    
    # 데이터 신선도 확인
    print("\n[3단계] 데이터 신선도 확인...")
    freshness = updater.get_data_freshness()
    
    for dataset, info in freshness.items():
        status_emoji = {
            'very_fresh': '🟢',
            'fresh': '🟢',
            'acceptable': '🟡',
            'stale': '🔴'
        }.get(info['status'], '⚪')
        
        print(f"  {status_emoji} {dataset}: {info['description']} ({info['age_hours']:.1f}시간 경과)")
    
    # 보고서 생성
    print("\n[4단계] 업데이트 보고서 생성...")
    report = updater.generate_update_report()
    
    report_path = Path("outputs/realtime_update_report.md")
    report_path.write_text(report, encoding='utf-8')
    
    print(f"  ✓ 보고서 저장: {report_path}")
    
    print("\n" + "=" * 80)
    print("✅ 데모 완료!")
    print("\n💡 자동 업데이트를 시작하려면:")
    print("   updater.start_auto_update()")
    print("=" * 80)


if __name__ == '__main__':
    demo_realtime_updater()

