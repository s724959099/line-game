class Games:
    def __init__(self):
        self.rooms = [1,3,4]

    def remove_group(self, group_id):
        def wrapper(room):
            self.rooms.remove(room)

        return self.__search_group(group_id, wrapper)

    def __search_group(self, group_id, fn):
        for room in self.rooms:
            if room == group_id:
                return fn(room)
        return False
