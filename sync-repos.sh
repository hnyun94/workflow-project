#!/bin/bash

echo "🚀 저장소 동기화 시작..."

# 현재 브랜치 확인
current_branch=$(git branch --show-current)
echo "📋 현재 브랜치: $current_branch"

# 메인 저장소에 푸시
echo "📦 메인 저장소에 푸시..."
git push origin $current_branch

if [ $? -eq 0 ]; then
    echo "✅ 메인 저장소 푸시 성공"
else
    echo "❌ 메인 저장소 푸시 실패"
    exit 1
fi

# 프론트엔드 저장소에 푸시
echo "🎨 프론트엔드 저장소에 푸시..."
git push frontend-love $current_branch

if [ $? -eq 0 ]; then
    echo "✅ 프론트엔드 저장소 푸시 성공"
else
    echo "❌ 프론트엔드 저장소 푸시 실패"
    exit 1
fi

echo "🎉 동기화 완료!"
echo ""
echo "🌐 저장소 정보:"
echo "   메인: https://github.com/hnyun94/workflow-project.git"
echo "   프론트엔드: https://github.com/hnyun94/github-frontend-love.git"
echo ""
echo "📊 최신 커밋:"
git log --oneline -1
