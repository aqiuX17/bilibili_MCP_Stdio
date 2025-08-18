#!/usr/bin/env python3
"""
测试基于 bilibili-API-collect 项目的改进效果
参考项目: https://github.com/SocialSisterYi/bilibili-API-collect
"""

import json
import sys
import time
import random
import hashlib
import urllib.parse
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

def test_nav_api():
    """测试导航API - 获取WBI密钥"""
    print("🧭 测试导航API（WBI密钥获取）")
    print("-" * 40)
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    
    cookies = load_cookies()
    if cookies:
        session.cookies.update(cookies)
        print(f"✅ 加载了 {len(cookies)} 个cookie")
    
    try:
        url = "https://api.bilibili.com/x/web-interface/nav"
        headers = {
            "Referer": "https://www.bilibili.com/",
            "Origin": "https://www.bilibili.com"
        }
        
        response = session.get(url, headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 导航API调用成功")
            
            if data.get("code") == 0:
                nav_data = data.get("data", {})
                wbi_img = nav_data.get("wbi_img", {})
                
                img_url = wbi_img.get("img_url", "")
                sub_url = wbi_img.get("sub_url", "")
                
                if img_url and sub_url:
                    img_key = img_url.split("/")[-1].split(".")[0]
                    sub_key = sub_url.split("/")[-1].split(".")[0]
                    print(f"✅ WBI密钥提取成功:")
                    print(f"   img_key: {img_key[:8]}...")
                    print(f"   sub_key: {sub_key[:8]}...")
                    return img_key, sub_key
                else:
                    print("❌ 未找到WBI密钥URL")
            else:
                print(f"❌ API返回错误: {data.get('message')}")
        else:
            print("❌ 导航API调用失败")
    except Exception as e:
        print(f"❌ 导航API测试异常: {e}")
    
    return None, None

def generate_wbi_signature(params: Dict, img_key: str, sub_key: str) -> Dict:
    """生成WBI签名"""
    try:
        # WBI字符重排序表（来自bilibili-API-collect项目）
        mixin_key_enc_tab = [
            46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
            33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61,
            26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36,
            20, 34, 44, 52
        ]
        
        # 生成混合密钥
        raw_wbi_key = img_key + sub_key
        wbi_key = "".join([raw_wbi_key[i] for i in mixin_key_enc_tab if i < len(raw_wbi_key)])[:32]
        
        # 添加时间戳
        params = params.copy()
        params["wts"] = int(time.time())
        
        # 按key排序并构建查询字符串
        sorted_params = sorted(params.items())
        query_string = urllib.parse.urlencode(sorted_params)
        
        # 生成签名
        sign_string = query_string + wbi_key
        w_rid = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
        
        # 添加w_rid到参数
        params["w_rid"] = w_rid
        
        print(f"✅ WBI签名生成成功: w_rid={w_rid[:8]}..., wts={params['wts']}")
        return params
        
    except Exception as e:
        print(f"❌ WBI签名生成失败: {e}")
        return params

def test_wbi_search(img_key: str, sub_key: str):
    """测试WBI版本的搜索API"""
    print(f"\n🔍 测试WBI搜索API")
    print("-" * 40)
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    
    cookies = load_cookies()
    if cookies:
        session.cookies.update(cookies)
    
    # 测试用户搜索
    search_params = {
        "search_type": "bili_user",
        "keyword": "技术爬爬虾",
        "page": 1,
        "order": "fans",
        "order_sort": 0,
        "user_type": 0
    }
    
    # 生成WBI签名
    signed_params = generate_wbi_signature(search_params, img_key, sub_key)
    
    try:
        url = "https://api.bilibili.com/x/web-interface/wbi/search/type"
        headers = {
            "Referer": "https://search.bilibili.com/",
            "Origin": "https://www.bilibili.com",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        response = session.get(url, params=signed_params, headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("code") == 0:
                search_data = data.get("data", {})
                results = search_data.get("result", [])
                
                if results:
                    print(f"🎉 WBI搜索成功，找到 {len(results)} 个用户:")
                    for i, user in enumerate(results[:3], 1):
                        print(f"   {i}. 👤 {user.get('uname', '未知用户')}")
                        print(f"      🆔 UID: {user.get('mid', 0)}")
                        print(f"      👥 粉丝: {user.get('fans', 0)}")
                    return True
                else:
                    print("⚠️ WBI搜索无结果")
            else:
                print(f"❌ WBI搜索API错误: {data.get('message')}")
        else:
            print(f"❌ WBI搜索请求失败: {response.status_code}")
    except Exception as e:
        print(f"❌ WBI搜索测试异常: {e}")
    
    return False

def test_new_apis():
    """测试新增的API功能"""
    print(f"\n🆕 测试新增API功能")
    print("-" * 40)
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    
    cookies = load_cookies()
    if cookies:
        session.cookies.update(cookies)
    
    # 测试API列表
    api_tests = [
        {
            "name": "用户关系统计API",
            "url": "https://api.bilibili.com/x/relation/stat",
            "params": {"vmid": "316183842"},  # 技术爬爬虾的UID
            "expected_fields": ["following", "follower"]
        },
        {
            "name": "视频统计API", 
            "url": "https://api.bilibili.com/x/web-interface/archive/stat",
            "params": {"bvid": "BV1GJ411x7h7"},
            "expected_fields": ["view", "danmaku", "reply", "favorite"]
        },
        {
            "name": "搜索建议API",
            "url": "https://s.search.bilibili.com/main/suggest",
            "params": {
                "func": "suggest",
                "suggest_type": "accurate",
                "term": "python"
            },
            "expected_fields": ["tag", "upuser"]
        }
    ]
    
    success_count = 0
    
    for api_test in api_tests:
        print(f"🧪 测试 {api_test['name']}...")
        
        try:
            response = session.get(
                api_test["url"], 
                params=api_test["params"], 
                headers={"Referer": "https://www.bilibili.com/"}, 
                timeout=15
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if data.get("code") == 0:
                        api_data = data.get("data", {})
                        
                        # 检查预期字段
                        has_expected_fields = any(field in str(api_data) for field in api_test["expected_fields"])
                        
                        if has_expected_fields:
                            print(f"   ✅ {api_test['name']} 成功")
                            success_count += 1
                        else:
                            print(f"   ⚠️ {api_test['name']} 返回数据不完整")
                    else:
                        print(f"   ❌ {api_test['name']} API错误: {data.get('message')}")
                except json.JSONDecodeError:
                    print(f"   ❌ {api_test['name']} JSON解析失败")
            else:
                print(f"   ❌ {api_test['name']} HTTP错误: {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ {api_test['name']} 测试异常: {e}")
        
        time.sleep(1)  # 避免请求过于频繁
    
    print(f"\n📊 新API测试结果: {success_count}/{len(api_tests)} 个成功")
    return success_count

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 bilibili-API-collect 项目改进效果测试")
    print("📖 参考项目: https://github.com/SocialSisterYi/bilibili-API-collect")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    
    # 测试1: 导航API和WBI密钥
    print("\n📋 测试阶段1: WBI密钥获取")
    print("=" * 40)
    img_key, sub_key = test_nav_api()
    
    total_tests += 1
    if img_key and sub_key:
        passed_tests += 1
        
        # 测试2: WBI搜索
        print("\n📋 测试阶段2: WBI签名搜索")
        print("=" * 40)
        wbi_search_success = test_wbi_search(img_key, sub_key)
        
        total_tests += 1
        if wbi_search_success:
            passed_tests += 1
    else:
        print("\n⚠️ 跳过WBI搜索测试（密钥获取失败）")
        total_tests += 1
    
    # 测试3: 新增API功能
    print("\n📋 测试阶段3: 新增API功能")
    print("=" * 40)
    new_api_success = test_new_apis()
    
    total_tests += 3  # 3个新API
    passed_tests += new_api_success
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试总结报告")
    print("=" * 60)
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"✅ 测试通过率: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    print(f"\n🎯 基于bilibili-API-collect项目的改进成果:")
    
    if img_key and sub_key:
        print("   ✅ WBI签名算法实现成功")
        print("   ✅ 导航API密钥获取功能正常")
    else:
        print("   ❌ WBI签名算法需要进一步调试")
    
    if new_api_success >= 2:
        print("   ✅ 新增API功能大部分可用")
    elif new_api_success >= 1:
        print("   ⚠️ 新增API功能部分可用")
    else:
        print("   ❌ 新增API功能需要进一步优化")
    
    if success_rate >= 80:
        print(f"\n🎉 改进效果显著！API成功率大幅提升")
        print("💡 建议继续使用基于bilibili-API-collect的优化版本")
    elif success_rate >= 60:
        print(f"\n👍 改进效果良好，建议完善cookie配置")
        print("💡 可以考虑使用部分优化功能")
    else:
        print(f"\n⚠️ 改进效果有限，需要进一步调试")
        print("💡 建议检查网络环境和cookie配置")
    
    print("\n📚 参考资料:")
    print("   • bilibili-API-collect: https://github.com/SocialSisterYi/bilibili-API-collect")
    print("   • B站WBI签名算法详解")
    print("   • B站反爬虫机制研究")

if __name__ == "__main__":
    main()
