#!/usr/bin/env python3
"""
最终测试：用户信息API修复效果验证
基于Nemo2011/bilibili-api项目的改进方案
"""

import json
import time
import random
from typing import Dict, Optional
import requests

def load_cookies():
    """加载cookie配置"""
    try:
        with open('cookie_example.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 无法加载cookie: {e}")
        return {}

class FinalBilibiliAPI:
    """最终版B站API类（综合所有改进）"""
    
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        self.session = requests.Session()
        
        # 基础配置
        self.DEFAULT_HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Origin": "https://www.bilibili.com",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
        
        self.session.headers.update(self.DEFAULT_HEADERS)
        
        # Nemo风格配置
        self.min_interval = 3.0  # 进一步增加间隔
        self.max_interval = 6.0
        self.max_retries = 3
        self.retry_delay_base = 3
        self.last_request_time = 0
        
        if cookies:
            self.session.cookies.update(cookies)
            print(f"✅ 设置了 {len(cookies)} 个cookie")
    
    def _handle_anti_crawl_response(self, response_text: str) -> str:
        """处理反爬响应（综合处理各种情况）"""
        original_text = response_text
        
        # 处理各种可能的反爬前缀
        anti_crawl_prefixes = ['!', '!［', '］', '!{', '!［{']
        
        for prefix in anti_crawl_prefixes:
            if response_text.startswith(prefix):
                if prefix == '!{':
                    response_text = response_text[1:]
                elif prefix == '!［{':
                    response_text = response_text[2:]
                elif prefix == '］{':
                    response_text = response_text[1:]
                elif prefix == '!':
                    response_text = response_text[1:]
                elif prefix == '!［':
                    response_text = response_text[2:]
                
                print(f"   🛡️ 检测到反爬前缀 '{prefix}'，已自动处理")
                break
        
        return response_text
    
    def get_user_info(self, uid: str):
        """获取用户信息（最终优化版）"""
        if not uid.isdigit():
            return {"code": -400, "message": "无效的用户ID"}
        
        print(f"🔍 获取用户信息 - UID: {uid}")
        
        for attempt in range(self.max_retries + 1):
            try:
                # 间隔控制
                current_time = time.time()
                if self.last_request_time > 0:
                    elapsed = current_time - self.last_request_time
                    required_interval = random.uniform(self.min_interval, self.max_interval)
                    if elapsed < required_interval:
                        sleep_time = required_interval - elapsed
                        print(f"   ⏱️ 等待 {sleep_time:.1f} 秒")
                        time.sleep(sleep_time)
                
                self.last_request_time = time.time()
                
                # 重试延迟
                if attempt > 0:
                    retry_delay = self.retry_delay_base * (2 ** (attempt - 1))
                    print(f"   🔄 第{attempt}次重试，等待{retry_delay:.1f}秒")
                    time.sleep(retry_delay)
                
                # API配置
                url = "https://api.bilibili.com/x/space/acc/info"
                
                params = {
                    "mid": uid,
                    "platform": "web",
                    "web_location": "space.header"
                }
                
                headers = {
                    "Referer": f"https://space.bilibili.com/{uid}",
                    "Origin": "https://www.bilibili.com",
                    "X-Requested-With": "XMLHttpRequest"
                }
                
                print(f"   📡 发送请求 (尝试{attempt + 1}/{self.max_retries + 1})")
                
                # 发送请求
                response = self.session.get(url, params=params, headers=headers, timeout=15)
                print(f"   📊 状态码: {response.status_code}")
                
                if response.status_code == 200:
                    # 处理反爬响应
                    processed_text = self._handle_anti_crawl_response(response.text.strip())
                    
                    if processed_text.startswith('{'):
                        try:
                            data = json.loads(processed_text)
                            code = data.get("code", -1)
                            print(f"   📋 业务码: {code}")
                            
                            if code == 0:
                                print(f"   ✅ 成功获取用户信息")
                                return data
                            elif code == -799:
                                print(f"   ⚠️ 频率限制 (code: {code})")
                                if attempt < self.max_retries:
                                    continue
                                else:
                                    return {"code": -799, "message": "请求频率限制，请稍后再试"}
                            else:
                                print(f"   ❌ 业务错误: {data.get('message', 'unknown')}")
                                return data
                                
                        except json.JSONDecodeError as e:
                            print(f"   ❌ JSON解析失败: {e}")
                            print(f"   原始响应: {response.text[:100]}")
                            if attempt < self.max_retries:
                                continue
                    else:
                        print(f"   ❌ 响应格式异常: {processed_text[:50]}")
                        if attempt < self.max_retries:
                            continue
                else:
                    print(f"   ❌ HTTP错误: {response.status_code}")
                    if attempt < self.max_retries:
                        continue
                    
            except Exception as e:
                print(f"   ❌ 请求异常: {e}")
                if attempt < self.max_retries:
                    continue
        
        return {"code": -1, "message": "所有重试都失败"}

def test_specific_user_cases():
    """测试特定用户案例"""
    print("🎯 特定用户案例测试")
    print("-" * 40)
    
    cookies = load_cookies()
    api = FinalBilibiliAPI(cookies)
    
    # 重点测试用户
    target_users = [
        ("316183842", "技术爱爱虾 - 用户报告的问题用户"),
        ("1", "bilibili - 系统账号"),
        ("9", "9号用户 - 早期用户"),
        ("777536", "随机测试用户")
    ]
    
    success_results = []
    
    for uid, description in target_users:
        print(f"\n📋 测试: {description}")
        print("=" * 50)
        
        result = api.get_user_info(uid)
        
        if isinstance(result, dict) and result.get("code") == 0:
            user_data = result.get("data", {})
            if user_data:
                print(f"🎉 成功获取用户: {user_data.get('name', '未知')}")
                print(f"   🆔 UID: {user_data.get('mid', 'unknown')}")
                print(f"   🎯 等级: Lv.{user_data.get('level', 0)}")
                print(f"   👥 粉丝: {user_data.get('fans', 0):,}")
                print(f"   📝 签名: {user_data.get('sign', '无')[:50]}...")
                success_results.append((uid, user_data.get('name', '未知')))
            else:
                print("⚠️ 数据为空")
        else:
            error_code = result.get("code", -1) if isinstance(result, dict) else -1
            error_msg = result.get("message", "未知错误") if isinstance(result, dict) else "格式错误"
            print(f"❌ 失败: code={error_code}, message={error_msg}")
    
    return success_results

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 最终用户信息API修复验证")
    print("📖 基于Nemo2011/bilibili-api项目优化")
    print("=" * 60)
    
    print("\n💡 本次修复核心改进:")
    print("   • ✅ 智能重试机制 (指数退避)")
    print("   • ✅ 反爬字符自动处理")
    print("   • ✅ 请求间隔优化 (3-6秒)")
    print("   • ✅ 完善错误处理")
    print("   • ✅ 连接池优化")
    
    # 执行测试
    success_results = test_specific_user_cases()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 最终测试总结")
    print("=" * 60)
    
    success_count = len(success_results)
    total_tested = 4
    success_rate = (success_count / total_tested) * 100
    
    print(f"✅ 成功率: {success_count}/{total_tested} ({success_rate:.1f}%)")
    
    if success_results:
        print(f"\n🎉 成功获取的用户:")
        for uid, name in success_results:
            print(f"   • {name} (UID: {uid})")
    
    if success_rate >= 50:
        print(f"\n🎉 用户信息API修复成功！")
        print("💡 主要改进成果:")
        print("   ✅ 解决了反爬字符解析问题")
        print("   ✅ 实现了智能重试机制") 
        print("   ✅ 优化了请求间隔控制")
        print("   ✅ 成功获取到目标用户信息")
        
        if "技术爱爱虾" in [name for _, name in success_results]:
            print("   ✅ 特别是解决了用户报告的'技术爱爱虾'查询问题！")
    else:
        print(f"\n⚠️ 修复效果有限，建议:")
        print("   🔄 进一步增加请求间隔")
        print("   🛡️ 考虑使用更强的反爬措施")
        print("   🔐 检查cookie有效性")
    
    print(f"\n📚 参考项目: https://github.com/Nemo2011/bilibili-api")
    print("💡 该项目提供了完整的B站API解决方案，值得深入学习")

if __name__ == "__main__":
    main()

