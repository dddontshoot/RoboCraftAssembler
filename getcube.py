# when this module is given the entire cubeData and colourData fields from the bot file,
# and an index (from 0 to the number of cubes -1)
# it will return all the relevant information for that cube
# eg  {'ID': 227205318, 'X': 19, 'Z': 10, 'Y': 32, 'O': 9, 'Colour': 32}
# to find the number of cubes in a bot, use an index of -1

def go(cubeData,colourData,index):
    if index==-1:
        # return the header info (first 8 characters)
        h1=cubeData[0:2]
        h2=cubeData[2:4]
        h3=cubeData[4:6]
        h4=cubeData[6:8]
        cubeCount=(int(h1,16)+(256*int(h2,16))+(256*256*int(h3,16))+(256*256*256*int(h4,16)))
        return(cubeCount)
    else:
        # find the position of the cube I'm looking for...
        # the first 8 characters are the header
        # data chunks are 16 characters long
        #   8 character ID
        #   2+2+2 character location
        #   2 character orientation
        #
        # for example, the first cube (zero)
        #   position = header of 8 + (0*16)
        #            = 8
        #
        # the second cube (1)
        #   position = header of 8 + (1*16)
        #            = 24

        marker=8+(index*16)

        output=dict() # start with an empty dictionary, and build it up as we go...

        ### Decode the ID number
        h1=cubeData[marker+0:marker+2]
        h2=cubeData[marker+2:marker+4]
        h3=cubeData[marker+4:marker+6]
        h4=cubeData[marker+6:marker+8]
        output["ID"]=(int(h1,16)+(256*int(h2,16))+(256*256*int(h3,16))+(256*256*256*int(h4,16)))
        
        ### Decode the location and orientation
        output["X"]=int(cubeData[marker+8:marker+10],16)
        output["Z"]=int(cubeData[marker+10:marker+12],16)
        output["Y"]=int(cubeData[marker+12:marker+14],16)
        output["O"]=int(cubeData[marker+14:marker+16],16)

        ### Decode the colour
        # The first 8 characters are the header (same as cubeData)
        # Colour data chunks are only 8 characters long
        # The next 2+2+2 characters are the location (same as cubeData)
        # Finally, the last 2 characters are the colour code
        #
        # I'm going to assume that each data chunk in cubeData matches up with the same index of colourData
        # which makes the header, and the first 6 characters of each data chunk superfluous.
        colourmarker=8+(index*8)+6
        output["Colour"]=int(colourData[colourmarker:colourmarker+2],16)

        return(output)