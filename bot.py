"""
Telegram 私聊双向机器人

功能说明：
1. 普通用户私聊机器人，机器人会把消息转发给管理员。
2. 管理员回复机器人转发过来的消息，机器人会把回复发回原用户。
3. 适合作为 Telegram 个人资料简介里的联系入口。

重要提醒：
- BOT_TOKEN 和 OWNER_ID 必须放在环境变量里，不要写死在代码中。
- message_map 默认保存在内存里，机器人重启后，旧消息的回复关系会丢失。
"""

# os：用于读取环境变量，例如 BOT_TOKEN、OWNER_ID
import os

# logging：用于输出运行日志，方便在 Render / VPS 后台查看问题
import logging

# Dict：用于给字典变量添加类型标注，让代码更清楚
from typing import Dict

# telebot：pyTelegramBotAPI 的主要模块，用来连接 Telegram Bot API
import telebot

# Message：Telegram 消息对象的类型标注，方便理解函数参数
from telebot.types import Message


# ==============================
# 1. 日志配置
# ==============================

# 设置日志等级为 INFO：正常运行信息、错误信息都会显示出来
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 创建一个日志对象，后面用 logger.info / logger.error 输出日志
logger = logging.getLogger(__name__)


# ==============================
# 2. 读取环境变量
# ==============================

# BOT_TOKEN：从 BotFather 获取的机器人 Token
# 注意：不要把 Token 直接写进代码，也不要上传到 GitHub
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()

# OWNER_ID：管理员自己的 Telegram 数字 ID，不是 @用户名
OWNER_ID_RAW = os.environ.get("OWNER_ID", "").strip()

# 如果没有设置 BOT_TOKEN，直接停止程序，并提示原因
if not BOT_TOKEN:
    raise RuntimeError("缺少环境变量 BOT_TOKEN，请先在 Render / VPS 中添加 BOT_TOKEN")

# 如果没有设置 OWNER_ID，直接停止程序，并提示原因
if not OWNER_ID_RAW:
    raise RuntimeError("缺少环境变量 OWNER_ID，请先填写你的 Telegram 数字 ID")

# OWNER_ID 必须是数字，所以这里转换成 int
try:
    OWNER_ID = int(OWNER_ID_RAW)
except ValueError as exc:
    raise RuntimeError("OWNER_ID 必须是纯数字，例如 123456789，不要填写 @用户名") from exc


# ==============================
# 3. 创建机器人实例
# ==============================

# 使用 BOT_TOKEN 创建 bot 对象，后面所有收发消息都通过 bot 完成
bot = telebot.TeleBot(BOT_TOKEN)


# ==============================
# 4. 可自定义文案
# ==============================

# 用户发送 /start 时看到的欢迎语
WELCOME_TEXT = (
    "你好，这里是 Telegram 联系机器人。\n\n"
    "你可以直接发送文字、图片、视频、语音或文件，"
    "消息会自动转交给本人。"
)

# 用户消息成功转发给管理员后，用户看到的提示
USER_SENT_TEXT = "消息已发送给本人，请等待回复。"

# 本人回复用户成功后，自己看到的提示
OWNER_REPLY_OK_TEXT = "回复已发送给对方。"

# 本人没有回复指定消息时，机器人给出的提示
OWNER_NEED_REPLY_TEXT = "请回复一条用户消息，我才能知道要发给谁。"

# 机器人不支持某种消息时的提示
UNSUPPORTED_TEXT = "暂时不支持这种消息类型，请换成文字、图片、视频、语音或文件。"


# ==============================
# 5. 消息映射表
# ==============================

# message_map 用来记录：
# key   = 机器人转发给管理员后的消息 ID
# value = 原始用户的 Telegram ID
#
# 例子：
# 用户 A 发消息给机器人 → 机器人转发给管理员 → 转发消息 ID 是 100
# message_map[100] = 用户 A 的 ID
# 管理员回复 ID 100 这条消息时，机器人就知道要回复给用户 A
message_map: Dict[int, int] = {}


