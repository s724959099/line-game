from utli.tool import *
from utli.commands import Invoker, SimpleCommandFactory
from utli import db
import config
if not config.DEBEG:
    from utli.line_api import *
else:
    print("-----------現在config 在Debug模式-----------")
    from utli.test.line_api import *
