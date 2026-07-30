import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dsj7000"


FOOTER = """

━━━━━━━━━━━━━━

⚠️ 温馨提示

本频道所有信息均为免费发布，请注意甄别，谨防诈骗。

🔍 骗术曝光 @jpzfzp
🤖 投稿发布 @xges_bot
📰 华人头条 @hwhrtt
📍 导航总群 @kaolaoerzhihuzheye
"""


async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if not msg:
        return

    if msg.text:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=msg.text + FOOTER
        )

    elif msg.photo:
        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=msg.photo[-1].file_id,
            caption=(msg.caption or "") + FOOTER
        )

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
        forward
    )
)


print("机器人启动成功")


app.run_polling()