# ==============================
# 6. 支持的消息类型
# ==============================

# 这里决定机器人会处理哪些消息类型
# 想支持更多类型，可以继续往列表里加
SUPPORTED_CONTENT_TYPES = [
    "text",        # 文字消息
    "photo",       # 图片消息
    "video",       # 视频消息
    "document",    # 文件消息
    "voice",       # 语音消息
    "audio",       # 音频消息
    "sticker",     # 贴纸消息
    "animation",   # GIF / 动图消息
    "video_note",  # 圆形视频消息
    "location",    # 位置消息
    "contact",     # 联系人消息
]


# ==============================
# 7. 工具函数：生成用户信息
# ==============================

def build_user_info(message: Message) -> str:
    """
    生成发送给本人的用户信息文本。

    参数：
    - message：普通用户发送给机器人的消息对象

    返回：
    - 一段包含用户昵称、用户名、用户 ID 的文本
    """

    # 获取发送消息的用户对象
    user = message.from_user

    # first_name 和 last_name 可能为空，所以用 or "" 防止显示 None
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    # username 可能为空，没有用户名时显示“无”
    username = f"@{user.username}" if user.username else "无"

    # 返回最终显示给本人的消息说明
    return (
        "📩 收到一条新私信\n\n"
        f"昵称：{full_name or '无'}\n"
        f"用户名：{username}\n"
        f"用户ID：{user.id}\n\n"
        "请直接回复下面转发的消息。"
    )


# ==============================
# 8. 工具函数：管理员回复用户
# ==============================

def send_owner_reply_to_user(message: Message, user_id: int) -> None:
    """
    把本人回复的内容发送给原用户。

    参数：
    - message：本人发给机器人的回复消息
    - user_id：原用户的 Telegram ID
    """

    # 文字消息
    if message.text:
        bot.send_message(user_id, message.text)

    # 图片消息：Telegram 可能会提供多种尺寸，[-1] 通常是最清晰的一张
    elif message.photo:
        bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)

    # 视频消息
    elif message.video:
        bot.send_video(user_id, message.video.file_id, caption=message.caption)

    # 文件消息
    elif message.document:
        bot.send_document(user_id, message.document.file_id, caption=message.caption)

    # 语音消息
    elif message.voice:
        bot.send_voice(user_id, message.voice.file_id)

    # 音频消息
    elif message.audio:
        bot.send_audio(user_id, message.audio.file_id, caption=message.caption)

    # 贴纸消息
    elif message.sticker:
        bot.send_sticker(user_id, message.sticker.file_id)

    # GIF / 动图消息
    elif message.animation:
        bot.send_animation(user_id, message.animation.file_id, caption=message.caption)

    # 圆形视频消息
    elif message.video_note:
        bot.send_video_note(user_id, message.video_note.file_id)

    # 位置消息
    elif message.location:
        bot.send_location(
            user_id,
            latitude=message.location.latitude,
            longitude=message.location.longitude
        )

    # 联系人消息
    elif message.contact:
        bot.send_contact(
            user_id,
            phone_number=message.contact.phone_number,
            first_name=message.contact.first_name,
            last_name=message.contact.last_name or ""
        )

    # 如果没有匹配到任何支持的类型，就提示不支持
    else:
        bot.reply_to(message, UNSUPPORTED_TEXT)


# ==============================
# 9. /start 命令
# ==============================

@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    """
    用户发送 /start 时触发。
    主要用于显示欢迎语和使用说明。
    """

    bot.reply_to(message, WELCOME_TEXT)


# ==============================
# 10. /help 命令
# ==============================

@bot.message_handler(commands=["help"])
def help_command(message: Message) -> None:
    """
    用户发送 /help 时触发。
    用来告诉用户机器人支持哪些内容。
    """

    help_text = (
        "使用方法：\n\n"
        "1. 直接给我发送消息，我会转交给管理员。\n"
        "2. 支持文字、图片、视频、文件、语音、音频、贴纸等。\n"
        "3. 我回复后，你会在这里收到回复。"
    )
    bot.reply_to(message, help_text)


