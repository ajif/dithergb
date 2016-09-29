#!python3

import time

from PIL import Image

import kd

# VARIABLES
SCALE = 4
NUM_COLORS = 9
LINEAR_SCALE = 1
CRUSH_FACTOR = 15
OUTPUT_FORMAT = "png"

# INPUT
input_image = input("Image file: ")

# takes a path and creates an Image object
image = Image.open(input_image)

# store the first value of size tuple, which corresponds to width
imagewidth = image.size[0]
imageheight = image.size[1]

# gets a flattened list of (RGB) values from the image
pixels = list(image.getdata())

print(str(len(pixels)) + " pixels to process.")

# make a list to use as a 2D array of pixels
pixelarray = []

# for every width-length chunk of the flattened list, append a row of pixels to the 2D array
for i in range(imagewidth - 1, len(pixels), imagewidth):
	row = pixels[(i + 1) - imagewidth:i + 1]
	pixelarray.append(row)

# Scale the image by an integer factor. This is useful for showing the dithering patterns.
pixelarray = kd.linearScale(pixelarray, LINEAR_SCALE)
	
# Create a new Image object with the same dimensions as the 2D array (also scaled by the same integer factor).
newimage = Image.new("RGB", (image.size[0] * LINEAR_SCALE, image.size[1] * LINEAR_SCALE))

index_colors = []

rec = kd.recursiveSplitList(pixels, 0, 4)

map = []

for a in rec:
	for b in a:
		for c in b:
			for d in c:
				map.append(d)

for seg in map:
	seg = sorted(seg)
	length = len(seg) // 2
	if length > 0:
		color = seg[length]
		index_colors.append(color[:3])

# color palette override
# zx spectrum
'''index_colors = [(0, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 255), (255, 0, 0),
							(255, 0, 255), (0, 255, 0), (0, 255, 255), (255, 255, 0),
							(0, 0, 215), (215, 0, 0), (215, 0, 215), (0, 215, 0), (0, 215, 215),
							(215, 215, 0), (215, 215, 215)]
'''
print(index_colors)

def encodeBayer(array):
	# unroll each 4x4 square of pixel into a sequence of 16 consecutive pixels
	bayer_array = []
	
	for i in range(0, imageheight, 4):
		for j in range(0, imagewidth, 4):
			
			index = (i * imagewidth) + j
			
			bayer_array += array[index:index+4]
			index += imagewidth
			bayer_array += array[index:index+4]
			index += imagewidth
			bayer_array += array[index:index+4]
			index += imagewidth
			bayer_array += array[index:index+4]
			
	return bayer_array

def decodeBayer(bayer_array):
	# cobble the image back together
	decoded_array1 = []
	decoded_array2 = []
	decoded_array3 = []
	decoded_array4 = []

	for i in range(0, len(bayer_array), 16):
			index = i
			
			decoded_array1 += bayer_array[index:index+4]
			index += 4
			decoded_array2 += bayer_array[index:index+4]
			index += 4
			decoded_array3 += bayer_array[index:index+4]
			index += 4
			decoded_array4 += bayer_array[index:index+4]
	
	decoded_array = []
	
	for i in range(0, len(decoded_array1), imagewidth):
		decoded_array += decoded_array1[i:i+imagewidth]
		decoded_array += decoded_array2[i:i+imagewidth]
		decoded_array += decoded_array3[i:i+imagewidth]
		decoded_array += decoded_array4[i:i+imagewidth]
	
	return decoded_array

def ditherBayer(bayer_array):
	i = 0
	output_array = []
	
	# apply unrolled Bayer matrix to each 16-pixel chunk of the data
	for i in range(0, len(bayer_array), 16):
		output_array.append((bayer_array[i][0] + 1, bayer_array[i][1] + 1, bayer_array[i][2] + 1))
		i += 1
		output_array.append((bayer_array[i][0] + 7, bayer_array[i][1] + 7, bayer_array[i][2] + 7))
		i += 1
		output_array.append((bayer_array[i][0] + 2, bayer_array[i][1] + 2, bayer_array[i][2] + 2))
		i += 1
		output_array.append((bayer_array[i][0] + 8, bayer_array[i][1] + 8, bayer_array[i][2] + 8))
		i += 1
		output_array.append((bayer_array[i][0] + 10, bayer_array[i][1] + 10, bayer_array[i][2] + 10))
		i += 1
		output_array.append((bayer_array[i][0] + 4, bayer_array[i][1] + 4, bayer_array[i][2] + 4))
		i += 1
		output_array.append((bayer_array[i][0] + 12, bayer_array[i][1] + 12, bayer_array[i][2] + 12))
		i += 1
		output_array.append((bayer_array[i][0] + 5, bayer_array[i][1] + 5, bayer_array[i][2] + 5))
		i += 1
		output_array.append((bayer_array[i][0] + 3, bayer_array[i][1] + 3, bayer_array[i][2] + 3))
		i += 1
		output_array.append((bayer_array[i][0] + 9, bayer_array[i][1] + 9, bayer_array[i][2] + 9))
		i += 1
		output_array.append((bayer_array[i][0] + 1, bayer_array[i][1] + 1, bayer_array[i][2] + 1))
		i += 1
		output_array.append((bayer_array[i][0] + 8, bayer_array[i][1] + 8, bayer_array[i][2] + 8))
		i += 1
		output_array.append((bayer_array[i][0] + 13, bayer_array[i][1] + 13, bayer_array[i][2] + 13))
		i += 1
		output_array.append((bayer_array[i][0] + 6, bayer_array[i][1] + 6, bayer_array[i][2] + 6))
		i += 1
		output_array.append((bayer_array[i][0] + 11, bayer_array[i][1] + 11, bayer_array[i][2] + 11))
		i += 1
		output_array.append((bayer_array[i][0] + 5, bayer_array[i][1] + 5, bayer_array[i][2] + 5))
	
	dithered_color_pixels = []
	
	print("dithering")
	
	first_time = time.time()
	
	# for each pixel's color
	for r1, g1, b1 in output_array:
		
		# err... I guess make the numbers negative and do the inverse of this
		# with a maximum of 0 instead of this arbitrary minimum
		minimum = 9999999999999999999
		
		closest_color = (0, 0, 0)
		
		# for each of the colors in the palette 
		# this part seems to be the bottleneck, since it has to happen 16 times per pixel
		for rcolor, gcolor, bcolor in index_colors:
			
			# calculate sort of Euclidean distance from the current color
			difference = abs(rcolor - r1) + abs(gcolor - g1) + abs(bcolor - b1)
			
			# keep the closest of the palette colors as we go along
			if difference < minimum:
				minimum = difference
				closest_color = (rcolor, gcolor, bcolor)
		
		dithered_color_pixels.append(closest_color)
		
	print(time.time() - first_time)
	return dithered_color_pixels

dithered_color_pixels = encodeBayer(pixels)

dithered_color_pixels = ditherBayer(dithered_color_pixels)

dithered_color_pixels = decodeBayer(dithered_color_pixels)

# put the flattened list of pixels into the new Image object
newimage.putdata(dithered_color_pixels)

# put all the index colors at top left
newimage.putdata(index_colors, offset=0.0)

# save Image object as a file
newimage.save("newimage." + OUTPUT_FORMAT)
