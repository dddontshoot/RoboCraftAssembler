import os
import base64

# open the output file, we'll need that later on
outputfile=open("output.csv","w")

# go find me a list of all the bots in this folder
filelist=os.listdir()

# repeat these steps for every file in the list
while len(filelist) > 0:
 filename=filelist.pop()
 
 # I'm only interested in the .bot files, folders and other files are ignored
 if filename[len(filename)-4:len(filename)] == ".bot":
  
  # open the .bot file and read the data
  file=open(filename,"r")
  line=file.readline()

  #find the cubeData and extract it
  fragment=line[0:17]
  while fragment != "    \"cubeData\": \"":
    line=file.readline()
    fragment=line[0:17]
  lengthofdata=len(line)-3
  cubeData=line[17:lengthofdata]

  # output some fragment to the screen so we can see what steps are being taken
  print()
  print(filename)
  print(cubeData[0:20])
  
  # convert the base64 code from the file into binary
  decodedstring=base64.b64decode(cubeData)
  print(decodedstring[0:20])

  # convert binary into hex
  datainhex=decodedstring.hex()
  print(datainhex[0:20])

  ######### now do it all over again, but this time look for culourData

  # find the colourData and extract it
  while fragment != "    \"colourData\": \"":
    line=file.readline()
    fragment=line[0:19]
  lengthofdata=len(line)-3
  colourData=line[19:lengthofdata]
  colourDataDecoded=base64.b64decode(colourData)
  
  # output the data to a csv file
  outputfile.write(filename+","+"cubeData"+","+str(decodedstring.hex())+"\n")
  outputfile.write(filename+","+"colourData"+","+str(colourDataDecoded.hex())+"\n")
