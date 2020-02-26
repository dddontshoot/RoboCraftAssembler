import base64
import json
import csv

class Parser():

    def __init__(self):
        pass

    def parseBotFile(self, botfile):
        if botfile[len(botfile) - 4: len(botfile)] == ".bot":
            file = open(botfile, "r")
            bot = json.loads(file.read())

            bot["cubeDataDecoded"] = base64.b64decode(bot["cubeData"])
            bot["cubeDataHex"] = bot["cubeDataDecoded"].hex()
            bot["colourDataDecoded"] = base64.b64decode(bot["colourData"])
            bot["colourDataHex"] = bot["colourDataDecoded"].hex()

        else:
            file = open(botfile, "r")
            bot["cubeDataHex"] = file.readline()
            bot["colourDataHex"] = "0" * len(bot["cubeDataHex"])

        h1 = bot["cubeDataHex"][0:2]
        h2 = bot["cubeDataHex"][2:4]
        h3 = bot["cubeDataHex"][4:6]
        h4 = bot["cubeDataHex"][6:8]
        cubeCount = int(h1, 16) + (256 * int(h2, 16)) + (256 * 256 * int(h3, 16))
        cubeCount += (256 * 256 * 256 * int(h4, 16))

        cubeData = {
                "cubeHex": bot["cubeDataHex"],
                "colourHex": bot["colourDataHex"],
                "cubeCount": cubeCount
                }

        return cubeData
#        return(bot["cubeDataHex"], bot["colourDataHex"], cubeCount)

    def parseCSVFile(self, csvfile):
        cubedatabase = dict()
        with open(csvfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                cubeimportdetails = dict()
                objectlist = list()
                cubeID = "#" 
                x = 0
                for item in row:
                    if (x == 0):
                        cubeimportdetails["cubename"] = item
                    if (x == 1): 
                        cubeimportdetails["cubeID"] = item
                        cubeID = item
                    if (x == 2):
                        cubeimportdetails["blendfile"] = item
                    if (x > 2): 
                        objectlist.append(item)
                    x = (x + 1)

                cubeimportdetails["object"] = json.dumps(objectlist)
                if cubeimportdetails["cubename"][0:1] != "#":
                    cubedatabase[cubeID] = json.dumps(cubeimportdetails)

        return(cubedatabase)

    def getCubeData(self, cubeData, colourData, index):
        if index == -1:
            # return the header info (first 8 characters)
            h1 = cubeData[0:2]
            h2 = cubeData[2:4]
            h3 = cubeData[4:6]
            h4 = cubeData[6:8]

            cubeCount = (int(h1, 16) + (256 * int(h2, 16)) + (256 * 256 * int(h3, 16)) + (256 * 256 * 256 * int(h4, 16)))
            return(cubeCount)

        else:
            marker = 8+(index*16)
            output = dict()

            # Decode the ID number
            h1 = cubeData[marker+0:marker+2]
            h2 = cubeData[marker+2:marker+4]
            h3 = cubeData[marker+4:marker+6]
            h4 = cubeData[marker+6:marker+8]
            output["ID"] = str(int(h1, 16) + (256 * int(h2, 16)) + (256 * 256 * int(h3, 16)) + (256 * 256 * 256 * int(h4, 16)))
            # Decode the location and orientation
            output["X"] = int(cubeData[marker + 8:marker+10], 16)
            output["Z"] = int(cubeData[marker + 10:marker+12], 16)
            output["Y"] = int(cubeData[marker + 12:marker+14], 16)
            output["O"] = int(cubeData[marker + 14:marker+16], 16)

            # Decode the colour
            colourmarker = 8 + (index * 8)
            output["Colour"] = int(colourData[colourmarker:colourmarker + 2], 16)

            return(output)
