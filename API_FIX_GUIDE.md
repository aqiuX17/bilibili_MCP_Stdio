# 🔧 B站API数据准确性修复指南

## 📌 问题诊断

### 发现的主要问题

通过深度测试，发现以下API存在数据准确性问题：

#### 1. 用户动态API (`get_user_dynamics`)
**问题**：
- ❌ 新版API (polymer/web-dynamic) 返回错误码-352（需要WBI签名）
- ❌ 旧版API虽然返回成功但数据为空
- ❌ 参数配置不正确，缺少必要的features参数

**根本原因**：
- 缺少正确的WBI签名实现
- API参数不完整
- 数据解析逻辑不适配新版API结构

#### 2. 用户视频API (`get_user_videos`)
**问题**：
- ❌ 频繁触发-799错误（请求过于频繁）
- ❌ WBI签名版本API无法访问（-352错误）
- ❌ 数据嵌套层级深，解析不准确

**根本原因**：
- 请求频率控制不当
- WBI签名算法未正确实现
- 数据结构解析逻辑有误

#### 3. 用户信息API (`get_user_info`)
**问题**：
- ⚠️ 详细信息需要WBI签名
- ⚠️ 部分字段可能为空或格式不一致

## 🛠️ 修复方案

### 1. 修复用户动态API

```python
def get_user_dynamics(self, uid: str, offset: str = "", page: int = 1) -> Dict:
    """获取用户动态信息（修复版）"""
    try:
        # 方案1：使用不需要WBI的旧版API
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
        params = {
            "visitor_uid": "0",
            "host_uid": uid,
            "offset_dynamic_id": offset if offset else "0",
            "need_top": "1",
            "platform": "web"
        }
        
        # 添加必要的请求头
        headers = {
            "Referer": f"https://space.bilibili.com/{uid}/dynamic",
            "Origin": "https://www.bilibili.com",
            "User-Agent": self.session.headers.get("User-Agent")
        }
        
        # 发送请求
        result = self._make_request(url, params=params, headers=headers)
        
        # 解析返回数据
        if isinstance(result, dict) and result.get("code") == 0:
            data = result.get("data", {})
            cards = data.get("cards", [])
            
            # 转换为统一格式
            formatted_items = []
            for card in cards:
                try:
                    # 解析card JSON字符串
                    card_data = json.loads(card.get("card", "{}"))
                    desc = card.get("desc", {})
                    
                    # 构建统一的动态项
                    item = {
                        "id": desc.get("dynamic_id_str", ""),
                        "type": desc.get("type", 0),
                        "timestamp": desc.get("timestamp", 0),
                        "author": {
                            "uid": desc.get("uid", 0),
                            "name": desc.get("user_profile", {}).get("info", {}).get("uname", "")
                        },
                        "content": self._parse_dynamic_content(card_data, desc.get("type", 0)),
                        "stats": {
                            "like": desc.get("like", 0),
                            "repost": desc.get("repost", 0),
                            "comment": desc.get("comment", 0)
                        }
                    }
                    formatted_items.append(item)
                except Exception as e:
                    logger.warning(f"解析动态卡片失败: {e}")
                    continue
            
            return {
                "code": 0,
                "message": "success",
                "data": {
                    "items": formatted_items,
                    "has_more": data.get("has_more", 0),
                    "next_offset": data.get("next_offset", "")
                }
            }
        
        # 方案2：如果旧版API失败，尝试用户投稿视频作为动态
        logger.warning(f"动态API失败，尝试获取用户投稿视频作为替代")
        return self._get_user_videos_as_dynamics(uid, page)
        
    except Exception as e:
        logger.error(f"获取用户动态失败: {e}")
        return {
            "code": -1,
            "message": f"获取用户动态失败: {str(e)}",
            "data": {"items": []}
        }

def _parse_dynamic_content(self, card_data: Dict, dtype: int) -> Dict:
    """解析不同类型的动态内容"""
    content = {}
    
    # 根据动态类型解析
    if dtype == 1:  # 转发动态
        content["type"] = "forward"
        content["text"] = card_data.get("item", {}).get("content", "")
    elif dtype == 2:  # 图文动态
        content["type"] = "draw"
        content["text"] = card_data.get("item", {}).get("description", "")
        content["pictures"] = card_data.get("item", {}).get("pictures", [])
    elif dtype == 4:  # 文字动态
        content["type"] = "text"
        content["text"] = card_data.get("item", {}).get("content", "")
    elif dtype == 8:  # 视频投稿
        content["type"] = "video"
        content["title"] = card_data.get("title", "")
        content["desc"] = card_data.get("desc", "")
        content["bvid"] = card_data.get("bvid", "")
        content["aid"] = card_data.get("aid", 0)
        content["pic"] = card_data.get("pic", "")
    elif dtype == 64:  # 专栏
        content["type"] = "article"
        content["title"] = card_data.get("title", "")
        content["summary"] = card_data.get("summary", "")
        content["id"] = card_data.get("id", 0)
    else:
        content["type"] = "unknown"
        content["raw"] = card_data
    
    return content

def _get_user_videos_as_dynamics(self, uid: str, page: int) -> Dict:
    """将用户投稿视频转换为动态格式（备用方案）"""
    try:
        # 获取用户视频列表
        url = "https://api.bilibili.com/x/space/arc/search"
        params = {
            "mid": uid,
            "ps": 20,
            "pn": page,
            "order": "pubdate"
        }
        
        result = self._make_request(url, params=params)
        
        if isinstance(result, dict) and result.get("code") == 0:
            vlist = result.get("data", {}).get("list", {}).get("vlist", [])
            
            # 转换为动态格式
            items = []
            for video in vlist:
                item = {
                    "id": f"video_{video.get('aid', 0)}",
                    "type": 8,  # 视频类型
                    "timestamp": video.get("created", 0),
                    "author": {
                        "uid": uid,
                        "name": video.get("author", "")
                    },
                    "content": {
                        "type": "video",
                        "title": video.get("title", ""),
                        "desc": video.get("description", ""),
                        "bvid": video.get("bvid", ""),
                        "aid": video.get("aid", 0),
                        "pic": video.get("pic", ""),
                        "play": video.get("play", 0),
                        "duration": video.get("length", "")
                    },
                    "stats": {
                        "view": video.get("play", 0),
                        "danmaku": video.get("video_review", 0),
                        "comment": video.get("comment", 0),
                        "favorite": video.get("favorites", 0)
                    }
                }
                items.append(item)
            
            return {
                "code": 0,
                "message": "success (视频列表转换)",
                "data": {
                    "items": items,
                    "has_more": len(vlist) >= 20,
                    "source": "video_list"
                }
            }
    except Exception as e:
        logger.error(f"获取视频列表失败: {e}")
    
    return {
        "code": -1,
        "message": "无法获取动态数据",
        "data": {"items": []}
    }
```

