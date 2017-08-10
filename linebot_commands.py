from game_enviroment import *
from line_api import *
from games import spy_game
import base_commands

add_list = [
    base_commands,
    spy_game,
]

commands = []
for cmd in add_list:
    commands.extend(cmd.commands())
invoker = Invoker()
invoker.appends(commands)


def events_excute(event):
    line = LineAPI(event)
    j = db.read_json()
    if event.message.text=="遊戲人數":
        print("")
    game = GameDB.init(db.read_json())
    invoker.execute(execute_all=True, event=event, line=line, game_db=game)
    g = game.to_dict()
    db.write_json(game.to_dict())
