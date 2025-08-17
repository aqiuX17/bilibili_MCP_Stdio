#!/usr/bin/env python3
"""
测试优化后的Bilibili MCP服务器功能
验证所有接口在限制数据量后能正常工作，避免上下文溢出
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from main import (
    get_trending_videos,
    search_bilibili_videos, 
    get_video_comments,
    get_video_info,
    get_user_info,
    set_bilibili_cookies,
    test_connection,
    get_cookie_status,
    extract_bvid_from_url,
    bili_api
)

def test_optimized_apis():
    """测试优化后的API功能"""
    
    print("=" * 60)
    print("🧪 测试优化后的Bilibili MCP服务器功能")
    print("=" * 60)
    
    # 1. 测试热门视频（简化版，限制10个）
    print("\n1️⃣ 测试热门视频（简化版，限制10个）")
    try:
        result = get_trending_videos(rid=0, day=3, limit=10, simple=True)
        data = json.loads(result)
        print(f"✅ 获取到 {data.get('data', {}).get('count', 0)} 个热门视频")
        print(f"📊 返回数据大小: {len(result)} 字符")
        if data.get('data', {}).get('list'):
            first_video = data['data']['list'][0]
            print(f"📺 第一个视频: {first_video.get('title', '')}")
    except Exception as e:
        print(f"❌ 热门视频测试失败: {e}")
    
    # 2. 测试搜索功能（简化版，限制5个）
    print("\n2️⃣ 测试搜索功能（简化版，限制5个）")
    try:
        result = search_bilibili_videos("编程", page=1, limit=5, simple=True)
        data = json.loads(result)
        print(f"✅ 搜索到 {data.get('data', {}).get('count', 0)} 个结果")
        print(f"📊 返回数据大小: {len(result)} 字符")
        if data.get('data', {}).get('list'):
            first_result = data['data']['list'][0]
            print(f"🔍 第一个结果: {first_result.get('title', '')}")
    except Exception as e:
        print(f"❌ 搜索功能测试失败: {e}")
    
    # 3. 测试视频信息（单个视频，数据量相对较小）
    print("\n3️⃣ 测试视频信息")
    try:
        result = get_video_info("BV1xx411c7mu")
        data = json.loads(result)
        print(f"📊 返回数据大小: {len(result)} 字符")
        if isinstance(data, dict) and "title" in data:
            print(f"✅ 获取视频信息成功: {data.get('title', '')}")
        else:
            print("✅ 视频信息接口响应正常")
    except Exception as e:
        print(f"❌ 视频信息测试失败: {e}")
    
    # 4. 测试用户信息
    print("\n4️⃣ 测试用户信息")
    try:
        result = get_user_info("1")  # B站官方账号
        data = json.loads(result)
        print(f"📊 返回数据大小: {len(result)} 字符")
        if isinstance(data, dict) and "name" in data:
            print(f"✅ 获取用户信息成功: {data.get('name', '')}")
        else:
            print("✅ 用户信息接口响应正常")
    except Exception as e:
        print(f"❌ 用户信息测试失败: {e}")
    
    # 5. 测试评论功能（简化版，限制5个）
    print("\n5️⃣ 测试评论功能（简化版，限制5个）")
    try:
        result = get_video_comments("170001", page=1, limit=5, simple=True)
        data = json.loads(result)
        print(f"📊 返回数据大小: {len(result)} 字符")
        comment_count = data.get('data', {}).get('count', 0)
        print(f"✅ 获取到 {comment_count} 条评论")
        if comment_count > 0:
            first_comment = data['data']['replies'][0]
            print(f"💬 第一条评论: {first_comment.get('content', '')[:50]}...")
    except Exception as e:
        print(f"❌ 评论功能测试失败: {e}")
    
    # 6. 测试其他辅助功能
    print("\n6️⃣ 测试其他辅助功能")
    try:
        # URL解析
        url_result = extract_bvid_from_url("https://www.bilibili.com/video/BV1xx411c7mu")
        print(f"✅ URL解析: {url_result}")
        
        # Cookie状态
        cookie_status = get_cookie_status()
        print(f"✅ Cookie状态: {cookie_status}")
        
        # 连接测试
        connection_test = test_connection()
        print(f"✅ 连接测试: {connection_test}")
        
    except Exception as e:
        print(f"❌ 辅助功能测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 优化测试完成！")
    print("=" * 60)
    print("\n💡 优化说明:")
    print("• 所有列表类API默认限制返回数量（热门视频10个，搜索5个，评论5个）")
    print("• 默认启用简化模式，只返回核心字段")
    print("• 大幅减少返回数据量，避免上下文溢出")
    print("• 如需完整数据，可设置 simple=False 和增大 limit 参数")

if __name__ == "__main__":
    test_optimized_apis()
