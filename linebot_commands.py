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

import json

FILE_NAME = "db.json"


def write_json(d):
    with open(FILE_NAME, "w") as f:
        json.dump(d, f)


def read_json():
    try:
        with open(FILE_NAME) as f:
            return json.load(f)
    except:
        return {}

a=[]
def events_excute(event):
    line = LineAPI(event)

    # line.reply("len={}".format(a))
    # a.append(1)
    # invoker.execute(execute_all=True, event=event, line=line, game_db=game)
