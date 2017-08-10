import random
from line_api import *
from utli import db


class SpyGame(db.Model):
    FILE = __file__

    def init_images(self):
        self.postion_images = [
            ("醫院", "https://i.imgur.com/ffgqsjU.png"),
            ("十字軍東征", "https://i.imgur.com/mIJZQkE.jpg"),
            ("海灘", "https://i.imgur.com/mRd9Hjb.jpg"),
            ("學校", "https://i.imgur.com/SVrPdGO.jpg"),
            ("演唱會", "https://i.imgur.com/PvyJ7rP.jpg"),
            ("月球", "https://i.imgur.com/UbBRqhS.jpg"),
            ("阿爾卑斯山", "https://i.imgur.com/5j0CHPP.jpg"),
            ("陰屍路", "https://i.imgur.com/hYrb1Pb.jpg"),
        ]
        self.spy_image = ("間諜", "https://i.imgur.com/K9R7i8R.jpg")

    def __init__(self):
        self.users = []
        self.spy_users = []
        self.picker_position = None
        self.init_images()

    def get_positions(self):
        return list(map(lambda item: item[0], self.postion_images))

    def picker_spy(self):
        while True:
            profile = random.choice(self.users)
            if profile not in self.spy_users:
                self.spy_users.append(profile)
                break

    def show_position(self, line):
        s = "場景為：\n"
        for item in self.get_positions():
            s += "{}\n".format(item)
        line.reply(s)

    def play(self, users, line):
        self.users = users
        if len(self.users) is None:
            line.reply("沒有玩家oops")
        print("user count=", len(users))
        user_count = len(users)
        spy_count = int(user_count / 3)
        if spy_count == 0:
            spy_count = 1
        self.spy_users = []
        for i in range(spy_count):
            self.picker_spy()

        self.picker_position = random.choice(self.postion_images)

    def show_card_to_user(self, line):
        for profile in self.users:
            if profile in self.spy_users:
                line.push(profile["user_id"], text_message(self.spy_image[0]))
                line.push(profile["user_id"], image_message(self.spy_image[1]))
            else:
                line.push(profile["user_id"], text_message(self.picker_position[0]))
                line.push(profile["user_id"], image_message(self.picker_position[1]))

    def show_spy(self, line):
        if self.users is None:
            return False
        msg = "間諜名單為:\n"
        msg += "-" * 30
        for profile in self.spy_users:
            msg += "\n"
            msg += profile["display_name"] + "\n"
            msg += "-" * 30

        line.reply(msg)
