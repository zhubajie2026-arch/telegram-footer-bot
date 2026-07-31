import os
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InputMediaPhoto
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

首次交易建议先查看骗术曝光频道。

⌚骗术曝光   @jpzfzp
⌚骗子查询   @jpzfzpbot
⌚投稿发布机器人   @xges_bot
⌚柬埔寨交友   @jpzjy
⌚华人头条   @hwhrtt
⌚导航总群   @kaolaoerzhihuzheye
"""


# Render端口
class HealthCheck(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


def run_web():

    port = int(os.environ.get("PORT", 10000))

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthCheck
    )

    server.serve_forever()



# 保存相册
album_cache = {}


async def send_album(group_id, context):

    await asyncio.sleep(5)

    album = album_cache.pop(group_id, None)

    if not album:
        return


    photos = album["photos"]
    caption = album["caption"]


    media = []

    for index, photo in enumerate(photos):

        if index == 0:

            media.append(
                InputMediaPhoto(
                    media=photo,
                    caption=caption + FOOTER
                )
            )

        else:

            media.append(
                InputMediaPhoto(
                    media=photo
                )
            )


    await context.bot.send_media_group(
        chat_id=CHANNEL_ID,
        media=media
    )



# 消息处理

async def handle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    msg = update.message

    if not msg:
        return


    print("收到消息")


    # 相册

    if msg.photo:

        if msg.media_group_id:

            group_id = msg.media_group_id


            if group_id not in album_cache:

                album_cache[group_id] = {
                    "photos": [],
                    "caption": msg.caption or ""
                }


            album_cache[group_id]["photos"].append(
                msg.photo[-1].file_id
            )


            # 只创建一个发送任务

            if len(album_cache[group_id]["photos"]) == 1:

                asyncio.create_task(
                    send_album(
                        group_id,
                        context
                    )
                )


            return



        # 单张图片

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=msg.photo[-1].file_id,
            caption=(msg.caption or "") + FOOTER
        )

        return



    # 视频

    if msg.video:

        await context.bot.send_video(
            chat_id=CHANNEL_ID,
            video=msg.video.file_id,
            caption=(msg.caption or "") + FOOTER
        )

        return



    # 文字

    if msg.text:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=msg.text + FOOTER
        )



threading.Thread(
    target=run_web,
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
