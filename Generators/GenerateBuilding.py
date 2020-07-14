import random
import math
import RNG
import logging
from pymclevel import alphaMaterials, BoundingBox
import utilityFunctions as utilityFunctions
from GenerateObject import *
from GenerateCarpet import generateCarpet

def generateBuilding(matrix, h_min, h_max, x_min, x_max, z_min, z_max):

	building = utilityFunctions.dotdict()
	building.type = "building"

	building.area = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

	utilityFunctions.cleanProperty(matrix, h_min+1, h_max, x_min, x_max, z_min, z_max)

	(h_min, h_max, x_min, x_max, z_min, z_max) = getBuildingAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max)
	building.constructionArea = (h_min, h_max, x_min, x_max, z_min, z_max)

	logging.info("Generating house at area {}".format(building.area))
	logging.info("Construction area {}".format(building.constructionArea))

	wall = (159, random.randint(0,15))
	ceiling = wall
	floor = wall

	floor_size = 8
	max_height = h_max-h_min
	if max_height > 32:
		h_max = h_min+random.randint(32, 80 if max_height > 80 else max_height)
		
	while (h_max-h_min) % floor_size != 0:
		h_max -= 1

	generateBuildingWalls(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall)
	generateFloorsDivision(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall)

	building.orientation = getOrientation()

	if building.orientation == "S":
		door_x = RNG.randint(x_min+1, x_max-1)
		door_z = z_max
		generateDoor(matrix, h_min+1, door_x, door_z, (64,9), (64,3))
		building.entranceLot = (h_min+1, door_x, building.area.z_max)
		for z in range(door_z+1, building.area.z_max):
			matrix.setValue(h_min,door_x,z, (4,0))
			matrix.setValue(h_min,door_x-1,z, (4,0))
			matrix.setValue(h_min,door_x+1,z, (4,0))

		generateWindows(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max)
		generateCorridorInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_max-6, z_max)
		generateFloorPlan(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall)
		
		generateStairs(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall)
		generateApartmentInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max-6)
		generateRoofTop(matrix, h_max, x_min, x_max, z_min, z_max, wall)

	return building

def getBuildingAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max):
	building_size_x = random.randint(15, 18)
	if x_max-x_min > building_size_x:
		x_mid = x_min + (x_max-x_min)/2
		x_min = x_mid - building_size_x/2
		x_max = x_mid + building_size_x/2

	building_size_z = random.randint(15, 18)
	if z_max-z_min > building_size_z:
		z_mid = z_min + (z_max-z_min)/2
		z_min = z_mid - building_size_z/2
		z_max = z_mid + building_size_z/2

	return (h_min, h_max, x_min, x_max, z_min, z_max)

def generateStairs(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall):
	cur_floor = h_min
	floor = 0
	while cur_floor < h_max-floor_size:
		step = cur_floor+floor_size-1
		if floor % 2 == 0:
			x = x_max-2
			z = z_max-2
			for x1 in range(x, x-3, -1):
				#removes the floor blocks
				matrix.setValue(step+1, x1, z, (0, 0))
				matrix.setValue(step+1, x1, z-1, (0, 0))
				#removes the carpet blocks
				matrix.setValue(step+2, x1, z, (0, 0))
				matrix.setValue(step+2, x1, z-1, (0, 0))

			while step > cur_floor:
				matrix.setValue(step, x, z, (109, 0))
				matrix.setValue(step, x, z-1, (109, 0))
				for h in range(cur_floor+1, step):
					matrix.setValue(h, x, z, (98, 0))
					matrix.setValue(h, x, z-1, (98, 0))
				
				step -= 1
				x -= 1
		if floor % 2 == 1:
			x = x_min+2
			z = z_max-2
			for x1 in range(x, x+3):
				#removes the floor blocks
				matrix.setValue(step+1, x1, z, (0, 0))
				matrix.setValue(step+1, x1, z-1, (0, 0))
				#removes the carpet blocks
				matrix.setValue(step+2, x1, z, (0, 0))
				matrix.setValue(step+2, x1, z-1, (0, 0))
			while step > cur_floor:
				matrix.setValue(step, x, z, (109, 1))
				matrix.setValue(step, x, z-1, (109, 1))
				for h in range(cur_floor+1, step):
					matrix.setValue(h, x, z, (98, 0))
					matrix.setValue(h, x, z-1, (98, 0))
				step -= 1
				x += 1	

		floor += 1
		cur_floor += floor_size

