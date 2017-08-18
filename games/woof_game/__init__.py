from games.base_commands import *


def template(title, msg, messages):
    url = 'https://i.imgur.com/K9R7i8R.jpg'
    return base_template(title, msg, url, messages)


def commands():
    return [

        SimpleCommandFactory(to_start, "OK"),
        SimpleCommandFactory(end_gmae, "結束遊戲"),
        SimpleCommandFactory(restart_gmae, "重新開始"),
    ]
