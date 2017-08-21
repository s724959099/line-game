# from games.tod_game import template
# from utli.base_import import *
from utli import db
from utli import color_print as cp
from utli.tool import *

user_list = []
RECEIVE_PRE_COLOR = cp.colors.white
RECEIVE_MESSAGE_COLOR = cp.colors.yellow


class Group:
    group_id = 999

    def __init__(self):
        self.users = user_list

    def receive(self, msg):
        cp.p("-------------群組start-------------\n", RECEIVE_PRE_COLOR)
        cp.p(msg, RECEIVE_MESSAGE_COLOR)
        cp.p("-------------群組end-------------\n", RECEIVE_PRE_COLOR)


class LineAPI:
    print("t2")
    def __init__(self, event):
        self.event = event
        self.group = Group()

    def __send(self, user_id, msg):
        if isinstance(msg, str):
            msg = text_message(msg)
        if self.group.group_id == user_id:
            self.group.receive(msg)
        else:
            for user in self.event.user_list:
                if user.profile["user_id"] == user_id:
                    user.receive(msg)
                    break

    def reply(self, msg):
        if self.event.source.type == "group":
            self.__send(self.group.group_id, msg)
        else:
            self.__send(self.event.source.user_id, msg)

    def push(self, user_id, msg):
        self.__send(user_id, msg)

    def reply_template(self, title, text, messages):
        while len(messages) > 4:
            pop = []
            while len(pop) <= 4 and len(messages) > 0:
                pop.append(messages.pop())
            self.reply(template(title, text, pop))

    def get_profile(self, user_id):
        for user in self.event.user_list:
            if user.profile["user_id"] == user_id:
                profile_dict = user.profile
                profile = MockClass()
                profile.display_name = profile_dict["display_name"]
                profile.picture_url = profile_dict["picture_url"]
                profile.status_message = profile_dict["status_message"]
                profile.user_id = profile_dict["user_id"]
                return profile


class User:
    message_type = MockClass()
    message_type.group = 1
    message_type.user = 2

    def __init__(self, profile):
        self.profile = profile

    def receive(self, msg):
        cp.p("-------------user:{} start-------------\n".format(self.profile["display_name"]), RECEIVE_PRE_COLOR)
        cp.p(msg, RECEIVE_MESSAGE_COLOR)
        cp.p("-------------user:{} end-------------\n".format(self.profile["display_name"]), RECEIVE_PRE_COLOR)

    def speak(self, message, message_type=message_type.group):
        """
        希望輸出 user[{}] speak: {}
        """

        cp.colorful("user[{}] speak: {}", (self.profile["display_name"], cp.colors.green), (message, cp.colors.blue))

        event = MockClass()
        event.message = MockClass()
        event.message.text = message
        event.source = MockClass()
        event.source.user_id = self.profile["user_id"]
        if self.message_type.group == message_type:
            event.source.type = "group"
            event.source.group_id = Group.group_id
        else:
            event.source.type = "user"
        event.user_list = user_list
        import linebot_commands
        linebot_commands.events_excute(event)


def base_template(title, msg, url, messages):
    options_text = ""
    index = 1
    for item in messages:
        if isinstance(item, str):
            options_text += "{} 選項是： {} \n".format(index, item)
        else:
            options_text += "{} 選項是： {} ()\n".format(index, item[0], item[1])
        index += 1
    result = """
title={}
text={}
url={}
-------------------
{}
""".format(title, msg, url, options_text)
    return result


def text_message(content):
    return content


def image_message(url):
    return "圖片網址： " + url


class UserFactory:
    index = 1

    @classmethod
    def get_instance(cls, name=None):
        if name is None:
            name = "test{}".format(cls.index)
        profile = {
            'display_name': name,
            'picture_url': None,
            'status_message': "無",
            'user_id': cls.index,
        }
        cls.index += 1
        return User(profile)


if __name__ == "__main__":
    db.write_json({})
    user_list.extend([
        UserFactory.get_instance(),
        UserFactory.get_instance(),
        UserFactory.get_instance(),
        UserFactory.get_instance(),
        UserFactory.get_instance(),
    ])
    user_list[0].speak("開始玩")
    user_list[0].speak("間諜遊戲")
    for user in user_list:
        user.speak("我")
    user_list[0].speak("遊戲人數")
    user_list[0].speak("OK")
    user_list[0].speak("重新開始")
    user_list[0].speak("結束遊戲")