### 2. 修复用户视频API

```python
def get_user_videos(self, uid: str, page: int = 1, page_size: int = 30) -> Dict:
    """获取用户投稿视频列表（修复版）"""
    try:
        # 先尝试不需要WBI的接口
        url = "https://api.bilibili.com/x/space/arc/search"
        params = {
            "mid": uid,
            "ps": min(page_size, 50),  # 限制最大50
            "pn": page,
            "order": "pubdate"
        }
        
        # 增加请求间隔
        time.sleep(3)  # 固定3秒间隔避免-799错误
        
        headers = {
            "Referer": f"https://space.bilibili.com/{uid}/video",
            "Origin": "https://www.bilibili.com"
        }
        
        result = self._make_request(url, params=params, headers=headers)
        
        if isinstance(result, dict) and result.get("code") == 0:
            return result
        elif result.get("code") == -799:
            # 频率限制，增加等待时间
            logger.warning("触发频率限制，等待10秒后重试")
            time.sleep(10)
            return self._make_request(url, params=params, headers=headers)
        
        # 如果失败，尝试获取投稿统计
        return self._get_video_stats_as_fallback(uid)
        
    except Exception as e:
        logger.error(f"获取用户视频失败: {e}")
        return {
            "code": -1,
            "message": f"获取用户视频失败: {str(e)}",
            "data": {"list": {"vlist": []}}
        }

def _get_video_stats_as_fallback(self, uid: str) -> Dict:
    """获取用户投稿统计作为备用"""
    try:
        url = "https://api.bilibili.com/x/space/navnum"
        params = {"mid": uid}
        
        result = self._make_request(url, params=params)
        
        if isinstance(result, dict) and result.get("code") == 0:
            navnum = result.get("data", {})
            return {
                "code": 0,
                "message": "仅统计数据可用",
                "data": {
                    "page": {
                        "count": navnum.get("video", 0),
                        "pn": 1,
                        "ps": 0
                    },
                    "list": {
                        "vlist": []
                    },
                    "stats": navnum
                }
            }
    except:
        pass
    
    return {
        "code": -1,
        "message": "无法获取视频数据",
        "data": {"list": {"vlist": []}}
    }
```

