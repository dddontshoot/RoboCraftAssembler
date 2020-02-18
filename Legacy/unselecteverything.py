def go():
    import bpy
    selected=bpy.context.selected_objects # generate a list of selected objects
    if len(selected) > 0:                 # I want to un-select everything
                for obj in selected:
                    obj.select=False
