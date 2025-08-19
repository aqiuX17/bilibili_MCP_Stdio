#!/bin/bash

# B站API接口测试脚本
# 使用curl直接测试API可用性

echo "============================================================"
echo "🚀 B站API接口测试"
echo "============================================================"
echo ""
echo "📅 测试时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数器
TOTAL=0
SUCCESS=0
FAILED=0
PARTIAL=0

# 测试函数
test_api() {
    local name=$1
    local url=$2
    local params=$3
    
    TOTAL=$((TOTAL + 1))
    
    echo -e "\n🔍 测试: $name"
    echo "   URL: $url"
    
    if [ -n "$params" ]; then
        full_url="${url}?${params}"
    else
        full_url="$url"
    fi
    
    # 执行请求
    response=$(curl -s -w "\n%{http_code}" \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
        -H "Referer: https://www.bilibili.com/" \
        -H "Accept: application/json, text/plain, */*" \
        "$full_url")
    
    # 分离响应体和状态码
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    
    # 检查HTTP状态码
    if [ "$http_code" = "200" ]; then
        # 检查是否是JSON格式
        if echo "$body" | python3 -m json.tool > /dev/null 2>&1; then
            # 提取code字段
            code=$(echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('code', -999))" 2>/dev/null)
            
            if [ "$code" = "0" ]; then
                echo -e "   ${GREEN}✅ 成功${NC} (HTTP $http_code, code=$code)"
                SUCCESS=$((SUCCESS + 1))
            elif [ "$code" = "-799" ]; then
                echo -e "   ${YELLOW}⚠️ 频率限制${NC} (HTTP $http_code, code=$code)"
                PARTIAL=$((PARTIAL + 1))
            else
                message=$(echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('message', 'Unknown error'))" 2>/dev/null)
                echo -e "   ${RED}❌ 失败${NC} (HTTP $http_code, code=$code, message=$message)"
                FAILED=$((FAILED + 1))
            fi
        else
            echo -e "   ${RED}❌ 非JSON响应${NC} (HTTP $http_code)"
            FAILED=$((FAILED + 1))
        fi
    else
        echo -e "   ${RED}❌ HTTP错误${NC} (状态码: $http_code)"
        FAILED=$((FAILED + 1))
    fi
    
    # 请求间隔
    sleep 2
}

# 开始测试
echo "============================================================"
echo "📹 视频相关API测试"
echo "------------------------------------------------------------"

test_api "视频详情API" \
    "https://api.bilibili.com/x/web-interface/view" \
    "bvid=BV1xx411c7mD"

test_api "视频标签API" \
    "https://api.bilibili.com/x/web-interface/view/detail/tag" \
    "bvid=BV1xx411c7mD"

test_api "视频分P列表API" \
    "https://api.bilibili.com/x/player/pagelist" \
    "bvid=BV1xx411c7mD"

test_api "相关推荐API" \
    "https://api.bilibili.com/x/web-interface/archive/related" \
    "bvid=BV1xx411c7mD"

echo ""
echo "============================================================"
echo "👤 用户相关API测试"
echo "------------------------------------------------------------"

test_api "用户信息API (需WBI签名)" \
    "https://api.bilibili.com/x/space/wbi/acc/info" \
    "mid=36081646"

test_api "用户卡片API" \
    "https://api.bilibili.com/x/web-interface/card" \
    "mid=36081646"

echo ""
echo "============================================================"
echo "🔍 搜索相关API测试"
echo "------------------------------------------------------------"

test_api "搜索建议API" \
    "https://s.search.bilibili.com/main/suggest" \
    "term=编程&func=suggest&suggest_type=accurate"

test_api "搜索视频API" \
    "https://api.bilibili.com/x/web-interface/search/type" \
    "search_type=video&keyword=Python&page=1"

echo ""
echo "============================================================"
echo "🔥 热门内容API测试"
echo "------------------------------------------------------------"

