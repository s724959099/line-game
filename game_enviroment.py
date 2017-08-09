import json
from line_api import *


class GameRoom:
    def __init__(self, group_id):
        self.group_id = group_id
        self.users = []
        self.game = None

    def append_user(self, user_id, line):
        if self.in_users(user_id):
            return False
        profile = line.get_profile(user_id)
        self.users.append(profile)
        line.reply("目前人數為＝{}".format(len(self.users)))
        return True

    def in_users(self, user_id):
        for item in self.users:
            if item.user_id == user_id:
                return True
        return False

    def show_game_player(self, line):
        message = "遊戲人數為: {}\n".format(len(self.users))
        message += "-" * 20 + "\n"
        for profile in self.users:
            message += "{} \n".format(profile.display_name)
        line.reply(message)


class GameDB:
    def __init__(self):
        self.rooms = []

    def debugger_rooms(self, line):
        msg = ""
        index = 0
        for room in self.rooms:
            temp_dict = room.__dict__
            arr = []
            for user in room.users:
                arr.append(user.__dict__)
            temp_dict["users"] = arr
            del temp_dict["game"]
            msg += "room{}: ".format(index) + json.dumps(temp_dict) + "\n"
            index += 1

        line.reply(msg)

    def append_group(self, group_id):
        if self.in_group(group_id):
            return False
        self.rooms.append(GameRoom(group_id))
        return True

    def append_user(self, group_id, user_id, line):
        def wrapper(room):
            if user_id is None:
                return False
            return room.append_user(user_id, line)

        return self.__search_group(group_id, wrapper)

    def __search_group(self, group_id, fn):
        for room in self.rooms:
            if room.group_id == group_id:
                return fn(room)

    def in_group(self, group_id):
        def wrapper(room):
            return True if room else False

        return self.__search_group(group_id, wrapper)

    def play(self, group_id, line, game):
        def wrapper(room):
            if not room:
                line.reply("找不到遊戲房間")
            else:
                room.game = game
                room.game.play(room.users[:], line)

        return self.__search_group(group_id, wrapper)

    def remove_group(self, group_id):
        def wrapper(room):
            self.rooms.remove(room)

        return self.__search_group(group_id, wrapper)

    def get_room(self, group_id):
        def wrapper(room):
            return room

        return self.__search_group(group_id, wrapper)

    def show_display_player(self):
        def wrapper(room):
            return room

        return self.__search_group(group_id, wrapper)
