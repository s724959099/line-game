from games.base_commands import *
from games.tod_game.game import TodGame


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
    if not room.users:
        line.reply("目前還沒有人進入遊戲喲！")
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


def finelcode_peo(line, event, game_db):
    pass


def end_gmae(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    room.game.show_game(event.source.group_id, line)
    room.game = None


def restart_gmae(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    room.game = TodGame()
    to_start(line, event, game_db)


def true_talk(line, event, game_db):
    room = game_db.get_room(event.source.group_id)
    tod_game = room.game
    # tod_game.play = (room.users[:], line)

    tod_game.truth_talk(line, event)
    line.push(event.source.group_id, template(
        "title",
        "msg",
        ["結束遊戲", "重新開始", "遊戲大廳"]
    ))


def adventure(line, event, game_db):

    room = game_db.get_room(event.source.group_id)
    tod_game = room.game
    tod_game.adventure(line, event)
    line.push(event.source.group_id, template(
        "title",
        "msg",
        ["結束遊戲", "重新開始", "遊戲大廳"]
    ))


def game_lobby(line, event, game_db):
    append_group(line, event, game_db)


def commands():
    return [
        SimpleCommandFactory(to_start, "OK"),

        SimpleCommandFactory(random_peo, "電腦隨機"),
        SimpleCommandFactory(finelcode_peo, "終極密碼"),
        SimpleCommandFactory(true_talk, "真心話"),
        SimpleCommandFactory(adventure, "大冒險"),

        SimpleCommandFactory(restart_gmae, "重新開始"),
        SimpleCommandFactory(end_gmae, "結束遊戲"),
        SimpleCommandFactory(game_lobby, "遊戲大廳"),
    ]
