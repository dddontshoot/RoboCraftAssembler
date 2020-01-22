def go():
    import bpy
    selected=bpy.context.selected_objects # generate a list of selected objects
    if len(selected) > 0:                 # I want to un-select everything
                for obj in selected:
                    obj.select=False

def deletethecube():
    import bpy
    if not bpy.context.object == None:
        print("found some trash")
        if bpy.context.object.name=="Cube":
            print("cleaning up some trash")
            bpy.ops.object.delete(use_global=True)
            print("existing object:",bpy.context.object.name)
