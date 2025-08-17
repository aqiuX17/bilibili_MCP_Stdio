#!/usr/bin/env python3
"""
MCP服务器启动脚本
用于测试和启动B站信息获取MCP服务器
"""

import sys
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mcp_server():
    """测试MCP服务器配置"""
    try:
        logger.info("测试MCP服务器配置...")
        
        # 导入MCP服务器
        from main import mcp
        
        logger.info(f"✅ MCP服务器导入成功: {mcp.name}")
        
        # 检查工具函数
        logger.info("检查工具函数...")
        
        # 测试基本功能
        from main import set_bilibili_cookies, get_cookie_status
        
        # 测试cookie状态
        status = get_cookie_status()
        logger.info(f"Cookie状态: {status}")
        
        logger.info("✅ MCP服务器配置测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP服务器配置测试失败: {e}")
        return False

def start_mcp_server():
    """启动MCP服务器"""
    try:
        logger.info("启动MCP服务器...")
        
        if not test_mcp_server():
            logger.error("MCP服务器配置测试失败，无法启动")
            return False
        
        # 导入并启动服务器
        from main import main
        main()
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务器...")
        return True
    except Exception as e:
        logger.error(f"启动MCP服务器失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 只测试配置
        test_mcp_server()
    else:
        # 启动服务器
        start_mcp_server()
