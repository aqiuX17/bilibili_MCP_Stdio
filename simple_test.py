#!/usr/bin/env python3
"""
简化的B站API测试脚本
"""

import json
import sys
import os

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试B站API基本功能...")
    
    try:
        # 导入必要的模块
        from main import BilibiliAPI
        
        # 创建API实例
        api = BilibiliAPI()
        print("✅ 成功创建B站API实例")
        
        # 测试获取热门视频
        print("\n📊 测试获取热门视频...")
        result = api.get_trending_videos(0, 3)
        
        if "error" not in result:
            print("✅ 获取热门视频成功")
            print(f"   返回数据大小: {len(str(result))} 字符")
            
            # 尝试解析返回的数据
            if "data" in result:
                print(f"   数据结构: {list(result['data'].keys())}")
            else:
                print(f"   数据结构: {list(result.keys())}")
        else:
            print(f"❌ 获取热门视频失败: {result['error']}")
        
        print("\n🎉 基本功能测试完成！")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_basic_functionality()
