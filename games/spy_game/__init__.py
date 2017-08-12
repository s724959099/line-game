from base_commands import *


def template(title, msg, messages):
    url = 'https://i.imgur.com/K9R7i8R.jpg'
    return base_template(title, msg, url, messages)


def to_start(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    if not room.users:
        line.reply("目前還沒有人加入遊戲唷")
        return
    spy_game = room.game
    spy_game.play(room.users[:], line)
    spy_game.show_position(event.source.group_id, line)
    spy_game.show_card_to_user(line)
    line.push(event.source.group_id, template(
        "遊戲指令",
        "間諜遊戲指令如下",
        ["結束遊戲", "重新開始"]
    ))


def end_gmae(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    room.game.show_game(event.source.group_id, line)
    room.game = None


def restart_gmae(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    room.game.show_game(event.source.group_id, line)
    room.game = SpyGame()
    to_start(line, event, game_db)


def commands():
    return [

        SimpleCommandFactory(to_start, "OK"),
        SimpleCommandFactory(end_gmae, "結束遊戲"),
        SimpleCommandFactory(restart_gmae, "重新開始"),
    ]
