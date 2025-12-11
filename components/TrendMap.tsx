'use client'

import { useState, useCallback } from 'react'
import Map, { Marker, Popup } from 'react-map-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import styles from './TrendMap.module.css'

interface Hotspot {
  순위: number
  핫스팟명: string
  핫스팟코드: string
  실시간지역프로필점수: number
  실시간등급: string
  상권활성도: number
  특화점수: number
  인구통계: number
  특화업종: string
  결제건수: number
  결제금액: number
  업종수: number
  lng?: number
  lat?: number
}

// 서울 주요 지역 좌표 (대략적 위치)
const SEOUL_COORDINATES: Record<string, { lng: number; lat: number }> = {
  '홍대 관광특구': { lng: 126.9236, lat: 37.5563 },
  '강남역': { lng: 127.0276, lat: 37.4979 },
  '용리단길': { lng: 126.9882, lat: 37.5406 },
  '회기역': { lng: 127.0579, lat: 37.5895 },
  '보신각': { lng: 126.9850, lat: 37.5701 },
  '구로역': { lng: 126.8814, lat: 37.5031 },
  '강남 MICE 관광특구': { lng: 127.0276, lat: 37.4979 },
  '광화문·덕수궁': { lng: 126.9768, lat: 37.5658 },
  '충정로역': { lng: 126.9636, lat: 37.5611 },
  '잠실 관광특구': { lng: 127.1000, lat: 37.5133 },
  '건대입구역': { lng: 127.0700, lat: 37.5406 },
  '합정역': { lng: 126.9146, lat: 37.5495 },
  '역삼역': { lng: 127.0364, lat: 37.5000 },
  '교대역': { lng: 127.0145, lat: 37.4936 },
  '서울역': { lng: 126.9726, lat: 37.5547 },
  '종로·청계 관광특구': { lng: 126.9780, lat: 37.5701 },
  '이태원 관광특구': { lng: 126.9942, lat: 37.5345 },
  '왕십리역': { lng: 127.0456, lat: 37.5612 },
  '이태원역': { lng: 126.9942, lat: 37.5345 },
  '신촌·이대역': { lng: 126.9369, lat: 37.5563 },
  '연신내역': { lng: 126.9210, lat: 37.6191 },
  '혜화역': { lng: 127.0017, lat: 37.5824 },
  '영등포 타임스퀘어': { lng: 126.9033, lat: 37.5264 },
  '신림역': { lng: 126.9298, lat: 37.4842 },
  '홍대입구역(2호선)': { lng: 126.9236, lat: 37.5563 },
  '가락시장': { lng: 127.1185, lat: 37.4932 },
  '수유역': { lng: 127.0246, lat: 37.6378 },
  '신논현역·논현역': { lng: 127.0254, lat: 37.5045 },
  '동대문역': { lng: 127.0098, lat: 37.5714 },
  '서울대입구역': { lng: 126.9526, lat: 37.4812 },
  '선릉역': { lng: 127.0490, lat: 37.5045 },
  '사당역': { lng: 126.9819, lat: 37.4765 },
  '발산역': { lng: 126.8366, lat: 37.5512 },
  '미아사거리역': { lng: 127.0259, lat: 37.6133 },
  '성신여대입구역': { lng: 127.0164, lat: 37.5926 },
  '노량진': { lng: 126.9419, lat: 37.5133 },
  '성수카페거리': { lng: 127.0436, lat: 37.5433 },
  '고속터미널역': { lng: 127.0053, lat: 37.5047 },
  '동대문 관광특구': { lng: 127.0098, lat: 37.5714 },
  '가로수길': { lng: 127.0230, lat: 37.5197 },
  '양재역': { lng: 127.0356, lat: 37.4842 },
  '연남동': { lng: 126.9210, lat: 37.5641 },
  '명동 관광특구': { lng: 126.9850, lat: 37.5636 },
  '천호역': { lng: 127.1276, lat: 37.5383 },
  '대림역': { lng: 126.9019, lat: 37.4929 },
  '총신대입구(이수)역': { lng: 126.9819, lat: 37.4765 },
  '여의도': { lng: 126.9240, lat: 37.5270 },
  '인사동': { lng: 126.9850, lat: 37.5714 },
  '압구정로데오거리': { lng: 127.0276, lat: 37.5270 },
  '청담동 명품거리': { lng: 127.0476, lat: 37.5236 },
  '해방촌·경리단길': { lng: 126.9882, lat: 37.5406 },
  '이태원 앤틱가구거리': { lng: 126.9942, lat: 37.5345 },
  '북촌한옥마을': { lng: 126.9850, lat: 37.5824 },
  '서촌': { lng: 126.9700, lat: 37.5745 },
  '덕수궁길·정동길': { lng: 126.9745, lat: 37.5658 },
  'DDP(동대문디자인플라자)': { lng: 127.0098, lat: 37.5665 },
  'DMC(디지털미디어시티)': { lng: 126.9019, lat: 37.5762 },
  '광장(전통)시장': { lng: 126.9098, lat: 37.5450 },
  '창동 신경제 중심지': { lng: 127.0446, lat: 37.6533 },
  '청량리 제기동 일대 전통시장': { lng: 127.0456, lat: 37.5850 },
  '오목교역·목동운동장': { lng: 126.8754, lat: 37.5242 },
  '장한평역': { lng: 127.0680, lat: 37.5612 },
  '장지역': { lng: 127.1265, lat: 37.4783 },
  '고덕역': { lng: 127.1545, lat: 37.5547 },
  '가산디지털단지역': { lng: 126.8814, lat: 37.4812 },
  '구로디지털단지역': { lng: 126.9019, lat: 37.4852 },
  '용산역': { lng: 126.9646, lat: 37.5298 },
  '쌍문역': { lng: 127.0246, lat: 37.6483 },
  '군자역': { lng: 127.0776, lat: 37.5570 },
  '서울식물원·마곡나루역': { lng: 126.8366, lat: 37.5665 },
  '김포공항': { lng: 126.8014, lat: 37.5583 },
}

