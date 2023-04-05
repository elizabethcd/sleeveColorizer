import json
import argparse
from PIL import Image
from pathlib import Path
import numpy as np

shirtsFoldername = "input"

def main():
	# Create the parser
	parser = argparse.ArgumentParser()
	# Add an argument
	parser.add_argument('--showColorways', type=str, required=False, help="Whether to output colorway images too")
	# Parse the argument
	args = parser.parse_args()

	showColorways = False
	# Parse the input manually to handle case-sensitivity
	if args.showColorways is None:
		showColorways = False
	elif args.showColorways == "False" or args.showColorways == "false":
		showColorways = False
	elif args.showColorways == "True" or args.showColorways == "true":
		showColorways = True
	else:
		print("Invalid input, defaulting to no colorways")

	# Get all images in shirts folder
	folderPath = Path(shirtsFoldername)
	filelist = folderPath.glob("**/*.png")

	# Crunch through all the images
	for file in filelist:
		print("Processing " + str(file))
		originalImage = Image.open(Path(file))

		# Grab the colors and sort them by sum of RGB values
		colorList = originalImage.getcolors()
		pixelsOnly = [i[1] for i in colorList]
		sortedPixels = sorted(pixelsOnly, key=lambda x: x[0]+x[1]+x[2])

		# Remove transparent pixel
		if (0, 0, 0, 0) in sortedPixels:
			sortedPixels.remove((0, 0, 0, 0))

		# Save a colorway image if desired
		if showColorways:
			# Convert the pixels into an array using numpy
			npPix = [(i[0],i[1],i[2]) for i in sortedPixels]
			npPix = [npPix]
			npPix = np.array(npPix, dtype=np.uint8)

			# Use PIL to create an image from the new array of pixels
			new_image = Image.fromarray(npPix, mode="RGB")
			new_image.save(file.parent.joinpath('colorway.png'))

		# Grab the first, middle, and last colors
		color1 = sortedPixels[0]
		color2 = sortedPixels[len(sortedPixels)//2]
		color3 = sortedPixels[-1]
		fileDict = {}
		fileDict["SleeveColors"] = [[color1[0],color1[1],color1[2]],[color2[0],color2[1],color2[2]],[color3[0],color3[1],color3[2]]]
		
		with file.parent.joinpath("sleeve_colors.json").open("w") as write_file:
			json.dump(fileDict, write_file, indent=4)

# Call the main function
main()