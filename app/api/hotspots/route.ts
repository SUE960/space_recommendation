import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    // CSV 파일 읽기
    const csvPath = path.join(process.cwd(), 'public', 'api_all_72_hotspots_realtime_scores.csv')
    
    // public 폴더에 없으면 outputs 폴더에서 찾기
    let csvContent: string
    if (fs.existsSync(csvPath)) {
      csvContent = fs.readFileSync(csvPath, 'utf-8')
    } else {
      const altPath = path.join(process.cwd(), 'outputs', 'api_all_72_hotspots_realtime_scores.csv')
      if (fs.existsSync(altPath)) {
        csvContent = fs.readFileSync(altPath, 'utf-8')
      } else {
        return NextResponse.json({ error: '데이터 파일을 찾을 수 없습니다' }, { status: 404 })
      }
    }

    // CSV 파싱
    const lines = csvContent.split('\n').filter((line) => line.trim())
    const headers = lines[0].split(',').map((h) => h.trim())

    const hotspots = []
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',')
      if (values.length >= headers.length) {
        const row: any = {}
        headers.forEach((header, idx) => {
          const value = values[idx]?.trim() || ''
          // 숫자 변환 시도
          if (!isNaN(Number(value)) && value !== '') {
            row[header] = Number(value)
          } else {
            row[header] = value
          }
        })
        hotspots.push(row)
      }
    }

    return NextResponse.json(hotspots)
  } catch (error) {
    console.error('Hotspots API error:', error)
    return NextResponse.json(
      { error: '데이터를 불러오는데 실패했습니다' },
      { status: 500 }
    )
  }
}
