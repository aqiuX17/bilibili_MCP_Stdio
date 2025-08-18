#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站MCP服务器API功能测试脚本
测试所有主要API接口的可用性
"""

import sys
import json
import time
from main import BilibiliAPI

def test_user_info_api():
    """测试用户信息API（使用WBI签名版本）"""
    print("\n=== 测试用户信息API ===")
    api = BilibiliAPI()
    
    # 测试知名UP主的UID
    test_uids = ["946974", "37663924", "208259"]  # 一些知名UP主
    
    for uid in test_uids:
        print(f"\n测试UID: {uid}")
        result = api.get_user_info(uid)
        
        if isinstance(result, dict):
            code = result.get("code", -1)
            if code == 0:
                data = result.get("data", {})
                name = data.get("name", "未知")
                print(f"✅ 成功获取用户信息: {name}")
            else:
                message = result.get("message", "未知错误")
                print(f"❌ 获取用户信息失败: {message}")
        else:
            print(f"❌ 返回数据格式异常: {type(result)}")
        
        time.sleep(2)  # 避免请求过快

def test_user_search_api():
    """测试用户搜索API（多端点降级策略）"""
    print("\n=== 测试用户搜索API ===")
    api = BilibiliAPI()
    
    # 测试搜索关键词
    test_keywords = ["老番茄", "敖厂长", "回形针PaperClip"]
    
    for keyword in test_keywords:
        print(f"\n搜索关键词: {keyword}")
        result = api.search_user_by_nickname(keyword)
        
        if isinstance(result, dict):
            code = result.get("code", -1)
            if code == 0:
                data = result.get("data", {})
                users = data.get("result", [])
                source = data.get("source", "未知")
                print(f"✅ 搜索成功，找到{len(users)}个用户，来源: {source}")
                
                # 显示前3个结果
                for i, user in enumerate(users[:3]):
                    name = user.get("uname", "未知")
                    mid = user.get("mid", "未知")
                    print(f"  {i+1}. {name} (UID: {mid})")
            else:
                message = result.get("message", "未知错误")
                print(f"❌ 搜索失败: {message}")
        else:
            print(f"❌ 返回数据格式异常: {type(result)}")
        
        time.sleep(3)  # 搜索间隔稍长

def test_video_search_api():
    """测试视频搜索API"""
    print("\n=== 测试视频搜索API ===")
    api = BilibiliAPI()
    
    # 测试搜索关键词
    test_keywords = ["Python教程", "机器学习", "游戏解说"]
    
    for keyword in test_keywords:
        print(f"\n搜索视频: {keyword}")
        result = api.search_videos(keyword, page=1)
        
        if isinstance(result, dict):
            code = result.get("code", -1)
            if code == 0:
                data = result.get("data", {})
                videos = data.get("result", [])
                print(f"✅ 视频搜索成功，找到{len(videos)}个视频")
                
                # 显示前3个结果
                for i, video in enumerate(videos[:3]):
                    title = video.get("title", "未知")
                    author = video.get("author", "未知")
                    print(f"  {i+1}. {title} - {author}")
            else:
                message = result.get("message", "未知错误")
                print(f"❌ 视频搜索失败: {message}")
        else:
            print(f"❌ 返回数据格式异常: {type(result)}")
        
        time.sleep(2)

def test_wbi_functionality():
    """测试WBI签名功能"""
    print("\n=== 测试WBI签名功能 ===")
    api = BilibiliAPI()
    
    # 测试WBI密钥更新
    print("测试WBI密钥更新...")
    success = api._update_wbi_keys()
    if success:
        print(f"✅ WBI密钥更新成功")
        print(f"  img_key: {api.wbi_img_key[:8]}...")
        print(f"  sub_key: {api.wbi_sub_key[:8]}...")
    else:
        print("❌ WBI密钥更新失败")
    
    # 测试WBI签名生成
    print("\n测试WBI签名生成...")
    test_params = {"mid": "946974", "platform": "web"}
    signed_params = api._generate_wbi_signature(test_params)
    
    if "w_rid" in signed_params and "wts" in signed_params:
        print(f"✅ WBI签名生成成功")
        print(f"  w_rid: {signed_params['w_rid'][:8]}...")
        print(f"  wts: {signed_params['wts']}")
    else:
        print("❌ WBI签名生成失败")

def test_additional_apis():
    """测试其他API功能"""
    print("\n=== 测试其他API功能 ===")
    api = BilibiliAPI()
    
    # 测试URL提取功能（使用内置的正则表达式实现）
    print("\n测试UID提取功能...")
    test_urls = [
        "https://space.bilibili.com/946974",
        "https://space.bilibili.com/37663924/",
        "https://www.bilibili.com/video/BV1xx411c7mD"
    ]
    
    import re
    from urllib.parse import urlparse, parse_qs
    
    for url in test_urls:
        if "space.bilibili.com" in url:
            # 模拟extract_uid_from_bilibili_url功能
            uid_match = re.search(r'space\.bilibili\.com/(\d+)', url)
            if uid_match:
                uid = uid_match.group(1)
                print(f"  ✅ URL: {url} -> UID: {uid}")
            else:
                print(f"  ❌ URL: {url} -> 无法提取UID")
        elif "video" in url:
            # 模拟extract_bvid_from_url功能
            bv_match = re.search(r'BV[a-zA-Z0-9]+', url)
            if bv_match:
                bvid = bv_match.group()
                print(f"  ✅ URL: {url} -> BVID: {bvid}")
            else:
                print(f"  ❌ URL: {url} -> 无法提取BVID")
    
    # 测试连接状态
    print("\n测试连接状态...")
    try:
        # 简单的连接测试
        result = api._get_nav_info()
        if isinstance(result, dict) and result.get("code") == 0:
            print("✅ 连接状态: 正常")
        else:
            print("❌ 连接状态: 异常")
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")

def test_request_rate_limiting():
    """测试请求频率控制"""
    print("\n=== 测试请求频率控制 ===")
    api = BilibiliAPI()
    
    print("连续发送3个请求，观察间隔控制...")
    start_time = time.time()
    
    for i in range(3):
        print(f"\n发送第{i+1}个请求...")
        request_start = time.time()
        result = api.get_user_info("946974")
        request_end = time.time()
        
        if i > 0:
            interval = request_start - last_request_end
            print(f"与上次请求间隔: {interval:.2f}秒")
        
        last_request_end = request_end
    
    total_time = time.time() - start_time
    print(f"\n总耗时: {total_time:.2f}秒")
    
    # 显示请求统计
    success_rate = (api.request_success_count / api.request_total_count) * 100
    print(f"请求成功率: {success_rate:.1f}% ({api.request_success_count}/{api.request_total_count})")

def main():
    """主测试函数"""
    print("B站MCP服务器API功能测试")
    print("=" * 50)
    
    try:
        # 基础功能测试
        test_wbi_functionality()
        test_user_info_api()
        test_user_search_api()
        test_video_search_api()
        test_additional_apis()
        test_request_rate_limiting()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试完成")
        
    except KeyboardInterrupt:
        print("\n\n❌ 测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()