#!/bin/bash

# Musix FastAPI 测试脚本
# 用于测试所有 API 端点，支持从 .env 文件自动登录

BASE_URL="http://localhost:8000"
API_BASE="${BASE_URL}/api/v1"

# 加载 .env 文件
if [ -f ../.env ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

echo "======================================"
echo "Musix FastAPI 测试脚本"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 测试 1: 健康检查
echo -e "${YELLOW}测试 1: 健康检查${NC}"
RESPONSE=$(curl -s -X GET "${BASE_URL}/health")
if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
    echo "$RESPONSE" | jq
else
    echo -e "${RED}❌ 服务未运行或响应错误:${NC}"
    echo "$RESPONSE"
    echo -e "\n${YELLOW}请先启动服务: python main.py${NC}"
    exit 1
fi
echo ""

# 测试 2: 根路径
echo -e "${YELLOW}测试 2: 根路径${NC}"
RESPONSE=$(curl -s -X GET "${BASE_URL}/")
if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
    echo "$RESPONSE" | jq
else
    echo -e "${RED}❌ 响应不是有效的 JSON:${NC}"
    echo "$RESPONSE"
fi
echo ""

# 测试 3: 搜索歌曲（不需要认证）
echo -e "${YELLOW}测试 3: 搜索歌曲${NC}"
RESPONSE=$(curl -s -G "${API_BASE}/netease/search" \
  --data-urlencode "keywords=电棍" \
  --data-urlencode "page=1" \
  --data-urlencode "limit=5")
if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
    echo "$RESPONSE" | jq '.data.items[] | {id, name, artists: [.artists[].name]}'
else
    echo -e "${RED}❌ 响应不是有效的 JSON:${NC}"
    echo "$RESPONSE"
fi
echo ""

# 测试 4: 搜索视频（不需要认证）
echo -e "${YELLOW}测试 4: 搜索 Bilibili 视频${NC}"
RESPONSE=$(curl -s -G "${API_BASE}/bilibili/search" \
  --data-urlencode "keywords=说的道理" \
  --data-urlencode "page=1")
if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
    # 提取第一个视频的 BVID 用于后续测试
    FIRST_BVID=$(echo "$RESPONSE" | jq -r '.data.items[0].bvid // empty')
    echo "$RESPONSE" | jq '.data.items[0:3] | .[] | {bvid, title, author}'
    echo ""
    
    if [ ! -z "$FIRST_BVID" ]; then
        # 测试 5: 获取视频详情
        echo -e "${YELLOW}测试 5: 获取视频详情 (BVID: $FIRST_BVID)${NC}"
        VIDEO_RESPONSE=$(curl -s -X GET "${API_BASE}/bilibili/videos/${FIRST_BVID}")
        if echo "$VIDEO_RESPONSE" | jq . >/dev/null 2>&1; then
            echo "$VIDEO_RESPONSE" | jq '{
              code,
              data: {
                bvid: .data.bvid,
                title: .data.title,
                owner: .data.owner.name,
                stat: {
                  view: .data.stat.view,
                  like: .data.stat.like,
                  coin: .data.stat.coin
                },
                video_url: .data.video_url,
                audio_url: .data.audio_url,
                pages: .data.pages
              }
            }'
        else
            echo -e "${RED}❌ 响应不是有效的 JSON:${NC}"
            echo "$VIDEO_RESPONSE"
        fi
    else
        echo -e "${YELLOW}⚠️  未找到视频，跳过视频详情测试${NC}"
    fi
else
    echo -e "${RED}❌ 响应不是有效的 JSON:${NC}"
    echo "$RESPONSE"
fi
echo ""

