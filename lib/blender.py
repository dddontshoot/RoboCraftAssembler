import bpy

def unselectEverything():
    selected = bpy.context.selected_objects
    if len(selected) > 0:
        for obj in selected:
            obj.select = False
