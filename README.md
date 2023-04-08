# sleeveColorizer

This is a script that extracts the darkest, lightest, and middlest colors from pngs and writes them up as a SleeveColor for use copy-pasting into FS sleeves. 

# Python modules used

json
argparse
PIL
pathlib
numpy

You may need to `pip install json` etc for some of these

# How to Run

1. Download script
2. Make a folder named `input` in the same folder as the script, and put all of the FS folders into this folder. The input has to be a series of folders, each with `shirt.json` and `shirt.png` in there, with `shirt.json` having front, back, left, and right models in the FS format and the `shirt.png` must have a normal game format front-facing shirt in the top left corner if you want to use the `useGamePixels` option. Basically, it will work with shirts converted from JA and will sort of work with shirts that were not generated that way. 
3. Navigate to location of script
4. Run `python sleeve_colorizer.py` in command line. Optionally, `--showColorway True` to make it dump a `colorway.png` with the colors next to each image. Also optionally, `--useGamePixels True` to make it use instead exactly the three pixels I think the game uses for the colors. 
5. The `shirt.json` will be edited for each folder in the `input` folder
