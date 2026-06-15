# Telegram 私聊双向留言机器人

一个适合个人博客、个人主页、频道简介使用的 Telegram 私聊双向机器人。

用户给机器人发送消息后，机器人会自动转发给管理员；管理员直接回复那条转发消息，机器人会把回复发回给原用户。

```txt
用户 → 私聊机器人 → 转发给管理员
管理员 → 回复转发消息 → 发回给原用户
```

---

## 功能特点

- 支持私聊双向回复
- 支持文字、图片、视频、文件、语音、音频、贴纸、动图等消息
- 支持 `/start`、`/help`、`/id` 命令
- 适合部署到 Render / Railway / VPS / 宝塔面板
- 配置简单，只需要 `BOT_TOKEN` 和 `OWNER_ID`
- 代码带中文注释，适合新手学习和二次修改

---

## 适合场景

- 个人博客留言入口
- Telegram 私信客服
- 匿名留言机器人
- 个人主页联系方式
- 项目反馈机器人
- 频道投稿机器人

---

## 项目结构

```txt
Telegram-bot-main/
├─ bot.py                # 机器人主程序，核心逻辑都在这里
├─ requirements.txt      # Python 依赖列表
├─ render.yml            # Render 一键部署配置
├─ .env.example          # 环境变量示例文件
├─ .gitignore            # GitHub 忽略文件配置
├─ TELEGRAM_PROFILE.md   # Telegram 主页简介文案
└─ README.md             # 项目说明文档
```

---

## 准备工作

部署前需要准备两个环境变量：

| 变量名 | 说明 |
|---|---|
| `BOT_TOKEN` | BotFather 给你的机器人 Token |
| `OWNER_ID` | 管理员自己的 Telegram 数字 ID |

注意：`OWNER_ID` 是纯数字，不是 `@用户名`。

---

## 获取 BOT_TOKEN

1. 打开 Telegram
2. 搜索 `@BotFather`
3. 发送 `/newbot`
4. 按提示创建机器人
5. 复制 BotFather 给你的 Token

Token 格式大概像这样：

```txt
1234567890:ABCxxxxxxxxxxxxxxxxxxxxxxxx
```

不要把 Token 发给别人，也不要直接写进代码。

---

## 获取 OWNER_ID

方法一：

1. 先运行本项目
2. 给机器人发送 `/id`
3. 机器人会返回你的 Telegram 数字 ID

方法二：

也可以使用 Telegram 里的 ID 查询机器人获取数字 ID。

---

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置环境变量

Windows PowerShell：

```powershell
$env:BOT_TOKEN="你的机器人Token"
$env:OWNER_ID="你的Telegram数字ID"
python bot.py
```

macOS / Linux：

```bash
export BOT_TOKEN="你的机器人Token"
export OWNER_ID="你的Telegram数字ID"
python bot.py
```

看到类似提示就说明启动成功：

```txt
机器人已启动，正在监听 Telegram 消息...
```

---

## 部署到 Render

本项目已经提供 `render.yml`，可以直接部署为后台 Worker。

### 部署步骤

1. Fork 或上传本项目到 GitHub
2. 打开 Render
3. New Project / New Worker
4. 选择你的 GitHub 仓库
5. Build Command 填：

```bash
pip install -r requirements.txt
```

6. Start Command 填：

```bash
python bot.py
```

7. 添加环境变量：

```txt
BOT_TOKEN = 你的机器人 Token
OWNER_ID = 你的 Telegram 数字 ID
```

8. 点击部署

部署成功后，给机器人发送 `/start` 测试。

---

## 使用方法

### 普通用户

用户打开机器人后，可以发送：

```txt
/start
```

然后直接发送文字、图片、视频、语音或文件即可。

---

### 管理员

管理员收到机器人转发的消息后，需要直接回复那条转发消息。

正确操作：

```txt
长按机器人转发的消息 → 回复 → 输入内容 → 发送
```

错误操作：

```txt
直接给机器人发一句新消息
```

因为直接发送新消息时，机器人不知道你要回复给哪个用户。

---

## 支持的消息类型

当前支持：

- 文字 text
- 图片 photo
- 视频 video
- 文件 document
- 语音 voice
- 音频 audio
- 贴纸 sticker
- 动图 animation
- 圆形视频 video_note
- 位置 location
- 联系人 contact

---

## 可修改位置

常用文案都在 `bot.py` 顶部的“可自定义文案”区域。

| 想修改什么 | 搜索关键词 |
|---|---|
| 欢迎语 | `WELCOME_TEXT` |
| 用户发送成功提示 | `USER_SENT_TEXT` |
| 管理员回复成功提示 | `OWNER_REPLY_OK_TEXT` |
| 管理员未正确回复提示 | `OWNER_NEED_REPLY_TEXT` |
| 不支持消息提示 | `UNSUPPORTED_TEXT` |
| 支持的消息类型 | `SUPPORTED_CONTENT_TYPES` |

---

## Telegram 主页简介

机器人主页简介文案已经放在：

```txt
TELEGRAM_PROFILE.md
```

里面包含：

- Bot Name
- About 简短简介
- Description 详细介绍
- Commands 命令列表
- 博客按钮文案

可以直接复制到 BotFather 里使用。

---

## 常见问题

### 机器人没有反应怎么办？

检查：

- `BOT_TOKEN` 是否正确
- `OWNER_ID` 是否是纯数字
- Render / VPS 服务是否正在运行
- 机器人是否已经部署成功
- 是否给机器人发送过 `/start`

---

### 管理员回复失败怎么办？

管理员必须回复机器人转发过来的那条消息。

如果只是直接给机器人发新消息，机器人不知道要回复给谁。

---

### 重启后旧消息为什么不能回复？

当前版本使用内存变量保存消息对应关系：

```python
message_map = {}
```

机器人重启后，内存会清空，所以旧消息对应关系会丢失。

如果要长期稳定使用，可以后期接入数据库，例如：

- SQLite
- PostgreSQL
- Redis

---

### 可以把 BOT_TOKEN 写进代码吗？

不建议。

错误做法：

```python
BOT_TOKEN = "你的机器人Token"
```

推荐做法：

```python
BOT_TOKEN = os.environ.get("BOT_TOKEN")
```

这样可以避免 Token 上传到 GitHub 后泄露。

---

## 后续可优化方向

- 增加多管理员支持
- 增加黑名单功能
- 增加关键词自动回复
- 增加数据库保存消息关系
- 增加 Web 管理后台
- 增加群组消息转发
- 增加用户来源统计

---

## 安全提醒

请不要公开：

- `BOT_TOKEN`
- `.env` 文件
- 管理员真实数字 ID 截图

如果 Token 泄露，请立刻去 BotFather 重新生成 Token。

---

## License

本项目可用于个人学习、个人博客、个人项目和二次修改。
