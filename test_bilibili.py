#!/usr/bin/env python3
"""
B站信息获取功能测试脚本
用于测试各个API功能是否正常工作
"""

import json
import sys
import os
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_bilibili_api():
    """测试B站API功能"""
    print("🧪 开始测试B站API功能...")
    
    try:
        from main import BilibiliAPI, set_bilibili_cookies
        
        # 测试1: 设置cookie
        print("\n🔐 测试设置cookie...")
        try:
            # 读取示例cookie文件
            with open('cookie_example.json', 'r', encoding='utf-8') as f:
                cookies_data = f.read()
            
            result = set_bilibili_cookies(cookies_data)
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ 设置cookie失败: {e}")
            return
        
        # 创建API实例
        api = BilibiliAPI()
        
        # 测试2: 获取热门视频
        print("\n📊 测试获取热门视频...")
        try:
            result = api.get_trending_videos(0, 3)
            if "error" not in result:
                print("✅ 获取热门视频成功")
                if "data" in result and "list" in result["data"]:
                    videos = result["data"]["list"]
                    print(f"   获取到 {len(videos)} 个视频")
                    if videos:
                        first_video = videos[0]
                        title = first_video.get("title", "未知标题")
                        author = first_video.get("owner", {}).get("name", "未知作者")
                        print(f"   第一个视频: {title} (作者: {author})")
                else:
                    print(f"   返回数据结构: {list(result.keys())}")
            else:
                print(f"❌ 获取热门视频失败: {result['error']}")
        except Exception as e:
            print(f"❌ 获取热门视频异常: {e}")
        
        # 测试3: 搜索视频
        print("\n🔍 测试搜索视频...")
        try:
            result = api.search_videos("Python", 1, "totalrank")
            if "error" not in result:
                print("✅ 搜索视频成功")
                if "data" in result and "result" in result["data"]:
                    videos = result["data"]["result"]
                    print(f"   搜索到 {len(videos)} 个视频")
                    if videos:
                        first_video = videos[0]
                        title = first_video.get("title", "未知标题")
                        author = first_video.get("author", "未知作者")
                        print(f"   第一个视频: {title} (作者: {author})")
                else:
                    print(f"   返回数据结构: {list(result.keys())}")
            else:
                print(f"❌ 搜索视频失败: {result['error']}")
        except Exception as e:
            print(f"❌ 搜索视频异常: {e}")
        
        # 测试4: 获取用户信息（使用一个已知的UID）
        print("\n👤 测试获取用户信息...")
        try:
            result = api.get_user_info("1")  # 使用UID 1进行测试
            if "error" not in result:
                print("✅ 获取用户信息成功")
                if "data" in result:
                    user_data = result["data"]
                    name = user_data.get("name", "未知用户名")
                    level = user_data.get("level", "未知等级")
                    print(f"   用户: {name} (等级: {level})")
                else:
                    print(f"   返回数据结构: {list(result.keys())}")
            else:
                print(f"❌ 获取用户信息失败: {result['error']}")
        except Exception as e:
            print(f"❌ 获取用户信息异常: {e}")
        
        # 测试5: 测试连接状态
        print("\n🌐 测试连接状态...")
        try:
            from main import test_connection
            result = test_connection()
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ 连接测试异常: {e}")
        
        print("\n🎉 测试完成！")
        print("\n💡 提示:")
        print("   - 如果某些测试失败，可能是网络问题或B站API限制")
        print("   - Cookie已设置，应该能避免大部分反爬限制")
        print("   - 可以使用 test_connection() 函数检查连接状态")
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保在正确的环境中运行此脚本")
    except Exception as e:
        print(f"❌ 测试过程中发生未知错误: {e}")

if __name__ == "__main__":
    test_bilibili_api()
