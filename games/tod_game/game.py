from utli.base_import import *

class TodGame(db.Model):
    FILE = __file__



    def __init__(self):
        self.users = []
        self.speical_man = None
        self.tod_users = []
        self.picker_position = None
        self.finel_user = 0
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
            "跟旁邊的女生要賴(如果沒有就跟群組的人要)",
            "大喊我愛大咪咪(我愛大香腸)",
            "把鞋子拿起來當電話(說您撥的電話無人回應)",
            "拿一個人的襪子(沒穿就拿隔壁的)玩擠眉弄眼",
            "拿手機播一首哥走一圈(邊做動作邊走)",
            "打電話跟一個異性朋友告白",
            "去跟不認識的人自我介紹然後一起聊天(5分鐘)",
            "抱一個異性(ex：公主抱...)",
            "跟異性講冷笑話(可以上網查或指定)",
            "對不認識的人唱歌用嘴巴含水(飲料)直到對方猜出來",


        ]

    def random_user(self, line):
        self.speical_man = choose_list(self.users, 1)[0]
        line.reply('the man is {}'.format(self.speical_man["display_name"]))

    def finelcode_user(self, line, pw_head, pw_tail, pw):
        cp.p(line.profile["display_name"] + "請輸入密碼: ", cp.colors.red)
        input_msg = input()

        while True:

            if input_msg.isdigit() :
                if int(input_msg) > pw_head and int(input_msg) < pw_tail and int(input_msg) != pw:
                    return int(input_msg)
                elif int(input_msg) == pw:
                    self.speical_man = line.profile
                    return int(input_msg)
            else:
                print("Please input number({}-{})!!!!".format(pw_head, pw_tail))
                cp.p(self.users.name + "請輸入密碼: ", cp.colors.red)
                input_msg = input()



    def truth_talk(self, line, event):
        self.picker_position = random.choice(self.truth_talk_db)

        if event.source.user_id == self.speical_man["user_id"]:
            line.push(event.source.group_id, text_message("Ｑ：" + self.picker_position))
            return True
            # line.push(event.source.group_id,"say truth")


    def adventure(self, line, event):
        self.picker_position = random.choice(self.adventure_db)

        if event.source.user_id == self.speical_man["user_id"]:
            line.push(event.source.group_id, text_message("Ｑ：" + self.picker_position))
            return True
        #     line.push(event.source.group_id, "say adventure")


