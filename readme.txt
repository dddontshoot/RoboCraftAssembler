Hello everyone, and welcome to the RoboCraftAssembler written by dddontshoot, and based on bots downloaded using NGnius's python bot downloader, which can be found here https://github.com/NGnius/rcbup
I have included the bot downloader in this archive, but if there are more recent versions, they can be found on github.

These tools can be used to
1) download bots from the Freejam Factory
2) Assemble a 3D model of your bot in blender.


Improvements since the last version (0.1)

- Textures are included in each library, there are some more in a folder called "Textures"
- Duplication. Each cube type is imported once, then stored as a datum which is duplicated for every cube of that type in the bot. The datums are then removed at the end of the script.
- ColourOveride. You might notice some random looking characters in the csv file. Until I figure out how to do persistant colours properly in blender (I know it's possible, I stumbled onto it) those objects that are designed to not change colour, have been flagged in the csv file.
- A handful of new cubes (T5 laser, the two largest electroshields, full set of compact cubes, T5 Hover, T5 Mech Leg)
- Scale is now 100%, the previous version was 25%






Requirements:

Blender - I'm using 2.7.9b
python - I'm using 3.6.8

For context, I tested this on my laptop which uses blender 2.7.6 and python 3.5.2 and it fails miserably when trying to import objects.






We all got a bit of a scare when FreeJam announced that it wouldn't be releasing any more updates for RoboCraft, we're hoping it doesn't mean RoboCrafts days are numbered because we love playing it, but in case they decide to pull the plug, we want to at least keep our bots that we spent hours building.
Which is why we're working on this RoboCraftAssembler project, once you have your bot saved in blender you could print it out and put it on your desk, the hood of your car, or use it in a roleplaying game or whatever you want really.





And here's what you need to know to do it:

1) once you have downloaded your bot file, put it in the same folder as the RoboCraftAssembler

2) open RoboCraftAssembler0.3.blend in blender

3) find the main script called "gobuild"

4) change line 12 to match the filename of your bot

5) hit "run script". This can take anything from a few seconds to just over a minute. If you're using linux, it will display a progress report in the terminal.

6) finally, blender gets confused when importing external textures. So click on file > External Data > Find Missing Files and point it to the subfolder called "Textures"




Notes regarding cubes
At the moment we're still extracting all the complex 3D models for each cube type.
We did all the basic ones first, T1-Medium-Cube, T1-Edge-Medium, etc, but we still don't have any round cubes or and guns or wings or rotors or anything really cool like that.
Just the basic cubes.

Any cubes that aren't listed in the csv file will be substituted by a T1-Medium-Cube.
The csv file does contain some substitutions. For example, there's no library for the T1 plasma, so the csv file points to a T1 Laser instead.

The good news it that should you aquire some new 3D models, you (hopefully) won't have to change your code to include them, just update cubes.csv with the names of the new blend libraries and the RoboCraftAssembler will import them when you run the script.

And finally, RoboCraft is currently still operational, and we go there to play against each other, and we want to keep playing there as long as we can because we all love it. So go and keep playing RoboCraft and keep buying cosmetics and robobits and things because Freejam isn't one guy sitting at home on his computer, it's a company and they'll only keep it going for as long as it makes them money. So go and support them by buying cosmetics and things, and hopefully we can keep playing for a long time yet.





Happy gaming everyone.
- dddontshoot