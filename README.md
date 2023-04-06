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
2. Make a folder named `input` in the same folder as the script
3. Navigate to location of script
4. Run `python sleeve_colorizer.py` in command line. Optionally, `--showColorway True` to make it dump a `colorway.png` with the colors next to each image. Also optionally, `--useGamePixels True` to make it use instead exactly the three pixels I think the game uses for the colors. 
5. There will be `sleeve_colors.json` next to each png file in the `input` folder
