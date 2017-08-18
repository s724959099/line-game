from termcolor import colored, cprint
from utli.tool import *

colors = MockClass()
colors.grey = "grey"
colors.red = "red"
colors.green = "green"
colors.yellow = "yellow"
colors.blue = "blue"
colors.magenta = "magenta"
colors.cyan = "cyan"
colors.white = "white"

highlights = MockClass()
highlights.on_grey = "on_grey"
highlights.on_red = "on_red"
highlights.on_green = "on_green"
highlights.on_yellow = "on_yellow"
highlights.on_blue = "on_blue"
highlights.on_magenta = "on_magenta"
highlights.on_cyan = "on_cyan"
highlights.on_white = "on_white"

attributes = MockClass()
attributes.bold = "bold"
attributes.underline = "underline"
attributes.reverse = "reverse"

p = cprint


def colorful(message, *args):
    str_split = message.split("{}")
    for s, a in zip(str_split, args):
        print(s, end="")
        a_args = a[1:]
        p(a[0], *a_args, end="")

    print("")


def demo1():
    cprint('Hello, World!', colors.grey)
    cprint('Hello, World!', colors.red)
    cprint('Hello, World!', colors.green)
    cprint('Hello, World!', colors.yellow)
    cprint('Hello, World!', colors.blue)
    cprint('Hello, World!', colors.magenta)
    cprint('Hello, World!', colors.cyan)
    cprint('Hello, World!', colors.white)


def demo2():
    cprint('Hello, World!', colors.red, highlights.on_grey)
    cprint('Hello, World!', colors.red, highlights.on_red)
    cprint('Hello, World!', colors.red, highlights.on_green)
    cprint('Hello, World!', colors.red, highlights.on_yellow)
    cprint('Hello, World!', colors.red, highlights.on_blue)
    cprint('Hello, World!', colors.red, highlights.on_magenta)
    cprint('Hello, World!', colors.red, highlights.on_cyan)
    cprint('Hello, World!', colors.red, highlights.on_white)


def demo3():
    cprint('Hello, World!', colors.white, attrs=[attributes.bold])
    cprint('Hello, World!', colors.white, attrs=[attributes.underline])
    cprint('Hello, World!', colors.white, attrs=[attributes.reverse])


if __name__ == "__main__":
    demo1()
    demo2()
    demo3()
