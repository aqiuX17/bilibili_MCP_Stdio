#!/usr/bin/env python3
"""
标准MCP服务器启动脚本
使用正确的MCP协议格式启动服务器
"""

import sys
import os
import logging
import asyncio

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """主函数"""
    try:
        logger.info("启动B站信息获取MCP服务器...")
        logger.info("服务器名称: B站信息获取")
        logger.info("传输协议: stdio")
        
        # 导入MCP服务器
        from main import mcp
        
        logger.info(f"✅ MCP服务器导入成功: {mcp.name}")
        
        # 启动MCP服务器
        await mcp.run_stdio_async()
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务器...")
    except Exception as e:
        logger.error(f"服务器运行异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
