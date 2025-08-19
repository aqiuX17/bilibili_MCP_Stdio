#!/usr/bin/env python3
"""
B站MCP服务器API独立测试脚本
直接调用main.py中的函数进行测试
"""

import json
import time
import traceback
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 动态导入main模块
import importlib.util
spec = importlib.util.spec_from_file_location("main", "main.py")
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

# 获取需要的对象
bili_api = main.bili_api
BilibiliAPI = main.BilibiliAPI
logger = main.logger

class APITester:
    """API测试器类"""
    
    def __init__(self):
        self.results = []
        self.success_count = 0
        self.failed_count = 0
        self.partial_count = 0
        self.start_time = datetime.now()
        
        # 测试用例参数 - 使用更常见的测试数据
        self.test_bvid = "BV1xx411c7mD"  # 一个经典视频
        self.test_uid = "36081646"       # 一个活跃UP主
        self.test_keyword = "编程"       # 搜索关键词
        self.test_room_id = "22"         # 直播间ID
        
    def test_api(self, name: str, func, *args, **kwargs) -> Tuple[str, Dict]:
        """测试单个API接口"""
        print(f"\n🔍 测试 {name}...")
        
        try:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            # 解析结果
            if isinstance(result, str):
                try:
                    result_data = json.loads(result)
                except:
                    result_data = {"raw_response": result}
            elif isinstance(result, dict):
                result_data = result
            else:
                result_data = {"raw_response": str(result)}
            
            # 判断成功状态
            status = self._determine_status(result_data)
            
            # 记录结果
            test_result = {
                "name": name,
                "status": status,
                "elapsed": round(elapsed, 2),
                "response": self._summarize_response(result_data)
            }
            
            self.results.append(test_result)
            
            if status == "✅ 成功":
                self.success_count += 1
                print(f"  ✅ 成功 (耗时: {elapsed:.2f}秒)")
            elif status == "⚠️ 部分可用":
                self.partial_count += 1
                print(f"  ⚠️ 部分可用 (耗时: {elapsed:.2f}秒)")
            else:
                self.failed_count += 1
                print(f"  ❌ 失败 (耗时: {elapsed:.2f}秒)")
                
            return status, result_data
            
        except Exception as e:
            elapsed = 0
            error_msg = str(e)
            print(f"  ❌ 异常: {error_msg}")
            
            test_result = {
                "name": name,
                "status": "❌ 异常",
                "elapsed": 0,
                "response": {"error": error_msg}
            }
            
            self.results.append(test_result)
            self.failed_count += 1
            
            return "❌ 异常", {"error": error_msg}
    
    def _determine_status(self, response: Dict) -> str:
        """判断API响应状态"""
        # 检查是否有错误标记
        if "error" in response:
            return "❌ 失败"
        
        # 检查code字段
        if "code" in response:
            code = response.get("code")
            if code == 0:
                # 检查数据是否有效
                if "data" in response and response["data"]:
                    return "✅ 成功"
                else:
                    return "⚠️ 部分可用"
            elif code == -799:
                return "⚠️ 部分可用"  # 频率限制
            else:
                return "❌ 失败"
        
        # 检查是否有数据
        if "data" in response:
            return "✅ 成功"
        
        # 检查是否是字符串响应
        if "raw_response" in response:
            if "成功" in str(response["raw_response"]) or "✅" in str(response["raw_response"]):
                return "✅ 成功"
        
        # 默认为部分可用
        return "⚠️ 部分可用"
    
    def _summarize_response(self, response: Dict) -> Dict:
        """生成响应摘要"""
        summary = {}
        
        if "code" in response:
            summary["code"] = response["code"]
        
        if "message" in response:
            summary["message"] = response["message"][:100]
        
        if "data" in response:
            data = response["data"]
            if isinstance(data, dict):
                summary["data_keys"] = list(data.keys())[:5]
                # 统计数据量
                for key in ["list", "users", "replies", "items"]:
                    if key in data and isinstance(data[key], list):
                        summary[f"{key}_count"] = len(data[key])
            elif isinstance(data, list):
                summary["data_count"] = len(data)
            else:
                summary["data_type"] = type(data).__name__
        
        if "error" in response:
            summary["error"] = str(response["error"])[:200]
            
        return summary
    
    def run_core_tests(self):
        """运行核心功能测试（精简版）"""
        print("=" * 60)
        print("🚀 B站MCP服务器核心API测试")
        print("=" * 60)
        
        # 1. 基础功能测试
        print("\n📦 基础功能测试")
        print("-" * 40)
        
        # 测试连接
        self.test_api("test_connection - 测试连接", main.test_connection)
        time.sleep(1)
        
        # 获取cookie状态
        self.test_api("get_cookie_status - Cookie状态", main.get_cookie_status)
        time.sleep(1)
        
        # 2. 视频相关接口测试（核心）
        print("\n🎬 视频相关接口测试")
        print("-" * 40)
        
        # 获取视频信息 - 最重要的API
        self.test_api(
            "get_video_info - 获取视频信息",
            main.get_video_info,
            self.test_bvid,
            True
        )
        time.sleep(2)
        
        # 获取视频评论
        self.test_api(
            "get_video_comments - 获取视频评论",
            main.get_video_comments,
            self.test_bvid,
            1,    # page
            3,    # limit
            True, # simple
            "hot" # sort_type
        )
        time.sleep(2)
        
        # 3. 用户相关接口测试（核心）
        print("\n👤 用户相关接口测试")
        print("-" * 40)
        
        # 获取用户信息
        self.test_api(
            "get_user_info - 获取用户信息",
            main.get_user_info,
            self.test_uid,
            True
        )
        time.sleep(2)
        
        # 搜索用户
        self.test_api(
            "search_user_by_nickname - 搜索用户",
            main.search_user_by_nickname,
            "科技",
            3,
            True
        )
        time.sleep(3)
        
        # 4. 搜索功能测试
        print("\n🔍 搜索功能测试")
        print("-" * 40)
        
        # 搜索视频
        self.test_api(
            "search_bilibili_videos - 搜索视频",
            main.search_bilibili_videos,
            self.test_keyword,
            1,
            "totalrank",
            3,
            True
        )
        time.sleep(3)
        
        # 5. 热门内容测试
        print("\n🔥 热门内容测试")
        print("-" * 40)
        
        # 获取热门视频
        self.test_api(
            "get_trending_videos - 获取热门视频",
            main.get_trending_videos,
            0,    # rid
            3,    # day
            3,    # limit
            True  # simple
        )
        time.sleep(2)
        
        # 6. 工具函数测试
        print("\n🛠️ 工具函数测试")
        print("-" * 40)
        
        # 从URL提取UID
        self.test_api(
            "extract_uid_from_bilibili_url - 提取UID",
            main.extract_uid_from_bilibili_url,
            "https://space.bilibili.com/36081646"
        )
        time.sleep(1)
        
        # 从URL提取BV号
        self.test_api(
            "extract_bvid_from_url - 提取BV号",
            main.extract_bvid_from_url,
            f"https://www.bilibili.com/video/{self.test_bvid}"
        )
        time.sleep(1)
        
        # API成功率统计
        self.test_api("get_api_success_rate - API统计", main.get_api_success_rate)
        
    def generate_report(self) -> str:
        """生成测试报告"""
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        
        report = []
        report.append("=" * 60)
        report.append("📊 B站MCP服务器API测试报告")
        report.append("=" * 60)
        report.append(f"\n📅 测试时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"⏱️ 总耗时: {elapsed_time:.2f}秒")
        report.append(f"📈 测试总数: {len(self.results)}")
        report.append(f"✅ 成功: {self.success_count}")
        report.append(f"⚠️ 部分可用: {self.partial_count}")
        report.append(f"❌ 失败: {self.failed_count}")
        
        # 计算成功率
        total = len(self.results)
        if total > 0:
            success_rate = (self.success_count / total) * 100
            partial_rate = ((self.success_count + self.partial_count) / total) * 100
            report.append(f"📊 完全成功率: {success_rate:.1f}%")
            report.append(f"📊 可用率(含部分): {partial_rate:.1f}%")
        
        # 详细结果
        report.append("\n" + "=" * 60)
        report.append("📋 详细测试结果")
        report.append("=" * 60)
        
        # 按状态分组
        success_apis = []
        partial_apis = []
        failed_apis = []
        
        for result in self.results:
            if result["status"] == "✅ 成功":
                success_apis.append(result)
            elif result["status"] == "⚠️ 部分可用":
                partial_apis.append(result)
            else:
                failed_apis.append(result)
        
        # 成功的API
        if success_apis:
            report.append("\n✅ 完全可用的API接口:")
            report.append("-" * 40)
            for api in success_apis:
                report.append(f"  • {api['name']} ({api['elapsed']}秒)")
        
        # 部分可用的API
        if partial_apis:
            report.append("\n⚠️ 部分可用的API接口:")
            report.append("-" * 40)
            for api in partial_apis:
                report.append(f"  • {api['name']} ({api['elapsed']}秒)")
                if "message" in api['response']:
                    report.append(f"    原因: {api['response']['message']}")
        
        # 失败的API
        if failed_apis:
            report.append("\n❌ 不可用的API接口:")
            report.append("-" * 40)
            for api in failed_apis:
                report.append(f"  • {api['name']}")
                if "error" in api['response']:
                    report.append(f"    错误: {api['response']['error'][:100]}")
        
        # 建议
        report.append("\n" + "=" * 60)
        report.append("💡 优化建议")
        report.append("=" * 60)
        
        if self.failed_count > 0 or self.partial_count > 0:
            report.append("\n📌 API访问受限，主要原因:")
            report.append("  • B站反爬虫机制导致部分API需要cookie认证")
            report.append("  • 某些API有频率限制")
            report.append("  • 部分接口需要特定的请求头和参数")
        
        report.append("\n🔧 提升成功率的方法:")
        report.append("  1. 配置有效的SESSDATA cookie:")
        report.append("     - 从浏览器开发者工具获取cookie")
        report.append("     - 使用set_bilibili_cookies工具设置")
        report.append("     - 参考cookie_example.json配置文件")
        report.append("  2. 增加请求间隔:")
        report.append("     - 默认已设置2-5秒随机间隔")
        report.append("     - 可适当增加间隔时间")
        report.append("  3. 使用WBI签名:")
        report.append("     - 已自动为部分API生成WBI签名")
        report.append("     - 确保cookie中包含bili_jct")
        
        if success_rate >= 70:
            report.append("\n🎉 大部分核心API可正常使用!")
        elif success_rate >= 40:
            report.append("\n⚠️ 部分核心API可用，建议添加cookie提升成功率")
        else:
            report.append("\n❌ 多数API不可用，强烈建议配置完整cookie")
        
        # API可用性总结
        report.append("\n" + "=" * 60)
        report.append("📱 核心功能可用性总结")
        report.append("=" * 60)
        
        # 检查核心功能
        core_features = {
            "视频信息获取": False,
            "用户信息查询": False,
            "热门视频浏览": False,
            "搜索功能": False,
            "评论获取": False
        }
        
        for result in self.results:
            if "get_video_info" in result["name"] and result["status"] in ["✅ 成功", "⚠️ 部分可用"]:
                core_features["视频信息获取"] = True
            if "get_user_info" in result["name"] and result["status"] in ["✅ 成功", "⚠️ 部分可用"]:
                core_features["用户信息查询"] = True
            if "trending" in result["name"] and result["status"] in ["✅ 成功", "⚠️ 部分可用"]:
                core_features["热门视频浏览"] = True
            if "search" in result["name"] and result["status"] in ["✅ 成功", "⚠️ 部分可用"]:
                core_features["搜索功能"] = True
            if "comments" in result["name"] and result["status"] in ["✅ 成功", "⚠️ 部分可用"]:
                core_features["评论获取"] = True
        
        for feature, available in core_features.items():
            status = "✅ 可用" if available else "❌ 不可用"
            report.append(f"  • {feature}: {status}")
        
        return "\n".join(report)

def main():
    """主测试函数"""
    print("\n🚀 开始B站MCP服务器核心API测试...\n")
    print("📌 本测试将验证核心功能的可用性\n")
    
    # 创建测试器
    tester = APITester()
    
    try:
        # 运行核心测试
        tester.run_core_tests()
        
        # 生成报告
        report = tester.generate_report()
        
        # 打印报告
        print("\n" + report)
        
        # 保存报告到文件
        report_file = f"api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 测试报告已保存到: {report_file}")
        
        # 返回总体状态
        if tester.failed_count == 0:
            print("\n✅ 所有核心API测试通过!")
            return 0
        elif tester.failed_count < len(tester.results) / 2:
            print("\n⚠️ 部分API测试失败，但核心功能基本可用")
            return 1
        else:
            print("\n❌ 大量API测试失败，建议配置cookie后再试")
            return 2
            
    except Exception as e:
        print(f"\n❌ 测试过程出现异常: {e}")
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)