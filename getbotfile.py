def go(botfile):
    import bpy
    import base64

    if botfile[len(botfile)-4:len(botfile)]==".bot":
        # I'm assuming this is an RC15 file
        file=open(botfile,"r")
        line=file.readline()

        #find the cubeData and extract it
        fragment=line[0:17]
        while fragment != "    \"cubeData\": \"":
          line=file.readline()
          fragment=line[0:17]
        lengthofdata=len(line)-3
        cubeDataRaw=line[17:lengthofdata]
        cubeDataDecoded=base64.b64decode(cubeDataRaw)
        cubeDataHex=cubeDataDecoded.hex()

        # find colourData and extract it
        while fragment != "    \"colourData\": \"":
          line=file.readline()
          fragment=line[0:19]
        lengthofdata=len(line)-3
        colourDataRaw=line[19:lengthofdata]
        colourDataDecoded=base64.b64decode(colourDataRaw)
        colourDataHex=colourDataDecoded.hex()

    else:
        # try and open raw data from the RC14 project
        file=open(botfile,"r")
        cubeDataHex=file.readline()
        colourDataHex="0"*len(cubeDataHex) # They didn't give me any colour data, but my code expects it, so I have to generate some. I chose white because it took less time to impliment than typing this remark.

    # break up cubeData into fragments
    # start with the header
    cubeData_header=cubeDataHex[0:8]
    h1=cubeData_header[0:2]
    h2=cubeData_header[2:4]
    h3=cubeData_header[4:6]
    h4=cubeData_header[6:8]

    # Assemble the header into a decimal integer
    cubeCount=int(h1,16)+(256*int(h2,16))+(256*256*int(h3,16))+(256*256*256*int(h4,16))

    return(cubeDataHex,colourDataHex,cubeCount)
