#!/usr/bin/env python3
"""
B站MCP服务器API综合测试脚本
测试所有主要接口的可用性和准确性
"""

import json
import time
import traceback
from datetime import datetime
from typing import Dict, List, Tuple, Any
from main import bili_api, BilibiliAPI, logger
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class APITester:
    """API测试器类"""
    
    def __init__(self):
        self.results = []
        self.success_count = 0
        self.failed_count = 0
        self.partial_count = 0
        self.start_time = datetime.now()
        
        # 测试用例参数
        self.test_bvid = "BV1GJ411x7h7"  # 一个存在的视频
        self.test_uid = "316183842"      # B站官方账号
        self.test_keyword = "科技"       # 搜索关键词
        self.test_room_id = "1"          # 直播间ID
        
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
                "response": {"error": error_msg, "traceback": traceback.format_exc()}
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
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("🚀 B站MCP服务器API综合测试")
        print("=" * 60)
        
        # 1. 基础功能测试
        print("\n📦 基础功能测试")
        print("-" * 40)
        
        # 测试连接
        from main import test_connection
        self.test_api("test_connection - 测试连接", test_connection)
        time.sleep(1)
        
        # 获取cookie状态
        from main import get_cookie_status
        self.test_api("get_cookie_status - Cookie状态", get_cookie_status)
        time.sleep(1)
        
        # 获取API成功率
        from main import get_api_success_rate
        self.test_api("get_api_success_rate - API统计", get_api_success_rate)
        time.sleep(1)
        
        # 2. 视频相关接口测试
        print("\n🎬 视频相关接口测试")
        print("-" * 40)
        
        # 获取视频信息
        from main import get_video_info
        self.test_api(
            "get_video_info - 获取视频信息",
            get_video_info,
            self.test_bvid,
            True
        )
        time.sleep(2)
        
        # 获取视频标签
        from main import get_video_tags
        self.test_api(
            "get_video_tags - 获取视频标签",
            get_video_tags,
            self.test_bvid
        )
        time.sleep(2)
        
        # 获取视频分P
        from main import get_video_pages
        self.test_api(
            "get_video_pages - 获取视频分P",
            get_video_pages,
            self.test_bvid
        )
        time.sleep(2)
        
        # 获取相关推荐
        from main import get_video_related
        self.test_api(
            "get_video_related - 获取相关推荐",
            get_video_related,
            self.test_bvid
        )
        time.sleep(2)
        
        # 获取视频评论
        from main import get_video_comments
        self.test_api(
            "get_video_comments - 获取视频评论",
            get_video_comments,
            self.test_bvid,
            1,    # page
            5,    # limit
            True, # simple
            "hot" # sort_type
        )
        time.sleep(2)
        
        # 3. 用户相关接口测试
        print("\n👤 用户相关接口测试")
        print("-" * 40)
        
        # 获取用户信息
        from main import get_user_info
        self.test_api(
            "get_user_info - 获取用户信息",
            get_user_info,
            self.test_uid,
            True
        )
        time.sleep(2)
        
        # 搜索用户
        from main import search_user_by_nickname
        self.test_api(
            "search_user_by_nickname - 搜索用户",
            search_user_by_nickname,
            "哔哩哔哩",
            5,
            True
        )
        time.sleep(3)
        
        # 获取用户动态
        from main import get_user_dynamics
        self.test_api(
            "get_user_dynamics - 获取用户动态",
            get_user_dynamics,
            self.test_uid,
            1
        )
        time.sleep(2)
        
        # 获取用户视频
        from main import get_user_videos
        self.test_api(
            "get_user_videos - 获取用户视频",
            get_user_videos,
            self.test_uid,
            1,
            10
        )
        time.sleep(2)
        
        # 获取用户粉丝
        from main import get_user_followers
        self.test_api(
            "get_user_followers - 获取用户粉丝",
            get_user_followers,
            self.test_uid,
            1,
            5
        )
        time.sleep(2)
        
        # 获取用户关注
        from main import get_user_following
        self.test_api(
            "get_user_following - 获取用户关注",
            get_user_following,
            self.test_uid,
            1,
            5
        )
        time.sleep(2)
        
        # 4. 搜索功能测试
        print("\n🔍 搜索功能测试")
        print("-" * 40)
        
        # 搜索视频
        from main import search_bilibili_videos
        self.test_api(
            "search_bilibili_videos - 搜索视频",
            search_bilibili_videos,
            self.test_keyword,
            1,
            "totalrank",
            5,
            True
        )
        time.sleep(3)
        
        # 获取搜索建议
        from main import get_search_suggestion
        self.test_api(
            "get_search_suggestion - 搜索建议",
            get_search_suggestion,
            "程序"
        )
        time.sleep(2)
        
        # 5. 热门内容测试
        print("\n🔥 热门内容测试")
        print("-" * 40)
        
        # 获取热门视频
        from main import get_trending_videos
        self.test_api(
            "get_trending_videos - 获取热门视频",
            get_trending_videos,
            0,    # rid
            3,    # day
            5,    # limit
            True  # simple
        )
        time.sleep(2)
        
        # 获取排行榜
        from main import get_ranking_videos
        self.test_api(
            "get_ranking_videos - 获取排行榜",
            get_ranking_videos,
            0,    # rid
            3,    # day
            0     # arc_type
        )
        time.sleep(2)
        
        # 获取综合热门
        from main import get_popular_videos
        self.test_api(
            "get_popular_videos - 综合热门",
            get_popular_videos,
            10,   # page_size
            1     # page_num
        )
        time.sleep(2)
        
        # 获取入站必刷
        from main import get_precious_videos
        self.test_api(
            "get_precious_videos - 入站必刷",
            get_precious_videos,
            10,   # page_size
            1     # page_num
        )
        time.sleep(2)
        
        # 6. 直播相关测试
        print("\n📺 直播相关测试")
        print("-" * 40)
        
        # 获取直播间信息
        from main import get_live_room_info
        self.test_api(
            "get_live_room_info - 直播间信息",
            get_live_room_info,
            self.test_room_id
        )
        time.sleep(2)
        
        # 获取用户直播间
        from main import get_live_user_info
        self.test_api(
            "get_live_user_info - 用户直播间",
            get_live_user_info,
            self.test_uid
        )
        time.sleep(2)
        
        # 获取直播分区
        from main import get_live_area_list
        self.test_api(
            "get_live_area_list - 直播分区列表",
            get_live_area_list
        )
        time.sleep(2)
        
        # 获取直播在线列表
        from main import get_live_online_list
        self.test_api(
            "get_live_online_list - 直播在线列表",
            get_live_online_list,
            0,    # parent_area_id
            0,    # area_id
            1,    # page
            10    # page_size
        )
        time.sleep(2)
        
        # 7. 工具函数测试
        print("\n🛠️ 工具函数测试")
        print("-" * 40)
        
        # 从URL提取UID
        from main import extract_uid_from_bilibili_url
        self.test_api(
            "extract_uid_from_bilibili_url - 提取UID",
            extract_uid_from_bilibili_url,
            "https://space.bilibili.com/316183842"
        )
        time.sleep(1)
        
        # 从URL提取BV号
        from main import extract_bvid_from_url
        self.test_api(
            "extract_bvid_from_url - 提取BV号",
            extract_bvid_from_url,
            f"https://www.bilibili.com/video/{self.test_bvid}"
        )
        time.sleep(1)
        
        # 测试增强功能
        from main import test_enhanced_features
        self.test_api(
            "test_enhanced_features - 增强功能测试",
            test_enhanced_features
        )
        
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
                if api['response']:
                    for key, value in api['response'].items():
                        if key != "data_keys":
                            report.append(f"    - {key}: {value}")
        
        # 部分可用的API
        if partial_apis:
            report.append("\n⚠️ 部分可用的API接口:")
            report.append("-" * 40)
            for api in partial_apis:
                report.append(f"  • {api['name']} ({api['elapsed']}秒)")
                if api['response']:
                    for key, value in api['response'].items():
                        report.append(f"    - {key}: {value}")
        
        # 失败的API
        if failed_apis:
            report.append("\n❌ 不可用的API接口:")
            report.append("-" * 40)
            for api in failed_apis:
                report.append(f"  • {api['name']}")
                if api['response'] and "error" in api['response']:
                    report.append(f"    - 错误: {api['response']['error']}")
        
        # 建议
        report.append("\n" + "=" * 60)
        report.append("💡 优化建议")
        report.append("=" * 60)
        
        if self.failed_count > 0:
            report.append("⚠️ 部分API失败，建议:")
            report.append("  1. 配置有效的SESSDATA cookie")
            report.append("  2. 增加请求间隔避免频率限制")
            report.append("  3. 检查网络连接状态")
        
        if self.partial_count > 0:
            report.append("📌 部分API受限，可能原因:")
            report.append("  • 缺少必要的cookie认证")
            report.append("  • 触发了反爬虫机制")
            report.append("  • API接口有访问限制")
        
        if success_rate < 50:
            report.append("🔧 成功率较低，强烈建议:")
            report.append("  • 使用set_bilibili_cookies设置完整cookie")
            report.append("  • 参考BILIBILI_COOKIES_GUIDE.md配置文档")
            report.append("  • 使用cookie_example.json模板")
        elif success_rate < 80:
            report.append("📈 成功率中等，建议优化:")
            report.append("  • 添加更多设备标识cookie(buvid3, b_nut等)")
            report.append("  • 适当增加请求间隔")
        else:
            report.append("🎉 API状态良好，大部分接口可正常使用!")
        
        return "\n".join(report)

def main():
    """主测试函数"""
    print("\n🚀 开始B站MCP服务器API综合测试...\n")
    
    # 创建测试器
    tester = APITester()
    
    try:
        # 运行所有测试
        tester.run_all_tests()
        
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
            print("\n✅ 所有API测试通过!")
            return 0
        elif tester.failed_count < len(tester.results) / 2:
            print("\n⚠️ 部分API测试失败，但大部分功能可用")
            return 1
        else:
            print("\n❌ 大量API测试失败，需要检查配置")
            return 2
            
    except Exception as e:
        print(f"\n❌ 测试过程出现异常: {e}")
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    exit(main())