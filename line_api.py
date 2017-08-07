import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
                            TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, URITemplateAction)
from utli.commands import Invoker, SimpleCommandFactory

channel_access_token = os.environ.get("channel_access_token", "YOUR_CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("channel_secret", "YOUR_CHANNEL_SECRET")
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


class LineAPI:
    def __init__(self, event):
        self.event = event
        self.line_bot_api = line_bot_api
        self.type = event.source.type
        self.group_id = event.source.group_id if self.type == "group" else None
        self.user_id = event.source.user_id

    def reply(self, msg):
        self.line_bot_api.reply_message(self.event.reply_token, msg)

    def push(self, user_id, msg):
        try:
            self.line_bot_api.push_message(user_id, msg)
        except Exception as e:
            print("done")

    def reply_template(self, title, text, messages):
        while len(messages) > 4:
            pop = []
            while len(pop) <= 4 and len(messages) > 0:
                pop.append(messages.pop())
            self.reply(template(title, text, pop))

    def get_profile(self, user_id):
        profile = line_bot_api.get_profile(user_id)

        print(profile.display_name)
        print(profile.user_id)
        print(profile.picture_url)
        print(profile.status_message)
        return profile


def template(title, text, messages):
    actions = []
    for message in messages:
        actions.append(MessageTemplateAction(
            label=message,
            text=message
        ))
    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title=title,
            text=text,
            thumbnail_image_url='https://i.imgur.com/K9R7i8R.jpg',
            actions=actions
        )
    )
    return buttons_template


def text(content):
    return TextSendMessage(text=content)


def image(url):
    return ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
    )
