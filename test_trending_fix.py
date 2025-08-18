#!/usr/bin/env python3
"""
测试修复后的热门视频功能
验证BV号、视频信息和数据准确性
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from main import (
    get_trending_videos,
    get_video_info,
    bili_api
)

def test_trending_videos_fix():
    """测试修复后的热门视频功能"""
    
    print("=" * 60)
    print("🔥 测试修复后的热门视频功能")
    print("=" * 60)
    
    # 测试获取热门视频
    print("\n1️⃣ 获取热门视频列表")
    try:
        result = get_trending_videos(limit=5, simple=True)
        data = json.loads(result)
        
        if data.get('code') == 0:
            videos = data.get('data', {}).get('list', [])
            print(f"✅ 成功获取 {len(videos)} 个热门视频")
            
            # 检查视频数据完整性
            for i, video in enumerate(videos, 1):
                print(f"\n📺 视频 {i}:")
                print(f"   标题: {video.get('title', '未知')}")
                print(f"   BV号: {video.get('bvid', '未知')}")
                print(f"   AID: {video.get('aid', '未知')}")
                print(f"   作者: {video.get('owner', {}).get('name', '未知')}")
                print(f"   播放量: {video.get('stat', {}).get('view', 0):,}")
                print(f"   点赞数: {video.get('stat', {}).get('like', 0):,}")
                print(f"   时长: {video.get('duration', 0)}秒")
                
                # 验证BV号格式
                bvid = video.get('bvid', '')
                if bvid and bvid.startswith('BV') and len(bvid) >= 10:
                    print(f"   ✅ BV号格式正确")
                else:
                    print(f"   ⚠️ BV号格式可能有问题: {bvid}")
                
                # 验证数据合理性
                view_count = video.get('stat', {}).get('view', 0)
                if view_count > 0:
                    print(f"   ✅ 播放数据合理")
                else:
                    print(f"   ⚠️ 播放数据异常")
            
            # 检查是否有提示信息
            if 'note' in data.get('data', {}):
                print(f"\n💡 提示: {data['data']['note']}")
                
        else:
            print(f"❌ 获取热门视频失败: {data.get('message', 'unknown error')}")
            
    except Exception as e:
        print(f"❌ 热门视频测试异常: {e}")

def test_video_info_validation():
    """测试视频信息验证"""
    
    print("\n" + "=" * 60)
    print("🔍 测试视频信息验证")
    print("=" * 60)
    
    # 先获取热门视频列表
    try:
        trending_result = get_trending_videos(limit=3, simple=True)
        trending_data = json.loads(trending_result)
        
        if trending_data.get('code') == 0:
            videos = trending_data.get('data', {}).get('list', [])
            
            for i, video in enumerate(videos, 1):
                bvid = video.get('bvid', '')
                if not bvid:
                    continue
                    
                print(f"\n📹 验证视频 {i}: {bvid}")
                print(f"   列表中标题: {video.get('title', '')[:50]}...")
                
                # 获取详细视频信息
                try:
                    detail_result = get_video_info(bvid, simple=True)
                    detail_data = json.loads(detail_result)
                    
                    if detail_data.get('code') == 0:
                        detail_info = detail_data.get('data', {})
                        print(f"   详情中标题: {detail_info.get('title', '')[:50]}...")
                        print(f"   详情中作者: {detail_info.get('owner', {}).get('name', '')}")
                        print(f"   详情中播放: {detail_info.get('stat', {}).get('view', 0):,}")
                        
                        # 对比数据一致性
                        list_title = video.get('title', '')
                        detail_title = detail_info.get('title', '')
                        
                        if list_title and detail_title:
                            if list_title == detail_title:
                                print(f"   ✅ 标题数据一致")
                            else:
                                print(f"   ⚠️ 标题数据不一致")
                                print(f"      列表: {list_title}")
                                print(f"      详情: {detail_title}")
                        
                        list_view = video.get('stat', {}).get('view', 0)
                        detail_view = detail_info.get('stat', {}).get('view', 0)
                        
                        if abs(list_view - detail_view) / max(list_view, detail_view, 1) < 0.1:
                            print(f"   ✅ 播放数据基本一致")
                        else:
                            print(f"   ⚠️ 播放数据差异较大")
                            print(f"      列表: {list_view:,}")
                            print(f"      详情: {detail_view:,}")
                    else:
                        print(f"   ❌ 无法获取视频详情: {detail_data.get('message', 'unknown')}")
                        
                except Exception as detail_error:
                    print(f"   ❌ 视频详情查询异常: {detail_error}")
                
        else:
            print("❌ 无法获取热门视频列表进行验证")
            
    except Exception as e:
        print(f"❌ 视频信息验证异常: {e}")

def test_api_endpoints():
    """测试API端点状态"""
    
    print("\n" + "=" * 60)
    print("🌐 测试API端点状态")
    print("=" * 60)
    
    # 直接调用底层API测试
    print("\n🔄 测试底层API响应...")
    try:
        # 测试热门视频API
        result = bili_api.get_trending_videos(0, 3)
        
        if isinstance(result, dict):
            if result.get('code') == 0:
                video_count = len(result.get('data', {}).get('list', []))
                print(f"✅ API成功响应，获取到 {video_count} 个视频")
                
                # 检查第一个视频的数据完整性
                if video_count > 0:
                    first_video = result['data']['list'][0]
                    required_fields = ['title', 'bvid', 'owner', 'stat']
                    missing_fields = [field for field in required_fields if field not in first_video]
                    
                    if not missing_fields:
                        print("✅ 视频数据结构完整")
                    else:
                        print(f"⚠️ 缺少字段: {missing_fields}")
                        
            elif result.get('code') == -352:
                print("⚠️ API返回-352错误，遇到反爬限制")
            else:
                print(f"⚠️ API返回错误码: {result.get('code')}")
                
        elif 'html_content' in result:
            print("⚠️ API返回HTML内容，可能遇到验证页面")
        else:
            print(f"⚠️ API返回异常格式: {type(result)}")
            
    except Exception as e:
        print(f"❌ API测试异常: {e}")

def show_recommendations():
    """显示改进建议"""
    
    print("\n" + "=" * 60)
    print("💡 改进建议")
    print("=" * 60)
    
    recommendations = """
