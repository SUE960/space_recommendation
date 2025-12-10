'use client'

import styles from './FloatingIcons.module.css'

export function FloatingIcons() {
  return (
    <div className={styles.container}>
      {/* 크리스마스 트리 - 밝은 초록색 */}
      <div className={`${styles.icon} ${styles.tree}`}>
        <svg viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="treeGreen1" x1="200" y1="60" x2="200" y2="140">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#059669" />
            </linearGradient>
            <linearGradient id="treeGreen2" x1="200" y1="120" x2="200" y2="220">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#047857" />
            </linearGradient>
            <linearGradient id="treeGreen3" x1="200" y1="200" x2="200" y2="340">
              <stop offset="0%" stopColor="#059669" />
              <stop offset="100%" stopColor="#047857" />
            </linearGradient>
            <radialGradient id="ornamentGold" cx="50%" cy="30%">
              <stop offset="0%" stopColor="#fbbf24" />
              <stop offset="50%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#d97706" />
            </radialGradient>
            <radialGradient id="ornamentRed" cx="50%" cy="30%">
              <stop offset="0%" stopColor="#f87171" />
              <stop offset="50%" stopColor="#ef4444" />
              <stop offset="100%" stopColor="#dc2626" />
            </radialGradient>
            <radialGradient id="starGold" cx="50%" cy="30%">
              <stop offset="0%" stopColor="#fde047" />
              <stop offset="50%" stopColor="#fbbf24" />
              <stop offset="100%" stopColor="#f59e0b" />
            </radialGradient>
          </defs>
          
          {/* 트리 층 1 - 입체감 강화 */}
          <path d="M200 80 L240 140 L160 140 Z" fill="url(#treeGreen1)" />
          <path d="M200 80 L240 140 L160 140 Z" fill="#10b981" opacity="0.8" transform="translate(5, 8)" />
          <path d="M200 80 L240 140 L160 140 Z" fill="#34d399" opacity="0.3" transform="translate(-3, -3)" />
          
          {/* 트리 층 2 */}
          <path d="M200 140 L280 240 L120 240 Z" fill="url(#treeGreen2)" />
          <path d="M200 140 L280 240 L120 240 Z" fill="#059669" opacity="0.8" transform="translate(8, 12)" />
          <path d="M200 140 L280 240 L120 240 Z" fill="#10b981" opacity="0.3" transform="translate(-5, -5)" />
          
          {/* 트리 층 3 */}
          <path d="M200 220 L320 360 L80 360 Z" fill="url(#treeGreen3)" />
          <path d="M200 220 L320 360 L80 360 Z" fill="#047857" opacity="0.8" transform="translate(10, 15)" />
          <path d="M200 220 L320 360 L80 360 Z" fill="#059669" opacity="0.3" transform="translate(-7, -7)" />
          
          {/* 장식품들 */}
          <circle cx="200" cy="110" r="16" fill="url(#ornamentGold)" />
          <ellipse cx="190" cy="105" rx="6" ry="8" fill="#ffffff" opacity="0.7" />
          
          <circle cx="230" cy="150" r="14" fill="url(#ornamentGold)" />
          <ellipse cx="220" cy="145" rx="5" ry="7" fill="#ffffff" opacity="0.7" />
          
          <circle cx="170" cy="150" r="14" fill="url(#ornamentRed)" />
          <ellipse cx="160" cy="145" rx="5" ry="7" fill="#ffffff" opacity="0.7" />
          
          <circle cx="260" cy="200" r="14" fill="url(#ornamentGold)" />
          <ellipse cx="250" cy="195" rx="5" ry="7" fill="#ffffff" opacity="0.7" />
          
          <circle cx="140" cy="200" r="14" fill="url(#ornamentRed)" />
          <ellipse cx="130" cy="195" rx="5" ry="7" fill="#ffffff" opacity="0.7" />
          
          <circle cx="200" cy="240" r="14" fill="url(#ornamentGold)" />
          <ellipse cx="190" cy="235" rx="5" ry="7" fill="#ffffff" opacity="0.7" />
          
          <circle cx="280" cy="280" r="14" fill="url(#ornamentRed)" />
          <ellipse cx="270" cy="275" rx="5" ry="7" fill="#ffffff" opacity="0.7" />
          
          <circle cx="120" cy="280" r="14" fill="url(#ornamentGold)" />
          <ellipse cx="110" cy="275" rx="5" ry="7" fill="#ffffff" opacity="0.7" />
          
          {/* 별 */}
          <path d="M200 50 L210 75 L237 75 L217 90 L222 115 L200 100 L178 115 L183 90 L163 75 L190 75 Z" fill="url(#starGold)" />
          <path d="M200 50 L210 75 L237 75 L217 90 L222 115 L200 100 L178 115 L183 90 L163 75 L190 75 Z" fill="#ffffff" opacity="0.5" transform="translate(3, 3)" />
          <ellipse cx="200" cy="60" rx="8" ry="10" fill="#ffffff" opacity="0.7" />
          
          {/* 나무 기둥 */}
          <rect x="180" y="360" width="40" height="40" rx="5" fill="#92400e" />
          <rect x="185" y="360" width="30" height="40" fill="#a16207" opacity="0.6" />
        </svg>
      </div>

      {/* 위치 핀 - 밝은 빨간색/주황색 */}
      <div className={`${styles.icon} ${styles.pin}`}>
        <svg viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="pinGradient" x1="200" y1="60" x2="200" y2="280">
              <stop offset="0%" stopColor="#f87171" />
              <stop offset="30%" stopColor="#fb923c" />
              <stop offset="70%" stopColor="#f97316" />
              <stop offset="100%" stopColor="#ea580c" />
            </linearGradient>
            <radialGradient id="pinRing1" cx="50%" cy="50%">
              <stop offset="0%" stopColor="#fbbf24" />
              <stop offset="100%" stopColor="#f97316" />
            </radialGradient>
            <radialGradient id="pinRing2" cx="50%" cy="50%">
              <stop offset="0%" stopColor="#f97316" />
              <stop offset="100%" stopColor="#ea580c" />
            </radialGradient>
          </defs>
          
          {/* 핀 본체 */}
          <ellipse cx="200" cy="160" rx="70" ry="110" fill="url(#pinGradient)" />
          <ellipse cx="195" cy="140" rx="55" ry="85" fill="#ffffff" opacity="0.4" />
          <ellipse cx="190" cy="130" rx="12" ry="18" fill="#ffffff" opacity="0.7" />
          <ellipse cx="185" cy="125" rx="6" ry="9" fill="#ffffff" opacity="0.9" />
          
          {/* 원형 구멍 */}
          <circle cx="200" cy="120" r="28" fill="#0a0e27" />
          <circle cx="200" cy="120" r="25" fill="url(#pinGradient)" opacity="0.4" />
          <ellipse cx="195" cy="115" rx="8" ry="10" fill="#ffffff" opacity="0.4" />
          
          {/* 바닥 링들 */}
          <ellipse cx="200" cy="340" rx="50" ry="12" fill="url(#pinRing1)" />
          <ellipse cx="200" cy="338" rx="42" ry="9" fill="url(#pinRing2)" />
          <ellipse cx="200" cy="336" rx="35" ry="6" fill="#fbbf24" opacity="0.7" />
        </svg>
      </div>

      {/* 엄지척 - 밝은 주황색/노란색 */}
      <div className={`${styles.icon} ${styles.thumbs}`}>
        <svg viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="sleeveGradient" x1="260" y1="120" x2="260" y2="280">
              <stop offset="0%" stopColor="#fb923c" />
              <stop offset="50%" stopColor="#f97316" />
              <stop offset="100%" stopColor="#ea580c" />
            </linearGradient>
            <radialGradient id="handGradient" cx="40%" cy="30%">
              <stop offset="0%" stopColor="#fef3c7" />
              <stop offset="50%" stopColor="#fde68a" />
              <stop offset="100%" stopColor="#fcd34d" />
            </radialGradient>
          </defs>
          
          {/* 소매 */}
          <ellipse cx="260" cy="240" rx="70" ry="100" fill="url(#sleeveGradient)" />
          <ellipse cx="255" cy="210" rx="60" ry="85" fill="#ffffff" opacity="0.4" />
          <ellipse cx="250" cy="200" rx="50" ry="75" fill="#ffffff" opacity="0.25" />
          <ellipse cx="245" cy="195" rx="30" ry="45" fill="#ffffff" opacity="0.2" />
          
          {/* 손 본체 */}
          <ellipse cx="230" cy="180" rx="55" ry="75" fill="url(#handGradient)" />
          <ellipse cx="225" cy="165" rx="45" ry="65" fill="#ffffff" opacity="0.5" />
          <ellipse cx="220" cy="155" rx="20" ry="25" fill="#ffffff" opacity="0.6" />
          <ellipse cx="215" cy="150" rx="10" ry="12" fill="#ffffff" opacity="0.8" />
          
          {/* 엄지 */}
          <ellipse cx="200" cy="130" rx="35" ry="50" fill="url(#handGradient)" />
          <ellipse cx="195" cy="120" rx="28" ry="42" fill="#ffffff" opacity="0.4" />
          <ellipse cx="190" cy="115" rx="12" ry="18" fill="#ffffff" opacity="0.6" />
          
          {/* 손가락들 */}
          <ellipse cx="250" cy="200" rx="18" ry="28" fill="url(#handGradient)" />
          <ellipse cx="245" cy="195" rx="12" ry="20" fill="#ffffff" opacity="0.4" />
          
          <ellipse cx="265" cy="210" rx="18" ry="28" fill="url(#handGradient)" />
          <ellipse cx="260" cy="205" rx="12" ry="20" fill="#ffffff" opacity="0.4" />
          
          <ellipse cx="280" cy="220" rx="18" ry="28" fill="url(#handGradient)" />
          <ellipse cx="275" cy="215" rx="12" ry="20" fill="#ffffff" opacity="0.4" />
          
          <ellipse cx="295" cy="230" rx="15" ry="25" fill="url(#handGradient)" />
          <ellipse cx="290" cy="225" rx="10" ry="18" fill="#ffffff" opacity="0.4" />
          
          {/* 버튼 */}
          <circle cx="220" cy="270" r="10" fill="#1f2937" />
          <ellipse cx="218" cy="268" rx="6" ry="8" fill="#ffffff" opacity="0.5" />
        </svg>
      </div>

      {/* 구체들 - 밝은 주황색/빨간색 */}
      <div className={`${styles.icon} ${styles.spheres}`}>
        <svg viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="sphere1Gradient" cx="35%" cy="30%">
              <stop offset="0%" stopColor="#fb923c" />
              <stop offset="40%" stopColor="#f97316" />
              <stop offset="80%" stopColor="#ea580c" />
              <stop offset="100%" stopColor="#dc2626" />
            </radialGradient>
            <radialGradient id="sphere2Gradient" cx="35%" cy="30%">
              <stop offset="0%" stopColor="#f97316" />
              <stop offset="40%" stopColor="#ea580c" />
              <stop offset="80%" stopColor="#dc2626" />
              <stop offset="100%" stopColor="#b91c1c" />
            </radialGradient>
          </defs>
          
          {/* 위 구체 */}
          <circle cx="200" cy="160" r="70" fill="url(#sphere1Gradient)" />
          <ellipse cx="170" cy="130" rx="25" ry="35" fill="#ffffff" opacity="0.5" />
          <ellipse cx="180" cy="145" rx="12" ry="16" fill="#ffffff" opacity="0.7" />
          <ellipse cx="175" cy="140" rx="6" ry="8" fill="#ffffff" opacity="0.9" />
          <ellipse cx="173" cy="138" rx="3" ry="4" fill="#ffffff" opacity="1" />
          
          {/* 아래 구체 */}
          <circle cx="200" cy="300" r="95" fill="url(#sphere2Gradient)" />
          <ellipse cx="170" cy="270" rx="30" ry="40" fill="#ffffff" opacity="0.5" />
          <ellipse cx="180" cy="285" rx="15" ry="20" fill="#ffffff" opacity="0.7" />
          <ellipse cx="175" cy="280" rx="8" ry="10" fill="#ffffff" opacity="0.9" />
          <ellipse cx="173" cy="278" rx="4" ry="5" fill="#ffffff" opacity="1" />
        </svg>
      </div>

      {/* 음표 - 밝은 파란색 */}
      <div className={`${styles.icon} ${styles.note}`}>
        <svg viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="noteGradient" x1="130" y1="100" x2="270" y2="300">
              <stop offset="0%" stopColor="#60a5fa" />
              <stop offset="50%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#2563eb" />
            </linearGradient>
          </defs>
          
          {/* 줄기 */}
          <rect x="130" y="100" width="28" height="160" rx="14" fill="url(#noteGradient)" />
          <rect x="133" y="103" width="22" height="154" rx="11" fill="#ffffff" opacity="0.4" />
          <rect x="136" y="106" width="16" height="148" rx="8" fill="#ffffff" opacity="0.25" />
          <rect x="139" y="109" width="10" height="142" rx="5" fill="#ffffff" opacity="0.15" />
          
          {/* 연결선 */}
          <rect x="158" y="200" width="80" height="12" rx="6" fill="url(#noteGradient)" />
          <rect x="161" y="203" width="74" height="6" rx="3" fill="#ffffff" opacity="0.4" />
          <rect x="164" y="205" width="68" height="2" rx="1" fill="#ffffff" opacity="0.6" />
          
          {/* 음표 머리 1 */}
          <ellipse cx="270" cy="200" rx="40" ry="35" fill="url(#noteGradient)" />
          <ellipse cx="255" cy="192" rx="20" ry="18" fill="#ffffff" opacity="0.5" />
          <ellipse cx="250" cy="190" rx="10" ry="9" fill="#ffffff" opacity="0.7" />
          <ellipse cx="248" cy="189" rx="5" ry="4" fill="#ffffff" opacity="0.9" />
          
          {/* 음표 머리 2 */}
          <ellipse cx="310" cy="250" rx="40" ry="35" fill="url(#noteGradient)" />
          <ellipse cx="295" cy="242" rx="20" ry="18" fill="#ffffff" opacity="0.5" />
          <ellipse cx="290" cy="240" rx="10" ry="9" fill="#ffffff" opacity="0.7" />
          <ellipse cx="288" cy="239" rx="5" ry="4" fill="#ffffff" opacity="0.9" />
        </svg>
      </div>

      {/* 북마크 - 밝은 핑크/보라색 */}
      <div className={`${styles.icon} ${styles.bookmark}`}>
        <svg viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="bookmarkGradient" x1="200" y1="60" x2="200" y2="340">
              <stop offset="0%" stopColor="#f472b6" />
              <stop offset="50%" stopColor="#ec4899" />
              <stop offset="100%" stopColor="#db2777" />
            </linearGradient>
            <radialGradient id="starSilver" cx="50%" cy="30%">
              <stop offset="0%" stopColor="#f3f4f6" />
              <stop offset="50%" stopColor="#e5e7eb" />
              <stop offset="100%" stopColor="#d1d5db" />
            </radialGradient>
          </defs>
          
          {/* 북마크 본체 */}
          <path d="M200 60 L340 60 L340 300 L200 240 L60 300 L60 60 Z" fill="url(#bookmarkGradient)" />
          <path d="M200 60 L340 60 L340 300 L200 240 L60 300 L60 60 Z" fill="#ffffff" opacity="0.3" transform="translate(4, 4)" />
          <path d="M200 60 L340 60 L340 300 L200 240 L60 300 L60 60 Z" fill="#fce7f3" opacity="0.3" transform="translate(2, 2)" />
          <path d="M200 60 L340 60 L340 300 L200 240 L60 300 L60 60 Z" fill="#fbcfe8" opacity="0.2" transform="translate(-2, -2)" />
          
          {/* 별 */}
          <path d="M200 140 L220 180 L265 180 L230 205 L240 250 L200 225 L160 250 L170 205 L135 180 L180 180 Z" fill="url(#starSilver)" />
          <path d="M200 140 L220 180 L265 180 L230 205 L240 250 L200 225 L160 250 L170 205 L135 180 L180 180 Z" fill="#ffffff" opacity="0.6" transform="translate(3, 3)" />
          <ellipse cx="200" cy="160" rx="12" ry="15" fill="#ffffff" opacity="0.8" />
          <ellipse cx="198" cy="158" rx="6" ry="8" fill="#ffffff" opacity="1" />
        </svg>
      </div>
    </div>
  )
}
