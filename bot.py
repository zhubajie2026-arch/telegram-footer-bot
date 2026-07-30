from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===========================
# 修改这里
# ===========================

BOT_TOKEN = "把这里改成你的Bot Token"

CHANNEL_ID = "@你的频道用户名"

FOOTER = """

━━━━━━━━━━━━━━

⚠️ 温馨提示

本频道所有信息均为免费发布，请自行甄别信息真实性，谨防诈骗。

🤝 初次交易建议先查看骗术曝光频道。

🔍 骗术曝光：@jpzfzp
🤖 投稿机器人：@xges_bot
📰 华人头条：@hwhrtt
📍 导航总群：@kaolaoerzhihuzheye
"""

# ===========================


async def receive(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if msg is None:
        return

    # 文字
    if msg.text:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=msg.text + FOOTER
        )

    # 图片
    elif msg.photo:

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=msg.photo[-1].file_id,
            caption=(msg.caption or "") + FOOTER
        )

    # 视频
    elif msg.video:

        await context.bot.send_video(
            chat_id=CHANNEL_ID,
            video=msg.video.file_id,
            caption=(msg.caption or "") + FOOTER
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.ALL,
        receive
    )
)

print("机器人启动成功...")

app.run_polling()
