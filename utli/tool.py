import random


class MockClass:
    pass


def happen_percent(percent):
    return True if random.random() < percent else False


def choose_list(arr, count, repeat=False):
    if not repeat:
        return random.sample(arr, count)
    else:
        result = []
        sr = random.SystemRandom()
        for i in range(count):
            result.append(sr.choice(arr))
        return result


def dict_list_check(key, val, arr):
    for item in arr:
        if item.get(key) == val:
            return True
    return False
