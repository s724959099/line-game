from utli.base_import import *


class TodGame(db.Model):
    FILE = __file__



    def __init__(self):
        self.users = []
        self.speical_man = None
        self.spy_users = []
        self.picker_position = None
        self.init_data()

    def init_data(self):
        self.truth_talk_db = [
            "現在有沒有喜歡的人",
            "玩遊戲中的人有你喜歡的人嗎",
            # ("現在有沒有喜歡的人","玩遊戲中的人有你喜歡的人嗎"),
            "第一次接吻幾歲",
            "有沒有過一夜情",
            "有沒有劈腿過",
            "分享一個另一半做過最印象深刻(感動)的事",
            "想生幾個小孩",
            "最想感謝的人跟為什麼",
            "未來的夢想",
            "如果時間能重來最想做什麼",
            # "破處了嗎",

        ],
        self.adventure_db = [
            "跟旁邊的女生要賴（如果沒有就跟群組的人要）",
            "大喊我愛大咪咪（我愛大香腸）",
            "把鞋子拿起來當電話（說您撥的電話無人回應）",
            "拿一個人的襪子（沒穿就拿隔壁的）玩擠眉弄眼",
            "拿手機播一首哥走一圈（邊做動作邊走）",
            "打電話跟一個異性朋友告白",
            "去跟不認識的人自我介紹然後一起聊天（5分鐘）",
            "抱一個異性（ex：公主抱...）",
            "跟異性講冷笑話（可以上網查或指定）",
            "對不認識的人唱歌用嘴巴含水（飲料）直到對方猜出來",


        ]
        # self.spy_image = ("間諜", "https://i.imgur.com/K9R7i8R.jpg")

    def play(self, users, line):
        self.users = users
        if len(self.users) is None:
            line.reply("沒有玩家oops")
        print("user count=", len(users))
        user_count = len(users)
        spy_count = int(user_count / 3)
        if spy_count == 0:
            spy_count = 1
        self.spy_users = []
        for i in range(spy_count):
            self.picker_spy()

        self.picker_position = random.choice(self.truth_talk_db)

    def random_user(self, line):
        self.speical_man = choose_list(self.users, 1)[0]
        line.reply('the man is {}'.format(self.speical_man["display_name"]))

    def truth_talk(self, line, event):
        # sr = random.SystemRandom()

        self.picker_position = random.choice(self.truth_talk_db)

        line.push(event.source.group_id, text_message("Ｑ：" + self.picker_position[random.choice(range(0,9))]))

        # if event.source.user_id == self.speical_man["user_id"]:
        #     line.push(event.source.group_id,"say truth")


    def adventure(self, line, event):
        self.picker_position = random.choice(self.adventure_db)
        line.push(event.source.group_id, text_message("Ｑ：" + self.picker_position[random.choice(range(0,9))]))
        # if event.source.user_id == self.speical_man["user_id"]:
        #     line.push(event.source.group_id, "say adventure")