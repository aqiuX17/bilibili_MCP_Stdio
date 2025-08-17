@echo off
REM B站信息获取 MCP 服务器启动脚本 (Windows版本)

echo 🚀 启动B站信息获取 MCP 服务器...
echo 📝 使用说明:
echo    - 这是一个基于 stdio 协议的 MCP 服务器
echo    - 支持获取B站视频信息、用户信息、搜索等功能
echo    - 建议先设置cookie以避免反爬限制
echo.

REM 检查Python环境
python main.py

pause
