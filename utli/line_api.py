import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
                            TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, URITemplateAction)
from utli.commands import Invoker, SimpleCommandFactory

try:
    import api_key

    channel_access_token = api_key.channel_access_token
    channel_secret = api_key.channel_secret
except Exception as e:
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
        if isinstance(msg, str):
            msg = text_message(msg)
        self.line_bot_api.reply_message(self.event.reply_token, msg)

    def push(self, user_id, msg):
        try:
            if isinstance(msg, str):
                msg = text_message(msg)
            self.line_bot_api.push_message(user_id, msg)
        except Exception as e:
            print("done")

    def reply_template(self, title, text, url, messages):
        while len(messages) > 4:
            pop = []
            while len(pop) <= 4 and len(messages) > 0:
                pop.append(messages.pop())
            self.reply(base_template(title, text, url, pop))

    def get_profile(self, user_id):
        """
        profile.display_name
        profile.user_id
        profile.picture_url
        profile.status_message
        :param user_id:
        :return:
        """
        profile = line_bot_api.get_profile(user_id)
        return profile


def base_template(title, msg, url, messages):
    actions = []
    for message in messages:
        if isinstance(message, str):
            actions.append(MessageTemplateAction(
                label=message,
                text=message
            ))
        else:
            actions.append(URITemplateAction(
                label=message[0],
                uri=message[1]
            ))
    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title=title,
            text=msg,
            thumbnail_image_url=url,
            actions=actions
        )
    )
    return buttons_template


def text_message(content):
    return TextSendMessage(text=content)


def image_message(url):
    return ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
    )
