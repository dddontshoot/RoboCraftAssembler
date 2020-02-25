import sys
if sys.version_info < (3, 0):
    print("Sorry, Robocraft Assembler requires Python 3.x")
    sys.exit(1)

try:
    import bpy
except ImportError:
    print("\nRobocraft Assembler needs to be ran inside blender, "
          "try invoking with blender --python " + sys.argv[0] + "\n")

try:
    import pathlib
except ImportError:
    print("\nRobocraft Assembler is missing dependencies! Try running: "
          "pip install -r requirements.txt \n")

sys.path.append(str(pathlib.Path().absolute()))
from lib import blender, parser, arguments


class Program():
    def __init__(self):
        self.botfile = arguments.getBotFile()
        blender.unselectEverything()
        print("\nNow building " + self.botfile + "...")
        cubeDataHex, colourDataHex, cubeCount = parser.parseBotFile(self.botfile)
        self.cubedatabase = parser.parseCSVFile("cubes.csv")
        blender.build(cubeDataHex, colourDataHex, cubeCount, self.cubedatabase)
        print("done!")


if __name__ == "__main__":
    main = Program()
