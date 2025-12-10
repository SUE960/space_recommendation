"""
Vercel Serverless Functions용 진입점
"""
from main import app

# Vercel은 이 핸들러를 호출합니다
handler = app

