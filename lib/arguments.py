from sys import argv



class Arguments():


    def __init__(self):
        pass

    def getBotFile(self):
        DEFAULT_BOT_FILE = "bots/TheDistractingCicada.bot"
        if "--" in argv:
            botfile = argv[argv.index("--") + 1:].pop(0)
        else:
            botfile = DEFAULT_BOT_FILE
        return botfile

