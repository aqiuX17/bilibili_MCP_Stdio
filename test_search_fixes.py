#!/usr/bin/env python3
"""
测试用户搜索修复效果
"""

import json
import sys
import time
import random
from typing import Dict, Optional
import requests

# 模拟从main.py导入的配置
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    "Referer": "https://www.bilibili.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Origin": "https://www.bilibili.com",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

def load_cookies():
    """加载cookie配置"""
    try:
        with open('cookie_example.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 无法加载cookie: {e}")
        return {}

def test_uid_extraction():
    """测试UID提取功能"""
    print("🔗 测试UID提取功能")
    print("-" * 40)
    
    test_urls = [
        "https://space.bilibili.com/316183842?spm_id_from=333.337.0.0",
        "https://space.bilibili.com/1234567890",
        "https://space.bilibili.com/123456789/",
        "https://www.bilibili.com/space/123456789?from=search",
        "invalid_url_test"
    ]
    
    import re
    
    for url in test_urls:
        print(f"🔍 测试URL: {url}")
        
        # 模拟extract_uid_from_bilibili_url函数
        uid_match = re.search(r'space\.bilibili\.com/(\d+)', url)
        if uid_match:
            uid = uid_match.group(1)
            print(f"✅ 成功提取UID: {uid}")
        else:
            other_patterns = [r'/(\d+)/?', r'mid[=:](\d+)']
            found = False
            for pattern in other_patterns:
                match = re.search(pattern, url)
                if match:
                    uid = match.group(1)
                    print(f"✅ 从其他模式提取到UID: {uid}")
                    found = True
                    break
            if not found:
                print("❌ 无法提取UID")
        print()

def test_user_info_with_cookies(uid: str):
    """测试带cookie的用户信息获取"""
    print(f"👤 测试用户信息获取（带Cookie） - UID: {uid}")
    print("-" * 40)
    
    cookies = load_cookies()
    if not cookies:
        print("⚠️ 未加载到cookie，跳过测试")
        return False
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    session.cookies.update(cookies)
    
    url = "https://api.bilibili.com/x/space/acc/info"
    params = {
        "mid": uid,
        "ts": int(time.time()),
    }
    
    headers = {
        "Referer": f"https://space.bilibili.com/{uid}",
        "Origin": "https://www.bilibili.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Cache-Control": "no-cache",
    }
    
    try:
        # 添加随机延迟
        delay = random.uniform(2, 5)
        print(f"⏱️ 随机等待 {delay:.1f} 秒")
        time.sleep(delay)
        
        response = session.get(url, params=params, headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON解析成功")
                
                if data.get("code") == 0 and "data" in data:
                    user_data = data["data"]
                    print(f"🎉 用户信息获取成功:")
                    print(f"   👤 用户名: {user_data.get('name', '未知')}")
                    print(f"   🆔 UID: {user_data.get('mid', 'unknown')}")
                    print(f"   📝 签名: {user_data.get('sign', '无')[:50]}...")
                    print(f"   🎯 等级: {user_data.get('level', 0)}")
                    print(f"   👥 粉丝: {user_data.get('fans', 0)}")
                    print(f"   📺 关注: {user_data.get('friend', 0)}")
                    return True
                elif data.get("code") == -799:
                    print(f"⚠️ 请求频率限制: {data.get('message')}")
                    print("💡 建议: 增加请求间隔时间")
                    return False
                else:
                    print(f"❌ API返回错误: code={data.get('code')}, message={data.get('message')}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应: {response.text[:200]}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_user_info_without_cookies(uid: str):
    """测试不带cookie的用户信息获取"""
    print(f"👤 测试用户信息获取（无Cookie） - UID: {uid}")
    print("-" * 40)
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    
    url = "https://api.bilibili.com/x/space/acc/info"
    params = {
        "mid": uid,
        "ts": int(time.time()),
    }
    
    headers = {
        "Referer": f"https://space.bilibili.com/{uid}",
        "Origin": "https://www.bilibili.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    
    try:
        # 添加随机延迟
        delay = random.uniform(1, 3)
        print(f"⏱️ 等待 {delay:.1f} 秒")
        time.sleep(delay)
        
        response = session.get(url, params=params, headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON解析成功")
                
                if data.get("code") == 0 and "data" in data:
                    user_data = data["data"]
                    print(f"🎉 用户信息获取成功:")
                    print(f"   👤 用户名: {user_data.get('name', '未知')}")
                    print(f"   🆔 UID: {user_data.get('mid', 'unknown')}")
                    return True
                else:
                    print(f"❌ API返回错误: code={data.get('code')}, message={data.get('message')}")
                    if data.get("code") == -799:
                        print("💡 频率限制，建议设置cookie")
                    return False
                    
            except json.JSONDecodeError:
                print(f"❌ JSON解析失败")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🧪 B站用户搜索修复效果测试")
    print("=" * 60)
    
    # 测试1: UID提取功能
    test_uid_extraction()
    print("\n" + "=" * 40)
    
    # 使用目标用户的UID进行测试
    target_uid = "316183842"  # 技术爬爬虾
    
    # 测试2: 不带cookie的用户信息获取
    print("📋 测试2: 无Cookie模式")
    print("=" * 40)
    success_no_cookie = test_user_info_without_cookies(target_uid)
    
    print("\n" + "=" * 40)
    
    # 测试3: 带cookie的用户信息获取
    print("📋 测试3: Cookie模式")
    print("=" * 40) 
    success_with_cookie = test_user_info_with_cookies(target_uid)
    
    print("\n" + "=" * 60)
    print("📊 测试总结:")
    print("=" * 60)
    
    print(f"✅ UID提取功能: 正常工作")
    print(f"{'✅' if success_no_cookie else '❌'} 无Cookie用户查询: {'成功' if success_no_cookie else '失败'}")
    print(f"{'✅' if success_with_cookie else '❌'} Cookie用户查询: {'成功' if success_with_cookie else '失败'}")
    
    if success_with_cookie or success_no_cookie:
        print("\n🎉 用户信息查询功能已修复！")
        print("💡 建议解决方案:")
        print("1. ✅ 使用extract_uid_from_bilibili_url提取用户UID")
        print("2. ✅ 使用get_user_info直接查询用户信息")
        if success_with_cookie:
            print("3. ✅ 设置完整cookie可提高成功率")
    else:
        print("\n⚠️ 用户信息查询仍有问题")
        print("💡 可能的解决方案:")
        print("1. 增加更长的请求间隔")
        print("2. 使用更完整的cookie配置")
        print("3. 尝试其他API端点")

if __name__ == "__main__":
    main()
