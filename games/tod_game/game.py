from utli.base_import import *
import re

adventure_db = [
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
truth_talk_db = [
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
    "如果時間能重來最想做什麼"

]


class Status:
    choose_game = 1
    in_final_code = 2
    game_lose = 3
    game_over = 4
    game_end = 5


class TodGame(db.Model):
    FILE = __file__

    def __init__(self):
        self.users = []
        self.loser = None

        # self.fipw = random.randint(1, 99)
        self.pw_head = 0
        self.pw_tail = 100
        self.boom = None

        # 遊戲狀態
        self.status = Status.choose_game
        self.reply_user = 0

        # 真心話
        self.truth_talk_db = truth_talk_db
        # 大冒險
        self.adventure_db = adventure_db

    def choose_loser(self, line, event):
        if self.status == Status.choose_game:
            # 跳過遊戲 直接從狀態2變成4
            self.loser = random.choice(self.users)
            line.push(event.source.group_id, "{} lose".format(
                self.loser["display_name"]
            ))
            self.status = Status.game_over

    def to_final_game(self,line,event):
        self.status = Status.in_final_code
        self.boom = random.randint(1, 99)
        self.push_range(line,event)

    def push_range(self,line,event):
        line.push(event.source.group_id, "{} Please input：{} - {}".format(
            self.users[self.reply_user]['display_name'], self.pw_head, self.pw_tail
        ))

    def __in_range(self, count):
        return self.pw_head < int(count) < self.pw_tail

    def in_final_code(self, line, event):
        if self.status == Status.in_final_code:
            input_msg = event.message.text
            if event.source.user_id == self.users[self.reply_user]['user_id'] and input_msg != "終極密碼":
                if re.compile(r'^[0-9]+$').match(input_msg):
                    if not self.__in_range(input_msg):
                        line.push(event.source.group_id, "{} Pleas input range {} - {}".format(self.users[self.reply_user]["display_name"], self.pw_head, self.pw_tail))
                    else:
                        if self.boom == int(input_msg):
                            line.push(event.source.group_id, "Boom!!!! \n{} is losers".format(
                                self.users[0]["display_name"]
                            ))

                            self.status = Status.game_over
                            return True

                        else:
                            temp = self.pw_head
                            self.pw_head = int(input_msg)
                            if not self.__in_range(self.boom):
                                self.pw_head = temp
                                self.pw_tail = int(input_msg)

                            if len(self.users)-1 > self.reply_user:
                                self.reply_user +=1
                            else:
                                self.reply_user =0

                            self.push_range(line, event)
                else:
                    line.push(event.source.group_id, "Pleas input number")


    def is_game_over(self):
        return self.status == Status.game_over

    def start_game(self, users):
        self.__init__()
        self.users = users

    def choose_punishment(self, line, event, choice):
        choice_list = {
            '真心話': 'truth_talk_db',
            '大冒險': 'adventure_db',
        }
        # if choice_list.get(choice) is not None and self.status == Status.game_over:
        if choice in choice_list is not None and self.status == Status.game_over:
            punishment_list = getattr(self, choice_list.get(choice))
            line.push(event.source.group_id, 'Q：{}'.format(random.choice(punishment_list)))
            self.status = Status.game_end
