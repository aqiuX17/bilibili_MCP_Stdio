#!/bin/bash

# 测试用户动态API的准确性

echo "============================================================"
echo "🔍 B站用户动态API准确性测试"
echo "============================================================"
echo ""

# 测试用户
TEST_UID="672328094"  # 嘉然
TEST_UID2="546195"    # 老番茄

echo "📌 测试用户动态API - UID: $TEST_UID"
echo "------------------------------------------------------------"

# 1. 新版动态API
echo -e "\n1️⃣ 新版动态API (polymer/web-dynamic)"
echo "   URL: https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"

response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Referer: https://space.bilibili.com/$TEST_UID/dynamic" \
    -H "Accept: application/json, text/plain, */*" \
    -H "Origin: https://www.bilibili.com" \
    "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid=$TEST_UID&timezone_offset=-480&platform=web&features=itemOpusStyle&web_location=333.999")

# 解析响应
if echo "$response" | python3 -m json.tool > /dev/null 2>&1; then
    code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('code', -1))" 2>/dev/null)
    
    if [ "$code" = "0" ]; then
        echo "   ✅ 请求成功 (code=0)"
        
        # 提取动态数量
        item_count=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('data', {}).get('items', [])
print(len(items))
" 2>/dev/null)
        
        echo "   📊 返回动态数: $item_count"
        
        # 分析第一条动态
        if [ "$item_count" != "0" ] && [ -n "$item_count" ]; then
            echo "   📝 第一条动态分析:"
            
            # 提取动态类型
            dtype=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('data', {}).get('items', [])
if items:
    print(items[0].get('type', 'N/A'))
" 2>/dev/null)
            echo "      - 类型: $dtype"
            
            # 提取作者信息
            author=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('data', {}).get('items', [])
if items:
    modules = items[0].get('modules', {})
    author = modules.get('module_author', {})
    print(f\"作者: {author.get('name', 'N/A')}\")
    print(f\"时间戳: {author.get('pub_ts', 'N/A')}\")
" 2>/dev/null)
            echo "      - $author"
            
            # 提取内容类型
            content_type=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('data', {}).get('items', [])
if items:
    modules = items[0].get('modules', {})
    dynamic = modules.get('module_dynamic', {})
    major = dynamic.get('major', {})
    print(major.get('type', 'N/A'))
" 2>/dev/null)
            echo "      - 内容类型: $content_type"
        fi
    else
        message=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('message', ''))" 2>/dev/null)
        echo "   ❌ 请求失败 (code=$code, message=$message)"
    fi
else
    echo "   ❌ 返回非JSON格式"
fi

sleep 2

# 2. 旧版动态API
echo -e "\n2️⃣ 旧版动态API (dynamic_svr)"
echo "   URL: https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"

response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Referer: https://www.bilibili.com/" \
    "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid=$TEST_UID&offset_dynamic_id=0&need_top=1&platform=web")

if echo "$response" | python3 -m json.tool > /dev/null 2>&1; then
    code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('code', -1))" 2>/dev/null)
    
    if [ "$code" = "0" ]; then
        echo "   ✅ 请求成功 (code=0)"
        
        # 提取动态数量
        card_count=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
cards = data.get('data', {}).get('cards', [])
print(len(cards))
" 2>/dev/null)
        
        echo "   📊 返回动态数: $card_count"
    else
        echo "   ❌ 请求失败 (code=$code)"
    fi
else
    echo "   ❌ 返回非JSON格式"
fi

sleep 2

# 3. 测试用户视频API
echo -e "\n📌 测试用户视频API - UID: $TEST_UID"
echo "------------------------------------------------------------"

echo -e "\n3️⃣ 用户视频列表API (无WBI)"
echo "   URL: https://api.bilibili.com/x/space/arc/search"

response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Referer: https://space.bilibili.com/$TEST_UID" \
    "https://api.bilibili.com/x/space/arc/search?mid=$TEST_UID&ps=10&pn=1&order=pubdate")

if echo "$response" | python3 -m json.tool > /dev/null 2>&1; then
    code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('code', -1))" 2>/dev/null)
    
    if [ "$code" = "0" ]; then
        echo "   ✅ 请求成功 (code=0)"
        
        # 提取视频数量
        video_count=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
vlist = data.get('data', {}).get('list', {}).get('vlist', [])
print(len(vlist))
" 2>/dev/null)
        
        total_count=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('data', {}).get('page', {}).get('count', 0))
" 2>/dev/null)
        
        echo "   📊 返回视频数: $video_count"
        echo "   📊 总视频数: $total_count"
        
        # 第一个视频信息
        if [ "$video_count" != "0" ] && [ -n "$video_count" ]; then
            echo "   📝 第一个视频:"
            
            first_video=$(echo "$response" | python3 -c "
import sys, json
from datetime import datetime
data = json.load(sys.stdin)
vlist = data.get('data', {}).get('list', {}).get('vlist', [])
if vlist:
    v = vlist[0]
    print(f\"标题: {v.get('title', 'N/A')}\")
    print(f\"BV号: {v.get('bvid', 'N/A')}\")
    print(f\"播放量: {v.get('play', 0):,}\")
    created = v.get('created', 0)
    if created:
        dt = datetime.fromtimestamp(created)
        print(f\"发布时间: {dt.strftime('%Y-%m-%d %H:%M:%S')}\")
" 2>/dev/null)
            echo "$first_video" | sed 's/^/      - /'
        fi
    elif [ "$code" = "-352" ]; then
        echo "   ⚠️ 需要WBI签名 (code=-352)"
    else
        echo "   ❌ 请求失败 (code=$code)"
    fi
else
    echo "   ❌ 返回非JSON格式"
fi

sleep 2

# 4. 投稿统计API
echo -e "\n4️⃣ 用户投稿统计API"
echo "   URL: https://api.bilibili.com/x/space/navnum"

response=$(curl -s \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    "https://api.bilibili.com/x/space/navnum?mid=$TEST_UID")

if echo "$response" | python3 -m json.tool > /dev/null 2>&1; then
    code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('code', -1))" 2>/dev/null)
    
    if [ "$code" = "0" ]; then
        echo "   ✅ 请求成功 (code=0)"
        
        stats=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
navnum = data.get('data', {})
print(f\"视频数: {navnum.get('video', 0)}\")
print(f\"专栏数: {navnum.get('article', 0)}\")
print(f\"音频数: {navnum.get('audio', 0)}\")
" 2>/dev/null)
        echo "$stats" | sed 's/^/      - /'
    else
        echo "   ❌ 请求失败 (code=$code)"
    fi
else
    echo "   ❌ 返回非JSON格式"
fi

echo ""
echo "============================================================"
echo "📊 测试总结"
echo "============================================================"
echo ""
echo "🎯 发现的问题:"
echo ""
echo "1. 用户动态API:"
echo "   • 新版API返回数据结构复杂，需要正确解析modules"
echo "   • 旧版API数据格式不同，card字段需要二次JSON解析"
echo "   • 动态类型多样（视频、图文、专栏等），需分别处理"
echo ""
echo "2. 用户视频API:"
echo "   • 部分API需要WBI签名才能返回数据"
echo "   • 返回数据嵌套层级深（data.list.vlist）"
echo "   • 时间戳需要转换为可读格式"
echo ""
echo "💡 修复建议:"
echo "   1. 优化数据解析逻辑，处理多层嵌套"
echo "   2. 实现完整的WBI签名算法"
echo "   3. 统一时间格式转换"
echo "   4. 添加动态类型识别和分类"
echo ""
echo "✅ 测试完成!"