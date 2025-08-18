#!/usr/bin/env python3
"""
测试当前用户信息API的实际错误情况
不依赖MCP框架，直接测试API类
"""

import json
import time
import random
import hashlib
import urllib.parse
from typing import Dict, Optional
import requests

# 从main.py中提取API类的核心实现（去掉MCP依赖）
class BilibiliAPITest:
    """测试版B站API类（不依赖MCP）"""
    
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        # 请求头配置（基于真实抓包数据）
        self.DEFAULT_HEADERS = {
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
        
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        
        if cookies:
            self.session.cookies.update(cookies)
            print(f"✅ 设置了 {len(cookies)} 个cookie")
    
    def get_user_info(self, uid: str) -> Dict:
        """获取用户基本信息（当前实现版本）"""
        try:
            # 检查参数有效性
            if not uid.isdigit():
                return {"code": -400, "message": "无效的用户ID"}
            
            # 接口地址（当前实现）
            url = "https://api.bilibili.com/x/space/acc/info"
            
            # 参数配置（当前版本）
            params = {
                "mid": uid,
                "platform": "web",
                "web_location": "space.header"
            }
            
            # 请求头配置（当前版本）
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
                "sec-fetch-mode": "cors",  # 当前使用cors模式
                "sec-fetch-site": "same-site",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
            
            # 添加认证头
            if self.session.cookies:
                headers.update({
                    "X-Requested-With": "XMLHttpRequest",
                })
            
            print(f"🔍 测试当前实现 - UID: {uid}")
            print(f"   URL: {url}")
            print(f"   参数: {params}")
            print(f"   关键头部: sec-fetch-mode={headers['sec-fetch-mode']}")
            
            # 发送请求
            response = self.session.get(url, params=params, headers=headers, timeout=15)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    # 处理可能的反爬字符
                    text = response.text
                    if text.startswith('!'):
                        text = text[1:]  # 去掉开头的感叹号
                    
                    data = json.loads(text)
                    print(f"   业务码: {data.get('code', 'unknown')}")
                    return data
                except json.JSONDecodeError as e:
                    print(f"   JSON解析失败: {e}")
                    print(f"   响应内容: {response.text[:200]}")
                    return {"code": -1, "message": f"JSON解析失败: {str(e)}"}
            else:
                return {"code": -1, "message": f"HTTP错误: {response.status_code}"}
                
        except Exception as e:
            print(f"   异常: {e}")
            return {"code": -1, "message": f"请求异常: {str(e)}"}

def load_cookies():
    """加载cookie配置"""
    try:
        with open('cookie_example.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 无法加载cookie: {e}")
        return {}

def analyze_nemo_bilibili_api_approach():
    """分析Nemo2011/bilibili-api项目的实现方式"""
    print("📚 Nemo2011/bilibili-api 项目分析")
    print("="*60)
    print("🔗 项目地址: https://github.com/Nemo2011/bilibili-api")
    print("⭐ Stars: 2.9k | 🍴 Forks: 272")
    print()
    
    print("🎯 项目特点:")
    print("   • 🔄 全异步操作 (asyncio)")
    print("   • 🌐 支持多种请求库 (aiohttp/httpx/curl_cffi)")
    print("   • 🔐 Credential类管理认证信息")
    print("   • 🛡️ 完善的反爬虫策略")
    print("   • 🎯 支持代理和TLS指纹伪装")
    print("   • 🔄 支持cookie自动刷新")
    print("   • 📊 全面的功能覆盖")
    print()
    
    print("🔑 关键实现差异:")
    print("   1. 📡 请求方式: 异步 vs 我们的同步")
    print("   2. 🔐 认证管理: Credential类 vs 直接cookie")
    print("   3. 🛡️ 反爬策略: curl_cffi + TLS伪装 vs 基础请求")
    print("   4. 📊 错误处理: 完整的状态码处理")
    print("   5. 🔄 重试机制: 智能重试 vs 单次请求")
    print()
    
    print("💡 推荐改进方向:")
    improvements = [
        "🔄 实现更智能的重试机制",
        "🛡️ 添加TLS指纹伪装 (curl_cffi)",
        "🎯 实现Credential风格的认证管理",
        "📊 完善错误码处理和用户提示",
        "⏱️ 实现更精确的请求间隔控制",
        "🔍 添加请求成功率监控",
        "🌐 支持代理轮换机制",
        "📝 改进日志和调试信息"
    ]
    
    for improvement in improvements:
        print(f"   • {improvement}")

def test_current_implementation():
    """测试当前实现的问题"""
    print("\n" + "="*60)
    print("🧪 测试当前用户信息API实现")
    print("="*60)
    
    # 加载cookie
    cookies = load_cookies()
    
    # 创建API实例
    api = BilibiliAPITest(cookies)
    
    # 测试用户列表
    test_users = [
        ("316183842", "技术爱爱虾"),
        ("1", "bilibili官方"),
        ("12345", "测试用户")
    ]
    
    results = []
    
    for uid, name in test_users:
        print(f"\n📋 测试用户: {name} (UID: {uid})")
        print("-" * 40)
        
        # 随机延迟
        delay = random.uniform(3, 6)
        print(f"⏱️ 等待 {delay:.1f} 秒")
        time.sleep(delay)
        
        # 测试API
        result = api.get_user_info(uid)
        
        # 分析结果
        if isinstance(result, dict):
            code = result.get("code", -1)
            if code == 0:
                user_data = result.get("data", {})
                if user_data:
                    print(f"✅ 成功: {user_data.get('name', '未知')}")
                    results.append(("success", uid, name))
                else:
                    print("⚠️ 成功但数据为空")
                    results.append(("empty_data", uid, name))
            elif code == -799:
                print("⚠️ 频率限制")
                results.append(("rate_limit", uid, name))
            elif code == -403:
                print("❌ 权限不足")
                results.append(("permission_denied", uid, name))
            elif code == -404:
                print("❌ 用户不存在")
                results.append(("user_not_found", uid, name))
            else:
                print(f"❌ 错误码: {code}")
                results.append(("error", uid, name))
        else:
            print("❌ 返回格式异常")
            results.append(("format_error", uid, name))
    
    # 汇总结果
    print(f"\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    success_count = len([r for r in results if r[0] == "success"])
    total_count = len(results)
    
    print(f"✅ 成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    # 分析问题
    issues = []
    if any(r[0] == "rate_limit" for r in results):
        issues.append("🚫 频率限制问题")
    if any(r[0] == "permission_denied" for r in results):
        issues.append("🔐 认证权限问题")
    if any(r[0] == "format_error" for r in results):
        issues.append("📊 数据格式问题")
    
    if issues:
        print(f"\n🔍 发现的问题:")
        for issue in issues:
            print(f"   • {issue}")
    
    return results

def suggest_improvements_based_on_nemo():
    """基于Nemo项目提出具体改进建议"""
    print(f"\n" + "="*60)
    print("💡 基于Nemo2011/bilibili-api的改进建议")
    print("="*60)
    
    suggestions = [
        {
            "问题": "频率限制严重",
            "Nemo解决方案": "智能重试 + 代理轮换",
            "具体实现": "实现指数退避重试，支持代理池"
        },
        {
            "问题": "反爬检测",
            "Nemo解决方案": "curl_cffi + TLS指纹伪装",
            "具体实现": "使用curl_cffi库模拟真实浏览器TLS握手"
        },
        {
            "问题": "认证管理复杂",
            "Nemo解决方案": "Credential类统一管理",
            "具体实现": "创建类似的认证管理类"
        },
        {
            "问题": "错误处理不完善",
            "Nemo解决方案": "完整的异常处理机制",
            "具体实现": "标准化错误码处理和用户友好提示"
        },
        {
            "问题": "请求性能低",
            "Nemo解决方案": "异步请求 + 连接池",
            "具体实现": "迁移到异步或改进连接复用"
        }
    ]
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. 📋 {suggestion['问题']}")
        print(f"   🎯 Nemo方案: {suggestion['Nemo解决方案']}")
        print(f"   🔧 实现建议: {suggestion['具体实现']}")
        print()

def main():
    """主函数"""
    print("🔧 B站用户信息API问题诊断与改进")
    print("📖 参考项目: https://github.com/Nemo2011/bilibili-api")
    print()
    
    # 分析Nemo项目
    analyze_nemo_bilibili_api_approach()
    
    # 测试当前实现
    test_results = test_current_implementation()
    
    # 改进建议
    suggest_improvements_based_on_nemo()
    
    print("="*60)
    print("🎯 下一步行动计划:")
    print("1. 🛡️ 实现curl_cffi反爬虫策略")
    print("2. 🔄 添加智能重试机制") 
    print("3. 🔐 改进认证管理")
    print("4. ⏱️ 优化请求频率控制")
    print("5. 📊 完善错误处理")
    print("="*60)

if __name__ == "__main__":
    main()

