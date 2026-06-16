# Telegram Bio 双向联系中转机器人

一个适合放在 **Telegram 个人资料简介 Bio** 里的双向联系机器人。

当你的 Telegram 账号风控不方便主动私信别人，或者你不想公开主号私信入口时，可以把机器人链接放在个人资料简介里。对方主动点击机器人链接并发送消息后，机器人会把消息转发给你；你直接回复机器人转发来的那条消息，机器人会把回复发回给对方。

```txt
对方 → 点击你个人资料 Bio 里的机器人链接
对方 → 主动给机器人发送 /start 或消息
机器人 → 把消息转发给你
你 → 回复机器人转发来的那条消息
机器人 → 自动把回复发回给对方
```
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
- 已加中文注释，方便修改

---

## 适合场景

- Telegram 个人资料简介联系方式
- 主号触发限制、不方便主动私信别人时的被动联系入口
- 不想把主号直接公开给陌生人私信
- 让别人通过机器人主动留言
- 项目反馈机器人
- 频道投稿机器人
- 客服 / 咨询机器人
---

## 项目结构

```txt
Telegram-bio-contact-bot/
├─ bot.py                # 机器人主程序，核心逻辑都在这里
├─ requirements.txt      # Python 依赖列表
├─ render.yml            # Render 一键部署配置
└─ README.md             # GitHub 仓库说明文档
```

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

使用 Telegram 里的 ID 查询机器人获取数字 ID。

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

---

## 常见问题

### 1. 机器人没有反应怎么办？

检查：

- `BOT_TOKEN` 是否正确
- `OWNER_ID` 是否是纯数字
- Render / VPS 服务是否正在运行
- 机器人是否已经部署成功
- 是否给机器人发送过 `/start`

### 2. 回复失败怎么办？

你必须回复机器人转发过来的那条消息。

如果只是直接给机器人发新消息，机器人不知道要回复给谁。

### 3. 可以把 BOT_TOKEN 写进代码吗？

不可以！ Token 上传到 GitHub 后可能泄露。

---

## 安全提醒

请不要公开：

- `BOT_TOKEN`
- `.env` 文件
- 管理员真实数字 ID 截图

如果 Token 泄露，请立刻去 BotFather 重新生成 Token。

---

## License

本项目可用于个人学习、Telegram 个人资料联系入口和二次修改。请遵守 Telegram 平台规则。
