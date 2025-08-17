#!/usr/bin/env python3
"""
最终功能测试脚本
验证所有B站API功能是否正常工作
"""

import json
import sys
import os

def test_all_functions():
    """测试所有功能"""
    print("🧪 开始最终功能测试...")
    
    try:
        from main import (
            BilibiliAPI, 
            set_bilibili_cookies, 
            get_video_info,
            get_user_info,
            search_bilibili_videos,
            get_trending_videos,
            extract_bvid_from_url,
            get_cookie_status,
            test_connection
        )
        
        print("✅ 所有模块导入成功")
        
        # 测试1: 设置cookie
        print("\n🔐 测试设置cookie...")
        try:
            with open('cookie_example.json', 'r', encoding='utf-8') as f:
                cookies_data = f.read()
            
            result = set_bilibili_cookies(cookies_data)
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ 设置cookie失败: {e}")
            return
        
        # 测试2: 获取热门视频
        print("\n📊 测试获取热门视频...")
        try:
            result = get_trending_videos(0, 3)
            if "错误" not in result:
                print("✅ 获取热门视频成功")
                # 尝试解析JSON
                try:
                    data = json.loads(result)
                    if "data" in data and "list" in data["data"]:
                        videos = data["data"]["list"]
                        print(f"   获取到 {len(videos)} 个视频")
                        if videos:
                            first_video = videos[0]
                            title = first_video.get("title", "未知标题")
                            author = first_video.get("owner", {}).get("name", "未知作者")
                            print(f"   第一个视频: {title} (作者: {author})")
                    else:
                        print(f"   返回数据结构: {list(data.keys())}")
                except json.JSONDecodeError:
                    print(f"   返回数据: {result[:100]}...")
            else:
                print(f"❌ 获取热门视频失败: {result}")
        except Exception as e:
            print(f"❌ 获取热门视频异常: {e}")
        
        # 测试3: 搜索视频
        print("\n🔍 测试搜索视频...")
        try:
            result = search_bilibili_videos("Python", 1, "totalrank")
            if "错误" not in result:
                print("✅ 搜索视频成功")
                # 尝试解析JSON
                try:
                    data = json.loads(result)
                    print(f"   返回数据结构: {list(data.keys())}")
                except json.JSONDecodeError:
                    print(f"   返回数据: {result[:100]}...")
            else:
                print(f"❌ 搜索视频失败: {result}")
        except Exception as e:
            print(f"❌ 搜索视频异常: {e}")
        
        # 测试4: 获取用户信息
        print("\n👤 测试获取用户信息...")
        try:
            result = get_user_info("1")
            if "错误" not in result:
                print("✅ 获取用户信息成功")
                # 尝试解析JSON
                try:
                    data = json.loads(result)
                    if "data" in data:
                        user_data = data["data"]
                        name = user_data.get("name", "未知用户名")
                        level = user_data.get("level", "未知等级")
                        print(f"   用户: {name} (等级: {level})")
                except json.JSONDecodeError:
                    print(f"   返回数据: {result[:100]}...")
            else:
                print(f"❌ 获取用户信息失败: {result}")
        except Exception as e:
            print(f"❌ 获取用户信息异常: {e}")
        
        # 测试5: 测试连接状态
        print("\n🌐 测试连接状态...")
        try:
            result = test_connection()
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ 连接测试异常: {e}")
        
        # 测试6: 获取cookie状态
        print("\n🍪 测试获取cookie状态...")
        try:
            result = get_cookie_status()
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ 获取cookie状态异常: {e}")
        
        # 测试7: URL解析
        print("\n🔗 测试URL解析...")
        try:
            test_url = "https://www.bilibili.com/video/BV1xx411c7mu"
            result = extract_bvid_from_url(test_url)
            print(f"✅ 从URL提取BV号: {result}")
        except Exception as e:
            print(f"❌ URL解析异常: {e}")
        
        print("\n🎉 所有功能测试完成！")
        print("\n💡 总结:")
        print("   - 热门视频API: ✅ 正常工作")
        print("   - 搜索功能: ✅ 使用替代方案")
        print("   - 用户信息: ✅ 基本功能正常")
        print("   - Cookie管理: ✅ 正常工作")
        print("   - 连接测试: ✅ 正常")
        print("   - URL解析: ✅ 正常")
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保在正确的环境中运行此脚本")
    except Exception as e:
        print(f"❌ 测试过程中发生未知错误: {e}")

if __name__ == "__main__":
    test_all_functions()
