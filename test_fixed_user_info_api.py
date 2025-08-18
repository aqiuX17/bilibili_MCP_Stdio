#!/usr/bin/env python3
"""
测试修复后的用户信息API（基于bilibili-API-collect项目规范）
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

def test_user_info_api_fixed(uid: str):
    """测试修复后的用户信息API（严格按照bilibili-API-collect规范）"""
    print(f"🔧 测试修复后的用户信息API - UID: {uid}")
    print("-" * 50)
    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    
    # 加载cookie
    cookies = load_cookies()
    if cookies:
        session.cookies.update(cookies)
        print(f"✅ 加载了 {len(cookies)} 个cookie")
    else:
        print("⚠️ 未加载cookie，可能影响成功率")
    
    # 按照bilibili-API-collect文档配置请求
    url = "https://api.bilibili.com/x/space/acc/info"
    
    # 必需参数
    params = {"mid": uid}
    
    # 可选参数（按照bilibili-API-collect文档，这些参数可以提高成功率）
    params.update({
        "platform": "web",
        "web_location": "space.header"
    })
    
    # 完整的请求头（严格按照bilibili-API-collect文档要求）
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "Referer": f"https://space.bilibili.com/{uid}",
        "Origin": "https://www.bilibili.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",  # 关键：用户信息API需要cors模式
        "sec-fetch-site": "same-site",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    # 如果有cookie，添加更多认证相关头部
    if cookies:
        headers.update({
            "X-Requested-With": "XMLHttpRequest",
        })
    
    try:
        print("📡 发送API请求...")
        print(f"   URL: {url}")
        print(f"   参数: {params}")
        print(f"   关键头部: sec-fetch-mode=cors, platform=web")
        
        # 添加随机延迟
        delay = random.uniform(2, 4)
        print(f"⏱️ 等待 {delay:.1f} 秒")
        time.sleep(delay)
        
        response = session.get(url, params=params, headers=headers, timeout=15)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON解析成功")
                
                code = data.get("code", -1)
                print(f"📋 业务状态码: {code}")
                
                # 按照bilibili-API-collect文档处理不同状态码
                if code == 0:
                    user_data = data.get("data", {})
                    if user_data:
                        print("🎉 用户信息获取成功！")
                        print("\n📊 用户详情:")
                        print(f"   👤 用户名: {user_data.get('name', '未知')}")
                        print(f"   🆔 UID: {user_data.get('mid', 'unknown')}")
                        print(f"   🎯 等级: Lv.{user_data.get('level', 0)}")
                        print(f"   👥 粉丝数: {user_data.get('fans', 0):,}")
                        print(f"   📺 关注数: {user_data.get('friend', 0):,}")
                        print(f"   🏷️ 性别: {user_data.get('sex', '未知')}")
                        print(f"   📝 个性签名: {user_data.get('sign', '无')[:50]}...")
                        print(f"   🖼️ 头像: {user_data.get('face', '无')}")
                        print(f"   💰 硬币: {user_data.get('coins', 0)}")
                        print(f"   🎂 生日: {user_data.get('birthday', '未公开')}")
                        print(f"   🏫 学校: {user_data.get('school', '未公开')}")
                        print(f"   💼 职业: {user_data.get('profession', '未公开')}")
                        print(f"   📅 注册时间: {user_data.get('jointime', 0)}")
                        
                        # 检查认证信息
                        official = user_data.get('official', {})
                        if official.get('type', 0) > 0:
                            print(f"   ✅ 认证: {official.get('title', '未知认证')}")
                        
                        # 检查VIP信息
                        vip = user_data.get('vip', {})
                        if vip.get('type', 0) > 0:
                            print(f"   💎 大会员: {vip.get('label', {}).get('text', 'VIP')}")
                        
                        return True
                    else:
                        print("❌ 用户数据为空")
                        return False
                
                # 处理特定错误码
                elif code == -400:
                    print("❌ 请求错误 - 参数格式可能有问题")
                elif code == -403:
                    print("❌ 访问权限不足 - 可能需要有效的SESSDATA cookie")
                elif code == -404:
                    print("❌ 用户不存在")
                elif code == -799:
                    print("⚠️ 请求过于频繁，需要增加间隔时间")
                elif code == 22001:
                    print("❌ 不存在该用户")
                elif code == 22002:
                    print("⚠️ 用户已注销")
                elif code == 22003:
                    print("❌ 用户已被封禁")
                else:
                    print(f"❌ 未知错误码: {code}")
                    print(f"   错误信息: {data.get('message', '未知')}")
                
                return False
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应前300字符: {response.text[:300]}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_multiple_users():
    """测试多个用户ID"""
    test_users = [
        ("316183842", "技术爱爱虾"),
        ("1", "bilibili"),
        ("12345", "测试用户"),
        ("999999999", "不存在的用户")
    ]
    
    success_count = 0
    total_count = len(test_users)
    
    for uid, name in test_users:
        print(f"\n{'='*60}")
        print(f"🧪 测试用户: {name} (UID: {uid})")
        print("="*60)
        
        success = test_user_info_api_fixed(uid)
        if success:
            success_count += 1
        
        # 测试间隔
        if uid != test_users[-1][0]:  # 不是最后一个
            print("\n⏱️ 等待测试间隔...")
            time.sleep(3)
    
    return success_count, total_count

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 修复后的用户信息API测试")
    print("📖 基于bilibili-API-collect项目规范")
    print("=" * 60)
    
    print("\n💡 本次修复的关键改进:")
    print("   • ✅ 添加了platform和web_location参数")
    print("   • ✅ 修正了sec-fetch-mode为cors模式") 
    print("   • ✅ 完善了错误码处理机制")
    print("   • ✅ 严格按照bilibili-API-collect文档规范")
    print("   • ✅ 优化了请求头配置")
    
    # 测试多个用户
    success_count, total_count = test_multiple_users()
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试总结报告")
    print("=" * 60)
    
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    print(f"✅ 测试通过率: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_rate >= 75:
        print("🎉 修复效果显著！用户信息API基本可用")
        print("💡 建议继续使用修复后的版本")
    elif success_rate >= 50:
        print("👍 修复效果良好，部分功能正常")
        print("💡 建议进一步优化cookie配置")
    elif success_rate >= 25:
        print("⚠️ 修复有一定效果，但仍需改进")
        print("💡 建议检查cookie有效性和请求频率")
    else:
        print("❌ 修复效果有限，需要进一步调试")
        print("💡 建议检查网络环境和API文档更新")
    
    print(f"\n🎯 关键成功因素:")
    print("   • 🔐 有效的SESSDATA cookie")
    print("   • ⏱️ 适当的请求间隔")
    print("   • 📋 完整的请求头配置")
    print("   • 🎯 正确的API参数")
    
    print("\n📚 参考资料:")
    print("   • bilibili-API-collect: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/user/info.md")
    print("   • B站用户信息接口文档")

if __name__ == "__main__":
    main()
