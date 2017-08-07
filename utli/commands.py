class Command:
    def execute(self):
        raise NotImplemented

    def undo(self):
        pass


class SimpleCommandFactory(Command):
    def __init__(self, func, *args, **kwargs):
        self.__fn = func
        self.__args = args
        self.__kwargs = kwargs

    def execute(self):
        self.__fn(*self.__args, **self.__kwargs)


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

    def for_loop(self, execute_type="execute"):
        if execute_type is "execute":
            for command in self.commands[self.__index:]:
                yield command
            self.__index += len(self.commands)
        if execute_type is "undo":
            for command in self.commands[self.__index - 1::-1]:
                yield command
            self.__index += 0

    def execute(self, execute_all=False):
        self.base_command(self.name_type[1], execute_all=execute_all)

    def undo(self, execute_all=False):
        self.base_command(self.name_type[2], execute_all=execute_all)

    def base_command(self, name, execute_all=False):
        cond1 = self.__index >= len(self.commands) and name is "execute"
        cond2 = self.__index < 0 and name is "undo"
        if cond1 or cond2:
            return False
        if execute_all:
            for command in self.for_loop(name):
                getattr(command, name)()
        else:
            command = self.commands[self.__index]
            getattr(command, name)()

            if name is "execute":
                self.__index += 1
            if name is "undo":
                self.__index -= 1
