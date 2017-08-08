from game_enviroment import *

test = []

game = GameGroups(SpyGame)


def just_records_message(event):
    """未來可以紀錄user 所有的message 現在先拿來測試用"""
    if event.message.text.lower() == "test":
        line = LineAPI(event)
        profile = line.get_profile(event.source.user_id)
        message = "user_id={}\n".format(event.source.user_id)
        message += profile.display_name + "\n"
        message += profile.user_id + "\n"
        message += profile.picture_url + "\n"
        message += profile.status_message + "\n"
        message += "-" * 10
        line.reply(text(message))


def show_spy(event):
    if event.message.text.lower() == "間諜現身" and event.source.type == "group" \
            and game.in_group(event.source.group_id):
        line = LineAPI(event)
        game.show_spy(event.source.group_id, line)


def show_display_player(event):
    if event.message.text.lower() == "遊戲人數" and event.source.type == "group" \
            and game.in_group(event.source.group_id):
        line = LineAPI(event)
        line.reply(text("i got it"))
        # game.show_display_player(event.source.group_id, line)


def to_start(event):
    if event.message.text.lower() == "好了" and event.source.type == "group" \
            and game.in_group(event.source.group_id):
        line = LineAPI(event)
        game.play(event.source.group_id, line)


def get_user(event):
    if event.message.text.lower() == "我" and event.source.type == "group" \
            and game.in_group(event.source.group_id):
        line = LineAPI(event)
        game.append_user(event.source.group_id, event.source.user_id, line)


def check_user(event):
    if event.message.text.lower() == "開始玩" and event.source.type == "group":
        game.append_group(event.source.group_id)
        line = LineAPI(event)
        content = """Hi ~我是Q醬
如果你要參與遊戲請說："我"
人數確定請跟我說:"好了"
要參與的人有誰呢？"""
        line.reply(template("間諜遊戲", content, ["我", "好了", "間諜現身"]))


def awake_bot(event):
    if event.message.text.lower() == "q bot":
        buttons_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ButtonsTemplate(
                title='間諜遊戲',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/K9R7i8R.jpg',
                actions=[
                    MessageTemplateAction(
                        label='開始玩',
                        text='開始玩'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)


invoker = Invoker()
functions = [
    awake_bot,
    check_user,
    get_user,
    to_start,
    show_spy,
    show_display_player,
    just_records_message,
]
for fn in functions:
    invoker.append(SimpleCommandFactory(fn))


def events_excute(event):
    invoker.execute(event, execute_all=True)