### 3. 优化请求频率控制

```python
class BilibiliAPI:
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        # ... 其他初始化代码 ...
        
        # 优化请求间隔
        self.min_interval = 3.0  # 增加到3秒
        self.max_interval = 6.0  # 增加到6秒
        
        # API特定的间隔
        self.api_intervals = {
            "dynamics": 5.0,  # 动态API需要更长间隔
            "videos": 4.0,    # 视频API
            "search": 5.0,    # 搜索API
            "default": 3.0    # 默认间隔
        }
        
        # 记录每个API的最后请求时间
        self.last_api_request = {}
    
    def _get_api_interval(self, api_type: str) -> float:
        """获取特定API的请求间隔"""
        return self.api_intervals.get(api_type, self.api_intervals["default"])
    
    def _wait_for_api(self, api_type: str):
        """等待适当的时间间隔"""
        current_time = time.time()
        last_time = self.last_api_request.get(api_type, 0)
        required_interval = self._get_api_interval(api_type)
        
        if last_time > 0:
            elapsed = current_time - last_time
            if elapsed < required_interval:
                wait_time = required_interval - elapsed
                logger.debug(f"API {api_type} 等待 {wait_time:.2f} 秒")
                time.sleep(wait_time)
        
        self.last_api_request[api_type] = time.time()
```

## 📊 修复后的效果

### 预期改进

1. **用户动态API**
   - ✅ 使用旧版API避免WBI签名问题
   - ✅ 正确解析不同类型的动态内容
   - ✅ 提供备用方案（视频列表转换）

2. **用户视频API**
   - ✅ 增加请求间隔避免-799错误
   - ✅ 实现重试机制
   - ✅ 提供统计数据作为备用

3. **请求频率控制**
   - ✅ 为不同API设置不同的间隔
   - ✅ 智能等待机制
   - ✅ 避免触发反爬限制

## 🚀 实施步骤

1. **更新main.py文件**
   - 替换现有的API实现
   - 添加新的辅助函数
   - 优化错误处理

2. **增加请求间隔**
   - 调整min_interval和max_interval
   - 实现API特定的间隔控制

3. **改进数据解析**
   - 处理多层嵌套的JSON
   - 统一时间格式
   - 标准化返回格式

4. **添加备用方案**
   - 当主API失败时自动切换
   - 提供降级服务
   - 保证基本功能可用

## 📈 测试验证

修复后应进行以下测试：

1. **功能测试**
   - 测试不同用户的动态获取
   - 验证视频列表的准确性
   - 检查错误处理机制

2. **性能测试**
   - 验证请求间隔是否生效
   - 测试是否还会触发-799错误
   - 评估整体响应时间

3. **准确性测试**
   - 对比官网显示的数据
   - 验证时间戳转换
   - 检查数据完整性

## 💡 长期优化建议

1. **实现完整的WBI签名**
   - 研究B站最新的WBI算法
   - 动态更新签名密钥
   - 支持所有需要WBI的API

2. **添加缓存机制**
   - 缓存用户信息
   - 缓存热门数据
   - 减少重复请求

3. **使用异步请求**
   - 提高并发能力
   - 优化响应时间
   - 更好的错误恢复

4. **监控和日志**
   - 记录API成功率
   - 追踪错误模式
   - 自动调整策略

## 📝 总结

通过以上修复方案，可以显著提高B站API的数据准确性和可靠性。重点是：

- **使用合适的API版本** - 避免需要复杂认证的接口
- **智能的请求控制** - 防止触发反爬机制
- **完善的错误处理** - 提供备用方案和降级服务
- **准确的数据解析** - 处理各种数据格式和结构

实施这些修复后，用户动态、视频列表等接口的准确性将大大提升。