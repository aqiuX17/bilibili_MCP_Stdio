#!/bin/bash

# 验证API修复效果的脚本

echo "============================================================"
echo "🔍 B站API修复效果验证"
echo "============================================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 测试用户
TEST_UID="546195"  # 老番茄

echo "📌 测试目标用户: 老番茄 (UID: $TEST_UID)"
echo ""

# 测试计数
TOTAL=0
SUCCESS=0
FAILED=0

# 1. 测试用户投稿统计（这个API通常最稳定）
echo "1️⃣ 测试用户投稿统计API (navnum)"
echo "   这是最基础的API，应该始终可用"
echo ""

TOTAL=$((TOTAL + 1))
response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    "https://api.bilibili.com/x/space/navnum?mid=$TEST_UID")

if echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); exit(0 if data.get('code')==0 else 1)" 2>/dev/null; then
    SUCCESS=$((SUCCESS + 1))
    stats=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin).get('data', {})
print(f'✅ 成功获取统计数据:')
print(f'   视频: {data.get(\"video\", 0)}')
print(f'   专栏: {data.get(\"article\", 0)}')
print(f'   音频: {data.get(\"audio\", 0)}')
")
    echo -e "$stats"
else
    FAILED=$((FAILED + 1))
    echo -e "${RED}❌ 获取失败${NC}"
fi

echo ""
sleep 3

# 2. 测试用户卡片API（基础信息）
echo "2️⃣ 测试用户卡片API (card)"
echo "   无需认证的基础用户信息"
echo ""

TOTAL=$((TOTAL + 1))
response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    "https://api.bilibili.com/x/web-interface/card?mid=$TEST_UID&photo=true")

if echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); exit(0 if data.get('code')==0 else 1)" 2>/dev/null; then
    SUCCESS=$((SUCCESS + 1))
    info=$(echo "$response" | python3 -c "
import sys, json
card = json.load(sys.stdin).get('data', {}).get('card', {})
print(f'✅ 成功获取用户信息:')
print(f'   昵称: {card.get(\"name\", \"N/A\")}')
print(f'   粉丝: {card.get(\"fans\", 0):,}')
print(f'   关注: {card.get(\"attention\", 0):,}')
print(f'   签名: {card.get(\"sign\", \"N/A\")[:30]}...')
")
    echo -e "$info"
else
    FAILED=$((FAILED + 1))
    echo -e "${RED}❌ 获取失败${NC}"
fi

echo ""
sleep 3

# 3. 测试旧版动态API
echo "3️⃣ 测试旧版动态API (dynamic_svr)"
echo "   修复方案推荐使用的API"
echo ""

TOTAL=$((TOTAL + 1))
response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Referer: https://t.bilibili.com/" \
    "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid=$TEST_UID&offset_dynamic_id=0&need_top=1&platform=web")

code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('code', -1))" 2>/dev/null)

if [ "$code" = "0" ]; then
    SUCCESS=$((SUCCESS + 1))
    
    # 检查是否有动态数据
    has_cards=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin).get('data', {})
cards = data.get('cards', [])
if cards:
    print(f'✅ 成功获取动态数据:')
    print(f'   动态数量: {len(cards)}')
    # 解析第一条动态
    try:
        first = cards[0]
        desc = first.get('desc', {})
        dtype = desc.get('type', 0)
        type_map = {1:'转发', 2:'图文', 4:'文字', 8:'视频', 64:'专栏'}
        print(f'   第一条类型: {type_map.get(dtype, f\"未知({dtype})\")}')
        print(f'   动态ID: {desc.get(\"dynamic_id_str\", \"N/A\")}')
    except:
        pass
else:
    print('⚠️ API返回成功但无动态数据')
" 2>/dev/null)
    echo -e "$has_cards"
else
    FAILED=$((FAILED + 1))
    echo -e "${RED}❌ 获取失败 (code=$code)${NC}"
fi

echo ""
sleep 4

# 4. 测试视频列表API（增加间隔）
echo "4️⃣ 测试用户视频列表API (加长间隔)"
echo "   使用5秒间隔避免-799错误"
echo ""

# 先等待5秒
echo "   ⏱️ 等待5秒避免频率限制..."
sleep 5

