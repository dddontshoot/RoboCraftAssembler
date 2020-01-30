def go(botfile):
    import json
    import base64

    if botfile[len(botfile)-4:len(botfile)]==".bot":
        # I'm assuming this is an RC15 file
        file=open(botfile,"r")

        bot=json.loads(file.read())

        bot["cubeDataDecoded"]=base64.b64decode(bot["cubeData"])
        bot["cubeDataHex"]=bot["cubeDataDecoded"].hex()

        bot["colourDataDecoded"]=base64.b64decode(bot["colourData"])
        bot["colourDataHex"]=bot["colourDataDecoded"].hex()

    else:
        # try and open raw data from the RC14 project
        file=open(botfile,"r")
        bot["cubeDataHex"]=file.readline()
        bot["colourDataHex"]="0"*len(bot["cubeDataHex"]) # They didn't give me any colour data, but my code expects it, so I have to generate some. I chose white because it took less time to impliment than typing this remark.

    # break up cubeData into fragments
    # start with the header
    
    h1=bot["cubeDataHex"][0:2]
    h2=bot["cubeDataHex"][2:4]
    h3=bot["cubeDataHex"][4:6]
    h4=bot["cubeDataHex"][6:8]

    # Assemble the header into a decimal integer
    cubeCount=int(h1,16)+(256*int(h2,16))+(256*256*int(h3,16))+(256*256*256*int(h4,16))

    return(bot["cubeDataHex"],bot["colourDataHex"],cubeCount)
