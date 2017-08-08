import random
from line_api import *


class GameRoom:
    def __init__(self, group_id):
        self.group_id = group_id
        self.users = []

    def append_user(self, user_id,line):
        if self.in_users(user_id):
            return False
        self.users.append(user_id)
        line.reply(text("目前人數為＝{}".format(len(self.users))))
        return True

    def in_users(self, user_id):
        for item in self.users:
            if item == user_id:
                return True
        return False


class SpyGame:
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
        self.room = None
        self.init_images()

    def get_positions(self):
        return list(map(lambda item: item[0], self.postion_images))

    def picker_spy(self):
        while True:
            user_id = random.choice(self.room.users)
            if user_id not in self.room.spy_users:
                self.room.spy_users.append(user_id)
                break

    def show_position(self, line):
        s = "場景為：\n"
        for item in self.get_positions():
            s += "{}\n".format(item)
        line.reply(text(s))

    def play(self, line):
        if self.room is None:
            return False
        print("user count=", len(self.room.users))
        user_count = len(self.room.users)
        spy_count = int(user_count / 3)
        if spy_count == 0:
            spy_count = 1
        self.room.spy_users = []
        for i in range(spy_count):
            self.picker_spy()

        picker_position = random.choice(self.postion_images)
        self.show_position(line)
        for user in self.room.users:
            if user in self.room.spy_users:
                line.push(user, text(self.spy_image[0]))
                line.push(user, image(self.spy_image[1]))
            else:
                line.push(user, text(picker_position[0]))
                line.push(user, image(picker_position[1]))

    def show_spy(self, line):
        if self.room is None:
            return False
        msg = "間諜名單為:\n"
        for item in self.room.spy_users:
            profile = line.get_profile(item)
            msg += profile.display_name + "\n"
            msg += "-" * 30
        line.reply(text(msg))


class GameGroups:
    def __init__(self, Game):
        self.rooms = []
        self.game = Game()

    def append_group(self, group_id):
        if self.in_group(group_id):
            return False
        self.rooms.append(GameRoom(group_id))
        return True

    def append_user(self, group_id, user_id,line):
        def wrapper(room):
            if user_id is None:
                return False
            return room.append_user(user_id,line)

        return self.__search_group(group_id, wrapper)

    def __search_group(self, group_id, fn):
        for room in self.rooms:
            if room.group_id == group_id:
                return fn(room)
        return False

    def in_group(self, group_id):
        return self.__search_group(group_id, lambda room: True)

    def play(self, group_id, line):
        def wrapper(room):
            self.game.room = room
            return self.game.play(line)

        return self.__search_group(group_id, wrapper)

    def remove_group(self, group_id):
        def wrapper(room):
            self.rooms.remove(room)

        return self.__search_group(group_id, wrapper)

    def show_spy(self, group_id, line):
        def wrapper(room):
            self.game.room = room
            return self.game.show_spy(line)

        return self.__search_group(group_id, wrapper)
