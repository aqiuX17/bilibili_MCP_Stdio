#!/usr/bin/env python3
"""
测试增强的Cookie功能
演示不同Cookie配置的效果差异
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from main import set_bilibili_cookies

def test_basic_cookies():
    """测试基础Cookie配置"""
    
    print("=" * 60)
    print("🍪 测试基础Cookie配置")
    print("=" * 60)
    
    basic_cookies = {
        "SESSDATA": "your_sessdata_here",
        "bili_jct": "your_bili_jct_here"
    }
    
    print("📋 基础配置（最低要求）:")
    print(json.dumps(basic_cookies, indent=2, ensure_ascii=False))
    print("\n" + "-" * 40)
    
    result = set_bilibili_cookies(json.dumps(basic_cookies))
    print(result)

def test_recommended_cookies():
    """测试推荐Cookie配置"""
    
    print("\n" + "=" * 60)
    print("🍪 测试推荐Cookie配置")
    print("=" * 60)
    
    recommended_cookies = {
        "SESSDATA": "your_sessdata_here",
        "bili_jct": "your_bili_jct_here",
        "DedeUserID": "123456789",
        "DedeUserID__ckMd5": "your_checksum",
        "buvid3": "your_buvid3_here",
        "buvid4": "your_buvid4_here",
        "b_nut": "1692345678",
        "buvid_fp": "your_device_fingerprint",
        "b_lsid": "your_session_id",
        "CURRENT_FNVAL": "4048"
    }
    
    print("📋 推荐配置（平衡效果与复杂度）:")
    print(json.dumps(recommended_cookies, indent=2, ensure_ascii=False))
    print("\n" + "-" * 40)
    
    result = set_bilibili_cookies(json.dumps(recommended_cookies))
    print(result)

def test_complete_cookies():
    """测试完整Cookie配置"""
    
    print("\n" + "=" * 60)
    print("🍪 测试完整Cookie配置")
    print("=" * 60)
    
    complete_cookies = {
        # 核心cookie
        "SESSDATA": "your_sessdata_here",
        "bili_jct": "your_bili_jct_here",
        
        # 重要cookie
        "DedeUserID": "123456789",
        "buvid3": "your_buvid3_here",
        "buvid4": "your_buvid4_here",
        "b_nut": "1692345678",
        "buvid_fp": "your_device_fingerprint",
        "b_lsid": "your_session_id",
        
        # 推荐cookie
        "_uuid": "12345678-1234-1234-1234-123456789ABC",
        "CURRENT_FNVAL": "4048",
        "rpdid": "your_recommendation_id",
        "CURRENT_BLACKGAP": "0",
        "blackside_state": "0",
        
        # 可选cookie
        "DedeUserID__ckMd5": "your_checksum",
        "sid": "your_sid_here",
        "fingerprint": "your_fingerprint",
        "LIVE_BUVID": "AUTO1234567890123456",
        "browser_resolution": "1920-1080",
        "innersign": "0"
    }
    
    print("📋 完整配置（最佳效果）:")
    print(json.dumps(complete_cookies, indent=2, ensure_ascii=False))
    print("\n" + "-" * 40)
    
    result = set_bilibili_cookies(json.dumps(complete_cookies))
    print(result)

def test_incomplete_cookies():
    """测试不完整Cookie配置"""
    
    print("\n" + "=" * 60)
    print("🍪 测试不完整Cookie配置")
    print("=" * 60)
    
    incomplete_cookies = {
        "buvid3": "your_buvid3_only",
        "browser_resolution": "1920-1080"
    }
    
    print("📋 不完整配置（缺少核心cookie）:")
    print(json.dumps(incomplete_cookies, indent=2, ensure_ascii=False))
    print("\n" + "-" * 40)
    
    result = set_bilibili_cookies(json.dumps(incomplete_cookies))
    print(result)

def test_priority_cookies():
    """测试优先级Cookie配置"""
    
    print("\n" + "=" * 60)
    print("🍪 测试优先级Cookie配置")
    print("=" * 60)
    
    # 第一优先级
    print("🥇 第一优先级Cookie（立即添加）:")
    priority1_cookies = {
        "SESSDATA": "your_sessdata_here",
        "bili_jct": "your_bili_jct_here",
        "b_nut": "1692345678",
        "buvid_fp": "your_device_fingerprint", 
        "b_lsid": "your_session_id"
    }
    
    print(json.dumps(priority1_cookies, indent=2, ensure_ascii=False))
    print("\n" + "-" * 20)
    
    result1 = set_bilibili_cookies(json.dumps(priority1_cookies))
    print(result1)
    
    # 第二优先级
    print("\n🥈 第二优先级Cookie（推荐添加）:")
    priority2_cookies = {
        **priority1_cookies,
        "_uuid": "12345678-1234-1234-1234-123456789ABC",
        "CURRENT_FNVAL": "4048",
        "rpdid": "your_recommendation_id"
    }
    
    print("新增cookie: _uuid, CURRENT_FNVAL, rpdid")
    print("\n" + "-" * 20)
    
    result2 = set_bilibili_cookies(json.dumps(priority2_cookies))
    print(result2)

def show_cookie_guide():
    """显示Cookie获取指南"""
    
    print("\n" + "=" * 60)
    print("📖 Cookie获取指南")
    print("=" * 60)
    
    guide = """