def generateFloorPlan(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall):
	cur_floor = h_min
	z_wall = z_max-6

	while cur_floor < h_max:

		# generating separating wall between hall and apartments
		for h in range(cur_floor, cur_floor+floor_size):
			for x in range(x_min, x_max):
				matrix.setValue(h, x, z_wall, wall)

		# generating door to the apartment
		x_door = x_max - ((x_max-x_min)/2)
		generateDoor(matrix, cur_floor+1, x_door, z_wall, (64,9), (64,3))

		cur_floor += floor_size

def generateApartmentInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max):
	
	cur_floor = h_min
	floor = 0
	x_mid = x_max - int((x_max - x_min)/2)
	z_mid = z_max - int((z_max - z_min)/2)
	
	while cur_floor < h_max:
		cur_floor_ceiling = cur_floor+floor_size

		generateCarpet(matrix.matrix, cur_floor+1, x_min+1, x_max, z_min+1, z_max)
		generateBed(matrix, cur_floor, x_max, z_min)
		generateCentralTable(matrix, cur_floor, x_mid, z_mid)
		generateBookshelf(matrix, cur_floor, x_max, z_max)
		generateCouch(matrix, cur_floor, x_min, z_max)

		x_mid = x_min + (x_max-x_min)/2
		z_mid = z_min + (z_max-z_min)/2
		generateChandelier(matrix, cur_floor_ceiling, x_mid-2, z_mid, 2)
		generateChandelier(matrix, cur_floor_ceiling, x_mid+2, z_mid, 2)

		cur_floor += floor_size

def generateCorridorInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max):
	cur_floor = h_min
	floor = 0
	x_mid = x_max - int((x_max - x_min)/2)
	z_mid = z_max - int((z_max - z_min)/2)

	while cur_floor < h_max:
		cur_floor_ceiling = cur_floor+floor_size

		x_mid = x_min + (x_max-x_min)/2
		z_mid = z_min + (z_max-z_min)/2
		generateChandelier(matrix, cur_floor_ceiling, x_mid, z_mid, 1)

		# corridor's carpet
		for x in range(x_min+1, x_max):
			for z in range(z_min+1, z_max):
				matrix.setValue(cur_floor+1,x,z, (171, 12))

		cur_floor += floor_size

def generateBuildingWalls(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall):

	# walls along x axis
	for x in range(x_min, x_max+1):
		for y in range(h_min, h_max):
			matrix.setValue(y,x,z_max, wall)
			matrix.setValue(y,x,z_min, wall)

	# walls along z axis
	for z in range(z_min, z_max+1):
		for y in range(h_min, h_max):
			matrix.setValue(y,x_max,z, wall)
			matrix.setValue(y,x_min,z, wall)

def generateFloorsDivision(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall):
	# floors division
	cur_floor = h_min
	while cur_floor <= h_max:
		for x in range(x_min, x_max+1):
			for z in range(z_min, z_max+1):
				matrix.setValue(cur_floor,x,z, wall)

		cur_floor += floor_size

def getOrientation():
	return "S"

def generateDoor(matrix, y, x, z, door_up, door_down):
	matrix.setValue(y+1, x, z, door_up)
	matrix.setValue(y, x, z, door_down)

