import random
import math
import RNG
import logging
from pymclevel import alphaMaterials, BoundingBox
import utilityFunctions as utilityFunctions
from GenerateObject import *

def generateCrous(matrix, h_min, h_max, x_min, x_max, z_min, z_max, ceiling = None):

	house = utilityFunctions.dotdict()
	house.type = "house"
	house.lotArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

	utilityFunctions.cleanProperty(matrix, h_min+1, h_max, x_min, x_max, z_min, z_max)

	room_size = 4
	(h_min, h_max, x_min, x_max, z_min, z_max) = getBuildArea(h_min, h_max, x_min, x_max, z_min, z_max, room_size)

	house.buildArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})
	
	logging.info("Generating lego house at area {}".format(house.lotArea))
	logging.info("Construction area {}".format(house.buildArea))

	height = 3
	floors_rooms = [0] * ((h_max-h_min) // height)
	ori = orientation()
	single_ori = RNG.random() < 0.5

	for z in range(z_min, z_max, room_size):
		for x in range(x_min, x_max, room_size):
			for f in range(h_min, h_max, height):
				ori = ori if single_ori else orientation()
				wood = (5, RNG.randint(0,5))
				generateRoom(f, f+height, x, x+room_size, z, z+room_size, matrix, wood, (floors_rooms[(f-h_min)//height] == 0), ori)
				generateLadder(f, x, z, matrix, ori, h_min)
				floors_rooms[(f-h_min)//height] += 1
				if RNG.random() < 0.3:
					generateRoof(f+height, x, x+room_size, z, z+room_size, matrix, wood)
					break
	
	z_mid = z_min + (z_max-z_min) // 2
	house.entranceLot = (h_min+1, house.lotArea.x_min, z_mid)

	for x in range(house.lotArea.x_min, x_min):
		matrix.setValue(h_min, x, z_mid-1, (4,0))
		matrix.setValue(h_min, x, z_mid, (4,0))
		matrix.setValue(h_min, x, z_mid+1, (4,0))
	for z in range(z_min+1, z_max):
		matrix.setValue(h_min, x_min-1, z, (4,0))
		matrix.setValue(h_min, x_min-2, z, (4,0))
	
	house.orientation = getOrientation(matrix, house.lotArea)

	return house

def generateRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix, wood, bedroom, orientation):
	#generate walls
	for y in range(h_min+1, h_max):
		for x in range(x_min, x_max+1):
			matrix.setValue(y, x, z_min, wood)
			matrix.setValue(y, x, z_max, wood)
		for z in range(z_min, z_max+1):
			matrix.setValue(y, x_min, z, wood)
			matrix.setValue(y, x_max, z, wood)

	#generate floor
	for x in range(x_min, x_max+1):
		for z in range(z_min, z_max+1):
			matrix.setValue(h_min, x, z, wood)

	#generate door
	if orientation == "n":
		matrix.setValue(h_min+2, x_min+1, z_max, (64,8))
		matrix.setValue(h_min+1, x_min+1, z_max, (64,3))
	elif orientation == "e":
		matrix.setValue(h_min+2, x_min, z_min+1, (64,8))
		matrix.setValue(h_min+1, x_min, z_min+1, (64,0))
	elif orientation == "s":
		matrix.setValue(h_min+2, x_max-1, z_min, (64,8))
		matrix.setValue(h_min+1, x_max-1, z_min, (64,1))
	elif orientation == "w":
		matrix.setValue(h_min+2, x_max, z_max-1, (64,8))
		matrix.setValue(h_min+1, x_max, z_max-1, (64,2))

	#generate window
	if orientation == "n":
		matrix.setValue(h_min+2, x_min+2, z_max, (20,0))
	elif orientation == "e":
		matrix.setValue(h_min+2, x_min, z_min+2, (20,0))
	elif orientation == "s":
		matrix.setValue(h_min+2, x_min+2, z_min, (20,0))
	elif orientation == "w":
		matrix.setValue(h_min+2, x_max, z_min+2, (20,0))

	rooms = [generateBedRoom, generateBathRoom, generateKitchenRoom, generateLivingRoom, generateDiningRoom, generateLibraryRoom]
	room = rooms[0] if bedroom else rooms[RNG.randint(1, len(rooms))]
	return room(h_min, h_max, x_min, x_max, z_min, z_max, matrix)


def generateRoof(h, x_min, x_max, z_min, z_max, matrix, ceiling):
	#43,5
	for x in range(x_min+1, x_max):
		#left
		if matrix.getValue(h,x,z_min) == (0, 0):
			matrix.setValue(h,x,z_min, (109,2))
		elif matrix.getValue(h,x,z_min) == (109,3):
			matrix.setValue(h,x,z_min, (43,5))

		#right
		if matrix.getValue(h,x,z_max) == (0, 0):
			matrix.setValue(h,x,z_max, (109,3))
		elif matrix.getValue(h,x,z_max) == (109,2):
			matrix.setValue(h,x,z_max, (43,5))

	for z in range(z_min+1, z_max):
		#front
		if matrix.getValue(h,x_min,z) == (0, 0):
			matrix.setValue(h,x_min,z, (109,0))
		elif matrix.getValue(h,x_min,z) == (109,1):
			matrix.setValue(h,x_min,z, (43,5))

		#back
		if matrix.getValue(h,x_max,z) == (0, 0):
			matrix.setValue(h,x_max,z, (109,1))
		elif matrix.getValue(h,x_max,z) == (109,0):
			matrix.setValue(h,x,x_max,z, (43,5))
	
	#corners
	if matrix.getValue(h,x_min,z_min) == (0, 0): matrix.setValue(h,x_min,z_min, (44,5))
	if matrix.getValue(h,x_min,z_max) == (0, 0): matrix.setValue(h,x_min,z_max, (44,5))
	if matrix.getValue(h,x_max,z_min) == (0, 0): matrix.setValue(h,x_max,z_min, (44,5))
	if matrix.getValue(h,x_max,z_max) == (0, 0): matrix.setValue(h,x_max,z_max, (44,5))

	#middle
	for x in range(x_min+1, x_max):
		for z in range(z_min+1, z_max):
			matrix.setValue(h,x,z, ceiling)
			matrix.setValue(h,x,z, ceiling)
			matrix.setValue(h,x,z, ceiling)

def possible_rooms(x_min, x_max, z_min, z_max, room_size):
	return ((x_max-x_min) // room_size, (z_max-z_min) // room_size)

def nb_rooms(possible_rooms_x, possible_rooms_z):
	return (RNG.randint(1, possible_rooms_x), RNG.randint(1, possible_rooms_z))

def fenceWood(w):
	if w == (5, 1):
		return (188,0)
	elif w == (5, 2):
		return (189,0)
	elif w == (5, 3):
		return (190,0)
	elif w == (5, 4):
		return (192,0)
	elif w == (5, 5):
		return (191,0)
	else:
		return (85,0)

def generateBedRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix):
	generateBed(matrix, h_min, x_max, z_max-2)
	generateTable(matrix, h_min, x_max-1, z_max-2)
	generateChestTorch(matrix, h_min, x_min+1, z_max-1)

def generateBathRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix):
	generateBed(matrix, h_min, x_max, z_max-2)
	generateTable(matrix, h_min, x_max-1, z_max-2)
	generateChestTorch(matrix, h_min, x_min+1, z_max-1)

def generateKitchenRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix):
	generateBed(matrix, h_min, x_max, z_max-2)
	generateTable(matrix, h_min, x_max-1, z_max-2)
	generateChestTorch(matrix, h_min, x_min+1, z_max-1)

def generateLivingRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix):
	generateBed(matrix, h_min, x_max, z_max-2)
	generateTable(matrix, h_min, x_max-1, z_max-2)
	generateChestTorch(matrix, h_min, x_min+1, z_max-1)

def generateDiningRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix):
	generateBed(matrix, h_min, x_max, z_max-2)
	generateTable(matrix, h_min, x_max-1, z_max-2)
	generateChestTorch(matrix, h_min, x_min+1, z_max-1)

def generateLibraryRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix):
	generateBed(matrix, h_min, x_max, z_max-2)
	generateTable(matrix, h_min, x_max-1, z_max-2)
	generateChestTorch(matrix, h_min, x_min+1, z_max-1)

def generateLadder(h, x, z, matrix, orientation, h_min, ladder = (65,4), path = (44,11)):
	f = h
	if orientation == "n":
		if matrix.getValue(f+2,x+1,z+4) == (64,8) and matrix.getValue(f,x+1,z+5) == (0,0):
			matrix.setValue(f,x+1,z+5, path)
			matrix.setValue(f,x+2,z+5, path)
		while matrix.getValue(f,x+3,z+5) == (0,0):
			matrix.setValue(f,x+3,z+5, (65,3))
			if matrix.getValue(f,x+1,z+4) == (64,8) and matrix.getValue(f-2,x+1,z+5) == (0,0):
				matrix.setValue(f-2,x+1,z+5, path)
				matrix.setValue(f-2,x+2,z+5, path)
			f -= 1
#		if f > h_min:
#			generateOnlyLadder(f-1, x, z+4, matrix, orientation, h_min)
	elif orientation == "e":
		if matrix.getValue(f+2,x,z+1) == (64,8) and matrix.getValue(f,x-1,z+1) == (0,0):
			matrix.setValue(f,x-1,z+1, path)
			matrix.setValue(f,x-1,z+2, path)
		while matrix.getValue(f,x-1,z+3) == (0,0):
			matrix.setValue(f,x-1,z+3, (65,4))
			if matrix.getValue(f,x,z+1) == (64,8) and matrix.getValue(f-2,x-1,z+1) == (0,0):
				matrix.setValue(f-2,x-1,z+1, path)
				matrix.setValue(f-2,x-1,z+2, path)
			f -= 1
