from sys import argv

def getBotFile():
    DEFAULT_BOT_FILE = "TheDistractingCicada.bot"
    if "--" in argv:
        botfile = argv[argv.index("--") + 1:].pop(0)
    else:
        botfile = DEFAULT_BOT_FILE
    return botfile