TOTAL=$((TOTAL + 1))
response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Referer: https://space.bilibili.com/$TEST_UID/video" \
    "https://api.bilibili.com/x/space/arc/search?mid=$TEST_UID&ps=5&pn=1&order=pubdate")

code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('code', -1))" 2>/dev/null)

if [ "$code" = "0" ]; then
    SUCCESS=$((SUCCESS + 1))
    videos=$(echo "$response" | python3 -c "
import sys, json
from datetime import datetime
data = json.load(sys.stdin).get('data', {})
vlist = data.get('list', {}).get('vlist', [])
total = data.get('page', {}).get('count', 0)
print(f'✅ 成功获取视频列表:')
print(f'   总视频数: {total}')
print(f'   本页返回: {len(vlist)}')
if vlist:
    v = vlist[0]
    print(f'   最新视频: {v.get(\"title\", \"N/A\")[:30]}...')
    print(f'   播放量: {v.get(\"play\", 0):,}')
" 2>/dev/null)
    echo -e "$videos"
elif [ "$code" = "-799" ]; then
    FAILED=$((FAILED + 1))
    echo -e "${YELLOW}⚠️ 触发频率限制 (-799)${NC}"
    echo "   建议: 进一步增加请求间隔"
else
    FAILED=$((FAILED + 1))
    echo -e "${RED}❌ 获取失败 (code=$code)${NC}"
fi

echo ""

# 5. 测试热门视频API（通常最稳定）
echo "5️⃣ 测试热门视频API (popular)"
echo "   作为备用数据源"
echo ""

TOTAL=$((TOTAL + 1))
response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    "https://api.bilibili.com/x/web-interface/popular?ps=3&pn=1")

if echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); exit(0 if data.get('code')==0 else 1)" 2>/dev/null; then
    SUCCESS=$((SUCCESS + 1))
    count=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin).get('data', {})
items = data.get('list', [])
print(f'✅ 成功获取热门视频: {len(items)}个')
")
    echo -e "$count"
else
    FAILED=$((FAILED + 1))
    echo -e "${RED}❌ 获取失败${NC}"
fi

echo ""
echo "============================================================"
echo "📊 验证结果汇总"
echo "============================================================"
echo ""

SUCCESS_RATE=$((SUCCESS * 100 / TOTAL))

echo "测试统计:"
echo "  总测试: $TOTAL"
echo -e "  ${GREEN}成功: $SUCCESS${NC}"
echo -e "  ${RED}失败: $FAILED${NC}"
echo "  成功率: ${SUCCESS_RATE}%"

echo ""
echo "📋 API可用性分析:"
echo ""

if [ $SUCCESS -ge 4 ]; then
    echo -e "${GREEN}✅ 核心API基本可用${NC}"
    echo ""
    echo "可用的数据获取方案:"
    echo "  1. 用户信息: 使用card API ✓"
    echo "  2. 投稿统计: 使用navnum API ✓"
    echo "  3. 热门内容: 使用popular API ✓"
    echo "  4. 用户动态: 优先使用旧版API，备用视频列表"
    echo "  5. 视频列表: 增加请求间隔(5-10秒)"
elif [ $SUCCESS -ge 2 ]; then
    echo -e "${YELLOW}⚠️ 部分API可用${NC}"
    echo ""
    echo "建议优化:"
    echo "  • 增加所有API的请求间隔"
    echo "  • 实现重试机制"
    echo "  • 使用备用API方案"
else
    echo -e "${RED}❌ 大部分API不可用${NC}"
    echo ""
    echo "可能原因:"
    echo "  • 网络连接问题"
    echo "  • IP被临时限制"
    echo "  • 需要配置cookie"
fi

echo ""
echo "💡 修复建议优先级:"
echo ""
echo "1. 🔴 高优先级:"
echo "   • 为所有API添加5秒以上间隔"
echo "   • 实现智能重试机制"
echo "   • 使用旧版API避免WBI签名"
echo ""
echo "2. 🟡 中优先级:"
echo "   • 添加请求缓存减少重复调用"
echo "   • 实现数据格式统一转换"
echo "   • 优化错误处理和降级方案"
echo ""
echo "3. 🟢 低优先级:"
echo "   • 实现完整WBI签名算法"
echo "   • 添加cookie自动获取"
echo "   • 支持更多API端点"
echo ""
echo "✅ 验证完成!"