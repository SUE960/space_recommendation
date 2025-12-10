#!/bin/bash

# 🚀 GitHub + Vercel 배포 스크립트
# 사용법: 이 파일을 열어서 YOUR_USERNAME을 본인 GitHub 아이디로 변경 후 실행

echo "📦 GitHub 저장소 연결 및 푸시..."

# 1. 현재 원격 저장소 확인
echo "현재 원격 저장소:"
git remote -v

# 2. 원격 저장소가 있으면 제거
if git remote | grep -q origin; then
    echo "기존 origin 제거..."
    git remote remove origin
fi

# 3. 새 원격 저장소 추가 (YOUR_USERNAME을 본인 아이디로 변경!)
echo "새 원격 저장소 추가..."
git remote add origin https://github.com/YOUR_USERNAME/fin-project.git

# 4. 브랜치 확인
echo "현재 브랜치:"
git branch

# 5. GitHub에 푸시
echo "GitHub에 푸시 중..."
git push -u origin main

echo ""
echo "✅ GitHub 푸시 완료!"
echo ""
echo "🎯 다음 단계:"
echo "1. https://vercel.com 접속"
echo "2. 'Continue with GitHub'로 로그인"
echo "3. 'Add New...' → 'Project' 클릭"
echo "4. 'fin-project' 저장소 선택"
echo "5. 'Deploy' 클릭"
echo ""
echo "🎉 배포 완료!"

