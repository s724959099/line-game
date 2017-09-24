from games.base_commands import *
from games.tod_game.game import TodGame
from games.game_enviroment import *

import random
import re


def template(title, msg, messages):
    url = 'https://i.imgur.com/K9R7i8R.jpg'
    return base_template(title, msg, url, messages)


def function_template(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    game = room.game
    # game.users = room.users[:]


def end_gmae(line, event, game_db):
    # 這樣就結束遊戲了
    room = game_db.get_room(event.source.group_id)
    room.game = None


def in_final_code(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    game = room.game
    game.in_final_code(line,event)


def start_game(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    game = room.game
    game.start_game(room.users[:])
    line.push(event.source.group_id, template(
        "title",
        "msg",
        messages=[
            "電腦隨機",
            "終極密碼"
        ]
    ))


def choose_game(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    game = room.game
    if event.message.text == "電腦隨機":
        game.choose_loser(line)
    if event.message.text == "終極密碼":
        game.to_final_game()


def game_lobby(line, event, game_db):
    # todo 大廳要顯示什麼 未來寫在base_commadns
    room = game_db.get_room(event.source.group_id)
    tod_game = room.game


def choose_punishment(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    game = room.game
    if game.is_game_over():
        game.choose_punishment(line, event, event.message.text)
        line.push(event.source.group_id,
                  template("遊戲已結束", "請選擇", ["結束遊戲", "遊戲大廳", "重新開始"]))


def commands():
    return [

        SimpleCommandFactory(start_game, "OK"),  # 1
        SimpleCommandFactory(start_game, "重新開始"),  # 1

        SimpleCommandFactory(choose_game, "電腦隨機"),  # 2
        SimpleCommandFactory(choose_game, "終極密碼"),  # 2
        SimpleCommandFactory(in_final_code, no_if=True),  # 3
        SimpleCommandFactory(choose_punishment, "真心話"),  # 4
        SimpleCommandFactory(choose_punishment, "大冒險"),  # 4

        SimpleCommandFactory(end_gmae, "結束遊戲"),  # 5
        SimpleCommandFactory(game_lobby, "遊戲大廳"),  #
    ]
