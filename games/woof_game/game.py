import random
from .player import *


class Base(db.Model):
    FILE = __file__


class WoofGame(Base):
    def __init__(self):
        self.users = []
        self.players = []
        self.leave_player = []
        self.game_type = "base"

        self.bad_camp = BadCamp(self)
        self.third_camp = ThirdCamp(self)
        self.good_camp = GoodCamp(self)

    def init_players(self):
        init_instance = {
            "base": BaseInit
        }
        init = init_instance[self.game_type](self.users)
        self.players = init.get_players()

    def play(self):
        self.init_players()

    def do_day_things(self):
        pass

    def do_vote_things(self):
        pass

    def do_night_things(self):
        pass


class InitTemplate:
    def __init__(self, users):
        self.users = users

    def woof_init(self, f):
        raise NotImplemented

    def special_init(self, f):
        raise NotImplemented

    def villagers_init(self, f, woof, special):
        raise NotImplemented

    def get_players(self):
        raise NotImplemented


class BaseInit(InitTemplate):
    def __init__(self, users):
        self.users = users

    def woof_init(self, f):
        return (f - 2) / 4

    def special_init(self, f):
        if f < 10:
            return 0
        elif 10 < f < 14:
            return 2
        elif f == 14:
            return 3

    def villagers_init(self, f, woof, special):
        return f - woof - special

    def get_players(self):
        count = len(users)
        result = []
        roles = []
        return result


class Vote(Base):
    pass


class State(Base):
    def __init__(self, game):
        self.game = game

    def toggle(self,state=None):
        raise NotImplemented


class DayState(State):
    def toggle(self,state=None):
        self.game.do_day_things()


class VoteState(State):
    def toggle(self,state=None):
        self.game.do_vote_things()


class NightState(State):
    def toggle(self,state=None):
        self.game.do_night_things()
