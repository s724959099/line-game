import json
from config import *
# from games.spy_game.game import SpyGame

FILE_NAME = "db.json"


def get_module(file):
    try:
        file_path = os.path.abspath(file)
        file_path= file_path.replace(ROOT_DIR + "/", "")
        path = file_path.rsplit(".py")[0]
        result = path.replace("/", ".")
        return result
    except:
        return ""


def write_json(d):
    with open(FILE_NAME, "w") as f:
        json.dump(d, f)


def read_json():
    try:
        with open(FILE_NAME) as f:
            return json.load(f)
    except:
        return {}


class Model:
    def __item_check(self, item):
        if isinstance(item, Model):
            result = item.to_dict()
            module_name = get_module(self.FILE)
            result["__module"] = module_name
            result["__class"] = item.__class__.__name__
        elif isinstance(item, list):
            result = []
            for i in item:
                new_dd = self.__item_check(i)
                result.append(new_dd)
        elif isinstance(item, dict):
            result = self.__dict_check(item)
        else:
            result = item
        return result

    def __dict_check(self, ddict):
        d = {}
        for key, item in ddict.items():
            d[key] = self.__item_check(item)
        return d

    def to_dict(self):
        return self.__dict_check(self.__dict__)

    @classmethod
    def init(cls, d):
        return cls.__dict_init(d)

    @classmethod
    def __dict_init(cls, d, is_dict=False):
        if not is_dict:
            c = cls()
        else:
            c = {}
        for key, item in d.items():
            if not is_dict:
                c.__dict__[key] = cls.__item_init(item)
            else:
                c[key] = cls.__item_init(item)
        return c

    @classmethod
    def __item_init(cls, item):
        if isinstance(item, dict) and item.get("__class"):
            m = __import__(item.get("__module"), globals(), locals(), [""])
            sub_cls = getattr(m, item.get("__class"))
            result = sub_cls.init(item)
        elif isinstance(item, dict):
            result = cls.__dict_init(item, is_dict=True)
        elif isinstance(item, list):
            result = []
            for i in item:
                result.append(cls.__item_init(i))
        else:
            result = item

        return result
