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
    import json
    import pathlib
except ImportError:
    print("\nRobocraft Assembler is missing dependencies! Try running: "
          "pip install -r requirements.txt \n")

sys.path.append(str(pathlib.Path().absolute()))
import lib.blender
import lib.parser
import lib.arguments

def makeitso(cubeDataHex,colourDataHex,cubeCount,cubedatabase):

    unknowncube=list()
    cubesinuse=list()
    coloursinuse=list()

    for x in range(0,cubeCount):
        if x/100-int(x/100)==0 and x > 0: 
            percentage_completed=int((x/cubeCount)*100)
            print(percentage_completed,"% complete")
        cube = lib.parser.getCubeData(cubeDataHex,colourDataHex,x)

        if cube["ID"] not in cubedatabase:
            if cube["ID"] not in unknowncube :
                print("Replacing cube",cube["ID"],"with Spotter-Mace-0000")
                unknowncube.append(cube["ID"])
            cube["name"]="#"+cube["ID"]
            cube["ID"]="Spotter-Mace-0000" 
        else:
            cube["name"]=cube["ID"]

        if not cube["ID"] in cubedatabase:
            print("\nError: cannot find ID#",cube["ID"],"in cubes.csv\n")
        cubeimportdetails=json.loads(cubedatabase[cube["ID"]])
        objectlist=json.loads(cubeimportdetails["object"]) # This list tells me which objects I want to import from the library.
        

        section="\\Object\\"
        
        filepath  = cubeimportdetails["blendfile"] + section + cubeimportdetails["object"]
        directory = cubeimportdetails["blendfile"] + section

        for filename in objectlist: # filename is a string. it is the name of the object we're importing from the library.
            if "ColourOveride" in filename:     # some objects are always the same colour eg. the back of the electroshield is always grey.
                        # I've just discovered that blender can perform this task but I need more experimentation when applying textures to faces.
                        filename,rubbish,cube["Colour"]=filename.split("=") # strip off the ColourOveride label, and break the field up into the filename and the colour
                        cube["Colour"]=int(cube["Colour"])
                        #print("item=",filename)
                        #print("rubbish=",rubbish)
                        #print("colourOveride=",cube["Colour"])
            datum=cube["name"]+"."+filename # I'm setting up a datum for every different type of cube. The first T1-Medium-Cube to be imported will be located at the origin
            #                           # and duplicated for every T1-Medium-Cube used in the bot. The same is true for every other type of cube.
            #                           # The datum name needs to include the cube["ID"] and the object because if I am importing a cube with two parts, I need to select each part individually.
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
            lib.blender.unselectEverything() 

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
                newcube.location=(cube["X"],cube["Y"],cube["Z"])

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
                
                if cube["O"] == 0:
                    # correct
                    #                               -90 deg       X  Y  Z
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 1:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 2:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 3:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 4:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 5:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 6:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 7:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 8:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 9:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 10:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 11:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 12:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)        
                if cube["O"] == 13:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 14:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 15:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 16:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 17:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 18:
                    # correct
                    #print("Orientation 18 needs no adjustment")
                    useless=0
                if cube["O"] == 19:
                    # correct
                    bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 20:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 21:
                    # correct
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 22:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 23:
                    # correct
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

       
                # This palette was created by eye, I looked at the screenshot and decided it looked like a light blue,
                # so I made a light blue material in blender as close as I could.
                textureandcolour=str(datum)+"."+str(cube["Colour"]) # built a name for the material out of the cubeID and colourID, eg "227205318.Cube.6" or "1576857358.black"
                if textureandcolour not in coloursinuse: # I keep a list of every material I use. If there's a meterial that's not on the list, we will create it now.
                        # copy, colourise and name the new material
                        newMaterial=bpy.data.objects[datum].active_material.copy()
                        if cube["Colour"]== 20 : newMaterial.diffuse_color=(1.0 ,0.683 ,0.107)     # Birch
                        if cube["Colour"]== 4  : newMaterial.diffuse_color=(0.02 ,0.02 ,0.02)      # Black
                        if cube["Colour"]== 23 : newMaterial.diffuse_color=(0.055 ,0.052 ,0.077)   # Blue01
                        if cube["Colour"]== 24 : newMaterial.diffuse_color=(0.029 ,0.13 ,0.199)    # Blue02
                        if cube["Colour"]== 25 : newMaterial.diffuse_color=(0.139 ,0.33 ,0.761)    # Blue03
                        if cube["Colour"]== 26 : newMaterial.diffuse_color=(0.202 ,0.234 ,0.296)   # Blue04
                        if cube["Colour"]== 27 : newMaterial.diffuse_color=(0.36 ,0.433 ,0.646)    # Blue05
                        if cube["Colour"]== 28 : newMaterial.diffuse_color=(0.406 ,0.877 ,1.0)     # Blue06
                        if cube["Colour"]== 29 : newMaterial.diffuse_color=(0.134 ,0.071 ,0.233)   # Blue07
                        if cube["Colour"]== 8  : newMaterial.diffuse_color=(1.0 ,0.0 ,0.51)        # Bright_Purple
                        if cube["Colour"]== 11 : newMaterial.diffuse_color=(0.416 ,0.098 ,0.012)   # Brown
                        if cube["Colour"]== 9  : newMaterial.diffuse_color=(0.068 ,0.028 ,0.834)   # Dark_Blue
                        if cube["Colour"]== 17 : newMaterial.diffuse_color=(0.528 ,0.059 ,0.038)   # Dark_Brown
                        if cube["Colour"]== 21 : newMaterial.diffuse_color=(0.0 ,0.136 ,0.044)     # Dark_Green
                        if cube["Colour"]== 22 : newMaterial.diffuse_color=(0.097 ,0.108 ,0.016)   # Dark_Olive
                        if cube["Colour"]== 7  : newMaterial.diffuse_color=(0.046 ,0.679 ,0.033)   # Green
                        if cube["Colour"]== 1  : newMaterial.diffuse_color=(0.288 ,0.288 ,0.288)   # Grey
                        if cube["Colour"]== 3  : newMaterial.diffuse_color=(0.0 ,0.748 ,0.8)       # Light_Blue
                        if cube["Colour"]== 13 : newMaterial.diffuse_color=(0.086 ,0.319 ,0.074)   # Light_Green
                        if cube["Colour"]== 12 : newMaterial.diffuse_color=(0.603 ,0.555 ,0.047)   # Light_Olive
                        if cube["Colour"]== 30 : newMaterial.diffuse_color=(0.828 ,0.077 ,0.81)    # Light_Purple
                        if cube["Colour"]== 16 : newMaterial.diffuse_color=(0.883 ,0.03 ,0.002)    # Light_Red
                        if cube["Colour"]== 2  : newMaterial.diffuse_color=(1.0 ,0.282 ,0.0)       # Orange
                        if cube["Colour"]== 15 : newMaterial.diffuse_color=(1.0 ,0.412 ,0.412)     # Pale_Pink
                        if cube["Colour"]== 31 : newMaterial.diffuse_color=(0.757 ,0.518 ,0.846)   # Pale_Purple
                        if cube["Colour"]== 14 : newMaterial.diffuse_color=(1.0 ,0.804 ,0.38)      # Pale_Yellow
                        if cube["Colour"]== 19 : newMaterial.diffuse_color=(0.321 ,0.229 ,0.229)   # Pink
                        if cube["Colour"]== 18 : newMaterial.diffuse_color=(0.367 ,0.175 ,0.211)   # Pinky_Brewster
                        if cube["Colour"]== 10 : newMaterial.diffuse_color=(0.376 ,0.0 ,0.336)     # Purple
                        if cube["Colour"]== 5  : newMaterial.diffuse_color=(0.448 ,0.008 ,0.007)   # Red
                        if cube["Colour"]== 0  : newMaterial.diffuse_color=(1.0 ,1.0 ,1.0)         # White
                        if cube["Colour"]== 6  : newMaterial.diffuse_color=(0.992 ,0.867 ,0.098)   # Yellow
                        newMaterial.specular_color=newMaterial.diffuse_color              # make the specular colour the same as the diffuse colour
                        newMaterial.name=textureandcolour                            # assign it a consistant name
                        # I now have a new material with the correct texture and colour
                        
                        # finally, add the new material to the list of materials in use
                        coloursinuse.append(textureandcolour)
                        
                # assign material to the current object
                newcube.active_material=bpy.data.materials[textureandcolour]
            else:
                # If I had no objects selected after the duplication process, then something went wrong.
                print("error, object ",cube["ID"],"didn't import properly")

    print("removing",len(cubesinuse),"datums now...")
    lib.blender.unselectEverything() 
    for obj in cubesinuse:
        bpy.data.objects[obj].select=True
        bpy.ops.object.delete()


def main(botfile):
    lib.blender.unselectEverything()
    print("\nNow building" + botfile + "...")
    cubeDataHex, colourDataHex, cubeCount = lib.parser.parseBotFile(botfile)
    cubedatabase = lib.parser.parseCSVFile("cubes.csv")
    makeitso(cubeDataHex, colourDataHex, cubeCount, cubedatabase)
    print("done!")


if __name__ == "__main__":
    botfile = lib.arguments.getBotFile()
    main(botfile)
