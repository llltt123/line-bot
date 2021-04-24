from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('PRhGqvqNHs7Rdr4fYVo20wfdbJXhQsNNVzX9WNZ10y3x5eUGHVXLJjPQkvEGLUAbG9JwmYvbv3gQoiFYYXcSujd18P9o11pVyr2yUFTpcj/afIHkcxqLs0GyRqa9cn4O79wftXKhmWq/LQ6DEBeXoQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e3512e448e7a564b49fc642121966298')

#最長的access token 24 hours 會過期要重新re-issue 並上傳git
# git add .
# git commit -m" ".
# git push
# git push heroku

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉,您說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return # 不return東西的return 為了讓function結束掉

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()