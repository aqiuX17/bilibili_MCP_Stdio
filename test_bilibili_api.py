#!/usr/bin/env python3
"""
B站API直接测试脚本
直接测试API接口的可用性，不依赖MCP服务器
"""

import json
import time
import requests
from datetime import datetime
import random
import hashlib
import urllib.parse

class SimpleBilibiliAPI:
    """简化的B站API测试类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "Referer": "https://www.bilibili.com/",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        })
        
        self.test_results = []
        
    def test_api(self, name: str, url: str, params: dict = None) -> dict:
        """测试单个API"""
        print(f"\n🔍 测试: {name}")
        print(f"   URL: {url}")
        
        try:
            start_time = time.time()
            response = self.session.get(url, params=params, timeout=10)
            elapsed = time.time() - start_time
            
            # 尝试解析JSON
            try:
                data = response.json()
                
                # 判断成功状态
                if isinstance(data, dict):
                    code = data.get("code", -1)
                    message = data.get("message", "")
                    
                    if code == 0:
                        status = "✅ 成功"
                        print(f"   ✅ 成功 (code=0, 耗时={elapsed:.2f}秒)")
                        if "data" in data:
                            # 统计数据量
                            if isinstance(data["data"], dict):
                                print(f"   📊 返回数据: {len(data['data'])}个字段")
                            elif isinstance(data["data"], list):
                                print(f"   📊 返回数据: {len(data['data'])}条记录")
                    elif code == -799:
                        status = "⚠️ 频率限制"
                        print(f"   ⚠️ 频率限制 (code=-799)")
                    elif code in [-400, -403, -404]:
                        status = "❌ 访问受限"
                        print(f"   ❌ 访问受限 (code={code}, message={message})")
                    else:
                        status = "❌ 失败"
                        print(f"   ❌ 失败 (code={code}, message={message})")
                else:
                    status = "⚠️ 格式异常"
                    print(f"   ⚠️ 返回格式异常")
                    
            except json.JSONDecodeError:
                status = "❌ 非JSON响应"
                print(f"   ❌ 返回非JSON格式 (可能是HTML)")
                data = {"html": response.text[:200]}
                
            result = {
                "name": name,
                "url": url,
                "status": status,
                "elapsed": round(elapsed, 2),
                "status_code": response.status_code,
                "response": data
            }
            
        except requests.RequestException as e:
            status = "❌ 请求失败"
            print(f"   ❌ 请求失败: {e}")
            result = {
                "name": name,
                "url": url,
                "status": status,
                "elapsed": 0,
                "error": str(e)
            }
        
        self.test_results.append(result)
        time.sleep(2)  # 请求间隔
        return result
    
    def run_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("🚀 B站API接口测试")
        print("=" * 60)
        
        # 测试视频信息API
        print("\n📹 视频相关API测试")
        print("-" * 40)
        
        # 测试视频详情
        self.test_api(
            "视频详情API",
            "https://api.bilibili.com/x/web-interface/view",
            {"bvid": "BV1xx411c7mD"}
        )
        
        # 测试视频标签
        self.test_api(
            "视频标签API",
            "https://api.bilibili.com/x/web-interface/view/detail/tag",
            {"bvid": "BV1xx411c7mD"}
        )
        
        # 测试视频分P
        self.test_api(
            "视频分P列表API",
            "https://api.bilibili.com/x/player/pagelist",
            {"bvid": "BV1xx411c7mD"}
        )
        
        # 测试相关推荐
        self.test_api(
            "相关推荐API",
            "https://api.bilibili.com/x/web-interface/archive/related",
            {"bvid": "BV1xx411c7mD"}
        )
        
        # 测试用户信息API
        print("\n👤 用户相关API测试")
        print("-" * 40)
        
        # 用户基本信息（需要WBI签名的版本）
        self.test_api(
            "用户信息API (需WBI签名)",
            "https://api.bilibili.com/x/space/wbi/acc/info",
            {"mid": "36081646"}
        )
        
        # 用户卡片信息（不需要WBI）
        self.test_api(
            "用户卡片API",
            "https://api.bilibili.com/x/web-interface/card",
            {"mid": "36081646"}
        )
        
        # 用户视频列表（需要WBI签名）
        self.test_api(
            "用户视频列表API",
            "https://api.bilibili.com/x/space/wbi/arc/search",
            {"mid": "36081646", "ps": 5, "pn": 1}
        )
        
        # 测试搜索API
        print("\n🔍 搜索相关API测试")
        print("-" * 40)
        
        # 搜索建议
        self.test_api(
            "搜索建议API",
            "https://s.search.bilibili.com/main/suggest",
            {"term": "编程", "func": "suggest", "suggest_type": "accurate"}
        )
        
        # 搜索视频（需要WBI）
        self.test_api(
            "搜索视频API",
            "https://api.bilibili.com/x/web-interface/search/type",
            {"search_type": "video", "keyword": "Python教程", "page": 1}
        )
        
        # 测试热门视频API
        print("\n🔥 热门内容API测试")
        print("-" * 40)
        
        # 热门推荐
        self.test_api(
            "热门推荐API",
            "https://api.bilibili.com/x/web-interface/popular",
            {"ps": 5, "pn": 1}
        )
        
        # 排行榜
        self.test_api(
            "排行榜API",
            "https://api.bilibili.com/x/web-interface/ranking/v2",
            {"rid": 0, "type": "all"}
        )
        
        # 入站必刷
        self.test_api(
            "入站必刷API",
            "https://api.bilibili.com/x/web-interface/popular/precious",
            {"ps": 5, "pn": 1}
        )
        
        # 测试评论API
        print("\n💬 评论相关API测试")
        print("-" * 40)
        
        # 视频评论
        self.test_api(
            "视频评论API",
            "https://api.bilibili.com/x/v2/reply",
            {"pn": 1, "type": 1, "oid": "170001", "sort": 2}
        )
        
        # 测试直播API
        print("\n📺 直播相关API测试")
        print("-" * 40)
        
        # 直播间信息
        self.test_api(
            "直播间信息API",
            "https://api.live.bilibili.com/room/v1/Room/get_info",
            {"room_id": "22"}
        )
        
        # 直播分区列表
        self.test_api(
            "直播分区列表API",
            "https://api.live.bilibili.com/room/v1/Area/getList",
            {}
        )
        
        # 测试导航API（获取WBI密钥）
        print("\n🔑 系统相关API测试")
        print("-" * 40)
        
        # 导航信息
        self.test_api(
            "导航信息API (含WBI密钥)",
            "https://api.bilibili.com/x/web-interface/nav",
            {}
        )
        
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告汇总")
        print("=" * 60)
        
        # 统计结果
        total = len(self.test_results)
        success = sum(1 for r in self.test_results if "成功" in r["status"])
        partial = sum(1 for r in self.test_results if "频率限制" in r["status"] or "格式异常" in r["status"])
        failed = sum(1 for r in self.test_results if "失败" in r["status"] or "受限" in r["status"] or "非JSON" in r["status"])
        
        print(f"\n📈 测试统计:")
        print(f"   总测试数: {total}")
        print(f"   ✅ 成功: {success}")
        print(f"   ⚠️ 部分可用: {partial}")
        print(f"   ❌ 失败: {failed}")
        
        if total > 0:
            success_rate = (success / total) * 100
            available_rate = ((success + partial) / total) * 100
            print(f"   📊 成功率: {success_rate:.1f}%")
            print(f"   📊 可用率: {available_rate:.1f}%")
        
        # 按状态分组显示
        print("\n📋 详细结果:")
        print("-" * 40)
        
        # 成功的API
        success_apis = [r for r in self.test_results if "成功" in r["status"]]
        if success_apis:
            print("\n✅ 可正常访问的API:")
            for api in success_apis:
                print(f"   • {api['name']} ({api['elapsed']}秒)")
        
        # 部分可用的API
        partial_apis = [r for r in self.test_results if "频率限制" in r["status"] or "格式异常" in r["status"]]
        if partial_apis:
            print("\n⚠️ 部分可用的API:")
            for api in partial_apis:
                print(f"   • {api['name']} - {api['status']}")
        
        # 失败的API
        failed_apis = [r for r in self.test_results if "失败" in r["status"] or "受限" in r["status"] or "非JSON" in r["status"]]
        if failed_apis:
            print("\n❌ 访问失败的API:")
            for api in failed_apis:
                print(f"   • {api['name']} - {api['status']}")
        
        # 分析和建议
        print("\n" + "=" * 60)
        print("💡 分析与建议")
        print("=" * 60)
        
        print("\n📌 当前状态分析:")
        
        if success_rate < 30:
            print("   • 大部分API需要认证或遇到反爬限制")
            print("   • 这是B站API的正常保护机制")
        elif success_rate < 60:
            print("   • 部分核心API可以访问")
            print("   • 某些功能受限但基本可用")
        else:
            print("   • 大部分API运行正常")
            print("   • 系统状态良好")
        
        print("\n🔧 优化建议:")
        print("   1. 配置Cookie认证:")
        print("      • 获取SESSDATA、bili_jct等关键cookie")
        print("      • 使用cookie_example.json配置文件")
        print("      • 通过set_bilibili_cookies工具设置")
        
        print("\n   2. 使用WBI签名:")
        print("      • 部分API需要WBI签名才能访问")
        print("      • 系统已实现自动WBI签名功能")
        print("      • 需要有效的cookie才能获取WBI密钥")
        
        print("\n   3. 控制请求频率:")
        print("      • 已设置2秒请求间隔")
        print("      • 可根据需要调整间隔时间")
        
        print("\n   4. 使用备用API:")
        print("      • 搜索功能可用热门视频替代")
        print("      • 用户信息可用卡片API替代")
        
        # 功能可用性总结
        print("\n" + "=" * 60)
        print("🎯 核心功能可用性评估")
        print("=" * 60)
        
        # 评估各项功能
        features = {
            "视频信息获取": any("视频详情" in r["name"] and "成功" in r["status"] for r in self.test_results),
            "用户信息查询": any("用户" in r["name"] and ("成功" in r["status"] or "部分" in r["status"]) for r in self.test_results),
            "热门内容浏览": any("热门" in r["name"] and "成功" in r["status"] for r in self.test_results),
            "搜索功能": any("搜索" in r["name"] and ("成功" in r["status"] or "部分" in r["status"]) for r in self.test_results),
            "评论查看": any("评论" in r["name"] and ("成功" in r["status"] or "部分" in r["status"]) for r in self.test_results),
            "直播功能": any("直播" in r["name"] and "成功" in r["status"] for r in self.test_results),
        }
        
        for feature, available in features.items():
            status = "✅ 可用" if available else "❌ 需要认证"
            print(f"   • {feature}: {status}")
        
        # 最终结论
        print("\n" + "=" * 60)
        print("📝 测试结论")
        print("=" * 60)
        
        available_features = sum(1 for v in features.values() if v)
        total_features = len(features)
        
        if available_features >= 4:
            print("\n✅ 系统基本功能正常，大部分接口可用!")
            print("   建议配置cookie以获得完整功能")
        elif available_features >= 2:
            print("\n⚠️ 部分功能可用，但受限较多")
            print("   强烈建议配置cookie提升可用性")
        else:
            print("\n❌ 大部分功能受限")
            print("   必须配置cookie才能正常使用")
        
        # 保存详细结果到文件
        report_file = f"api_test_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细测试结果已保存到: {report_file}")

def main():
    """主函数"""
    print("\n🚀 开始B站API接口测试...")
    print("📌 本测试将直接访问B站API，检查接口可用性")
    print("⏱️ 预计耗时: 1-2分钟\n")
    
    tester = SimpleBilibiliAPI()
    
    # 运行测试
    tester.run_tests()
    
    # 生成报告
    tester.generate_report()
    
    print("\n✅ 测试完成!")

if __name__ == "__main__":
    main()