def generateWindows(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max):
	if abs(x_max-x_min)+1 == 14:
		generateSize14(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, False)
		generateSize14(matrix, h_min, h_max, floor_size, x_min, x_max, z_max, True)
	elif abs(x_max-x_min)+1 == 15:
		generateSize15(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, False)
		generateSize15(matrix, h_min, h_max, floor_size, x_min, x_max, z_max, True)
	elif abs(x_max-x_min)+1 == 16:
		generateSize16(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, False)
		generateSize16(matrix, h_min, h_max, floor_size, x_min, x_max, z_max, True)
	elif abs(x_max-x_min)+1 == 17:
		generateSize17(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, False)
		generateSize17(matrix, h_min, h_max, floor_size, x_min, x_max, z_max, True)
	elif abs(x_max-x_min)+1 == 18:
		generateSize17(matrix, h_min, h_max, floor_size, x_min, x_max-1, z_min, False)
		generateSize17(matrix, h_min, h_max, floor_size, x_min, x_max-1, z_max, True)
	elif abs(x_max-x_min)+1 == 19:
		generateSize17(matrix, h_min, h_max, floor_size, x_min+1, x_max-1, z_min, False)
		generateSize17(matrix, h_min, h_max, floor_size, x_min+1, x_max-1, z_max, True)
	else:
		generateBuildingWindows_AlongZ(matrix, h_min, h_max, floor_size, x_min, x_max, z_min)
		generateBuildingWindows_AlongZ(matrix, h_min, h_max, floor_size, x_min, x_max, z_max)

def generateRoofTop(matrix, h, x_min, x_max, z_min, z_max, wall):
	for x in range(x_min, x_max+1):
		matrix.setValue(h+1, x, z_min, (85,0))
		matrix.setValue(h+1, x, z_max, (85,0))
	for z in range(z_min, z_max+1):
		matrix.setValue(h+1, x_min, z, (85,0))
		matrix.setValue(h+1, x_max, z, (85,0))

	block = matrix.getValue(h-8, x_max-2, z_max-2)
	if isinstance(block, tuple): block = block[0]
	if block == 0:
		for y in range(h-7, h+1):
			matrix.setValue(y, x_min+1, z_max-3, (65,5))
		for y in range(h+1, h+4):
			for x in range(x_min, x_min+2):
				matrix.setValue(y, x, z_max-4, wall)
				matrix.setValue(y, x, z_max-2, wall)
			matrix.setValue(y, x_min, z_max-3, wall)
		matrix.setValue(h+3, x_min+1, z_max-3, wall)

	else:
		for y in range(h-7, h+1):
			matrix.setValue(y, x_max-1, z_max-3, (65,4))
		for y in range(h+1, h+4):
			for x in range(x_max-1, x_max+1):
				matrix.setValue(y, x, z_max-4, wall)
				matrix.setValue(y, x, z_max-2, wall)
			matrix.setValue(y, x_max, z_max-3, wall)
		matrix.setValue(h+3, x_max-1, z_max-3, wall)

def generateBuildingWindows_AlongZ(matrix, h_min, h_max, floor_size, x_min, x_max, z):
	x_window_size = x_max-random.randint(x_min+2, x_max-2)

	# windows
	cur_floor = h_min+1
	while cur_floor < h_max:

		window_h = cur_floor + int(math.ceil(floor_size/2))
		for x in range(x_min+2, x_max-1, 3):
			# apartment windows
			matrix.setValue(window_h, x, z, (20,0))
			matrix.setValue(window_h-1, x, z, (20,0))
			matrix.setValue(window_h, x+1, z, (20,0))
			matrix.setValue(window_h-1, x+1, z, (20,0))

		cur_floor += floor_size

def generateSize14(matrix, h_min, h_max, floor_size, x_min, x_max, z, front):
	# windows
	cur_floor = h_min+1
	if front:
		while cur_floor < h_max:
			x = x_min+1
			x = generateWindow(matrix, cur_floor, x, 3, z, front)
			x = generateWindow(matrix, cur_floor, x, 4, z, front)
			x = generateWindow(matrix, cur_floor, x, 3, z, front)

			cur_floor += floor_size

	else:
		while cur_floor < h_max:
			x = x_min+1
			i = 1
			big = False
			while x < x_max:
				if not big:
					size = 3 if i==4 else random.choice([2,3])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					big = (size == 3)
				else:
					x = generateWindow(matrix, cur_floor, x, 2, z, front)
				i += 1

			cur_floor += floor_size

