#!/usr/bin/env python3
"""
测试cookie自动加载功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from main import BilibiliAPI
import json

def test_cookie_loading():
    """测试cookie自动加载"""
    print("🍪 测试Cookie自动加载功能")
    print("=" * 50)
    
    # 创建API实例（应该自动加载cookie）
    api = BilibiliAPI()
    
    # 检查cookie是否加载
    cookies = dict(api.session.cookies)
    
    if cookies:
        print(f"✅ 成功加载 {len(cookies)} 个cookie")
        
        # 检查关键cookie
        critical_cookies = ["SESSDATA", "bili_jct", "buvid3", "DedeUserID"]
        for cookie_name in critical_cookies:
            if cookie_name in cookies:
                value = cookies[cookie_name]
                # 只显示前10个字符，保护隐私
                masked_value = value[:10] + "..." if len(value) > 10 else value
                print(f"  🔑 {cookie_name}: {masked_value}")
            else:
                print(f"  ❌ 缺少: {cookie_name}")
                
        # 检查设备标识cookie
        device_cookies = ["buvid3", "buvid4", "b_nut", "buvid_fp"]
        device_count = sum(1 for c in device_cookies if c in cookies)
        print(f"  📱 设备标识cookie: {device_count}/{len(device_cookies)}")
        
        # 检查会话cookie
        session_cookies = ["b_lsid", "_uuid", "rpdid"]
        session_count = sum(1 for c in session_cookies if c in cookies)
        print(f"  🎯 会话cookie: {session_count}/{len(session_cookies)}")
        
    else:
        print("❌ 未加载到任何cookie")
        
    return api, cookies

def test_simple_api_call(api):
    """测试简单的API调用"""
    print("\n🔍 测试API调用")
    print("=" * 50)
    
    try:
        # 测试导航信息获取（不需要特殊权限）
        nav_info = api._get_nav_info()
        
        if nav_info and nav_info.get("code") == 0:
            print("✅ 导航信息获取成功")
            data = nav_info.get("data", {})
            if "isLogin" in data:
                is_login = data["isLogin"]
                print(f"  🔐 登录状态: {'已登录' if is_login else '未登录'}")
            
            if "wbi_img" in data:
                wbi_img = data["wbi_img"]
                print(f"  🔑 WBI密钥可用: {bool(wbi_img.get('img_url'))}")
                
        else:
            print(f"❌ 导航信息获取失败: {nav_info}")
            
    except Exception as e:
        print(f"❌ API调用异常: {e}")

def test_user_info_api(api):
    """测试用户信息API"""
    print("\n👤 测试用户信息API")
    print("=" * 50)
    
    # 测试一个知名UP主的UID
    test_uid = "946974"  # 影视飓风
    
    try:
        result = api.get_user_info(test_uid)
        
        if result.get("success"):
            user_data = result.get("data", {})
            print(f"✅ 用户信息获取成功")
            print(f"  👤 用户名: {user_data.get('name', '未知')}")
            print(f"  🆔 UID: {user_data.get('mid', '未知')}")
            print(f"  📊 粉丝数: {user_data.get('follower', 0)}")
        else:
            error_msg = result.get("error", "未知错误")
            print(f"❌ 用户信息获取失败: {error_msg}")
            
    except Exception as e:
        print(f"❌ 用户信息API异常: {e}")

def main():
    """主测试函数"""
    print("🚀 B站MCP服务器Cookie加载测试")
    print("=" * 60)
    
    # 测试cookie加载
    api, cookies = test_cookie_loading()
    
    # 测试API调用
    test_simple_api_call(api)
    
    # 测试用户信息API
    test_user_info_api(api)
    
    print("\n" + "=" * 60)
    print("🎯 测试总结")
    
    if cookies:
        critical_count = sum(1 for c in ["SESSDATA", "bili_jct", "buvid3"] if c in cookies)
        if critical_count >= 2:
            print("✅ Cookie配置良好，API功能应该正常")
        elif critical_count == 1:
            print("⚠️ Cookie配置不完整，部分功能可能受限")
        else:
            print("❌ 缺少关键Cookie，建议检查配置")
    else:
        print("❌ 未加载Cookie，API功能将严重受限")
        
    print("\n💡 如果遇到问题，请检查:")
    print("   1. cookie_example.json 文件是否存在")
    print("   2. cookie内容是否有效（特别是SESSDATA）")
    print("   3. 网络连接是否正常")

if __name__ == "__main__":
    main()