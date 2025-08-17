# 🚀 MCP服务器启动指南

## 问题诊断

你遇到的MCP启动失败问题通常是由于以下原因：

1. **启动命令格式不正确**
2. **Python环境问题**
3. **MCP协议配置问题**
4. **依赖包缺失**

## ✅ 解决方案

### 方法1: 使用标准启动脚本（推荐）

```bash
# 进入项目目录
cd /Users/octopus/Downloads/mcpnormol

# 使用标准启动脚本
uv run python run_mcp_server.py
```

### 方法2: 使用测试启动脚本

```bash
# 先测试配置
uv run python start_mcp_server.py test

# 如果测试通过，启动服务器
uv run python start_mcp_server.py
```

### 方法3: 直接启动主程序

```bash
# 直接启动main.py
uv run python main.py
```

## 🔧 正确的MCP启动命令

### 对于MCP客户端，使用以下格式：

```bash
# 基本格式
--directory /Users/octopus/Downloads/mcpnormol run main.py

# 或者使用启动脚本
--directory /Users/octopus/Downloads/mcpnormol run run_mcp_server.py
```

### 环境变量设置

```bash
export PYTHONPATH="/Users/octopus/Downloads/mcpnormol:$PYTHONPATH"
export PATH="/Users/octopus/Downloads/mcpnormol/.venv/bin:$PATH"
```

## 📋 启动前检查清单

### 1. 环境检查
```bash
# 检查Python版本
python --version

# 检查虚拟环境
uv run python --version

# 检查依赖
uv run python -c "import mcp; print('MCP模块已安装')"
```

### 2. 配置检查
```bash
# 测试MCP服务器配置
uv run python start_mcp_server.py test

# 检查工具函数
uv run python -c "from main import mcp; print(f'服务器: {mcp.name}')"
```

### 3. 功能测试
```bash
# 运行功能测试
uv run python final_test.py
```

## 🚨 常见错误及解决方案

### 错误1: "ModuleNotFoundError: No module named 'mcp'"
**解决方案:**
```bash
# 确保在虚拟环境中运行
uv run python main.py

# 或者激活虚拟环境
source .venv/bin/activate
python main.py
```

### 错误2: "AttributeError: 'FastMCP' object has no attribute 'tools'"
**解决方案:**
- 这是已知问题，已修复
- 使用 `mcp.list_tools()` 替代 `mcp.tools`

### 错误3: "Transport stdio not supported"
**解决方案:**
```bash
# 使用正确的启动方式
uv run python run_mcp_server.py
```

### 错误4: "Permission denied"
**解决方案:**
```bash
# 确保脚本有执行权限
chmod +x start_server.sh
chmod +x run_mcp_server.py
```

## 📱 MCP客户端配置

### 在MCP客户端中添加服务器：

```json
{
  "mcpServers": {
    "bilibili-server": {
      "command": "python",
      "args": ["run_mcp_server.py"],
      "cwd": "/Users/octopus/Downloads/mcpnormol",
      "env": {
        "PYTHONPATH": "/Users/octopus/Downloads/mcpnormol"
      }
    }
  }
}
```

## 🔍 调试步骤

### 步骤1: 检查日志
```bash
# 启动时查看详细日志
uv run python run_mcp_server.py 2>&1 | tee mcp.log
```

### 步骤2: 验证功能
```bash
# 测试所有功能
uv run python final_test.py
```

### 步骤3: 检查网络
```bash
# 测试B站连接
uv run python -c "from main import test_connection; print(test_connection())"
```

## 📞 获取帮助

如果仍然遇到问题：

1. **查看日志文件**: `mcp.log`
2. **运行诊断脚本**: `uv run python start_mcp_server.py test`
3. **检查依赖**: `uv sync`
4. **重新安装**: `uv sync --reinstall`

## 🎯 成功启动的标志

当你看到以下输出时，说明MCP服务器启动成功：

```
2025-08-17 21:03:37,022 - INFO - 启动B站信息获取MCP服务器...
2025-08-17 21:03:37,022 - INFO - 服务器名称: B站信息获取
2025-08-17 21:03:37,022 - INFO - 传输协议: stdio
2025-08-17 21:03:37,244 - INFO - ✅ MCP服务器导入成功: B站信息获取
```

## 🚀 快速启动命令

```bash
# 一键启动（推荐）
cd /Users/octopus/Downloads/mcpnormol && uv run python run_mcp_server.py

# 或者使用启动脚本
./start_server.sh
```

---

🎉 **按照以上步骤，你的MCP服务器应该能够正常启动！**