def generateSize15(matrix, h_min, h_max, floor_size, x_min, x_max, z, front):
	# windows
	cur_floor = h_min+1
	if front:
		while cur_floor < h_max:
			x = x_min+1
			x = generateWindow(matrix, cur_floor, x, 3, z, front)
			x = generateWindow(matrix, cur_floor, x, 5, z, front)
			x = generateWindow(matrix, cur_floor, x, 3, z, front)

			cur_floor += floor_size

	else:
		while cur_floor < h_max:
			x = x_min+1
			i = 1
			big = False
			while x < x_max:
				if not big:
					size = 4 if i==4 else random.choice([2,4])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					big = (size == 4)
				else:
					x = generateWindow(matrix, cur_floor, x, 2, z, front)
				i += 1

			cur_floor += floor_size

def generateSize16(matrix, h_min, h_max, floor_size, x_min, x_max, z, front):
	# windows
	cur_floor = h_min+1
	if front:
		while cur_floor < h_max:
			x = x_min+1
			x = generateWindow(matrix, cur_floor, x, 4, z, front)
			x = generateWindow(matrix, cur_floor, x, 4, z, front)
			x = generateWindow(matrix, cur_floor, x, 4, z, front)

			cur_floor += floor_size

	else:
		while cur_floor < h_max:
			x = x_min+1
			i = 1
			big = False
			bigbig = False
			while x < x_max:
				if not big and not bigbig:
					size = random.choice([3,4]) if i==3 else random.choice([2,3,4])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					big = (size == 3)
					bigbig = (size == 4)
				elif not big and bigbig:
					size = 3 if i==4 else random.choice([2,3])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					big = (size == 3)
				elif big and not bigbig:
					size = 4 if i==4 else random.choice([2,4])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					bigbig = (size == 4)
				else:
					x = generateWindow(matrix, cur_floor, x, 2, z, front)
				i += 1

			cur_floor += floor_size

def generateSize17(matrix, h_min, h_max, floor_size, x_min, x_max, z, front):
	# windows
	cur_floor = h_min+1
	if front:
		while cur_floor < h_max:
			x = x_min+1
			x = generateWindow(matrix, cur_floor, x, 4, z, front)
			x = generateWindow(matrix, cur_floor, x, 5, z, front)
			x = generateWindow(matrix, cur_floor, x, 4, z, front)

			cur_floor += floor_size

	else:
		while cur_floor < h_max:
			x = x_min+1
			i = 1
			smol = False
			bigbig = False
			while x < x_max:
				if not smol and not bigbig:
					if i==3: size = random.choice([2,4])
					else: 	 size = random.choice([2,3,4])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					smol = (size == 2)
					bigbig = (size == 4)
				elif not smol and bigbig:
					size = 2 if i==4 else random.choice([2,3])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					smol = (size == 2)
				elif smol and not bigbig:
					size = 4 if i==4 else random.choice([3,4])
					x = generateWindow(matrix, cur_floor, x, size, z, front)
					bigbig = (size == 4)
				else:
					x = generateWindow(matrix, cur_floor, x, 3, z, front)
				i += 1

			cur_floor += floor_size

def generateWindow(matrix, h_min, x_min, x_size, z, front):
	x = x_min
	window_h = h_min+1 if front else h_min+3 if x_size==2 else h_min+2
	while x < x_min+x_size:
		for h in range(window_h, h_min+5):
			block = matrix.getValue(h, x, z)
			if isinstance(block, tuple): block = block[0]
			if block != 64:
				matrix.setValue(h, x, z, (20,0))
		x += 1
	return x+1
