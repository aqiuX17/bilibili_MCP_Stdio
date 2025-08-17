#!/bin/bash

# 🚀 B站信息获取MCP服务器快速启动脚本

echo "🎯 启动B站信息获取MCP服务器..."
echo "📁 工作目录: $(pwd)"
echo ""

# 检查Python环境
if command -v uv &> /dev/null; then
    echo "✅ 使用 uv 虚拟环境..."
    
    # 检查服务器配置
    echo "🔧 检查服务器配置..."
    uv run python start_mcp_server.py test
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🚀 启动MCP服务器..."
        echo "💡 提示: 服务器启动后，请在MCP客户端中配置连接"
        echo "📱 配置示例:"
        echo "   command: python"
        echo "   args: [launch_mcp.py]"
        echo "   cwd: $(pwd)"
        echo ""
        echo "按 Ctrl+C 停止服务器"
        echo ""
        
        # 启动服务器
        uv run python launch_mcp.py
    else
        echo "❌ 服务器配置检查失败"
        exit 1
    fi
else
    echo "❌ uv 未找到，请先安装 uv"
    exit 1
fi
