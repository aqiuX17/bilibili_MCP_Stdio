#!/usr/bin/env python3
"""
简化的MCP服务器启动脚本
解决启动失败问题
"""

import sys
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    try:
        logger.info("🚀 启动B站信息获取MCP服务器...")
        
        # 检查Python环境
        logger.info(f"Python版本: {sys.version}")
        logger.info(f"工作目录: {os.getcwd()}")
        
        # 导入MCP服务器
        logger.info("导入MCP服务器...")
        from main import mcp
        
        logger.info(f"✅ MCP服务器导入成功: {mcp.name}")
        logger.info(f"传输协议: stdio")
        
        # 启动MCP服务器
        logger.info("启动MCP服务器...")
        mcp.run(transport="stdio")
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务器...")
        sys.exit(0)
    except ImportError as e:
        logger.error(f"导入错误: {e}")
        logger.error("请确保在正确的环境中运行: uv run python launch_mcp.py")
        sys.exit(1)
    except Exception as e:
        logger.error(f"服务器运行异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
