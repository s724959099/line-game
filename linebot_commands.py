from game_enviroment import *
from line_api import *
from games import spy_game
import base_commands

add_list = [
    base_commands,
    spy_game,
]

commands = []
print("linebot commands")
for cmd in add_list:
    commands.extend(cmd.commands())
invoker = Invoker()
invoker.appends(commands)
game = GameDB.get_instance()

a = []


def events_excute(event):
    line = LineAPI(event)
    # invoker.execute(execute_all=True, event=event, line=line, game_db=game)
