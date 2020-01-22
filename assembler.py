#RoboCraftAssembler0.3.5
# Will accept command line arguments. Even tho' the default cube is still being stubborn
# work around is to open a blank blender file.
#
# example command line:
#blender blank.blend --python assembler.py -- TheDistractingCicada.bot
#                                            ^ yes, there needs to be a space here!
#                                          ^ a double dash tells blender to pass all the following arguments to python





###################################
# Type your robots filename here: #
###################################
botfile="TheDistractingCicada.bot"
#botfile="Tester.RC14"




# Standard modules:
import bpy
import json
import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute()))


# Custom modules:
import unselecteverything
import getbotfile
import getdatabase


# Command line support:
argv = sys.argv
if "--" in argv:
    botfile = argv[argv.index("--") + 1:].pop(0)











def makeitso(cubeDataHex,colourDataHex,cubeCount,cubedatabase):
    # set the marker to the next character after the header
    marker=8
    colourmarker=8
    unknowncube=list()
    cubesinuse=list()
    coloursinuse=list()
    for x in range(0,cubeCount):
        if x/100-int(x/100)==0 and x > 0: # this is a cute little routine to display a progress message every hundred cubes
            percentage_completed=int((x/cubeCount)*100)
            print(percentage_completed,"% complete")
        # pull all the data relating to the current cube.
        cubeData_ID_hex=cubeDataHex[marker:marker+8]
        cubeData_loc=cubeDataHex[marker+8:marker+16]
        #print("ID=",cubeData_ID)
        #print("loc=",cubeData_loc)

        # don't let this confuse you...
        # cubeData stores the location in X,Z,Y, Orientation!!!
        # Blender works in a different order!!!
        #scale=0.25     # I'm going to try scaling the world down to the size of the cubes.
        scale=1         # now, I'm working with objects that don't need scaling.
        cubeData_X=int(cubeData_loc[0:2],16) * scale
        cubeData_Z=int(cubeData_loc[2:4],16) * scale
        cubeData_Y=int(cubeData_loc[4:6],16) * scale
        cubeData_O=int(cubeData_loc[6:8],16)
        
        # We've extracted the cubeID in decimal from cubeAmounts in the .bot file. I either give the prefab cubes decimal names to match the spreadsheet, or hex names to match the cubeData.
        # Libre Office doesn't convert from decimal to hex properly. It fails whenever it drops the leading zero
        # I will tell blender to convert the cubeData from hex into decimal.

        # converting cubeData_ID from hex into decimal
        h1=cubeData_ID_hex[0:2]
        h2=cubeData_ID_hex[2:4]
        h3=cubeData_ID_hex[4:6]
        h4=cubeData_ID_hex[6:8]
        cubeData_ID=str(int(h1,16)+(256*int(h2,16))+(256*256*int(h3,16))+(256*256*256*int(h4,16)))
        cubeData_name=cubeData_ID # if I don't have the cube I'm looking for I'll change the ID, so I need another variable to store the name
        
        # The database contains all the ID's that have been identified.
        # A known ID number that hasn't been extracted yet will be listed in the csv file, but will point to a substitution file. Probably Spotter-Mace-0.blend
        # An unidentified ID will not be listed in the csv file, and will be substituted with the file Spotter-Mace-2.blend
        if cubeData_ID not in cubedatabase:
            # Unidentified ID found
            if cubeData_ID not in unknowncube :
                print("Replacing cube",cubeData_ID,"with Spotter-Mace-0000")
                unknowncube.append(cubeData_ID)
            # I'm about to change the cubeData_ID, but I want the name of the cube to stay the same, also I'm putting a hash symbol in front
            # so that I know it was replaced. This system is very useful for identifying the ID number for that cosmetic part I've never seen before.
            cubeName="#"+cubeData_ID 
            #cubeData_ID="227205318" # T1-Cube-Medium
            cubeData_ID="Spotter-Mace-0000"  # There should be a line in the csv file that matches the ID "Spotter-Mace-0000" with a substitution file. Probably Spotter-Mace-1.blend 
            #                                # (the one with the rediculious long spikes that you can see a mile away)
            #                                # This is new for version 0.3.2 and does not exist in 0.3
        else:
            cubeName=cubeData_ID

        # go and get the details from the database
        if not cubeData_ID in cubedatabase:
            print("\nError: cannot find ID#",cubeData_ID,"in cubes.csv\n")
            # so... not being able to find an ID# in the csv file doesn't usually cause an error. It just means that you've stumbled upon an unidentified cube,
            # and RoboCraftAssembler will substitute it with the Spotter-Mace. However, if the Spotter-Mace is not in the csv file, then it will cause an error.
            # ID Number: Spotter-Mace-0000
            # file: Spotter-Mace-1.blend or Spotter-Mace-2.blend or what ever your favourite shape is.
        cubeimportdetails=json.loads(cubedatabase[cubeData_ID])
        objectlist=json.loads(cubeimportdetails["object"]) # This list tells me which objects I want to import from the library.
        
        #fullpath = "/Robocraft/Blender/"+cubeimportdetails["blendfile"] 
        #with bpy.data.libraries.load( fullpath  ) as (data_from,data_to):  # use these two lines to inport every object in the library
        #    objectlist=data_from.objects   # get a list of objects in the library. Ill import them seperately

        section="\\Object\\"
        
        filepath  = cubeimportdetails["blendfile"] + section + cubeimportdetails["object"]
        directory = cubeimportdetails["blendfile"] + section
        #filename  = json.loads(cubeimportdetails["object"]

        for filename in objectlist: # filename is a string. it is the name of the object we're importing from the library.
            if "ColourOveride" in filename:     # some objects are always the same colour eg. the back of the electroshield is always grey.
                        # I've just discovered that blender can perform this task but I need more experimentation when applying textures to faces.
                        filename,rubbish,colourData_C=filename.split("=") # strip off the ColourOveride label, and break the field up into the filename and the colour
                        colourData_C=int(colourData_C)
                        #print("item=",filename)
                        #print("rubbish=",rubbish)
                        #print("colourOveride=",colourData_C)
            else:
                colourData_C=int(colourDataHex[colourmarker:colourmarker+2],16) # If there is no ColourOveride, then just pull the colour out of the hex data, like normal.
            datum=cubeName+"."+filename # I'm setting up a datum for every different type of cube. The first T1-Medium-Cube to be imported will be located at the origin
            #                           # and duplicated for every T1-Medium-Cube used in the bot. The same is true for every other type of cube.
            #                           # The datum name needs to include the cubeData_ID and the object because if I am importing a cube with two parts, I need to select each part individually.
            #                           # Eventually, I want to put all the datums on another layer

            if datum not in cubesinuse:   #If we haven't imported one before, do that now.
                print("Importing",datum,"now...")
                # The csv told us which file to import, and which object from that file
                # So lets import it now
                bpy.ops.wm.append(
                filepath=filepath, 
                filename=filename, # lol
                directory=directory
                )

                # I'm going to try and name all the cubes by their ID number. It will make it easier to work with unidentified cubes.
                #bpy.data.objects[filename].hide=True
                bpy.data.objects[filename].name=datum  
                # Actually, that wasn't nearly as hard as I imagioned, blender handles duplicate cube names by adding a 3 digit serial number to the name
                cubesinuse.append(datum)  # now that it has been imported, we can add it to the list.
            
            # now we duplicate it, and move it to the correct location.
            # duplicating works on selected objects, so I have to make sure I unselect everything first.
            unselecteverything.go()

            bpy.data.objects.get(datum).select=True
            bpy.ops.object.duplicate(linked=True) # works perfectly. If the cube has more than one part, the previous for loop handles each object seperately.
            # Each cube's datum will be stored at the origin. Eventually, I want them to be stored on a differernt layer.

            # Move the duplicated cube to the main layer
            #bpy.context.object.hide=False # Make the duplicate visible # or move it from the other layer to the main layer
            #bpy.data.objects[newcube].layers[0]=True   #I will need this line if I'm going to import to a hidden layer, then dupicate to the main layer.
            ##bpy.data.objects[newcube].layers[1]=False # This line does remove the cubes from the prefab layer, but it confuses the location on the main layer

            # The duplicating process should result in one, and only one object selected, so set the location to the XYZ co-ordinates.
            selected=bpy.context.selected_objects # generate a list that contains the object I just created beause I don't actually know its name.
            if len(selected) > 0:
                newcube=selected.pop()  # from now on I will refer to the duplicate of the datum as newcube
                
                #newcube.hide=False
                # move to the correct location
                newcube.location=(cubeData_X,cubeData_Y,cubeData_Z)

                # unlink the old material from the current objects
                newcube.material_slots[0].link = 'OBJECT' # I don't want to have a datum for every colour, just every mesh.

                # Orientation
                # There's probably a simple systematic way of doing this, but I don't know what it is

                # I've imported a T1 Laser, and it is top mounted and facing left.
                # That is the same as Orientation 18
                # Therefore, I'm assuming that anything with orientation 18 does not need to be rotated,
                # and every other orientation can be rotated relative to it.
                
                # All those orientation adjustment were based on blocks that, really, didn't have any nominal orientation
                # So they were actually up the wrong way when I imported them
                # I didn't discover that until I inported a hover whci was the correct way up in the library, but the wrong way up once imported
                # This line corrects the problem.
                # bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                # screw it, I'll just rotate every library, the samples I'm recieving are all different anyway.
                
                if cubeData_O == 0:
                    # correct
                    #                               -90 deg       X  Y  Z
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 1:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 2:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 3:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 4:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 5:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 6:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 7:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 8:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 9:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 10:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 11:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 12:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)        
                if cubeData_O == 13:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 14:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 15:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 16:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 17:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 18:
                    # correct
                    #print("Orientation 18 needs no adjustment")
                    useless=0
                if cubeData_O == 19:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 20:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 21:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 22:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cubeData_O == 23:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

       
                # This palette was created by eye, I looked at the screenshot and decided it looked like a light blue,
                # so I made a light blue material in blender as close as I could.
                textureandcolour=str(datum)+"."+str(colourData_C) # built a name for the material out of the cubeID and colourID, eg "227205318.Cube.6" or "1576857358.black"
                if textureandcolour not in coloursinuse: # I keep a list of every material I use. If there's a meterial that's not on the list, we will create it now.
                        # copy, colourise and name the new material
                        newMaterial=bpy.data.objects[datum].active_material.copy()
                        if colourData_C== 20 : newMaterial.diffuse_color=(1.0 ,0.683 ,0.107)     # Birch
                        if colourData_C== 4  : newMaterial.diffuse_color=(0.02 ,0.02 ,0.02)      # Black
                        if colourData_C== 23 : newMaterial.diffuse_color=(0.055 ,0.052 ,0.077)   # Blue01
                        if colourData_C== 24 : newMaterial.diffuse_color=(0.029 ,0.13 ,0.199)    # Blue02
                        if colourData_C== 25 : newMaterial.diffuse_color=(0.139 ,0.33 ,0.761)    # Blue03
                        if colourData_C== 26 : newMaterial.diffuse_color=(0.202 ,0.234 ,0.296)   # Blue04
                        if colourData_C== 27 : newMaterial.diffuse_color=(0.36 ,0.433 ,0.646)    # Blue05
                        if colourData_C== 28 : newMaterial.diffuse_color=(0.406 ,0.877 ,1.0)     # Blue06
                        if colourData_C== 29 : newMaterial.diffuse_color=(0.134 ,0.071 ,0.233)   # Blue07
                        if colourData_C== 8  : newMaterial.diffuse_color=(1.0 ,0.0 ,0.51)        # Bright_Purple
                        if colourData_C== 11 : newMaterial.diffuse_color=(0.416 ,0.098 ,0.012)   # Brown
                        if colourData_C== 9  : newMaterial.diffuse_color=(0.068 ,0.028 ,0.834)   # Dark_Blue
                        if colourData_C== 17 : newMaterial.diffuse_color=(0.528 ,0.059 ,0.038)   # Dark_Brown
                        if colourData_C== 21 : newMaterial.diffuse_color=(0.0 ,0.136 ,0.044)     # Dark_Green
                        if colourData_C== 22 : newMaterial.diffuse_color=(0.097 ,0.108 ,0.016)   # Dark_Olive
                        if colourData_C== 7  : newMaterial.diffuse_color=(0.046 ,0.679 ,0.033)   # Green
                        if colourData_C== 1  : newMaterial.diffuse_color=(0.288 ,0.288 ,0.288)   # Grey
                        if colourData_C== 3  : newMaterial.diffuse_color=(0.0 ,0.748 ,0.8)       # Light_Blue
                        if colourData_C== 13 : newMaterial.diffuse_color=(0.086 ,0.319 ,0.074)   # Light_Green
                        if colourData_C== 12 : newMaterial.diffuse_color=(0.603 ,0.555 ,0.047)   # Light_Olive
                        if colourData_C== 30 : newMaterial.diffuse_color=(0.828 ,0.077 ,0.81)    # Light_Purple
                        if colourData_C== 16 : newMaterial.diffuse_color=(0.883 ,0.03 ,0.002)    # Light_Red
                        if colourData_C== 2  : newMaterial.diffuse_color=(1.0 ,0.282 ,0.0)       # Orange
                        if colourData_C== 15 : newMaterial.diffuse_color=(1.0 ,0.412 ,0.412)     # Pale_Pink
                        if colourData_C== 31 : newMaterial.diffuse_color=(0.757 ,0.518 ,0.846)   # Pale_Purple
                        if colourData_C== 14 : newMaterial.diffuse_color=(1.0 ,0.804 ,0.38)      # Pale_Yellow
                        if colourData_C== 19 : newMaterial.diffuse_color=(0.321 ,0.229 ,0.229)   # Pink
                        if colourData_C== 18 : newMaterial.diffuse_color=(0.367 ,0.175 ,0.211)   # Pinky_Brewster
                        if colourData_C== 10 : newMaterial.diffuse_color=(0.376 ,0.0 ,0.336)     # Purple
                        if colourData_C== 5  : newMaterial.diffuse_color=(0.448 ,0.008 ,0.007)   # Red
                        if colourData_C== 0  : newMaterial.diffuse_color=(1.0 ,1.0 ,1.0)         # White
                        if colourData_C== 6  : newMaterial.diffuse_color=(0.992 ,0.867 ,0.098)   # Yellow
                        newMaterial.specular_color=newMaterial.diffuse_color              # make the specular colour the same as the diffuse colour
                        newMaterial.name=textureandcolour                            # assign it a consistant name
                        # I now have a new material with the correct texture and colour
                        
                        # finally, add the new material to the list of materials in use
                        coloursinuse.append(textureandcolour)
                        
                # assign material to the current object
                newcube.active_material=bpy.data.materials[textureandcolour]
            else:
                # If I had no objects selected after the duplication process, then something went wrong.
                print("error, object ",cubeData_ID,"didn't import properly")

        # set the markers to the next block
        # set up the marker ready for the next cube...    
        marker=marker+16
        colourmarker=colourmarker+8


    # I should put the colour assignment in here because it protects against unexpected changes in the data,
    # but I'm to lazy to write all the code for it, so I'll just put the colour assignment in with the cubeData loop.
    #It'll probably work. I'm sure the data will be consistant. I doubt it'll go wrong, The chance of it happening are pretty slim...
    #marker=8
    #for x in range(1,cubeCount):
    #    colourData_C=int(colourDataHex[marker:marker+2],16)
    #    colourData_X=int(colourDataHex[marker+2:marker+4],16)
    #    colourData_Z=int(colourDataHex[marker+4:marker+6],16)
    #    colourData_Y=int(colourDataHex[marker+6:marker+8],16)

    # Finally, remove the leftovers
    print("removing",len(cubesinuse),"datums now...")
    unselecteverything.go()
    for obj in cubesinuse:
        bpy.data.objects[obj].select=True
        bpy.ops.object.delete()





###########################################################################################################################################################
# Main ####################################################################################################################################################
###########################################################################################################################################################

def main(botfile):

    ####################################################################
    # Lets _TRY_ and prevent the default cube from contaminating our bot
    ####################################################################


    unselecteverything.go() # lets unselect everything so that we don't get any pre-existing cubes duplicated
    unselecteverything.deletethecube()  # this doesn't actually work!

    
    #########################################################
    # open the .bot file and look for cubeData and colourData
    #########################################################
    
    
    print("\nNow building",botfile,"...")
    
    cubeDataHex,colourDataHex,cubeCount=getbotfile.go(botfile)
    
    
    ##############################################
    # Now open the csv file with the list of cubes
    ##############################################
    
    
    cubedatabase=getdatabase.go("cubes.csv")
    
    
    #################################################
    # We have all the resources, lets go make a robot
    #################################################
    
    
    makeitso(cubeDataHex,colourDataHex,cubeCount,cubedatabase)
    
    
    ##################
    # That's all folks
    ##################
    
    
    print("done!")
    
main(botfile)