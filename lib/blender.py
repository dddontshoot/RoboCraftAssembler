import sys
import bpy
import json
import pathlib

sys.path.append(str(pathlib.Path().absolute()))
import lib.parser

def unselectEverything():
    selected = bpy.context.selected_objects
    if len(selected) > 0:
        for obj in selected:
            obj.select = False


def build(cubeDataHex, colourDataHex, cubeCount, cubedatabase):

    unknowncube = list()
    cubesinuse = list()
    coloursinuse = list()

    for x in range(0, cubeCount):
        if (x / 100 - int(x/100) == 0) and (x > 0): 
            percentage_completed = int((x/cubeCount) * 100)
            print(percentage_completed,"% complete")
        cube = lib.parser.getCubeData(cubeDataHex,colourDataHex, x)

        if cube["ID"] not in cubedatabase:
            if cube["ID"] not in unknowncube :
                print("Replacing cube", cube["ID"], "with Spotter-Mace-0000")
                unknowncube.append(cube["ID"])
            cube["name"] = "#" + cube["ID"]
            cube["ID"] = "Spotter-Mace-0000" 
        else:
            cube["name"] = cube["ID"]

        if not cube["ID"] in cubedatabase:
            print("\nError: cannot find ID#", cube["ID"], "in cubes.csv\n")
        cubeimportdetails = json.loads(cubedatabase[cube["ID"]])
        objectlist = json.loads(cubeimportdetails["object"]) 

        section="\\Object\\"
        
        filepath  = cubeimportdetails["blendfile"] + section + cubeimportdetails["object"]
        directory = cubeimportdetails["blendfile"] + section

        for filename in objectlist: 
            if "ColourOveride" in filename: 
                        filename, rubbish, cube["Colour"] = filename.split("=") 
                        cube["Colour"] = int(cube["Colour"])
            datum = cube["name"] + "." + filename 
            if datum not in cubesinuse:  
                print("Importing", datum, "now...")
                bpy.ops.wm.append(
                filepath = filepath, 
                filename = filename, 
                directory = directory
                )

                bpy.data.objects[filename].name = datum  
                cubesinuse.append(datum) 

            unselectEverything() 

            bpy.data.objects.get(datum).select = True
            bpy.ops.object.duplicate(linked = True) 

            selected=bpy.context.selected_objects 
            if len(selected) > 0:
                newcube=selected.pop() 
                newcube.location=(cube["X"],cube["Y"],cube["Z"])
                newcube.material_slots[0].link = 'OBJECT' 


                if cube["O"] == 0:
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 1:
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 2:
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 3:

                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 4:
                     
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 5:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 6:
                     
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 7:
                     
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 8:
                     
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 9:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 10:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 11:
                     
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 12:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)        
                if cube["O"] == 13:
                     
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 14:
                     
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 15:
                     
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 16:
                     
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 17:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 18:
                     
                    useless=0
                if cube["O"] == 19:
                     
                    bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 20:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 21:
                     
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 22:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                if cube["O"] == 23:
                     
                    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


                textureandcolour=str(datum)+"."+str(cube["Colour"]) 
                if textureandcolour not in coloursinuse: 

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
                        newMaterial.name=textureandcolour                            # assign it a consistant nam
                        coloursinuse.append(textureandcolour)
                newcube.active_material=bpy.data.materials[textureandcolour]
            else:
               
                print("error, object ", cube["ID"], "didn't import properly")

    print("removing",len(cubesinuse),"datums now...")
    for obj in cubesinuse:
        bpy.data.objects[obj].select = True
        bpy.ops.object.delete()