# ==============================
# 11. /id 命令
# ==============================

@bot.message_handler(commands=["id"])
def show_user_id(message: Message) -> None:
    """
    用户发送 /id 时触发。
    这个命令方便管理员快速查看自己的 Telegram 数字 ID。
    """

    bot.reply_to(message, f"你的 Telegram 数字 ID 是：{message.from_user.id}")


# ==============================
# 12. 主消息处理函数
# ==============================

@bot.message_handler(content_types=SUPPORTED_CONTENT_TYPES)
def handle_message(message: Message) -> None:
    """
    处理普通消息。

    分两种情况：
    1. 消息来自本人：说明本人可能正在回复用户。
    2. 消息来自普通用户：把消息转发给管理员。
    """

    # ------------------------------
    # 情况 1：本人发来的消息
    # ------------------------------
    if message.from_user.id == OWNER_ID:

        # 本人必须“回复”机器人转发过来的消息
        # 如果没有 reply_to_message，机器人就不知道要回复给哪个用户
        if not message.reply_to_message:
            bot.reply_to(message, OWNER_NEED_REPLY_TEXT)
            return

        # 获取本人回复的那条消息 ID
        replied_message_id = message.reply_to_message.message_id

        # 检查这条消息 ID 是否在 message_map 中
        if replied_message_id not in message_map:
            bot.reply_to(message, OWNER_NEED_REPLY_TEXT)
            return

        # 从映射表中找到原用户 ID
        target_user_id = message_map[replied_message_id]

        try:
            # 把本人回复的内容发送给原用户
            send_owner_reply_to_user(message, target_user_id)

            # 给自己一个成功提示
            bot.reply_to(message, OWNER_REPLY_OK_TEXT)

            # 写入日志，方便后台查看
            logger.info("本人已回复用户：%s", target_user_id)

        except Exception as exc:
            # 如果发送失败，把错误显示给管理员
            logger.exception("回复用户失败")
            bot.reply_to(message, f"发送失败：{exc}")

        return

    # ------------------------------
    # 情况 2：普通用户发来的消息
    # ------------------------------

    try:
        # 先把用户信息发送给本人
        bot.send_message(OWNER_ID, build_user_info(message))

        # 再把用户原消息转发给本人
        forwarded_message = bot.forward_message(
            OWNER_ID,          # 目标：本人
            message.chat.id,   # 来源：用户聊天窗口
            message.message_id # 要转发的消息 ID
        )

        # 记录“转发消息 ID”和“原用户 ID”的对应关系
        message_map[forwarded_message.message_id] = message.from_user.id

        # 给普通用户发送成功提示
        bot.reply_to(message, USER_SENT_TEXT)

        # 写入日志，方便后台查看
        logger.info("已收到用户 %s 的消息，并转发给本人", message.from_user.id)

    except Exception as exc:
        # 如果转发失败，把错误提示给用户
        logger.exception("转发用户消息失败")
        bot.reply_to(message, f"发送失败：{exc}")


# ==============================
# 13. 兜底处理：不支持的消息类型
# ==============================

@bot.message_handler(func=lambda message: True)
def fallback(message: Message) -> None:
    """
    如果消息没有被前面的处理函数接收，就会来到这里。
    作用是给用户一个友好的提示，而不是完全没有反应。
    """

    bot.reply_to(message, UNSUPPORTED_TEXT)


# ==============================
# 14. 启动机器人
# ==============================

if __name__ == "__main__":
    # 输出启动日志
    logger.info("机器人已启动，正在监听 Telegram 消息...")

    # infinity_polling 表示一直轮询 Telegram 消息
    # skip_pending=True 表示启动时跳过离线期间积压的旧消息
    bot.infinity_polling(skip_pending=True)
