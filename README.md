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
4. Run `python sleeve_colorizer.py` in command line (optionally, `--showColorway True` to make it dump a `colorway.png` with the colors next to each image)
5. There will be `sleeve_colors.json` next to each png file in the `input` folder
