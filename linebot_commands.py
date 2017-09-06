from games import spy_game, base_commands, tod_game
from games.game_enviroment import *
from utli.base_import import *
add_list = [
    (None, base_commands),
    (SpyGame, spy_game),
    (TodGame, tod_game),
]


def events_excute(event):
    line = LineAPI(event)
    game_db = GameDB.init(db.read_json())

    commands = []
    for item in add_list:
        class_game = item[0]
        cmd = item[1]
        # 基本命令 所以不是屬於任何遊戲
        if class_game is None:
            commands.extend(cmd.commands())
        else:
            # 如果 user 在某個game room 裡面 且game 相同則增加commands
            for room in game_db.rooms:
                if dict_list_check("user_id", event.source.user_id, room.users) \
                        and isinstance(room.game, class_game):
                    commands.extend(cmd.commands())
                    break

    invoker = Invoker()
    invoker.appends(commands)
    invoker.execute(execute_all=True, event=event, line=line, game_db=game_db)
    g = game_db.to_dict()
    db.write_json(game_db.to_dict())
