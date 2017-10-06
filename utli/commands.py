class Command:
    def execute(self):
        raise NotImplemented

    def undo(self):
        pass


class SimpleCommandFactory(Command):
    def __init__(self, func, trigger_text=None, only_group=True, no_if=False):
        """

        :param func: 要執行的function
        :param trigger_text: 判斷的文字
        :param only_group: 只在group的message 判斷
        :param no_if: 前面兩個就不判斷了
        """
        self.__fn = func
        self.__text = trigger_text
        if isinstance(self.__text, str):
            self.__text = [self.__text]
        if self.__text == None:
            self.__text = []

        self.__text = list(map(lambda x: x.lower(), self.__text))
        self.__only_group = only_group
        self.__no_if = no_if

    def execute(self, *args, **kwargs):
        event = kwargs["event"]
        if self.__no_if:
            print("before function= {} called".format(self.__fn.__name__))
            self.__fn(*args, **kwargs)
        elif event.message.text.lower() in self.__text:
            if not self.__only_group or event.source.type == "group":
                print("before function= {} called".format(self.__fn.__name__))
                self.__fn(*args, **kwargs)


class Invoker:
    def __init__(self):
        self.commands = []
        self.__index = 0
        self.name_type = {
            1: "execute",
            2: "undo"
        }

    def append(self, command):
        self.commands.append(command)

    def appends(self, commands):
        for command in commands:
            self.commands.append(command)

    def appends_factory(self, commands):
        for command in commands:
            self.commands.append(SimpleCommandFactory(command))

    def for_loop(self, execute_type="execute"):
        if execute_type is "execute":
            for command in self.commands[self.__index:]:
                yield command
            self.__index += len(self.commands)
        if execute_type is "undo":
            for command in self.commands[self.__index - 1::-1]:
                yield command
            self.__index += 0

    def execute(self, execute_all=False, *args, **kwargs):
        self.base_command(self.name_type[1], execute_all=execute_all, *args, **kwargs)

    def undo(self, execute_all=False, *args, **kwargs):
        self.base_command(self.name_type[2], execute_all=execute_all, *args, **kwargs)

    def base_command(self, name, execute_all=False, *args, **kwargs):
        cond1 = self.__index >= len(self.commands) and name is "execute"
        cond2 = self.__index < 0 and name is "undo"
        if cond1 or cond2:
            return False
        if execute_all:
            for command in self.commands:
                getattr(command, name)(*args, **kwargs)
        else:
            command = self.commands[self.__index]
            getattr(command, name)(*args, **kwargs)

            if name is "execute":
                self.__index += 1
            if name is "undo":
                self.__index -= 1
