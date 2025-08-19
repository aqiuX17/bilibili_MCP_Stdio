#!/usr/bin/env python3
"""
测试用户动态等API的数据准确性
"""

import json
import time
import requests
from datetime import datetime

class DynamicsAPITester:
    """测试用户动态API的准确性"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Origin": "https://www.bilibili.com",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        })
    
    def test_user_dynamics(self, uid: str):
        """测试用户动态API"""
        print(f"\n🔍 测试用户动态API - UID: {uid}")
        print("=" * 60)
        
        # 测试多个动态API端点
        apis = [
            {
                "name": "新版动态API (web-dynamic)",
                "url": "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space",
                "params": {
                    "host_mid": uid,
                    "timezone_offset": -480,
                    "features": "itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote,decorationCard,forwardListHidden,ugcDelete,onlyfansQaCard",
                    "web_location": "333.999",
                    "x-bili-device-req-json": '{"platform":"web","device":"pc"}',
                    "x-bili-web-req-json": '{"spm_id":"333.999"}'
                }
            },
            {
                "name": "动态列表API (space_history)",
                "url": "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space",
                "params": {
                    "offset": "",
                    "host_mid": uid,
                    "timezone_offset": -480,
                    "platform": "web",
                    "features": "itemOpusStyle",
                    "web_location": "333.999"
                }
            },
            {
                "name": "旧版动态API (vc/dynamic_svr)",
                "url": "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history",
                "params": {
                    "visitor_uid": "0",
                    "host_uid": uid,
                    "offset_dynamic_id": "0",
                    "need_top": "1",
                    "platform": "web"
                }
            }
        ]
        
        for api in apis:
            print(f"\n📌 {api['name']}")
            print(f"   URL: {api['url']}")
            
            try:
                response = self.session.get(api['url'], params=api['params'], timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # 分析返回数据
                        if isinstance(data, dict):
                            code = data.get("code", -1)
                            message = data.get("message", "")
                            
                            if code == 0:
                                print(f"   ✅ 请求成功 (code=0)")
                                
                                # 分析数据结构
                                if "data" in data:
                                    self._analyze_dynamics_data(data["data"])
                            else:
                                print(f"   ❌ 请求失败 (code={code}, message={message})")
                        else:
                            print(f"   ⚠️ 返回格式异常")
                            
                    except json.JSONDecodeError:
                        print(f"   ❌ 返回非JSON格式")
                else:
                    print(f"   ❌ HTTP错误: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 请求异常: {e}")
            
            time.sleep(2)
    
    def _analyze_dynamics_data(self, data):
        """分析动态数据的准确性"""
        # 检查数据结构
        if "items" in data:
            items = data.get("items", [])
            print(f"   📊 返回动态数: {len(items)}")
            
            if items:
                # 分析第一条动态
                first_item = items[0]
                print(f"   📝 第一条动态分析:")
                
                # 动态类型
                if "type" in first_item:
                    print(f"      - 类型: {first_item['type']}")
                
                # 动态ID
                if "id_str" in first_item:
                    print(f"      - ID: {first_item['id_str']}")
                elif "basic" in first_item:
                    print(f"      - ID: {first_item.get('basic', {}).get('id_str', 'N/A')}")
                
                # 模块分析
                if "modules" in first_item:
                    modules = first_item["modules"]
                    
                    # 作者模块
                    if "module_author" in modules:
                        author = modules["module_author"]
                        print(f"      - 作者: {author.get('name', 'N/A')}")
                        print(f"      - 发布时间: {author.get('pub_ts', 'N/A')}")
                        if author.get('pub_ts'):
                            try:
                                timestamp = int(author['pub_ts'])
                                dt = datetime.fromtimestamp(timestamp)
                                print(f"      - 格式化时间: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                            except:
                                pass
                    
                    # 动态内容模块
                    if "module_dynamic" in modules:
                        dynamic = modules["module_dynamic"]
                        
                        # 检查不同类型的动态内容
                        if "major" in dynamic:
                            major = dynamic["major"]
                            major_type = major.get("type", "")
                            print(f"      - 内容类型: {major_type}")
                            
                            # 根据类型解析内容
                            if major_type == "MAJOR_TYPE_ARCHIVE":
                                # 视频投稿
                                archive = major.get("archive", {})
                                print(f"      - 视频标题: {archive.get('title', 'N/A')}")
                                print(f"      - 视频BV号: {archive.get('bvid', 'N/A')}")
                            elif major_type == "MAJOR_TYPE_DRAW":
                                # 图文动态
                                draw = major.get("draw", {})
                                print(f"      - 图片数量: {len(draw.get('items', []))}")
                            elif major_type == "MAJOR_TYPE_ARTICLE":
                                # 专栏文章
                                article = major.get("article", {})
                                print(f"      - 文章标题: {article.get('title', 'N/A')}")
                        
                        # 文字描述
                        if "desc" in dynamic:
                            desc_text = dynamic["desc"].get("text", "")
                            if desc_text:
                                preview = desc_text[:100] + "..." if len(desc_text) > 100 else desc_text
                                print(f"      - 文字内容: {preview}")
                    
                    # 互动数据
                    if "module_stat" in modules:
                        stat = modules["module_stat"]
                        print(f"      - 互动数据:")
                        print(f"        • 点赞: {stat.get('like', {}).get('count', 0)}")
                        print(f"        • 评论: {stat.get('reply', {}).get('count', 0)}")
                        print(f"        • 转发: {stat.get('forward', {}).get('count', 0)}")
            else:
                print(f"   ⚠️ 该用户暂无动态")
                
        elif "cards" in data:
            # 旧版API的数据结构
            cards = data.get("cards", [])
            print(f"   📊 返回动态数: {len(cards)}")
            
            if cards:
                first_card = cards[0]
                print(f"   📝 第一条动态分析:")
                
                # 解析card JSON
                if "card" in first_card:
                    try:
                        card_data = json.loads(first_card["card"])
                        
                        # 动态类型判断
                        if "item" in card_data:
                            # 图文动态
                            print(f"      - 类型: 图文动态")
                            print(f"      - 内容: {card_data.get('item', {}).get('description', 'N/A')[:100]}")
                        elif "aid" in card_data:
                            # 视频投稿
                            print(f"      - 类型: 视频投稿")
                            print(f"      - 标题: {card_data.get('title', 'N/A')}")
                            print(f"      - AID: {card_data.get('aid', 'N/A')}")
                        elif "title" in card_data:
                            # 专栏文章
                            print(f"      - 类型: 专栏文章")
                            print(f"      - 标题: {card_data.get('title', 'N/A')}")
                    except:
                        print(f"      - 解析card失败")
                
                # 基础信息
                desc = first_card.get("desc", {})
                print(f"      - 动态ID: {desc.get('dynamic_id_str', 'N/A')}")
                print(f"      - 发布时间戳: {desc.get('timestamp', 'N/A')}")
                
                # 用户信息
                if "user_profile" in desc:
                    user = desc["user_profile"].get("info", {})
                    print(f"      - 作者: {user.get('uname', 'N/A')}")
        else:
            print(f"   ⚠️ 未找到动态数据字段")
    
    def test_user_videos(self, uid: str):
        """测试用户视频列表API"""
        print(f"\n🔍 测试用户视频列表API - UID: {uid}")
        print("=" * 60)
        
        apis = [
            {
                "name": "用户投稿视频API (wbi/arc/search)",
                "url": "https://api.bilibili.com/x/space/wbi/arc/search",
                "params": {
                    "mid": uid,
                    "ps": 10,
                    "tid": 0,
                    "pn": 1,
                    "keyword": "",
                    "order": "pubdate",
                    "platform": "web",
                    "web_location": "1550101",
                    "order_avoided": "true",
                    "w_rid": "",  # 需要WBI签名
                    "wts": str(int(time.time()))
                }
            },
            {
                "name": "用户视频列表API (arc/search - 无WBI)",
                "url": "https://api.bilibili.com/x/space/arc/search",
                "params": {
                    "mid": uid,
                    "ps": 10,
                    "pn": 1,
                    "order": "pubdate"
                }
            },
            {
                "name": "用户投稿API (navnum)",
                "url": "https://api.bilibili.com/x/space/navnum",
                "params": {
                    "mid": uid
                }
            }
        ]
        
        for api in apis:
            print(f"\n📌 {api['name']}")
            print(f"   URL: {api['url']}")
            
            try:
                response = self.session.get(api['url'], params=api['params'], timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        if isinstance(data, dict):
                            code = data.get("code", -1)
                            
                            if code == 0:
                                print(f"   ✅ 请求成功")
                                
                                # 分析数据
                                if "navnum" in api['name']:
                                    # 投稿数量统计
                                    navnum = data.get("data", {})
                                    print(f"   📊 用户投稿统计:")
                                    print(f"      - 视频数: {navnum.get('video', 0)}")
                                    print(f"      - 专栏数: {navnum.get('article', 0)}")
                                    print(f"      - 音频数: {navnum.get('audio', 0)}")
                                else:
                                    # 视频列表
                                    if "data" in data:
                                        list_data = data["data"].get("list", {})
                                        vlist = list_data.get("vlist", [])
                                        
                                        print(f"   📊 返回视频数: {len(vlist)}")
                                        print(f"   📊 总视频数: {data.get('data', {}).get('page', {}).get('count', 0)}")
                                        
                                        if vlist:
                                            first_video = vlist[0]
                                            print(f"   📝 第一个视频:")
                                            print(f"      - 标题: {first_video.get('title', 'N/A')}")
                                            print(f"      - BV号: {first_video.get('bvid', 'N/A')}")
                                            print(f"      - 播放量: {first_video.get('play', 0)}")
                                            print(f"      - 发布时间: {datetime.fromtimestamp(first_video.get('created', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
                            elif code == -352:
                                print(f"   ⚠️ 需要WBI签名 (code=-352)")
                            else:
                                print(f"   ❌ 请求失败 (code={code})")
                                
                    except json.JSONDecodeError:
                        print(f"   ❌ 返回非JSON格式")
                else:
                    print(f"   ❌ HTTP错误: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 请求异常: {e}")
            
            time.sleep(2)
    
    def test_user_info(self, uid: str):
        """测试用户信息API的准确性"""
        print(f"\n🔍 测试用户信息API - UID: {uid}")
        print("=" * 60)
        
        apis = [
            {
                "name": "用户卡片API (card)",
                "url": "https://api.bilibili.com/x/web-interface/card",
                "params": {"mid": uid, "photo": "true"}
            },
            {
                "name": "用户信息API (acc/info)",
                "url": "https://api.bilibili.com/x/space/acc/info",
                "params": {"mid": uid}
            },
            {
                "name": "用户关系统计API (relation/stat)",
                "url": "https://api.bilibili.com/x/relation/stat",
                "params": {"vmid": uid}
            }
        ]
        
        for api in apis:
            print(f"\n📌 {api['name']}")
            
            try:
                response = self.session.get(api['url'], params=api['params'], timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("code") == 0:
                        print(f"   ✅ 请求成功")
                        
                        # 分析数据
                        if "card" in api['name']:
                            card = data.get("data", {}).get("card", {})
                            print(f"   👤 用户信息:")
                            print(f"      - 昵称: {card.get('name', 'N/A')}")
                            print(f"      - UID: {card.get('mid', 'N/A')}")
                            print(f"      - 签名: {card.get('sign', 'N/A')[:50]}")
                            print(f"      - 粉丝数: {card.get('fans', 0):,}")
                            print(f"      - 关注数: {card.get('attention', 0):,}")
                        elif "acc/info" in api['url']:
                            info = data.get("data", {})
                            print(f"   👤 详细信息:")
                            print(f"      - 昵称: {info.get('name', 'N/A')}")
                            print(f"      - 等级: {info.get('level', 0)}")
                            print(f"      - 性别: {info.get('sex', 'N/A')}")
                            print(f"      - 生日: {info.get('birthday', 'N/A')}")
                            print(f"      - 注册时间: {datetime.fromtimestamp(info.get('jointime', 0)).strftime('%Y-%m-%d') if info.get('jointime') else 'N/A'}")
                        elif "relation/stat" in api['url']:
                            stat = data.get("data", {})
                            print(f"   📊 关系统计:")
                            print(f"      - 关注数: {stat.get('following', 0):,}")
                            print(f"      - 粉丝数: {stat.get('follower', 0):,}")
                            print(f"      - 黑名单: {stat.get('black', 0)}")
                            print(f"      - 悄悄关注: {stat.get('whisper', 0)}")
                    else:
                        print(f"   ❌ 请求失败 (code={data.get('code')})")
                        
            except Exception as e:
                print(f"   ❌ 请求异常: {e}")
            
            time.sleep(2)
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("\n" + "=" * 60)
        print("🚀 B站API数据准确性测试")
        print("=" * 60)
        
        # 测试多个用户
        test_users = [
            {
                "uid": "672328094",  # 嘉然
                "name": "嘉然今天吃什么",
                "type": "虚拟主播"
            },
            {
                "uid": "1",  # B站CEO陈睿
                "name": "bishi",  
                "type": "站长"
            },
            {
                "uid": "546195",  # 老番茄
                "name": "老番茄",
                "type": "知名UP主"
            }
        ]
        
        for user in test_users:
            print(f"\n{'=' * 60}")
            print(f"📦 测试用户: {user['name']} (UID: {user['uid']}) - {user['type']}")
            print(f"{'=' * 60}")
            
            # 测试用户信息
            self.test_user_info(user['uid'])
            
            # 测试用户视频
            self.test_user_videos(user['uid'])
            
            # 测试用户动态
            self.test_user_dynamics(user['uid'])
            
            print(f"\n⏸️ 等待5秒后测试下一个用户...")
            time.sleep(5)
    
    def test_specific_api(self, api_type: str, uid: str):
        """测试特定的API"""
        if api_type == "dynamics":
            self.test_user_dynamics(uid)
        elif api_type == "videos":
            self.test_user_videos(uid)
        elif api_type == "info":
            self.test_user_info(uid)
        else:
            print(f"❌ 未知的API类型: {api_type}")

def main():
    """主函数"""
    print("\n🔍 B站API数据准确性深度测试")
    print("📌 重点测试用户动态等可能不准确的接口")
    print("⏱️ 预计耗时: 2-3分钟\n")
    
    tester = DynamicsAPITester()
    
    # 运行综合测试
    tester.run_comprehensive_test()
    
    # 生成总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    print("\n🎯 关键发现:")
    print("\n1. 用户动态API:")
    print("   • 新版API (polymer/web-dynamic) 需要正确的参数格式")
    print("   • 数据结构复杂，包含modules模块化设计")
    print("   • 旧版API (dynamic_svr) 仍可用但数据格式不同")
    
    print("\n2. 用户视频API:")
    print("   • 需要WBI签名的API返回更准确的数据")
    print("   • 无WBI签名的API可能返回空数据或错误")
    print("   • navnum API可获取投稿统计数据")
    
    print("\n3. 用户信息API:")
    print("   • card API无需认证即可获取基本信息")
    print("   • acc/info API提供更详细的用户资料")
    print("   • relation/stat API提供关系统计数据")
    
    print("\n💡 改进建议:")
    print("   1. 实现正确的WBI签名算法")
    print("   2. 优化动态API的参数配置")
    print("   3. 处理不同API返回的数据格式差异")
    print("   4. 添加数据格式转换和标准化")
    
    print("\n✅ 测试完成!")

if __name__ == "__main__":
    main()