interface TrendMapProps {
  hotspots: Hotspot[]
}

export default function TrendMap({ hotspots }: TrendMapProps) {
  const [selectedHotspot, setSelectedHotspot] = useState<Hotspot | null>(null)
  const [viewState, setViewState] = useState({
    longitude: 126.9780,
    latitude: 37.5665,
    zoom: 11,
  })

  const mapboxToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || ''

  // 좌표가 있는 핫스팟만 필터링
  const hotspotsWithCoords = hotspots
    .map((hotspot) => {
      const coords = SEOUL_COORDINATES[hotspot.핫스팟명]
      if (coords) {
        return { ...hotspot, lng: coords.lng, lat: coords.lat }
      }
      return null
    })
    .filter((h): h is Hotspot & { lng: number; lat: number } => h !== null)

  const getMarkerColor = (score: number) => {
    if (score >= 70) return '#FF6B6B' // 빨강 - 활성화
    if (score >= 60) return '#FFA500' // 주황
    if (score >= 50) return '#FFD700' // 노랑
    return '#90EE90' // 연두
  }

  if (!mapboxToken) {
    return (
      <div className={styles.errorContainer}>
        <p>⚠️ Mapbox API 토큰이 설정되지 않았습니다.</p>
        <p>환경 변수 NEXT_PUBLIC_MAPBOX_TOKEN을 설정해주세요.</p>
      </div>
    )
  }

  return (
    <div className={styles.mapContainer}>
      <Map
        {...viewState}
        onMove={(evt) => setViewState(evt.viewState)}
        mapboxAccessToken={mapboxToken}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/light-v11"
      >
        {hotspotsWithCoords.map((hotspot) => (
          <Marker
            key={hotspot.핫스팟코드}
            longitude={hotspot.lng}
            latitude={hotspot.lat}
            anchor="bottom"
            onClick={(e) => {
              e.originalEvent.stopPropagation()
              setSelectedHotspot(hotspot)
            }}
          >
            <div
              className={styles.marker}
              style={{
                backgroundColor: getMarkerColor(hotspot.실시간지역프로필점수),
              }}
            >
              <span className={styles.markerText}>
                {hotspot.순위}
              </span>
            </div>
          </Marker>
        ))}

        {selectedHotspot && selectedHotspot.lng && selectedHotspot.lat && (
          <Popup
            longitude={selectedHotspot.lng}
            latitude={selectedHotspot.lat}
            anchor="bottom"
            onClose={() => setSelectedHotspot(null)}
            closeButton={true}
            closeOnClick={false}
          >
            <div className={styles.popup}>
              <h3 className={styles.popupTitle}>{selectedHotspot.핫스팟명}</h3>
              <div className={styles.popupInfo}>
                <div className={styles.popupRow}>
                  <span className={styles.label}>순위:</span>
                  <span className={styles.value}>{selectedHotspot.순위}위</span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.label}>종합 점수:</span>
                  <span className={styles.value}>
                    {selectedHotspot.실시간지역프로필점수.toFixed(1)}점
                  </span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.label}>등급:</span>
                  <span className={styles.value}>{selectedHotspot.실시간등급}</span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.label}>특화 업종:</span>
                  <span className={styles.value}>{selectedHotspot.특화업종}</span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.label}>상권 활성도:</span>
                  <span className={styles.value}>
                    {selectedHotspot.상권활성도.toFixed(1)}
                  </span>
                </div>
                <div className={styles.popupRow}>
                  <span className={styles.label}>결제 건수:</span>
                  <span className={styles.value}>
                    {selectedHotspot.결제건수.toLocaleString()}건
                  </span>
                </div>
              </div>
            </div>
          </Popup>
        )}
      </Map>
    </div>
  )
}
