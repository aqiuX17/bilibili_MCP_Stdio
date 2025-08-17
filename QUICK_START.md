# 🚀 快速开始指南

## 1. 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -r requirements.txt
```

## 2. 启动服务器

### Linux/Mac
```bash
./start_server.sh
```

### Windows
```cmd
start_server.bat
```

### 手动启动
```bash
uv run python main.py
```

## 3. 设置Cookie (重要!)

为了避免反爬限制，建议设置B站cookie：

```json
{
  "SESSDATA": "你的SESSDATA值",
  "bili_jct": "你的bili_jct值",
  "DedeUserID": "你的用户ID"
}
```

## 4. 测试功能

运行测试脚本验证功能：

```bash
uv run python test_bilibili.py
```

## 5. 主要功能

- 🔐 **Cookie管理**: `set_bilibili_cookies()`
- 📹 **视频信息**: `get_video_info()`
- 👤 **用户信息**: `get_user_info()`
- 🔍 **视频搜索**: `search_bilibili_videos()`
- 💬 **评论获取**: `get_video_comments()`
- 📊 **热门视频**: `get_trending_videos()`
- 🔗 **URL解析**: `extract_bvid_from_url()`

## 6. 使用示例

```python
# 获取视频信息
get_video_info("BV1xx411c7mu")

# 搜索视频
search_bilibili_videos("Python教程", 1, "click")

# 获取热门视频
get_trending_videos(0, 3)
```

## 7. 注意事项

- 首次使用建议设置cookie
- 避免过于频繁的请求
- 所有数据以JSON格式返回
- 支持错误处理和状态查询

## 8. 获取帮助

- 查看 `README.md` 获取详细文档
- 运行 `get_cookie_status()` 检查cookie状态
- 查看 `cookie_example.json` 了解cookie格式

---

🎉 **现在你可以开始使用B站信息获取MCP服务器了！**
