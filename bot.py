import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)


BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dsj7000"


FOOTER = """

━━━━━━━━━━━━━━

⚠️ 温馨提示

本频道所有信息均为免费发布，请注意甄别，谨防上当。

⌚骗术曝光   @jpzfzp
⌚骗子查询   @jpzfzpbot
⌚投稿发布机器人   @xges_bot
⌚柬埔寨交友   @jpzjy
⌚华人头条   @hwhrtt
⌚导航总群   @kaolaoerzhihuzheye
"""


# Render端口检测
class HealthCheck(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


def web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(
        ("0.0.0.0", port),
        HealthCheck
    )
    server.serve_forever()


# 消息处理
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if not msg:
        return


    print("收到消息")


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



threading.Thread(
    target=web_server,
    daemon=True
).start()


app = Application.builder().token(BOT_TOKEN).build()


app.add_handler(
    MessageHandler(
        filters.ALL,
        handle
    )
)


print("机器人启动成功")


app.run_polling()
