# Cookie配置指南

## 🔒 隐私保护说明

本项目已对所有敏感信息进行脱敏处理，`cookie_example.json` 文件中的所有Cookie值均为占位符，不包含任何真实的用户信息。

## 📋 Cookie获取步骤

### 方法一：通过浏览器开发者工具

1. **登录B站**
   - 打开 [bilibili.com](https://www.bilibili.com)
   - 使用您的账号登录

2. **打开开发者工具**
   - 按 `F12` 键（或右键选择"检查"）
   - 切换到 `Network`（网络）标签页

3. **获取Cookie**
   - 刷新页面（F5）
   - 点击任意一个请求
   - 在 `Request Headers` 中找到 `Cookie` 字段
   - 复制完整的Cookie字符串

### 方法二：通过浏览器设置

1. **Chrome浏览器**
   - 地址栏输入：`chrome://settings/content/cookies`
   - 搜索 `bilibili.com`
   - 查看并复制需要的Cookie值

2. **Firefox浏览器**
   - 按 `F12` → `Storage` → `Cookies` → `https://www.bilibili.com`
   - 查看并复制需要的Cookie值

## 🔑 重要Cookie字段说明

| Cookie名称 | 作用说明 | 重要程度 |
|------------|----------|----------|
| `SESSDATA` | 用户会话标识，最重要的认证Cookie | ⭐⭐⭐⭐⭐ |
| `bili_jct` | CSRF令牌，用于防止跨站请求伪造 | ⭐⭐⭐⭐⭐ |
| `DedeUserID` | 用户ID，标识当前登录用户 | ⭐⭐⭐⭐ |
| `DedeUserID__ckMd5` | 用户ID的MD5校验值 | ⭐⭐⭐⭐ |
| `buvid3` | 浏览器唯一标识符 | ⭐⭐⭐ |
| `buvid4` | 新版浏览器标识符 | ⭐⭐⭐ |
| `sid` | 会话ID | ⭐⭐ |
| `b_nut` | 用户注册时间戳 | ⭐⭐ |
| `buvid_fp` | 浏览器指纹 | ⭐⭐ |

## 📝 配置示例

### 完整配置（推荐）

```json
{
  "SESSDATA": "您的SESSDATA值",
  "bili_jct": "您的bili_jct值",
  "DedeUserID": "您的用户ID",
  "DedeUserID__ckMd5": "您的MD5值",
  "sid": "您的会话ID",
  "buvid3": "您的buvid3值",
  "buvid4": "您的buvid4值",
  "b_nut": "时间戳",
  "buvid_fp": "您的指纹值",
  "b_lsid": "您的本地会话ID",
  "_uuid": "您的UUID值",
  "CURRENT_FNVAL": "4048",
  "enable_web_push": "DISABLE",
  "rpdid": "您的rpdid值",
  "home_feed_column": "5",
  "theme-tip-show": "SHOWED",
  "theme-avatar-tip-show": "SHOWED",
  "bili_ticket": "您的bili_ticket值",
  "bili_ticket_expires": "过期时间戳",
  "bp_t_offset_您的用户ID": "您的偏移值",
  "CURRENT_QUALITY": "120",
  "browser_resolution": "1462-725"
}
```

### 最小配置（基本功能）

```json
{
  "SESSDATA": "您的SESSDATA值",
  "bili_jct": "您的bili_jct值",
  "DedeUserID": "您的用户ID",
  "buvid3": "您的buvid3值"
}
```

## ⚠️ 安全注意事项

### 🔐 Cookie安全

1. **保密性**
   - Cookie包含您的登录凭证，请妥善保管
   - 不要将Cookie分享给他人
   - 不要在公共场所或不安全的网络环境下获取Cookie

2. **时效性**
   - Cookie有过期时间，通常为几天到几周
   - 如遇到"未登录"或"认证失败"错误，请更新Cookie
   - 建议定期更新Cookie以确保功能正常

3. **存储安全**
   - 不要将包含真实Cookie的配置文件提交到公共代码仓库
   - 建议将 `cookie_example.json` 添加到 `.gitignore` 文件中
   - 在本地使用时，确保文件权限设置合理

### 🚫 禁止行为

- ❌ 不要使用他人的Cookie
- ❌ 不要将Cookie用于恶意目的
- ❌ 不要进行大规模自动化操作
- ❌ 不要违反B站的服务条款

## 🔧 配置验证

配置完成后，可以运行以下测试脚本验证Cookie是否有效：

```bash
# 测试Cookie加载
python test_cookie_loading.py

# 测试API功能
python test_api_functionality.py
```

成功的输出应该包含：
- ✅ Cookie加载成功
- ✅ 用户登录状态：已登录
- ✅ API调用成功

## 🆘 常见问题

### Q1: Cookie获取后仍然提示未登录？
**A1**: 检查以下几点：
- 确保Cookie格式正确（JSON格式）
- 确认SESSDATA和bili_jct字段存在且不为空
- 尝试重新获取Cookie（可能已过期）

### Q2: 如何知道Cookie是否过期？
**A2**: 运行测试脚本，如果出现以下情况说明Cookie可能过期：
- 返回"未登录"状态
- API调用返回401或403错误
- 获取用户信息失败

### Q3: 是否需要配置所有Cookie字段？
**A3**: 不需要，最小配置只需要：
- `SESSDATA`（必需）
- `bili_jct`（必需）
- `DedeUserID`（推荐）
- `buvid3`（推荐）

### Q4: Cookie配置后功能仍不稳定？
**A4**: 可能的原因：
- B站反爬虫机制升级
- 请求频率过高
- 网络环境问题
- 建议降低请求频率并检查网络连接

## 📞 技术支持

如果在Cookie配置过程中遇到问题，欢迎联系：

**邮箱**：aqiuX17@yeah.net

请在邮件中详细描述问题和错误信息，我们会尽快为您解答。

---

**最后更新**：2025年1月

**版本**：v1.0.0