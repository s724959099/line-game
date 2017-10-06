import random
from utli.base_import import *


class SpyGame(db.Model):
    FILE = __file__

    def init_images(self):
        self.position_images = [
            ("醫院", "https://i.imgur.com/ffgqsjU.png",
             ["俏護士", "怪醫黑傑克", "兩光醫生", "帶兩串香蕉探病的病人家屬", "頭髮骨折的病人", "院長", "志工", "保全", "水電工", "外送小弟"]),
            ("十字軍東征", "https://i.imgur.com/mIJZQkE.jpg",
             ["弓箭手", "你是一隻馬", "騎士", "教宗", "雜兵", "高級雜兵", "不知道哪裡來的傭兵", "躺在地上假死的士兵", "聖職人員", "步兵", "主教", "農民"]),
            ("海灘", "https://i.imgur.com/mRd9Hjb.jpg",
             ["比基尼辣妹", "比丘尼", "鮪魚線的男人", "救生員", "很猛的猛男", "小孩子", "潛水員", "剛讀大學的小Q醬"]),
            ("學校", "https://i.imgur.com/SVrPdGO.jpg",
             ["數學老師", "小混混", "英文老師", "教務主任", "訓導主任", "糾察隊", "風紀股長", "電器股長", "no function 吸％等畢業的學生", "籃球隊隊長隔壁的球隊經理",
              "籃球隊隊長"]),
            ("演唱會", "https://i.imgur.com/PvyJ7rP.jpg",
             ["賣黃牛票的小弟", "高雄金城武", "高雄鹽埕區", "李光洙", "范范范曉宣", "范范范尾鰭", "小粉絲", "工作人員", "防彈少年團"]),
            ("月球", "https://i.imgur.com/UbBRqhS.jpg",
             ["嫦娥", "火星人", "科學家", "阿姆斯壯", "月兔", "太空戰士", "太空人"]),
            ("阿爾卑斯山", "https://i.imgur.com/5j0CHPP.jpg",
             ["登山客", "阿爾卑斯山的小女孩", "大雪怪", "大腳怪", "雪女"]),
            ("陰屍路", "https://i.imgur.com/hYrb1Pb.jpg",
             ["弓箭手", "手拿消防栓的人", "喪屍", "狼師", "拿拐杖的老人", "拿棒棒糖的小孩", "警察", "活屍"]),
            ("百貨公司", "https://i.imgur.com/uCkvDXj.jpg",
             ["櫃姐", "小P孩", "保全", "清潔阿姨", "客人", "董事長"]),
            ("迪士尼", "https://i.imgur.com/5DRre9V.jpg",
             ["小丑", "米奇", "唐老鴨", "高飛", "海盜船長", "白雪公主", "小熊維尼", "尼莫", "多莉", "樂樂", "巴斯光年", "毛怪", "胡迪", ]),
            ("星際大戰", "https://i.imgur.com/zlzctzh.jpg",
             ["黑武士", "尤達", "天行者", "複製人士兵"]),
            ("白宮", "https://i.imgur.com/27z23dr.jpg",
             ["總通先生", "總統夫人", "保鑣", "殺手", "司機", "園丁", "廚師"]),
            ("西遊記", "https://i.imgur.com/9xxHzfZ.jpg",
             ["吸油面紙", "孫悟空", "唐三藏", "沙悟淨", "豬八戒", "牛魔王", "鐵扇公主", ]),
            ("夜市", "https://i.imgur.com/zBPjQCO.jpg",
             ["射氣球的客人", "小吃攤販", "客人", "警衛", "臭豆腐老闆", "牛排店老闆", ]),
            ("棒球場", "https://i.imgur.com/DEW2Kk4.jpg",
             ["陳金鋒", "球員", "教練", "撿球小弟", "啦啦隊美女", "賣爆米花的人", ]),
            ("北極", "https://i.imgur.com/fX2DLnj.jpg",
             ["北極熊", "海狗", "探勘家", "愛斯基摩人", ]),
            ("尼斯湖", "https://i.imgur.com/NhV1OQH.jpg",
             ["尼斯湖大水怪", "尼斯湖大內褲", "遊客", "漁夫", ]),
            ("海盜船", "",
             ["傑克船長", "打雜小弟", "伊莉莎白", "巴伯沙船長", "威爾特納", ]),

        ]
        self.spy_image = ("間諜", "https://i.imgur.com/K9R7i8R.jpg")

    def __init__(self):
        self.last_positions = []
        self.users = []
        self.main_player = None
        self.spy_users = []
        self.picker_position = None
        self.init_images()

    def get_positions(self):
        return list(map(lambda item: item[0], self.position_images))

    def picker_spy(self):
        while True:
            profile = random.choice(self.users)
            if profile not in self.spy_users:
                self.spy_users.append(profile)
                break

    def show_position(self, line):
        s = "場景為：\n"
        for item in self.get_positions():
            s += "{}\n".format(item)
        for profile in self.users:
            line.push(profile["user_id"], s)

    def choose_position(self):
        while True:
            position = random.choice(self.position_images)
            if position not in self.last_positions:
                break
        if len(self.last_positions) > 3:
            self.last_positions.pop(0)
        self.last_positions.append(position)
        self.picker_position = position

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
        self.choose_position()

    def show_card_to_user(self, line):
        role = choose_list(self.picker_position[2], 1)
        for profile in self.users:
            if profile in self.spy_users:
                line.push(profile["user_id"], text_message(self.spy_image[0]))
                line.push(profile["user_id"], image_message(self.spy_image[1]))
            else:
                line.push(profile["user_id"], text_message(self.picker_position[0]))
                line.push(profile["user_id"], image_message(self.picker_position[1]))
                line.push(profile["user_id"], text_message("您這場的角色為: {}".format(role)))

    def show_game(self, group_id, line):
        if self.users is None:
            return False
        msg = "間諜名單為:\n"
        msg += "-" * 30
        for profile in self.spy_users:
            msg += "\n"
            msg += profile["display_name"] + "\n"
            msg += "-" * 30

        line.push(group_id, msg)
        line.push(group_id, "地點為: {}".format(self.picker_position[0]))
        line.push(group_id, image_message(self.picker_position[1]))
