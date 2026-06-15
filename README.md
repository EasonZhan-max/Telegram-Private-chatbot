# Telegram Bio 双向联系中转机器人

一个适合放在 **Telegram 个人资料简介 Bio** 里的双向联系机器人。

当你的 Telegram 账号不方便主动私信别人，或者你不想公开主号私信入口时，可以把机器人链接放在个人资料简介里。对方主动点击机器人链接并发送消息后，机器人会把消息转发给你；你直接回复机器人转发来的那条消息，机器人会把回复发回给对方。

```txt
对方 → 点击你个人资料 Bio 里的机器人链接
对方 → 主动给机器人发送 /start 或消息
机器人 → 把消息转发给你
你 → 回复机器人转发来的那条消息
机器人 → 自动把回复发回给对方
```

> 说明：这是一个“被动联系入口 / 双向中转工具”。它不能主动私信从未启动过机器人的用户，也不应该用于群发广告、骚扰陌生人或绕过平台风控规则。

---

## 功能特点

- 支持 Telegram 私聊双向回复
- 适合放在 Telegram 个人资料简介 Bio 里
- 适合账号不方便主动私信时，让别人主动留言联系你
- 不需要公开主号私信入口
- 支持文字、图片、视频、文件、语音、音频、贴纸、动图等消息
- 支持 `/start`、`/help`、`/id` 命令
- 适合部署到 Render / Railway / VPS / 宝塔面板
- 只需要配置 `BOT_TOKEN` 和 `OWNER_ID`
- 代码已加中文注释，方便新手修改

---

## 适合场景

- Telegram 个人资料简介联系方式
- 主号触发限制、不方便主动私信别人时的被动联系入口
- 不想把主号直接公开给陌生人私信
- 让别人通过机器人主动留言
- 项目反馈机器人
- 频道投稿机器人
- 客服 / 咨询机器人

不适合用于：

- 批量私信陌生人
- 群发广告
- 骚扰用户
- 规避 Telegram 平台规则

---

## 项目结构

```txt
Telegram-bio-contact-bot/
├─ bot.py                # 机器人主程序，核心逻辑都在这里
├─ requirements.txt      # Python 依赖列表
├─ render.yml            # Render 一键部署配置
├─ .env.example          # 环境变量示例文件
├─ .gitignore            # GitHub 忽略文件配置
└─ README.md             # GitHub 仓库说明文档
```

---

## 工作原理

这个机器人本质上是一个“消息中转站”：

1. 对方先主动打开机器人并发送消息。
2. 机器人把对方的消息转发给你。
3. 你回复机器人转发来的那条消息。
4. 机器人根据消息记录，把你的回复发回原用户。

注意：你必须 **回复机器人转发来的那条消息**，不能直接给机器人发一句新消息。否则机器人不知道要回复给哪个用户。

---

## 准备工作

部署前需要准备两个环境变量：

| 变量名 | 说明 |
|---|---|
| `BOT_TOKEN` | BotFather 给你的机器人 Token |
| `OWNER_ID` | 你自己的 Telegram 数字 ID |

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
3. 新建 Worker / Background Worker
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

## 怎么放到 Telegram 个人资料简介？

部署成功后，你会得到一个机器人用户名，例如：

```txt
@your_contact_bot
```

你的机器人链接就是：

```txt
https://t.me/your_contact_bot
```

然后打开 Telegram：

```txt
设置 → 编辑个人资料 → 简介 / Bio → 粘贴机器人链接
```

推荐简介：

```txt
联系请走机器人留言：https://t.me/your_contact_bot
```

更适合“不能主动私信别人”这个场景的写法：

```txt
如果我无法主动私信你，请在这里留言：https://t.me/your_contact_bot
```

更短一点：

```txt
私信留言入口：https://t.me/your_contact_bot
```

---

## 使用方法

### 对方怎么联系你？

对方点开你 Telegram 个人资料简介里的机器人链接，然后发送：

```txt
/start
```

之后可以直接发送文字、图片、视频、语音或文件。

### 你怎么回复对方？

你收到机器人转发的消息后，需要直接回复那条转发消息。

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
| 回复成功提示 | `OWNER_REPLY_OK_TEXT` |
| 未正确回复提示 | `OWNER_NEED_REPLY_TEXT` |
| 不支持消息提示 | `UNSUPPORTED_TEXT` |
| 支持的消息类型 | `SUPPORTED_CONTENT_TYPES` |

---

## Telegram 个人资料简介文案

相关文案已经放在：

```txt
TELEGRAM_PROFILE.md
```

里面包含：

- 个人资料简介 Bio 文案
- 机器人 About 简短简介
- 机器人 Description 详细介绍
- BotFather Commands 命令列表

---

## 常见问题

### 1. 这个机器人可以主动私信别人吗？

不可以。

Telegram 机器人一般不能主动给从未启动过机器人的用户发私信。对方需要先点击机器人并发送 `/start` 或任意消息，机器人才能在这个聊天里回复。Telegram 官方 FAQ 也说明，BotFather 用于创建机器人并连接后端，机器人可以接收用户私聊消息；官方功能页也说明用户可以向机器人发送文本、文件、位置、贴纸、语音等内容。

所以这个项目的正确用法是：

```txt
把机器人链接放到个人资料简介 → 对方主动打开机器人留言 → 你通过机器人回复
```

### 2. 机器人没有反应怎么办？

检查：

- `BOT_TOKEN` 是否正确
- `OWNER_ID` 是否是纯数字
- Render / VPS 服务是否正在运行
- 机器人是否已经部署成功
- 是否给机器人发送过 `/start`

### 3. 回复失败怎么办？

你必须回复机器人转发过来的那条消息。

如果只是直接给机器人发新消息，机器人不知道要回复给谁。

### 4. 重启后旧消息为什么不能回复？

当前版本使用内存变量保存消息对应关系：

```python
message_map = {}
```

机器人重启后，内存会清空，所以旧消息对应关系会丢失。

如果要长期稳定使用，可以后期接入数据库，例如：

- SQLite
- PostgreSQL
- Redis

### 5. 可以把 BOT_TOKEN 写进代码吗？

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

本项目可用于个人学习、Telegram 个人资料联系入口和二次修改。请遵守 Telegram 平台规则，不要用于骚扰、垃圾消息或违法用途。
