#!/usr/bin/env python3
"""
调试API数据结构
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from main import bili_api

def debug_api_structure():
    """调试API数据结构"""
    
    print("🔍 调试B站热门视频API数据结构")
    print("=" * 60)
    
    try:
        # 直接调用底层API
        result = bili_api.get_trending_videos(0, 3)
        
        if isinstance(result, dict) and "data" in result:
            videos = result["data"].get("list", [])
            
            if videos:
                print(f"📊 获取到 {len(videos)} 个视频")
                
                # 打印第一个视频的完整结构
                first_video = videos[0]
                print(f"\n📺 第一个视频的完整数据结构:")
                print(json.dumps(first_video, indent=2, ensure_ascii=False))
                
                # 分析数据字段
                print(f"\n🔍 数据字段分析:")
                print(f"title: {first_video.get('title', 'NOT_FOUND')}")
                print(f"bvid: {first_video.get('bvid', 'NOT_FOUND')}")
                
                # 检查owner字段
                owner = first_video.get("owner", {})
                print(f"owner: {owner}")
                print(f"owner.name: {owner.get('name', 'NOT_FOUND')}")
                
                # 检查stat字段
                stat = first_video.get("stat", {})
                print(f"stat: {stat}")
                print(f"stat.view: {stat.get('view', 'NOT_FOUND')}")
                print(f"stat.vv: {stat.get('vv', 'NOT_FOUND')}")
                
                print(f"duration: {first_video.get('duration', 'NOT_FOUND')}")
                
            else:
                print("❌ 没有获取到视频列表")
        else:
            print("❌ API响应格式异常")
            print(f"响应内容: {result}")
            
    except Exception as e:
        print(f"❌ 调试异常: {e}")

if __name__ == "__main__":
    debug_api_structure()
