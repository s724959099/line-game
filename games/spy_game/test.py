from utli.test.line_api import *

if __name__ == "__main__":
    db.write_json({})
    user_list.extend([
        UserFactory.get_instance(),
        UserFactory.get_instance(),
        UserFactory.get_instance(),
        UserFactory.get_instance(),
        UserFactory.get_instance(),
    ])
    user_list[0].speak("開始玩")
    user_list[0].speak("間諜遊戲")
    for user in user_list:
        user.speak("我")
    user_list[0].speak("遊戲人數")
    user_list[0].speak("OK")
    user_list[0].speak("重新開始", message_type=User.message_type.user)
    user_list[0].speak("重新開始", message_type=User.message_type.user)
    user_list[0].speak("重新開始", message_type=User.message_type.user)
    user_list[0].speak("重新開始", message_type=User.message_type.user)
    user_list[0].speak("重新開始", message_type=User.message_type.user)
    user_list[0].speak("重新開始", message_type=User.message_type.user)
    user_list[0].speak("重新開始", message_type=User.message_type.user)
    user_list[0].speak("結束遊戲")
