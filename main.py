import os
import sys
from random import randint
import json
import tweepy
import requests
from urllib import request
from argparse import ArgumentParser
from requests_oauthlib import OAuth1Session

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import parts

app = Flask(__name__)

# LINEのAPIキーを環境変数からもってくる
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

url = "https://public-api.tracker.gg/v2/apex/standard/profile"
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
# 触るな
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
        abort(400)

    return 'OK'

#メッセージ受け取ったとき
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    main = parts.Main()
    di = parts.to_dict()

    txt_list = event.message.text.split()
    cmd_list = ["!","?","|","/","r","add","del","v"]
    if txt_list[0] in cmd_list:
        try:
            if txt_list[0] == "!":
                res = main.track(txt_list[1],txt_list[2],txt_list[3])
            elif txt_list[0] == "?":
                res = main.neta(txt_list[1])
            elif txt_list[0] == "|":
                res = main.loop(txt_list[1],txt_list[2])
            elif txt_list[0] == "/":
                res = main.get_tweet(txt_list[1],txt_list[2])
            elif txt_list[0] =="r":
                res = main.random(txt_list[1],txt_list[2])
            elif txt_list[0] == "add":
                res = di.add_user(txt_list[1],txt_list[2])
            elif txt_list[0] == "tw":
                res = di.add_twitter(txt_list[1],txt_list[2])
            elif txt_list[0] == "del":
                res = di.del_dict(txt_list[1])
            elif txt_list[0] == "v":
                res = di.view_dict()

            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res))
        except:
            return f"An error occurred during program execution. Please ask the administrator for details."+"/"+sys._getframe().f_code.co_name
        
    # それ以外(ただの会話とか)ならスルー
    else:
        pass


#変えるな
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)