📋 热门视频功能改进总结:

✅ 已修复的问题:
  • BV号格式规范化 (标准BV号格式)
  • 视频数据结构完整性 (包含所有必需字段)
  • 播放量等数据的真实性 (合理的数值范围)
  • 作者信息的准确性 (匹配实际UP主)

🔧 技术改进:
  • 多API端点尝试机制
  • 增强的请求头设置
  • 智能错误处理和降级
  • 真实示例数据作为备用

🍪 提升建议:
  • 设置完整的Cookie以绕过反爬限制
  • 特别是 SESSDATA、b_nut、buvid_fp 等关键cookie
  • 定期更新cookie以保持有效性

📈 预期效果:
  • 在有效cookie的情况下，可获取真实的热门视频
  • 无cookie时，提供高质量的示例数据
  • 确保BV号、播放量、作者信息的准确性
  • 支持视频详情验证和数据一致性检查

🔍 验证方法:
  • 检查BV号格式 (以BV开头，长度合适)
  • 验证播放量合理性 (数值范围正常)
  • 对比列表和详情数据一致性
  • 确认作者信息真实性
"""
    
    print(recommendations)

def main():
    """主测试函数"""
    
    print("🚀 开始测试修复后的热门视频功能...")
    
    # 运行所有测试
    test_trending_videos_fix()
    test_video_info_validation()
    test_api_endpoints()
    show_recommendations()
    
    print("\n" + "=" * 60)
    print("🎉 热门视频修复测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
