#!/usr/bin/env python3
"""
测试基于Nemo2011/bilibili-api项目的修复效果
"""

import json
import time
import random
import hashlib
import urllib.parse
from typing import Dict, Optional
import requests

class NemoInspiredBilibiliAPI:
    """基于Nemo2011/bilibili-api项目改进的API类"""
    
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        # 请求头配置
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
        
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        
        # 基于Nemo项目的配置
        self.min_interval = 2.0  # 增加间隔
        self.max_interval = 5.0
        self.max_retries = 3
        self.retry_delay_base = 2
        self.last_request_time = 0
        self.request_success_count = 0
        self.request_total_count = 0
        
        if cookies:
            self.session.cookies.update(cookies)
            print(f"✅ 设置了 {len(cookies)} 个cookie")
        
        # 改进连接池配置
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=20,
            pool_maxsize=50,
            max_retries=0  # 禁用自动重试，使用自定义重试
        )
        self.session.mount('https://', adapter)
    
    def _parse_response(self, response):
        """解析响应（处理B站反爬字符）"""
        try:
            response_text = response.text.strip()
            
            # 处理B站可能的反爬前缀
            if response_text.startswith('!'):
                response_text = response_text[1:]
                print("   🛡️ 检测到反爬字符，已自动处理")
            
            if response_text.startswith('{'):
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError as e:
                    print(f"   ❌ JSON解析失败: {e}")
                    return None
            else:
                print(f"   ❌ 响应不是JSON格式")
                return None
                
        except Exception as e:
            print(f"   ❌ 响应解析异常: {e}")
            return None
    
    def _make_request_with_retry(self, url: str, params: Dict, headers: Dict):
        """智能重试请求（参考Nemo项目）"""
        self.request_total_count += 1
        
        for attempt in range(self.max_retries + 1):
            try:
                # 请求间隔控制
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
                    retry_delay = self.retry_delay_base * (2 ** (attempt - 1)) + random.uniform(0, 1)
                    print(f"   🔄 第{attempt}次重试，等待{retry_delay:.1f}秒")
                    time.sleep(retry_delay)
                
                print(f"   📡 发送请求 (尝试{attempt + 1}/{self.max_retries + 1})")
                
                # 发送请求
                response = self.session.get(url, params=params, headers=headers, timeout=15)
                print(f"   📊 状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = self._parse_response(response)
                    if data:
                        code = data.get("code", -1)
                        print(f"   📋 业务码: {code}")
                        
                        if code == 0:
                            self.request_success_count += 1
                            success_rate = (self.request_success_count / self.request_total_count) * 100
                            print(f"   ✅ 请求成功 (成功率: {success_rate:.1f}%)")
                            return data
                        elif code == -799:
                            print(f"   ⚠️ 频率限制，重试中...")
                            if attempt < self.max_retries:
                                continue
                            else:
                                return {"code": -799, "message": "请求频率过快，请稍后再试"}
                        else:
                            print(f"   ❌ 业务错误: {data.get('message', 'unknown')}")
                            return data
                    else:
                        print(f"   ❌ 响应解析失败")
                        if attempt < self.max_retries:
                            continue
                else:
                    print(f"   ❌ HTTP错误: {response.status_code}")
                    if attempt < self.max_retries and response.status_code in [412, 429]:
                        continue
                    else:
                        return {"code": -1, "message": f"HTTP错误: {response.status_code}"}
                        
            except Exception as e:
                print(f"   ❌ 请求异常: {e}")
                if attempt < self.max_retries:
                    continue
                else:
                    return {"code": -1, "message": f"请求异常: {str(e)}"}
        
        return {"code": -1, "message": "所有重试都失败"}
    
    def get_user_info(self, uid: str):
        """获取用户信息（Nemo风格实现）"""
        if not uid.isdigit():
            return {"code": -400, "message": "无效的用户ID"}
        
        url = "https://api.bilibili.com/x/space/acc/info"
        
        # 参数配置（基于bilibili-API-collect文档）
        params = {
            "mid": uid,
            "platform": "web",
            "web_location": "space.header"
        }
        
        # 请求头（基于真实浏览器）
        headers = {
            "Referer": f"https://space.bilibili.com/{uid}",
            "Origin": "https://www.bilibili.com",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        return self._make_request_with_retry(url, params, headers)

def load_cookies():
    """加载cookie配置"""
    try:
        with open('cookie_example.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 无法加载cookie: {e}")
        return {}

def test_nemo_inspired_implementation():
    """测试基于Nemo项目的改进实现"""
    print("🚀 测试基于Nemo2011/bilibili-api的改进实现")
    print("=" * 60)
    
    # 创建API实例
    cookies = load_cookies()
    api = NemoInspiredBilibiliAPI(cookies)
    
    # 测试用户
    test_users = [
        ("316183842", "技术爱爱虾"),
        ("1", "bilibili官方"),
        ("12345", "测试用户")
    ]
    
    results = []
    
    for uid, name in test_users:
        print(f"\n📋 测试用户: {name} (UID: {uid})")
        print("-" * 40)
        
        result = api.get_user_info(uid)
        
        if isinstance(result, dict):
            code = result.get("code", -1)
            if code == 0:
                user_data = result.get("data", {})
                if user_data:
                    print(f"🎉 成功获取用户信息:")
                    print(f"   👤 用户名: {user_data.get('name', '未知')}")
                    print(f"   🆔 UID: {user_data.get('mid', 'unknown')}")
                    print(f"   🎯 等级: Lv.{user_data.get('level', 0)}")
                    print(f"   👥 粉丝: {user_data.get('fans', 0):,}")
                    results.append("success")
                else:
                    print("⚠️ 数据为空")
                    results.append("empty")
            elif code == -799:
                print("⚠️ 频率限制")
                results.append("rate_limit")
            elif code == -403:
                print("❌ 权限不足")
                results.append("permission")
            elif code == -404:
                print("❌ 用户不存在")
                results.append("not_found")
            else:
                print(f"❌ 其他错误: {code}")
                results.append("error")
        else:
            print("❌ 返回格式异常")
            results.append("format_error")
    
    return results

def compare_implementations():
    """对比实现效果"""
    print(f"\n" + "=" * 60)
    print("📊 实现效果对比")
    print("=" * 60)
    
    print("🔧 基于Nemo2011/bilibili-api的关键改进:")
    print("   ✅ 智能重试机制 (指数退避)")
    print("   ✅ 反爬字符自动处理 (感叹号前缀)")
    print("   ✅ 请求间隔优化 (2-5秒)")
    print("   ✅ 连接池优化 (20/50连接)")
    print("   ✅ 请求成功率统计")
    print("   ✅ 完善的错误处理")
    
    print(f"\n🎯 Nemo项目核心优势:")
    print("   • 🔄 全异步操作提升性能")
    print("   • 🛡️ curl_cffi库TLS指纹伪装")
    print("   • 🔐 Credential类统一认证管理")
    print("   • 📊 完整的状态码处理")
    print("   • 🌐 代理和反爬虫策略")
    print("   • 🔄 自动cookie刷新")

def main():
    """主函数"""
    print("🔧 基于Nemo2011/bilibili-api的用户信息API修复")
    print("📖 参考项目: https://github.com/Nemo2011/bilibili-api")
    print()
    
    # 测试改进后的实现
    results = test_nemo_inspired_implementation()
    
    # 统计结果
    success_count = results.count("success")
    total_count = len(results)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"\n" + "=" * 60)
    print("📊 测试结果统计")
    print("=" * 60)
    print(f"✅ 成功率: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    # 分析结果
    if success_rate >= 80:
        print("🎉 修复效果优秀！")
        print("💡 建议继续使用基于Nemo项目的优化版本")
    elif success_rate >= 60:
        print("👍 修复效果良好！")
        print("💡 建议完善cookie配置和请求策略")
    elif success_rate >= 40:
        print("⚠️ 修复有一定效果")
        print("💡 建议进一步优化反爬策略")
    else:
        print("❌ 修复效果有限")
        print("💡 建议考虑使用Nemo项目的完整解决方案")
    
    # 对比分析
    compare_implementations()
    
    print(f"\n🎯 下一步建议:")
    if success_rate < 80:
        print("1. 🔄 考虑迁移到异步实现")
        print("2. 🛡️ 集成curl_cffi库")
        print("3. 🔐 实现Credential类管理")
        print("4. 🌐 添加代理支持")
    else:
        print("1. ✅ 当前实现效果良好")
        print("2. 📊 继续监控成功率")
        print("3. 🔄 考虑长期迁移到Nemo架构")

if __name__ == "__main__":
    main()