#		if f > h_min:
#			generateOnlyLadder(f-1, x-4, z, matrix, orientation, h_min)
	elif orientation == "s":
		if matrix.getValue(f+2,x+3,z) == (64,8) and matrix.getValue(f,x+3,z-1) == (0,0):
			matrix.setValue(f,x+3,z-1, path)
			matrix.setValue(f,x+2,z-1, path)
		while matrix.getValue(f,x+1,z-1) == (0,0):
			matrix.setValue(f,x+1,z-1, (65,2))
			if matrix.getValue(f,x+3,z) == (64,8) and matrix.getValue(f-2,x+3,z-1) == (0,0):
				matrix.setValue(f-2,x+3,z-1, path)
				matrix.setValue(f-2,x+2,z-1, path)
			f -= 1
#		if f > h_min:
#			generateOnlyLadder(f-1, x, z-4, matrix, orientation, h_min)
	elif orientation == "w":
		if matrix.getValue(f+2,x+4,z+3) == (64,8) and matrix.getValue(f,x+5,z+3) == (0,0):
			matrix.setValue(f,x+5,z+2, path)
			matrix.setValue(f,x+5,z+3, path)
		while matrix.getValue(f,x+5,z+1) == (0,0):
			matrix.setValue(f,x+5,z+1, (65,5))
			if matrix.getValue(f,x+4,z+3) == (64,8) and matrix.getValue(f-2,x+5,z+3) == (0,0):
				matrix.setValue(f-2,x+5,z+2, path)
				matrix.setValue(f-2,x+5,z+3, path)
			f -= 1
#		if f > h_min:
#			generateOnlyLadder(f-1, x+4, z, matrix, orientation, h_min)

def generateOnlyLadder(h, x, z, matrix, orientation, h_min, ladder = (65,4), path = (44,11)):
	f = h
	if orientation == "n":
		while matrix.getValue(f,x+3,z+5) == (0,0):
			matrix.setValue(f,x+3,z+5, (65,3))
			f -= 1
		if f > h_min:
			generateOnlyLadder(f-1, x, z+4, matrix, orientation, h_min)
	elif orientation == "e":
		while matrix.getValue(f,x-1,z+3) == (0,0):
			matrix.setValue(f,x-1,z+3, (65,4))
			f -= 1
		if f > h_min:
			generateOnlyLadder(f-1, x-4, z, matrix, orientation, h_min)
	elif orientation == "s":
		while matrix.getValue(f,x+1,z-1) == (0,0):
			matrix.setValue(f,x+1,z-1, (65,2))
			f -= 1
		if f > h_min:
			generateOnlyLadder(f-1, x, z-4, matrix, orientation, h_min)
	elif orientation == "w":
		while matrix.getValue(f,x+5,z+1) == (0,0):
			matrix.setValue(f,x+5,z+1, (65,5))
			f -= 1
		if f > h_min:
			generateOnlyLadder(f-1, x+4, z, matrix, orientation, h_min)

def getHouseAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max):
	house_size_x = x_max - x_min - 2
	if x_max-x_min > house_size_x:
		x_mid = x_min + (x_max-x_min)/2
		x_min = x_mid - house_size_x/2
		x_max = x_mid + house_size_x/2

	house_size_z = z_max - z_min - 2
	if z_max-z_min > house_size_z:
		z_mid = z_min + (z_max-z_min)/2
		z_min = z_mid - house_size_z/2
		z_max = z_mid + house_size_z/2

	crous_size_h = 3
	h_max = h_min + crous_size_h * 20

	return (h_min, h_max, x_min, x_max, z_min, z_max)

def getBuildArea(h_min, h_max, x_min, x_max, z_min, z_max, room_size):
	(h_min, h_max, x_min, x_max, z_min, z_max) = getHouseAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max)
	(x_rooms, z_rooms) = possible_rooms(x_min, x_max, z_min, z_max, room_size)
	(x_rooms, z_rooms) = nb_rooms(x_rooms, z_rooms)

	house_size_x = x_rooms * room_size
	if x_max-x_min > house_size_x:
		x_mid = x_min + (x_max-x_min)/2
		x_min = x_mid - house_size_x/2
		x_max = x_mid + house_size_x/2

	house_size_z = z_rooms * room_size
	if z_max-z_min > house_size_z:
		z_mid = z_min + (z_max-z_min)/2
		z_min = z_mid - house_size_z/2
		z_max = z_mid + house_size_z/2

	crous_size_h = 3
	h_max = h_min + crous_size_h * 20

	return (h_min, h_max, x_min, x_max, z_min, z_max)	

def orientation():
	oris = ["n", "e", "s", "w"]
	ori = RNG.randint(0, 4)
	return oris[ori]

def getOrientation(matrix, area):
	x_mid = matrix.width/2
	z_mid = matrix.depth/2

	bx_mid = area.x_min + (area.x_max-area.x_min)/2
	bz_mid = area.z_min + (area.z_max-area.z_min)/2

	if bx_mid <= x_mid:
		if bz_mid <= z_mid:
			#SOUTH, EAST
			return RNG.choice(["S", "E"])
		elif bz_mid > z_mid:
			# SOUTH, WEST
			return RNG.choice(["N", "E"])

	elif bx_mid > x_mid:
		if bz_mid <= z_mid:
			# return NORTH, EAST
			return RNG.choice(["S", "W"])
		elif bz_mid > z_mid:
			# return NORTH, WEST
			return RNG.choice(["N", "W"])
	return None
