from base_commands import *
from .game import SpyGame


def template(title, msg, messages):
    url = 'https://i.imgur.com/K9R7i8R.jpg'
    return base_template(title, msg, url, messages)


def init_game(line, event, game_db):
    if game_db.in_group(event.source.group_id):
        game_db.get_room(event.source.group_id).game = SpyGame()
        line.reply(template(
            "遊戲建立中",
            "參加玩家回答完後回答好了即可開始",
            [
                "我",
                "好了",
                "遊戲人數",
            ]
        ))
        # line.reply("debugger 中 in group init game")
    else:
        game_db.debugger_rooms(line)
        # awake_bot(line, event, game_db)


def show_spy(line, event, game_db):
    if game_db.in_group(event.source.group_id):
        room = game_db.get_room(event.source.group_id)
        if not room:
            line.reply("找不到遊戲房間")
        else:
            spy_game = room.game
            spy_game.show_spy(line)


def commands():
    return [
        SimpleCommandFactory(init_game, "間諜遊戲"),
        SimpleCommandFactory(show_spy, "間諜現身"),
    ]
