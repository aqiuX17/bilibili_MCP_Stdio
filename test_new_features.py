#!/usr/bin/env python3
"""
测试新增功能：最热评论和昵称搜索用户
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from main import (
    get_video_comments,
    search_user_by_nickname,
    set_bilibili_cookies,
    get_user_info,
    bili_api
)

def test_hot_comments():
    """测试最热评论功能"""
    
    print("=" * 60)
    print("🔥 测试最热评论功能")
    print("=" * 60)
    
    # 测试不同排序方式
    bv_id = "BV1WgYYzhEKw"  # 古剑预告片
    
    print(f"\n📹 测试视频: {bv_id}")
    
    # 测试1: 热度排序（默认）
    print("\n1️⃣ 热度排序（默认最热评论）")
    try:
        result = get_video_comments(bv_id, limit=5, simple=True, sort_type="hot")
        data = json.loads(result)
        
        if data.get('code') == 0:
            comments = data.get('data', {}).get('replies', [])
            print(f"✅ 获取到 {len(comments)} 条热门评论")
            
            for i, comment in enumerate(comments[:3], 1):
                print(f"  {i}. 👤 {comment.get('author', '未知')}")
                print(f"     💬 {comment.get('content', '')[:80]}...")
                print(f"     👍 点赞: {comment.get('like', 0)}")
        else:
            print(f"⚠️ {data.get('message', '获取失败')}")
    except Exception as e:
        print(f"❌ 热度排序测试失败: {e}")
    
    # 测试2: 点赞排序
    print("\n2️⃣ 点赞数排序")
    try:
        result = get_video_comments(bv_id, limit=3, simple=True, sort_type="like")
        data = json.loads(result)
        
        if data.get('code') == 0:
            comments = data.get('data', {}).get('replies', [])
            print(f"✅ 获取到 {len(comments)} 条高赞评论")
            
            for i, comment in enumerate(comments, 1):
                print(f"  {i}. 👍 {comment.get('like', 0)} 赞 | {comment.get('author', '未知')}: {comment.get('content', '')[:60]}...")
        else:
            print(f"⚠️ {data.get('message', '获取失败')}")
    except Exception as e:
        print(f"❌ 点赞排序测试失败: {e}")
    
    # 测试3: 时间排序
    print("\n3️⃣ 时间排序（最新评论）")
    try:
        result = get_video_comments(bv_id, limit=3, simple=True, sort_type="time")
        data = json.loads(result)
        
        if data.get('code') == 0:
            comments = data.get('data', {}).get('replies', [])
            print(f"✅ 获取到 {len(comments)} 条最新评论")
            
            for i, comment in enumerate(comments, 1):
                print(f"  {i}. 🕐 {comment.get('ctime', 0)} | {comment.get('author', '未知')}: {comment.get('content', '')[:60]}...")
        else:
            print(f"⚠️ {data.get('message', '获取失败')}")
    except Exception as e:
        print(f"❌ 时间排序测试失败: {e}")

def test_nickname_search():
    """测试昵称搜索用户功能"""
    
    print("\n" + "=" * 60)
    print("👤 测试昵称搜索用户功能")
    print("=" * 60)
    
    # 测试搜索不同类型的用户
    test_nicknames = ["技术爬爬虾", "老番茄", "程序员", "up主"]
    
    for nickname in test_nicknames:
        print(f"\n🔍 搜索用户: '{nickname}'")
        try:
            result = search_user_by_nickname(nickname, limit=3, simple=True)
            data = json.loads(result)
            
            if data.get('code') == 0:
                users = data.get('data', {}).get('users', [])
                print(f"✅ 找到 {len(users)} 个相关用户")
                
                for i, user in enumerate(users, 1):
                    print(f"  {i}. 👤 {user.get('uname', '未知用户')}")
                    print(f"     🆔 UID: {user.get('mid', 0)}")
                    print(f"     👥 粉丝: {user.get('fans', 0)}")
                    print(f"     📺 视频: {user.get('videos', 0)}")
                    print(f"     📝 签名: {user.get('usign', '无')[:50]}...")
            else:
                print(f"⚠️ {data.get('message', '搜索失败')}")
                if 'suggestion' in data.get('data', {}):
                    print(f"💡 建议: {data['data']['suggestion']}")
                    
        except Exception as e:
            print(f"❌ 搜索 '{nickname}' 失败: {e}")
        
        print("-" * 40)

def test_enhanced_cookies():
    """测试增强的cookie支持"""
    
    print("\n" + "=" * 60)
    print("🍪 测试增强的Cookie支持")
    print("=" * 60)
    
    # 测试1: 基础cookie
    print("\n1️⃣ 测试基础cookie设置")
    try:
        basic_cookies = {
            "SESSDATA": "test_sessdata_123",
            "bili_jct": "test_bili_jct_456"
        }
        result = set_bilibili_cookies(json.dumps(basic_cookies))
        print("✅ 基础cookie设置:")
        print(result)
    except Exception as e:
        print(f"❌ 基础cookie测试失败: {e}")
    
    # 测试2: 完整cookie
    print("\n2️⃣ 测试完整cookie设置")
    try:
        full_cookies = {
            "SESSDATA": "test_sessdata_123",
            "bili_jct": "test_bili_jct_456",
            "DedeUserID": "123456789",
            "DedeUserID__ckMd5": "test_checksum",
            "buvid3": "test_buvid3_device_id",
            "buvid4": "test_buvid4_device_id",
            "sid": "test_session_id",
            "fingerprint": "test_fingerprint"
        }
        result = set_bilibili_cookies(json.dumps(full_cookies))
        print("✅ 完整cookie设置:")
        print(result)
    except Exception as e:
        print(f"❌ 完整cookie测试失败: {e}")
    
    # 测试3: 缺少重要cookie
    print("\n3️⃣ 测试缺少重要cookie的情况")
    try:
        incomplete_cookies = {
            "buvid3": "test_buvid3_only"
        }
        result = set_bilibili_cookies(json.dumps(incomplete_cookies))
        print("✅ 不完整cookie设置:")
        print(result)
    except Exception as e:
        print(f"❌ 不完整cookie测试失败: {e}")

def test_integration():
    """测试完整功能集成"""
    
    print("\n" + "=" * 60)
    print("🔗 测试功能集成")
    print("=" * 60)
    
    print("\n📋 功能集成测试流程:")
    print("1. 搜索用户 '技术爬爬虾'")
    print("2. 获取找到的用户信息")
    print("3. 查询热门视频的最热评论")
    
    # 步骤1: 搜索用户
    print("\n步骤1: 搜索用户...")
    try:
        search_result = search_user_by_nickname("技术爬爬虾", limit=1, simple=True)
        search_data = json.loads(search_result)
        
        if search_data.get('code') == 0 and search_data.get('data', {}).get('users'):
            user = search_data['data']['users'][0]
            user_uid = user.get('mid', 0)
            user_name = user.get('uname', '未知')
            print(f"✅ 找到用户: {user_name} (UID: {user_uid})")
            
            # 步骤2: 获取用户详细信息
            print(f"\n步骤2: 获取用户 {user_uid} 的详细信息...")
            user_info_result = get_user_info(str(user_uid), simple=True)
            user_info_data = json.loads(user_info_result)
            
            if user_info_data.get('code') == 0:
                info = user_info_data.get('data', {})
                print(f"✅ 用户详情: {info.get('name', '未知')} | 等级: {info.get('level', 0)} | 粉丝: {info.get('fans', 0)}")
            else:
                print(f"⚠️ 用户信息获取失败: {user_info_data.get('message', 'unknown')}")
        else:
            print("⚠️ 未找到相关用户")
    except Exception as e:
        print(f"❌ 用户搜索失败: {e}")
    
    # 步骤3: 查询热门评论
    print(f"\n步骤3: 查询热门视频的最热评论...")
    try:
        hot_comments = get_video_comments("BV1WgYYzhEKw", limit=2, simple=True, sort_type="hot")
        comments_data = json.loads(hot_comments)
        
        if comments_data.get('code') == 0:
            replies = comments_data.get('data', {}).get('replies', [])
            print(f"✅ 获取到 {len(replies)} 条最热评论")
            
            for i, reply in enumerate(replies, 1):
                print(f"  🔥 {i}. {reply.get('author', '未知')}: {reply.get('content', '')[:60]}... (👍{reply.get('like', 0)})")
        else:
            print(f"⚠️ 评论获取失败: {comments_data.get('message', 'unknown')}")
    except Exception as e:
        print(f"❌ 评论查询失败: {e}")

def main():
    """主测试函数"""
    
    print("🚀 开始测试新增功能...")
    
    # 运行所有测试
    test_hot_comments()
    test_nickname_search()
    test_enhanced_cookies()
    test_integration()
    
    print("\n" + "=" * 60)
    print("🎉 新功能测试完成！")
    print("=" * 60)
    print("\n📋 新功能总结:")
    print("• ✅ 最热评论排序 - 支持热度/点赞/时间三种排序")
    print("• ✅ 昵称搜索用户 - 通过关键词找到相关用户")
    print("• ✅ 增强Cookie支持 - 支持更多cookie字段，详细设置反馈")
    print("• ✅ 功能集成优化 - 各功能间协同工作")
    print("\n💡 使用建议:")
    print("• 获取最热评论：使用 sort_type='hot' 参数")
    print("• 搜索用户：提供昵称关键词即可找到相关用户")
    print("• 设置完整Cookie：包含SESSDATA、bili_jct、buvid3等提升效果")

if __name__ == "__main__":
    main()
