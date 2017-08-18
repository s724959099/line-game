from utli.base_import import *


class BaseCamp(db.Model):
    FILE = __file__

    def __init__(self, game):
        slef.game = game


class BadCamp(BaseCamp):
    pass


class ThirdCamp(BaseCamp):
    pass


class GoodCamp(BaseCamp):
    pass
