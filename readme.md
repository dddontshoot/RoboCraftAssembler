# Robocraft Assembler


Hello everyone, and welcome to the RoboCraftAssembler written by dddontshoot, and based on bots downloaded using NGnius's python bot downloader, which can be found here https://github.com/NGnius/rcbup
I have included the bot downloader in this archive, but if there are more recent versions, they can be found on github.

These tools can be used to
1) download bots from the Freejam Factory
2) Assemble a 3D model of your bot in blender.




## Requirements:

Blender - I'm using 2.7.9b (https://download.blender.org/release/Blender2.79)

Python - I'm using 3.6.8


For context, I tested this on my laptop which uses blender 2.7.6 and python 3.5.2 and it fails miserably when trying to import objects.




## List of improvements:

### 0.3.5
- Command line support ~~(even tho' we still haven't figured out the best way to stop the default cube from contaminating our bots)~~ Solved it!
- Modules are now in separate files
- filename change from RoboCraftAssembler0.3.3.py to assembler.py

### 0.3.3
- Same features as 0.3.2, but the code has been broken up into modules

### 0.3.2
New Features:
- The code no longer relies on the prefab blender objects located on layer 2. It was only using them to store the colour information, which has now been embedded in the code.
  It is because of this that I no longer need to embed the code inside a blender file. You can import the code into an empty blender file yourself. It would be nice to run it from the command line terminal, but its clunky and there's still a few bugs to iron out first.
- Unidentified cubes can be substituted with a Spotter-Mace (a basic cube with stickey out bits that make it easy to spot)
  I've included a new csv file which includes the Spotter-Mace, but if you want to update the old csv file from 0.3 yourself, then you need to add the following line:
  Placeholder for cubes I've never seen before,Spotter-Mace-0000,Spotter-Mace-1.blend,Cube
- Compatible with bots from RC14. I've only tested this using Tester.RC14, which was mostly the same format as the RC15 bots, except that the file I was given did not need to be decoded from Base64.
  RC15 uses some of the same ID numbers as the old RC14, some ID were discarded, some are new. It is assumed that RC14 files use the extension .RC14, and that RC15 files use the .bot extension.
  eg. T1 Cube Medium  \ Armored Cube T10 is still 227205318
      Heavy Chassis Cube 1654632428 is not used in RC15
      Neon Cube 150161008 is new to RC15

Boring code stuff that I changed:
- Added a deselecter subroutine
- Attempted and failed to delete the default cube

### 0.3
- Textures are included in each library, there are some more in a folder called "Textures"
- Duplication. Each cube type is imported once, then stored as a datum which is duplicated for every cube of that type in the bot. The datums are then removed at the end of the script.
- ColourOveride. You might notice some random looking characters in the csv file. Until I figure out how to do persistant colours properly in blender (I know it's possible, I stumbled onto it) those objects that are designed to not change colour, have been flagged in the csv file.
- A handful of new cubes (T5 laser, the two largest electroshields, full set of compact cubes, T5 Hover, T5 Mech Leg)
- Scale is now 100%, the previous version was 25%

### 0.1 First version
- Very basic :-)

We all got a bit of a scare when FreeJam announced that it wouldn't be releasing any more updates for RoboCraft, we're hoping it doesn't mean RoboCrafts days are numbered because we love playing it, but in case they decide to pull the plug, we want to at least keep our bots that we spent hours building.
Which is why we're working on this RoboCraftAssembler project, once you have your bot saved in blender you could print it out and put it on your desk, the hood of your car, or use it in a roleplaying game or whatever you want really.


#### And here's what you need to know to do it:
Version 0.3.2 and 0.3.3
1) Open a blank Blender document

2) Find the text editor inside blender, and use it to open RoboCraftAssembler0.3.3.py

3) Change line 12 to match the filename of your bot.

4) hit "run script". This can take anything from a few seconds to just over a minute. If you're using linux, it will display a progress report in the terminal.

5) finally, blender gets confused when importing external textures. So click on file > External Data > Find Missing Files and point it to the subfolder called "Textures"


### Version 0.3
1) once you have downloaded your bot file, put it in the same folder as the RoboCraftAssembler

2) open RoboCraftAssembler0.3.blend in blender

3) find the main script called "gobuild"

4) change line 12 to match the filename of your bot

5) hit "run script". This can take anything from a few seconds to just over a minute. If you're using linux, it will display a progress report in the terminal.

6) finally, blender gets confused when importing external textures. So click on file > External Data > Find Missing Files and point it to the subfolder called "Textures"





## Notes regarding cubes
At the moment we're still extracting all the complex 3D models for each cube type.
We did all the basic ones first, T1-Medium-Cube, T1-Edge-Medium, etc, but we still don't have any round cubes or and guns or wings or rotors or anything really cool like that.
Just the basic cubes.

Any cubes that aren't listed in the csv file will be substituted by Spotter-Mace-1.blend.
The csv file does contain some substitutions. For example, there's no library for the T1 plasma, so the csv file points to a T1 Laser instead.

The good news is that should you aquire some new 3D models, you (hopefully) won't have to change your code to include them, just update cubes.csv with the names of the new blend libraries and the RoboCraftAssembler will import them when you run the script.

### Happy gaming everyone.
**- dddontshoot**

