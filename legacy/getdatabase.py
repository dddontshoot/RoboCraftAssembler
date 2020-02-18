def go(csvfile):
    import csv
    import json

    #Example csv file:                             # See how it can handle 2 objects in the same file (TX_Hover_0 and Mega_Hover_Blade_0)
    # T5 Hovers,      3835205776,  RC_TX_Hover.blend,   TX_Hover_0,  Mega_Hover_Blade_0
    # T1 Cube Heavy,  123901970,   Compact_Cube.blend,  Sim_0
    cubedatabase=dict()
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            cubeimportdetails=dict()
            x=0
            objectlist=list()
            cubeID="#" # csv file can handle remarks
            # step 1) load the file into cubeimportdetails
            for item in row:
                if x==0:
                    cubeimportdetails["cubename"]=item
                if x==1:
                    cubeimportdetails["cubeID"]=item
                    cubeID=item
                if x==2:
                    cubeimportdetails["blendfile"]=item
                if x>2: # after the first 3 fields have been read, everything left over gets added to the list of objects
                    objectlist.append(item)
                x=x+1
            cubeimportdetails["object"]=json.dumps(objectlist)
            # step 2) load cubeimportdetails into cubedatabase
            if cubeimportdetails["cubename"][0:1] != "#":
                cubedatabase[cubeID]=json.dumps(cubeimportdetails)

    #print("cubedatabase=",cubedatabase)
    # now we have a database of all the cubes, and everything we need to import them.
    # all strings, no integers.

    return(cubedatabase)
