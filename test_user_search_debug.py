#!/usr/bin/env python3
"""
调试用户搜索功能
"""

import json
import requests
import time
import random
from typing import Dict, Optional

# 模拟配置
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

def test_direct_uid(uid: str):
    """直接测试UID获取用户信息"""
    print(f"🔍 测试直接获取用户信息 - UID: {uid}")
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    
    url = "https://api.bilibili.com/x/space/acc/info"
    params = {
        "mid": uid,
        "ts": int(time.time() * 1000),
        "w_rid": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=32)),
    }
    
    headers = {
        "Referer": f"https://space.bilibili.com/{uid}",
        "Origin": "https://www.bilibili.com",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    try:
        response = session.get(url, params=params, headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ 解析JSON成功")
                
                if data.get("code") == 0 and "data" in data:
                    user_data = data["data"]
                    print(f"✅ 用户信息获取成功:")
                    print(f"   👤 用户名: {user_data.get('name', '未知')}")
                    print(f"   🆔 UID: {user_data.get('mid', 'unknown')}")
                    print(f"   📝 签名: {user_data.get('sign', '无')[:50]}...")
                    print(f"   🎯 等级: {user_data.get('level', 0)}")
                    print(f"   👥 粉丝: {user_data.get('fans', 0)}")
                    return True
                else:
                    print(f"❌ API返回错误: code={data.get('code')}, message={data.get('message')}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应前500字符: {response.text[:500]}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_search_by_nickname(nickname: str):
    """测试昵称搜索"""
    print(f"\n🔍 测试昵称搜索 - 关键词: '{nickname}'")
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    
    # 尝试多个搜索端点
    search_apis = [
        {
            "name": "用户搜索API v1",
            "url": "https://api.bilibili.com/x/web-interface/search/type",
            "params": {
                "search_type": "bili_user",
                "keyword": nickname,
                "page": 1,
                "order": "fans",
                "order_sort": 0,
                "user_type": 0,
                "duration": 0
            }
        },
        {
            "name": "用户搜索API v2",
            "url": "https://api.bilibili.com/x/web-interface/wbi/search/type",
            "params": {
                "search_type": "bili_user",
                "keyword": nickname,
                "page": 1
            }
        },
        {
            "name": "综合搜索API",
            "url": "https://api.bilibili.com/x/web-interface/search/all/v2",
            "params": {
                "keyword": nickname,
                "page": 1
            }
        }
    ]
    
    for api in search_apis:
        print(f"\n  🧪 尝试: {api['name']}")
        try:
            headers = {
                "Referer": "https://search.bilibili.com/",
                "Origin": "https://www.bilibili.com"
            }
            
            response = session.get(api["url"], params=api["params"], headers=headers, timeout=15)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  ✅ JSON解析成功")
                    
                    # 分析返回结构
                    if "data" in data:
                        if data.get("code") == 0:
                            data_content = data["data"]
                            
                            # 查找用户结果
                            users_found = []
                            if "result" in data_content:
                                if isinstance(data_content["result"], list):
                                    users_found = data_content["result"]
                                elif isinstance(data_content["result"], dict):
                                    # 可能包含多种类型的搜索结果
                                    for key, value in data_content["result"].items():
                                        if "user" in key.lower() and isinstance(value, list):
                                            users_found = value
                                            break
                            
                            if users_found:
                                print(f"  ✅ 找到 {len(users_found)} 个用户:")
                                for i, user in enumerate(users_found[:3], 1):  # 只显示前3个
                                    print(f"    {i}. 👤 {user.get('uname', user.get('title', '未知用户'))}")
                                    print(f"       🆔 UID: {user.get('mid', 'unknown')}")
                                    print(f"       👥 粉丝: {user.get('fans', 0)}")
                                return True
                            else:
                                print(f"  ⚠️ 未找到用户结果")
                                print(f"  数据结构: {list(data_content.keys()) if isinstance(data_content, dict) else type(data_content)}")
                        else:
                            print(f"  ❌ API错误: code={data.get('code')}, message={data.get('message')}")
                    else:
                        print(f"  ❌ 响应格式异常")
                        print(f"  响应结构: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                    
                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON解析失败: {e}")
                    print(f"  原始响应前200字符: {response.text[:200]}")
            else:
                print(f"  ❌ HTTP请求失败: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"  ❌ 请求异常: {e}")
    
    return False

def extract_uid_from_url(url: str):
    """从B站用户空间URL提取UID"""
    import re
    
    print(f"🔗 解析B站用户链接: {url}")
    
    # 匹配 space.bilibili.com/数字
    match = re.search(r'space\.bilibili\.com/(\d+)', url)
    if match:
        uid = match.group(1)
        print(f"✅ 提取到UID: {uid}")
        return uid
    else:
        print("❌ 无法从URL中提取UID")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("🔍 B站用户搜索功能调试")
    print("=" * 60)
    
    # 测试1: 从URL提取UID
    test_url = "https://space.bilibili.com/316183842?spm_id_from=333.337.0.0"
    uid = extract_uid_from_url(test_url)
    
    if uid:
        # 测试2: 直接通过UID获取用户信息
        print("\n" + "=" * 40)
        print("📋 测试1: 直接UID查询")
        print("=" * 40)
        success = test_direct_uid(uid)
        
        if success:
            print("✅ 直接UID查询成功！这证明用户存在且API可访问")
        else:
            print("❌ 直接UID查询失败")
    
    # 测试3: 昵称搜索
    print("\n" + "=" * 40)
    print("📋 测试2: 昵称搜索")
    print("=" * 40)
    search_success = test_search_by_nickname("技术爬爬虾")
    
    if not search_success:
        print("❌ 昵称搜索功能确实存在问题")
        print("\n💡 建议解决方案:")
        print("1. 优先使用直接UID查询功能")
        print("2. 添加从B站链接提取UID的工具")
        print("3. 改进搜索API实现或使用其他搜索策略")
    
    print("\n" + "=" * 60)
    print("🎯 调试总结:")
    if uid:
        print(f"✅ URL解析成功: 用户UID = {uid}")
    else:
        print("❌ URL解析失败")
    
    print("💡 下一步优化建议:")
    print("1. 添加extract_uid_from_url工具函数")
    print("2. 优化搜索API参数和端点")
    print("3. 提供备用的搜索方案")

if __name__ == "__main__":
    main()