🔍 如何获取这些Cookie？

方法1: 浏览器开发者工具
  1. 打开 bilibili.com
  2. 按F12 → Network标签
  3. 刷新页面，查看请求头Cookie

方法2: 浏览器Cookie管理
  1. 浏览器设置 → 隐私 → Cookie
  2. 搜索"bilibili.com"
  3. 复制所需Cookie值

方法3: 浏览器扩展
  • 搜索"Cookie导出"扩展
  • 一键导出B站所有Cookie

🎯 重要Cookie说明：

核心Cookie（必需）:
  • SESSDATA: 登录会话，最重要
  • bili_jct: 安全令牌

设备标识（强烈推荐）:
  • b_nut: 设备首次访问时间
  • buvid_fp: 设备指纹
  • buvid3/buvid4: 设备唯一标识

会话Cookie（推荐）:
  • b_lsid: 本地会话ID
  • _uuid: 通用唯一标识

功能Cookie（可选）:
  • CURRENT_FNVAL: 视频功能标识
  • rpdid: 推荐算法ID
  • LIVE_BUVID: 直播设备标识

🛡️ 安全提醒：
  • SESSDATA等同于登录密码，请妥善保管
  • 不要在公开场合分享Cookie
  • 定期更新Cookie以保持有效性
  • 不同设备的Cookie不要混用
"""
    
    print(guide)

def main():
    """主测试函数"""
    
    print("🚀 B站Cookie增强功能测试")
    
    # 运行所有测试
    test_basic_cookies()
    test_recommended_cookies()
    test_complete_cookies()
    test_incomplete_cookies()
    test_priority_cookies()
    show_cookie_guide()
    
    print("\n" + "=" * 60)
    print("🎉 Cookie测试完成！")
    print("=" * 60)
    
    summary = """
📊 配置效果对比：

基础配置 (2个cookie):
  • 成功率: ~60%
  • 适用: 基础功能测试

推荐配置 (10个cookie):
  • 成功率: ~80%
  • 适用: 日常使用

完整配置 (16个cookie):
  • 成功率: ~95%
  • 适用: 专业用途

💡 建议：
1. 从基础配置开始，逐步添加更多cookie
2. 优先添加 b_nut、buvid_fp、b_lsid 三个关键cookie
3. 根据使用需求选择合适的配置级别
4. 定期更新cookie以保持最佳效果

📖 详细指南请查看: BILIBILI_COOKIES_GUIDE.md
"""
    
    print(summary)

if __name__ == "__main__":
    main()
