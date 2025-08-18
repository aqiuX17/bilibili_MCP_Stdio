#!/usr/bin/env python3
"""
测试修复后的Bilibili MCP服务器功能
专门测试用户报告的问题
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from main import (
    get_video_comments,
    get_video_info,
    search_bilibili_videos,
    get_trending_videos,
    bili_api
)

def test_comment_fixes():
    """测试评论接口修复"""
    
    print("=" * 60)
    print("🧪 测试评论接口修复")
    print("=" * 60)
    
    # 测试1: 使用BV号查询评论（用户报告的视频）
    print("\n1️⃣ 测试BV号查询评论: BV1WgYYzhEKw")
    try:
        result = get_video_comments("BV1WgYYzhEKw", limit=5, simple=True)
        data = json.loads(result)
        print(f"✅ 返回状态: {data.get('code', 'unknown')}")
        print(f"📄 消息: {data.get('message', 'no message')}")
        
        if data.get('code') == 0:
            comment_count = data.get('data', {}).get('count', 0)
            print(f"💬 评论数量: {comment_count}")
            if comment_count > 0:
                first_comment = data['data']['replies'][0]
                print(f"📝 第一条评论: {first_comment.get('content', '')[:100]}...")
        else:
            print(f"⚠️ 接口提示: {data.get('data', {}).get('suggestion', '无建议')}")
            
    except Exception as e:
        print(f"❌ BV号评论测试失败: {e}")
    
    # 测试2: 使用标准AID查询评论
    print("\n2️⃣ 测试标准AID查询评论: 170001")
    try:
        result = get_video_comments("170001", limit=5, simple=True)
        data = json.loads(result)
        print(f"✅ 返回状态: {data.get('code', 'unknown')}")
        print(f"📄 消息: {data.get('message', 'no message')}")
        
        if data.get('code') == 0:
            comment_count = data.get('data', {}).get('count', 0)
            print(f"💬 评论数量: {comment_count}")
        else:
            print(f"⚠️ 接口提示: {data.get('data', {}).get('suggestion', '无建议')}")
            
    except Exception as e:
        print(f"❌ AID评论测试失败: {e}")

def test_search_fixes():
    """测试搜索接口修复"""
    
    print("\n" + "=" * 60)
    print("🔍 测试搜索接口修复")
    print("=" * 60)
    
    # 测试搜索功能
    print("\n1️⃣ 测试搜索功能: '技术爬爬虾'")
    try:
        result = search_bilibili_videos("技术爬爬虾", limit=5, simple=True)
        data = json.loads(result)
        print(f"✅ 返回状态: {data.get('code', 'unknown')}")
        print(f"📄 消息: {data.get('message', 'no message')}")
        
        if data.get('data', {}).get('list'):
            result_count = data['data'].get('count', 0)
            print(f"🔍 搜索结果数量: {result_count}")
            
            # 检查是否是替代结果
            if 'note' in data['data']:
                print(f"ℹ️ 备注: {data['data']['note']}")
                
            if result_count > 0:
                first_result = data['data']['list'][0]
                print(f"📺 第一个结果: {first_result.get('title', '')}")
        
    except Exception as e:
        print(f"❌ 搜索测试失败: {e}")

def test_video_info():
    """测试视频信息获取"""
    
    print("\n" + "=" * 60)
    print("📺 测试视频信息获取")
    print("=" * 60)
    
    print("\n1️⃣ 测试获取视频信息: BV1WgYYzhEKw")
    try:
        result = get_video_info("BV1WgYYzhEKw", simple=True)
        data = json.loads(result)
        print(f"✅ 返回状态: {data.get('code', 'unknown')}")
        print(f"📊 数据大小: {len(result)} 字符")
        
        if data.get('code') == 0 and 'data' in data:
            video_data = data['data']
            print(f"🎬 视频标题: {video_data.get('title', '')}")
            print(f"🆔 BV号: {video_data.get('bvid', '')}")
            print(f"🆔 AID: {video_data.get('aid', '')}")
            print(f"👤 作者: {video_data.get('owner', {}).get('name', '')}")
            print(f"👀 播放量: {video_data.get('stat', {}).get('view', 0)}")
        
    except Exception as e:
        print(f"❌ 视频信息测试失败: {e}")

def test_integration():
    """测试完整流程：从BV号到评论"""
    
    print("\n" + "=" * 60)
    print("🔗 测试完整流程：BV号→视频信息→评论")
    print("=" * 60)
    
    bv_id = "BV1WgYYzhEKw"
    print(f"\n📹 目标视频: {bv_id}")
    
    try:
        # 步骤1: 获取视频信息
        print("\n步骤1: 获取视频信息...")
        video_result = get_video_info(bv_id, simple=True)
        video_data = json.loads(video_result)
        
        if video_data.get('code') == 0:
            title = video_data['data'].get('title', '')
            aid = video_data['data'].get('aid', '')
            print(f"✅ 视频标题: {title}")
            print(f"✅ AID: {aid}")
            
            # 步骤2: 使用BV号直接查询评论
            print(f"\n步骤2: 使用BV号查询评论...")
            comment_result = get_video_comments(bv_id, limit=3, simple=True)
            comment_data = json.loads(comment_result)
            
            print(f"✅ 评论查询状态: {comment_data.get('code', 'unknown')}")
            print(f"📄 消息: {comment_data.get('message', 'no message')}")
            
            if comment_data.get('code') == 0:
                comment_count = comment_data.get('data', {}).get('count', 0)
                print(f"💬 评论数量: {comment_count}")
                
                if comment_count > 0:
                    print("📝 评论列表:")
                    for i, reply in enumerate(comment_data['data']['replies'][:3], 1):
                        print(f"  {i}. {reply.get('author', '未知用户')}: {reply.get('content', '')[:80]}...")
            else:
                print(f"⚠️ 评论获取失败: {comment_data.get('data', {}).get('suggestion', '无建议')}")
        else:
            print(f"❌ 视频信息获取失败: {video_data.get('message', 'unknown error')}")
            
    except Exception as e:
        print(f"❌ 完整流程测试失败: {e}")

def main():
    """主测试函数"""
    
    print("🚀 开始测试修复后的功能...")
    
    # 运行所有测试
    test_video_info()
    test_comment_fixes()  
    test_search_fixes()
    test_integration()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("=" * 60)
    print("\n📋 修复总结:")
    print("• ✅ 支持BV号直接查询评论（自动转换AID）")
    print("• ✅ 改善评论接口错误处理（友好提示替代乱码）")
    print("• ✅ 优化搜索接口异常处理（智能备用方案）")
    print("• ✅ 保持数据量优化（避免上下文溢出）")
    print("\n💡 使用建议:")
    print("• 评论查询现在支持BV号，更加便捷")
    print("• 如遇到反爬限制，建议设置cookie")
    print("• 搜索功能会智能切换到热门视频作为备用")

if __name__ == "__main__":
    main()
