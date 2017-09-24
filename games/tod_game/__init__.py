from games.base_commands import *
from games.tod_game.game import TodGame
from games.game_enviroment import *

import random
import re

def template(title, msg, messages):
    url = 'https://i.imgur.com/K9R7i8R.jpg'
    return base_template(title, msg, url, messages)


def to_start(line, event, game_db):

    line.push(event.source.group_id, template(
        "title",
        "msg",
        messages=[
            "電腦隨機",
            "終極密碼"
        ]
    ))


def random_peo(line, event, game_db):
    room = game_db.get_room(event.source.group_id)

    game = room.game
    game.users = room.users[:]
    game.random_user(line)
    line.push(event.source.group_id, template(
        "title",
        "msg",
        messages=[
            "真心話",
            "大冒險"
        ]
    ))


def end_gmae(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    # room.game.show_game(event.source.group_id, line)
    room.game = None


def restart_gmae(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    room.game = TodGame()
    to_start(line, event, game_db)


def finalcode(line, event, game_db, pw=None):
    room = game_db.get_room(event.source.group_id)

    game = room.game

    tod_game.finelcode_user()


    # game.users = room.users[:]
    # game.random_user(line)







def final_pw(line, event, game_db, pw=None):
    room = game_db.get_room(event.source.group_id)

    game = room.game
    # game.users = room.users[:]
    # game.random_user(line)



    if(tod_game.finel_pw(line, event))

        line.push(event.source.group_id, template(
            "title",
            "msg",
            messages=[
                "真心話",
                "大冒險"
            ]
        ))


def true_talk(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    tod_game = room.game
    # tod_game.play = (room.users[:], line)

    if(tod_game.truth_talk(line, event)):
        line.push(event.source.group_id, template(
            "title",
            "msg",
            ["結束遊戲", "重新開始", "遊戲大廳"]
        ))


def adventure(line, event, game_db):

    room = game_db.get_room(event.source.group_id)
    tod_game = room.game

    if(tod_game.adventure(line, event)):
        line.push(event.source.group_id, template(
            "title",
            "msg",
            ["結束遊戲", "重新開始", "遊戲大廳"]
        ))


def game_lobby(line, event, game_db):
    append_group(line, event, game_db)
    # room = game_db.get_room(event.source.group_id)
    # if room.game == None:
    #     append_group(line, event, game_db)
    # else:
    #     line.push(event.source.group_id, template(
    #         "",
    #         "請按下方結束遊戲",
    #         ["結束遊戲"]
    #     ))


def commands():


    return [

        SimpleCommandFactory(to_start, "OK"), #1
        SimpleCommandFactory(restart_gmae, "重新開始"),  # 1

        SimpleCommandFactory(random_peo, "電腦隨機"),  #2
        SimpleCommandFactory(finalcode, "終極密碼"),   #2
        SimpleCommandFactory(final_pw, no_if=True), #3
        SimpleCommandFactory(true_talk, "真心話"), #4
        SimpleCommandFactory(adventure, "大冒險"), #4


        SimpleCommandFactory(end_gmae, "結束遊戲"), #5
        SimpleCommandFactory(game_lobby, "遊戲大廳"), #
    ]


