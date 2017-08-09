import json

FILE_NAME = "db.json"


def write_json(d):
    with open(FILE_NAME, "w") as f:
        json.dump(d, f)


def read_json():
    try:
        with open(FILE_NAME) as f:
            return json.load(f)
    except:
        return {}
