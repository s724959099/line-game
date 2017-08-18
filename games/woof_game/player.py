from .camp import *
from utli.base_import import *


class Base(db.Model):
    FILE = __file__


class Player(Base):
    belong_camp = None


class Woof(Player):
    pass


class Villagers(Player):
    pass


class Hunter(Player):
    pass


class Prophet(Player):
    pass
