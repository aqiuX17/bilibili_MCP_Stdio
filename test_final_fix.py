#!/usr/bin/env python3
"""
最终测试修复后的热门视频功能
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from main import get_trending_videos

def test_final_fix():
    """最终测试修复后的功能"""
    
    print("🎯 最终测试：修复后的热门视频功能")
    print("=" * 60)
    
    try:
        # 获取热门视频
        result = get_trending_videos(limit=5, simple=True)
        data = json.loads(result)
        
        if data.get('code') == 0:
            videos = data.get('data', {}).get('list', [])
            print(f"✅ 成功获取 {len(videos)} 个热门视频\n")
            
            for i, video in enumerate(videos, 1):
                print(f"📺 视频 {i}:")
                print(f"   标题: {video.get('title', '')}")
                print(f"   BV号: {video.get('bvid', '')}")
                print(f"   AID: {video.get('aid', '')}")
                print(f"   作者: {video.get('author', '')}")
                print(f"   作者UID: {video.get('author_mid', '')}")
                print(f"   播放量: {video.get('view', 0):,}")
                print(f"   点赞数: {video.get('like', 0):,}")
                print(f"   投币数: {video.get('coin', 0):,}")
                print(f"   收藏数: {video.get('favorite', 0):,}")
                print(f"   分享数: {video.get('share', 0):,}")
                print(f"   评论数: {video.get('reply', 0):,}")
                print(f"   弹幕数: {video.get('danmaku', 0):,}")
                print(f"   时长: {video.get('duration', 0)}秒")
                print(f"   简介: {video.get('desc', '')[:80]}...")
                
                # 验证数据完整性
                issues = []
                if not video.get('bvid', '').startswith('BV'):
                    issues.append("BV号格式错误")
                if not video.get('author', ''):
                    issues.append("缺少作者信息")
                if video.get('view', 0) <= 0:
                    issues.append("播放量异常")
                if video.get('aid', 0) <= 0:
                    issues.append("AID异常")
                
                if not issues:
                    print(f"   ✅ 数据完整性检查通过")
                else:
                    print(f"   ⚠️ 数据问题: {', '.join(issues)}")
                
                print("-" * 40)
                
        else:
            print(f"❌ 获取失败: {data.get('message', 'unknown error')}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def main():
    test_final_fix()

if __name__ == "__main__":
    main()
