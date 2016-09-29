def chooseMedian(input_list):	
	# gives a number one below the median point for odd-length lists
	median = int(len(input_list) / 2)
	
	return input_list[median]

def colorNess(rgb, color_index):
	red = rgb[0]
	green = rgb[1]
	blue = rgb[2]
	
	if color_index == 0:
		return ((red + red) - green) - blue
	elif color_index == 1:
		return ((green + green) - red) - blue
	elif color_index == 2:
		return ((blue + blue) - red) - green
	
def recursiveSplitList(list, sort_index, iteration):
	if iteration != 0:
		list = sorted(list, key=lambda x: x[sort_index])#list = sorted(list, key=lambda x: colorNess(x, sort_index)) 
		
		sort_index = (sort_index + 1) % 3
		iteration -= 1
		
		length = int(len(list) / 2)
		
		list2 = recursiveSplitList(list[:length], sort_index, iteration)
		list1 = recursiveSplitList(list[length:], sort_index, iteration)
	
	else:
		return list
		
	return list1, list2

def linearScale(pixel_array, int_scale):
	new_array = []
	for row in pixel_array:
		new_row = []
		for pixel in row:
			for i in range(int_scale):
				new_row.append(pixel)
		for i in range(int_scale):
			new_array.append(new_row)
	return new_array