test_api "热门推荐API" \
    "https://api.bilibili.com/x/web-interface/popular" \
    "ps=5&pn=1"

test_api "排行榜API" \
    "https://api.bilibili.com/x/web-interface/ranking/v2" \
    "rid=0&type=all"

test_api "入站必刷API" \
    "https://api.bilibili.com/x/web-interface/popular/precious" \
    "ps=5&pn=1"

echo ""
echo "============================================================"
echo "💬 评论相关API测试"
echo "------------------------------------------------------------"

test_api "视频评论API" \
    "https://api.bilibili.com/x/v2/reply" \
    "pn=1&type=1&oid=170001&sort=2"

echo ""
echo "============================================================"
echo "📺 直播相关API测试"
echo "------------------------------------------------------------"

test_api "直播间信息API" \
    "https://api.live.bilibili.com/room/v1/Room/get_info" \
    "room_id=22"

test_api "直播分区列表API" \
    "https://api.live.bilibili.com/room/v1/Area/getList" \
    ""

echo ""
echo "============================================================"
echo "🔑 系统相关API测试"
echo "------------------------------------------------------------"

test_api "导航信息API (含WBI密钥)" \
    "https://api.bilibili.com/x/web-interface/nav" \
    ""

# 生成报告
echo ""
echo ""
echo "============================================================"
echo "📊 测试报告汇总"
echo "============================================================"
echo ""
echo "📈 测试统计:"
echo "   总测试数: $TOTAL"
echo -e "   ${GREEN}✅ 成功: $SUCCESS${NC}"
echo -e "   ${YELLOW}⚠️ 部分可用: $PARTIAL${NC}"
echo -e "   ${RED}❌ 失败: $FAILED${NC}"

if [ $TOTAL -gt 0 ]; then
    SUCCESS_RATE=$((SUCCESS * 100 / TOTAL))
    AVAILABLE_RATE=$(((SUCCESS + PARTIAL) * 100 / TOTAL))
    echo "   📊 成功率: ${SUCCESS_RATE}%"
    echo "   📊 可用率: ${AVAILABLE_RATE}%"
fi

echo ""
echo "============================================================"
echo "💡 分析与建议"
echo "============================================================"
echo ""

if [ $SUCCESS_RATE -lt 30 ]; then
    echo "📌 当前状态分析:"
    echo "   • 大部分API需要认证或遇到反爬限制"
    echo "   • 这是B站API的正常保护机制"
elif [ $SUCCESS_RATE -lt 60 ]; then
    echo "📌 当前状态分析:"
    echo "   • 部分核心API可以访问"
    echo "   • 某些功能受限但基本可用"
else
    echo "📌 当前状态分析:"
    echo "   • 大部分API运行正常"
    echo "   • 系统状态良好"
fi

echo ""
echo "🔧 优化建议:"
echo "   1. 配置Cookie认证:"
echo "      • 获取SESSDATA、bili_jct等关键cookie"
echo "      • 使用cookie_example.json配置文件"
echo ""
echo "   2. 使用WBI签名:"
echo "      • 部分API需要WBI签名才能访问"
echo "      • 需要有效的cookie才能获取WBI密钥"
echo ""
echo "   3. 控制请求频率:"
echo "      • 建议请求间隔2-5秒"
echo "      • 避免触发频率限制"
echo ""

echo "============================================================"
echo "📝 测试结论"
echo "============================================================"
echo ""

if [ $SUCCESS -ge 8 ]; then
    echo -e "${GREEN}✅ 系统基本功能正常，大部分接口可用!${NC}"
    echo "   建议配置cookie以获得完整功能"
elif [ $SUCCESS -ge 4 ]; then
    echo -e "${YELLOW}⚠️ 部分功能可用，但受限较多${NC}"
    echo "   强烈建议配置cookie提升可用性"
else
    echo -e "${RED}❌ 大部分功能受限${NC}"
    echo "   必须配置cookie才能正常使用"
fi

echo ""
echo "✅ 测试完成!"
echo ""