from game_enviroment import *
from line_api import *
from games import spy_game
import base_commands

add_list = [
    (None, base_commands),
    (SpyGame, spy_game),
]


def events_excute(event):
    line = LineAPI(event)
    game_db = GameDB.init(db.read_json())

    commands = []
    for item in add_list:
        class_game = item[0]
        cmd = item[1]

        if class_game is None:
            commands.extend(cmd.commands())
        else:
            if event.source.type == "group":
                room = game_db.get_room(event.source.group_id)
                if hasattr(room, "game"):
                    if isinstance(room.game, class_game):
                        commands.extend(cmd.commands())

    invoker = Invoker()
    invoker.appends(commands)
    invoker.execute(execute_all=True, event=event, line=line, game_db=game_db)
    g = game_db.to_dict()
    db.write_json(game_db.to_dict())
