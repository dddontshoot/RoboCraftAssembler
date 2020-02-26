import sys

if sys.version_info < (3, 0):
    print("Sorry, Robocraft Assembler requires Python 3.x")
    sys.exit(1)


try:
    import pathlib
except ImportError:
    print("\nRobocraft Assembler is missing dependencies! Try running: "
          "pip install -r requirements.txt \n")


sys.path.append(str(pathlib.Path().absolute()))
from lib.arguments import Arguments
from lib.blender import Blender
from lib.parser import Parser


class Program():
    def __init__(self):
        self.arguments = Arguments()
        self.blender = Blender()
        self.parser = Parser()

        self.botfile = self.arguments.getBotFile()
        self.blender.unselectEverything()
        print("\nNow building " + self.botfile + "...")
        self.cubeData = self.parser.parseBotFile(self.botfile)
        self.cubedatabase = self.parser.parseCSVFile("cubes.csv")
        self.blender.build(self.cubeData, self.cubedatabase)
        print("done!")


if __name__ == "__main__":
    main = Program()
