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
	parser.add_argument('--useGamePixels', type=str, required=False, help="Whether to use the 3 pixels the game uses")
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

	gamePixelMode = False
	# Parse the input manually to handle case-sensitivity
	if args.useGamePixels is None:
		gamePixelMode = False
	elif args.useGamePixels == "False" or args.useGamePixels == "false":
		gamePixelMode = False
	elif args.useGamePixels == "True" or args.useGamePixels == "true":
		gamePixelMode = True
	else:
		print("Invalid input, defaulting to pulling from all colors in shirt")

	# Get all images in shirts folder
	folderPath = Path(shirtsFoldername)
	# filelist = folderPath.glob("**/*.png")
	shirtFolds = [x for x in folderPath.iterdir() if x.is_dir()]

	# Crunch through all the images
	for folder in shirtFolds:
		print("Processing " + str(folder))

		shirtImage = folder.joinpath('shirt.png')
		shirtJson = folder.joinpath('shirt.json')

		# Make sure you have both a shirt json and a shirt png
		if (shirtImage.is_file() and shirtJson.is_file()):

			originalImage = Image.open(shirtImage)

			# Load in the shirt json
			file_contents = shirtJson.read_text(encoding="UTF-8")
			try:
				originalJson = json.loads(file_contents)
			except json.decoder.JSONDecodeError:
				originalJson = {}
				print("The json file (" + str(shirtJson) + ") specified is not a valid json file. Please try putting it through smapi.io/json and correcting any errors shown there.")
				continue

			# Get the colors out of the image in one of two ways
			if gamePixelMode:
				originalImage = originalImage.convert('RGB')
				color1 = originalImage.getpixel((0,4))
				color2 = originalImage.getpixel((0,3))
				color3 = originalImage.getpixel((0,2))
			else:
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

			print(color1)
			print(color2)
			print(color3)

			# Save the pixels
			sleevecolors = [[color1[0],color1[1],color1[2]],[color2[0],color2[1],color2[2]],[color3[0],color3[1],color3[2]]]
			
			# Do some replacing in the shirt json
			originalJson["FrontShirt"]["SleeveColors"] = sleevecolors
			originalJson["RightShirt"]["SleeveColors"] = sleevecolors
			originalJson["LeftShirt"]["SleeveColors"] = sleevecolors
			originalJson["BackShirt"]["SleeveColors"] = sleevecolors

			# Save the edited shirt json
			with folder.joinpath("shirt.json").open("w") as write_file:
				json.dump(originalJson, write_file, indent=4)

# Call the main function
main()