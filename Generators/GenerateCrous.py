import random
import math
import RNG
import logging
from pymclevel import alphaMaterials, BoundingBox
import utilityFunctions as utilityFunctions
from GenerateCarpet import generateCarpet
from GenerateObject import *

def generateCrous(matrix, h_min, h_max, x_min, x_max, z_min, z_max, material = None, ceiling = None):

	crous = utilityFunctions.dotdict()
	crous.type = "crous"
	crous.lotArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

	utilityFunctions.cleanProperty(matrix, h_min+1, h_max, x_min, x_max, z_min, z_max)

	(h_min, h_max, x_min, x_max, z_min, z_max) = getCrousAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max)

	crous.buildArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})
	
	crous.orientation = getOrientation(matrix, crous.lotArea)

	logging.info("Generating crous apt at area {}".format(crous.lotArea))
	logging.info("Construction area {}".format(crous.buildArea))
	
	wood = RNG.randint(0,5) if material == None else material
	wall = (5, wood) if material == None else material
	fence = fenceWood(wood)
	ceiling = wall if ceiling == None else ceiling
	floor = wall

	if RNG.random() < 0.5:
		generateRoom(h_min, h_max, x_min, x_max, z_min-2, z_max-2, matrix, wall, floor, ceiling)
		generateRoom(h_min, h_max, x_min, x_max, z_min+1, z_max+1, matrix, wall, floor, ceiling)
		crous.entranceLot = (h_min+1, crous.lotArea.x_min, z_min)
		for x in range(crous.lotArea.x_min, x_min):
			matrix.setValue(h_min, x, z_min, (4,0))
			matrix.setValue(h_min, x, z_min+1, (4,0))
		for z in range(z_min-1, z_min+3):
			matrix.setValue(h_min, x_min-1, z, (4,0))
			matrix.setValue(h_min, x_min-2, z, (4,0))
		
		for i in range(3, 100, 3):
			if RNG.random() < 0.3:
				matrix.setValue(h_min+i, x_min, z_min+1, (109,0))
				for x in range(x_min+1, x_max):
					matrix.setValue(h_min+i, x, z_min+1, (43,5))
				matrix.setValue(h_min+i, x_min+4, z_min+1, (109,1))
				break
			j = 1 + i - 3
			generateRoom(h_min+i, h_max+i, x_min, x_max, z_min-2, z_max-2, matrix, wall, floor, ceiling)
			generateLadder(h_min+j, x_min-1, z_min+1-2, matrix, fence)
			generateRoom(h_min+i, h_max+i, x_min, x_max, z_min+1, z_max+1, matrix, wall, floor, ceiling)
			generateLadder(h_min+j, x_min-1, z_min+1+1, matrix, fence)
	
	else:
		generateRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix, wall, floor, ceiling)
		crous.entranceLot = (h_min+1, crous.lotArea.x_min, z_min+1)
		for x in range(crous.lotArea.x_min, x_min):
			matrix.setValue(h_min, x, z_min+1, (4,0))
			matrix.setValue(h_min, x, z_min+2, (4,0))
	
		for i in range(3, 100, 3):
			if RNG.random() < 0.3:
				break
			j = 1 + i - 3
			generateRoom(h_min+i, h_max+i, x_min, x_max, z_min, z_max, matrix, wall, floor, ceiling)
			generateLadder(h_min+j, x_min-1, z_min+1, matrix, fence)

	return crous

def fenceWood(w):
	if w == 1:
		return (188,0)
	elif w == 2:
		return (189,0)
	elif w == 3:
		return (190,0)
	elif w == 4:
		return (192,0)
	elif w == 5:
		return (191,0)
	else:
		return (85,0)

def generateRoom(h_min, h_max, x_min, x_max, z_min, z_max, matrix, wall, floor, ceiling):
	#generate walls
	for y in range(h_min+1, h_max):
		for x in range(x_min, x_max+1):
			matrix.setValue(y, x, z_min, wall)
			matrix.setValue(y, x, z_min+3, wall)
		for z in range(z_min, z_max):
			matrix.setValue(y, x_min, z, wall)
			matrix.setValue(y, x_min+4, z, wall)

	#generate floor
	for x in range(x_min, x_max+1):
		for z in range(z_min, z_max):
			matrix.setValue(h_min, x, z, floor)

	#generate door
	matrix.setValue(h_min+2, x_min, z_min+1, (64,8))
	matrix.setValue(h_min+1, x_min, z_min+1, (64,0))

	#generate window
	matrix.setValue(h_min+2, x_min+4, z_min+1, (20,0))

	#generate ceiling
	for x in range(x_min, x_min+5):
		matrix.setValue(h_min+3,x,z_min, (109,2))
		matrix.setValue(h_min+3,x,z_min+3, (109,3))
		matrix.setValue(h_min+3,x,z_min+1, ceiling)
		matrix.setValue(h_min+3,x,z_min+2, ceiling)
	for z in range(z_min+1, z_min+3):
		matrix.setValue(h_min+3,x_min,z, (109,0))
		matrix.setValue(h_min+3,x_min+4,z, (109,1))

	#generate interior
	generateBed(matrix, h_min, x_min+4, z_min+1)
	generateTable(matrix, h_min, x_min+3, z_min+1)
	generateChestTorch(matrix, h_min, x_min+1, z_min+2)

def generateLadder(h_min, x, z, matrix, fence, ladder = (65,4), path = (44,11)):
	for h in range(h_min, h_min+3):
		matrix.setValue(h,x,z+1, ladder)
		matrix.setValue(h,x,z+2, fence)
	matrix.setValue(h_min+3,x,z+2, fence)
	matrix.setValue(h_min+2,x,z, path)

def getCrousAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max):
	crous_size_x = 5
	if x_max-x_min > crous_size_x:
		x_mid = x_min + (x_max-x_min)/2
		x_min = x_mid - crous_size_x/2
		x_max = x_mid + crous_size_x/2

	crous_size_z = 4
	if z_max-z_min > crous_size_z:
		z_mid = z_min + (z_max-z_min)/2
		z_min = z_mid - crous_size_z/2
		z_max = z_mid + crous_size_z/2

	crous_size_h = 3
	if h_max-h_min > 15 or h_max-h_min > crous_size_h: 
		h_max = h_min+ ((crous_size_x+crous_size_z)/2)

	return (h_min, h_max, x_min, x_max, z_min, z_max)

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
