# B站信息获取 MCP 服务器

> ⚠️ **重要声明**：本项目仅供学习交流使用，严禁商业用途。详细声明请查看 [应用介绍与声明.md](./应用介绍与声明.md)

> 🔒 **隐私保护**：本项目已对所有敏感信息进行脱敏处理，请在使用前配置您自己的Cookie信息

这是一个基于 FastMCP 的 B站信息获取服务器，支持通过 stdio 协议与 MCP 客户端通信，可以获取B站的各种信息，包括视频信息、用户信息、搜索功能等。
## 预览
https://github.com/aqiuX17/bilibili_MCP_Stdio/blob/main/B%E7%AB%99%E7%94%A8%E6%88%B7%E6%8A%80%E6%9C%AF%E7%88%AC%E7%88%AC%E8%99%BE%E4%BF%A1%E6%81%AF%E6%9F%A5%E8%AF%A2.png

## 🚀 最新更新

**v1.1.0** - 修复了所有已知问题，确保功能稳定运行：
- ✅ 修复了MCP服务器启动异常
- ✅ 修复了编码问题
- ✅ 改进了错误处理机制
- ✅ 添加了日志记录功能
- ✅ 优化了API调用稳定性
- ✅ 添加了连接测试功能

## 功能特性

### 🔐 Cookie 管理
- 支持设置B站cookie，避免反爬限制
- 自动管理cookie状态
- 安全的cookie信息显示（隐藏敏感部分）

### 📹 视频相关功能
- 获取视频详细信息（标题、简介、播放量、点赞数等）
- 支持BV号查询
- 从B站URL自动提取BV号
- 获取视频评论信息

### 👤 用户相关功能
- 获取用户基本信息
- 支持UID查询

### 🔍 搜索功能
- 视频搜索（当前使用热门视频替代，确保稳定性）
- 支持多种排序方式（综合排序、点击量、发布时间、弹幕数、收藏数）
- 分页支持

### 📊 热门内容
- 获取热门视频榜单
- 支持不同分区（动画、音乐、游戏、科技等）
- 支持不同时间范围（日榜、三日榜、周榜、月榜）

### 🛠️ 工具函数
- `set_bilibili_cookies()` - 设置B站cookie
- `get_video_info()` - 获取视频信息
- `get_user_info()` - 获取用户信息
- `search_bilibili_videos()` - 搜索视频
- `get_video_comments()` - 获取视频评论
- `get_trending_videos()` - 获取热门视频
- `extract_bvid_from_url()` - 从URL提取BV号
- `get_cookie_status()` - 查看cookie状态
- `test_connection()` - 测试连接状态

## 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或者使用 pip
pip install -r requirements.txt
```

## 使用方法

### 1. 启动服务器

```bash
# Linux/Mac
./start_server.sh

# Windows
start_server.bat

# 手动启动
uv run python main.py
```

### 2. 设置Cookie（重要!）

> 🔒 **隐私保护说明**：本项目的 `cookie_example.json` 文件已进行脱敏处理，所有敏感信息已替换为占位符。

为了避免反爬限制，您需要配置自己的B站cookie：

**步骤1：获取Cookie**
1. 登录 [bilibili.com](https://www.bilibili.com)
2. 打开浏览器开发者工具（F12）
3. 在Network标签页中刷新页面
4. 找到任意请求，复制Cookie信息

**步骤2：配置Cookie**
编辑 `cookie_example.json` 文件，将占位符替换为您的实际Cookie值：

```json
{
  "SESSDATA": "你的SESSDATA值",
  "bili_jct": "你的bili_jct值",
  "DedeUserID": "你的用户ID",
  "DedeUserID__ckMd5": "你的MD5值",
  "buvid3": "你的buvid3值",
  "buvid4": "你的buvid4值"
}
```

**重要提醒**：
- ⚠️ 请妥善保管您的Cookie信息，不要泄露给他人
- 🔄 Cookie有时效性，如遇到认证失败请及时更新
- 🚫 严禁将真实Cookie提交到公共代码仓库

### 3. 测试功能

运行测试脚本验证功能：

```bash
# 基本功能测试
uv run python simple_test.py

# 完整功能测试
uv run python test_bilibili.py

# 最终功能测试
uv run python final_test.py
```

## 使用示例

### 获取视频信息
```python
# 获取BV号为 BV1xx411c7mu 的视频信息
result = get_video_info("BV1xx411c7mu")
```

### 搜索视频
```python
# 搜索"Python教程"，第1页，按点击量排序
result = search_bilibili_videos("Python教程", 1, "click")
```

### 获取热门视频
```python
# 获取全站3日热门视频
result = get_trending_videos(0, 3)

# 获取游戏分区周榜
result = get_trending_videos(4, 7)
```

## 分区ID说明

| 分区ID | 分区名称 |
|--------|----------|
| 0 | 全站 |
| 1 | 动画 |
| 3 | 音乐 |
| 4 | 游戏 |
| 5 | 科技 |
| 36 | 科技 |
| 119 | 鬼畜 |
| 129 | 舞蹈 |
| 155 | 生活 |
| 160 | 时尚 |
| 162 | 娱乐 |
| 21 | 日常 |
| 75 | 电影 |
| 76 | 电视剧 |
| 77 | 纪录片 |

## 排序方式说明

| 排序值 | 说明 |
|--------|------|
| totalrank | 综合排序 |
| click | 点击量 |
| pubdate | 发布时间 |
| dm | 弹幕数 |
| stow | 收藏数 |

## 注意事项

1. **Cookie设置**: 强烈建议设置有效的B站cookie以避免反爬限制
2. **请求频率**: 避免过于频繁的请求，建议在请求之间添加适当延迟
3. **错误处理**: 所有API调用都包含错误处理，返回的错误信息会帮助诊断问题
4. **数据格式**: 返回的数据为JSON格式，便于程序处理
5. **稳定性**: 当前版本已修复所有已知问题，确保稳定运行

## 技术架构

- **FastMCP**: 基于FastMCP框架构建
- **Requests**: 处理HTTP请求
- **BeautifulSoup**: 解析HTML内容（备用）
- **JSON**: 数据序列化和反序列化
- **正则表达式**: URL解析和BV号提取
- **日志系统**: 完整的日志记录和错误追踪

## 故障排除

### 常见问题

1. **编码错误**: 已修复，当前版本支持中文
2. **API限制**: 使用cookie可以避免大部分限制
3. **连接超时**: 已设置合理的超时时间
4. **数据解析**: 改进了JSON解析的稳定性

## 📞 联系方式

如有技术问题、建议或合作意向，欢迎联系：

**邮箱**：aqiuX17@yeah.net

## ⚖️ 使用声明

**本项目仅供学习交流使用，严禁商业用途。**

详细的使用声明、免责条款和隐私保护说明，请查看：

📋 **[应用介绍与声明.md](./应用介绍与声明.md)**

### 重要提醒

- ✅ 允许：个人学习、技术研究、学术交流
- ❌ 禁止：商业使用、盈利活动、大规模数据采集
- ❌ 禁止：违反B站服务条款的任何行为
- 🔒 隐私：请妥善保管Cookie等敏感信息

使用本项目即表示您同意遵守相关声明和条款。

---

**最后更新**：2025年1月 | **版本**：v1.1.0

### 调试方法

1. 查看日志输出
2. 使用 `test_connection()` 测试连接
3. 检查cookie状态
4. 运行测试脚本验证功能

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

---

🎉 **当前版本已修复所有已知问题，功能稳定可靠！**
