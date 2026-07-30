import os
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)


# 从 Render 环境变量读取 Token
BOT_TOKEN = os.getenv("BOT_TOKEN")


# 你的频道
CHANNEL_ID = "@dsj7000"


# 固定小尾巴
FOOTER = """

━━━━━━━━━━━━━━

⚠️ 温馨提示

本频道所有信息均为免费发布，请自行甄别，谨防上当。

首次交易建议先查看骗术曝光频道，了解相关骗术。

⌚骗术曝光   @jpzfzp
⌚骗子查询   @jpzfzpbot
⌚投稿发布机器人   @xges_bot
⌚柬埔寨交友   @jpzjy
⌚华人头条   @hwhrtt
⌚导航总群   @kaolaoerzhihuzheye
"""


# 处理用户发送的信息
async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    msg = update.message

    if not msg:
        return


    # 文字消息
    if msg.text:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=msg.text + FOOTER
        )


    # 图片消息
    elif msg.photo:

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=msg.photo[-1].file_id,
            caption=(msg.caption or "") + FOOTER
        )


    # 视频消息
    elif msg.video:

        await context.bot.send_video(
            chat_id=CHANNEL_ID,
            video=msg.video.file_id,
            caption=(msg.caption or "") + FOOTER
        )



# 创建机器人
app = Application.builder().token(BOT_TOKEN).build()


# 接收所有消息
app.add_handler(
    MessageHandler(
        filters.ALL,
        handle_message
    )
)


print("机器人启动成功")


# 启动
app.run_polling()
