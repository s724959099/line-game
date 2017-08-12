from games.spy_game.game import SpyGame
from utli.line_api import *


def template(title, msg, messages):
    url = 'https://i.imgur.com/yREmWQb.jpg'
    return base_template(title, msg, url, messages)


def just_records_message(line, event, game_db):
    """未來可以紀錄user 所有的message 現在先拿來測試用"""
    if event.message.text.lower() == "test":
        profile = line.get_profile(event.source.user_id)
        message = "user_id={}\n".format(event.source.user_id)
        message += profile.display_name + "\n"
        message += profile.user_id + "\n"
        message += profile.picture_url + "\n"
        message += profile.status_message + "\n"
        message += "-" * 10
        line.reply(message)
        return True


def show_game_player(line, event, game_db):
    if game_db.in_group(event.source.group_id):
        room = game_db.get_room(event.source.group_id)
        room.show_game_player(line)
    else:
        game_db.debugger_rooms(line)
        # awake_bot(line, event, game_db)


def append_group(line, event, game_db):
    game_db.append_group(event.source.group_id)
    line.reply(template("請選擇遊戲", "未來會陸續新增其他遊戲，敬請期待", ["間諜遊戲"]))


def awake_bot(line, event, game_db):
    line.reply(template("Game bot", "請選擇", [
        "開始玩",
        ("聯絡作者", "https://www.facebook.com/profile.php?id=100001313600594"),
    ]))


def get_user(line, event, game_db):
    if game_db.in_group(event.source.group_id):
        game_db.append_user(event.source.group_id, event.source.user_id, line)


def spy_gmae(line, event, game_db):
    if game_db.in_group(event.source.group_id):
        game_db.get_room(event.source.group_id).game = SpyGame()
        line.reply(template(
            "遊戲建立中",
            "參加玩家回答完後回答好了即可開始",
            [
                "我",
                "OK",
                "遊戲人數",
                ("遊戲說明", "http://boardgame-record.blogspot.tw/2015/06/spyfall.html")
            ]
        ))


def commands():
    return [
        SimpleCommandFactory(spy_gmae, "間諜遊戲"),
        SimpleCommandFactory(get_user, "我"),
        SimpleCommandFactory(awake_bot, "q bot"),
        SimpleCommandFactory(append_group, "開始玩"),
        SimpleCommandFactory(show_game_player, "遊戲人數"),
        SimpleCommandFactory(just_records_message, "test"),
    ]