# # 测试 6: 获取歌曲详情（不需要认证）
# echo -e "${YELLOW}测试 6: 获取歌曲详情${NC}"
# RESPONSE=$(curl -s -X GET "${API_BASE}/netease/songs/186016")
# if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
#     echo "$RESPONSE" | jq '{
#       code,
#       data: {
#         song_id: .data.song_id,
#         title: .data.title,
#         author: .data.author,
#         album_name: .data.album_name,
#         duration: .data.duration,
#         has_download_url: (.data.download_url != null)
#       }
#     }'
# else
#     echo -e "${RED}❌ 响应不是有效的 JSON:${NC}"
#     echo "$RESPONSE"
# fi
# echo ""

# # 尝试自动登录
# LOGGED_IN=false
# if [ ! -z "$NETEASE_MUSIC_U" ]; then
#     echo -e "${BLUE}📝 检测到 NETEASE_MUSIC_U 环境变量，尝试自动登录...${NC}"
    
#     LOGIN_RESPONSE=$(curl -s -X POST "${API_BASE}/auth/login" \
#       -H "Content-Type: application/json" \
#       -d "{
#         \"platform\": \"netease\",
#         \"method\": \"cookie\",
#         \"credentials\": {
#           \"cookie\": \"$NETEASE_MUSIC_U\"
#         }
#       }")
    
#     # 检查登录是否成功（基于 session 而非 token）
#     LOGIN_STATUS=$(echo $LOGIN_RESPONSE | jq -r '.data.is_logged_in // false')
    
#     if [ "$LOGIN_STATUS" = "true" ]; then
#         USER_NAME=$(echo $LOGIN_RESPONSE | jq -r '.data.nickname // "未知用户"')
#         USER_ID=$(echo $LOGIN_RESPONSE | jq -r '.data.user_id // "N/A"')
#         echo -e "${GREEN}✅ 登录成功！${NC}"
#         echo -e "   用户: $USER_NAME (ID: $USER_ID)"
#         echo -e "   Session 已保存在服务器端"
#         echo ""
#         LOGGED_IN=true
#     else
#         echo -e "${RED}❌ 自动登录失败${NC}"
#         echo -e "${YELLOW}提示：请检查 .env 文件中的 NETEASE_MUSIC_U 是否正确${NC}"
#         echo ""
#     fi
# else
#     echo -e "${YELLOW}⚠️  未找到 NETEASE_MUSIC_U 环境变量${NC}"
#     echo -e "提示：在 .env 文件中设置 NETEASE_MUSIC_U 以启用自动登录"
#     echo ""
# fi

# # 测试需要认证的端点（基于服务器端 Session）
# if [ "$LOGGED_IN" = true ]; then
#     # 测试 7: 获取当前用户信息
#     echo -e "${YELLOW}测试 7: 获取当前用户信息${NC}"
#     RESPONSE=$(curl -s -X GET "${API_BASE}/auth/me")
#     if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
#         echo "$RESPONSE" | jq
#     else
#         echo -e "${RED}❌ 响应不是有效的 JSON:${NC}"
#         echo "$RESPONSE"
#     fi
#     echo ""
    
#     # 测试 8: 获取用户歌单
#     echo -e "${YELLOW}测试 8: 获取用户歌单${NC}"
#     RESPONSE=$(curl -s -X GET "${API_BASE}/netease/playlists")
#     if echo "$RESPONSE" | jq . >/dev/null 2>&1; then
#         echo "$RESPONSE" | jq '.data.playlists[0:3] | .[] | {id, name, track_count}'
#     else
#         echo -e "${RED}❌ 响应不是有效的 JSON:${NC}"
#         echo "$RESPONSE"
#     fi
#     echo ""
    
#     echo -e "${BLUE}ℹ️  注意：当前实现使用服务器端全局 session${NC}"
#     echo -e "   所有客户端共享同一个登录状态（适用于单用户场景）"
#     echo ""
# else
#     echo -e "${YELLOW}⚠️  跳过需要认证的测试（未登录）${NC}"
#     echo ""
# fi

echo -e "${GREEN}======================================"
echo "测试完成！"
echo "======================================${NC}"
echo ""
echo "访问完整 API 文档："
echo "- Swagger UI: ${BASE_URL}/docs"
echo "- ReDoc: ${BASE_URL}/redoc"
