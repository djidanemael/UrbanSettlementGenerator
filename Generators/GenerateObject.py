
def generateCentralTable(world, y, x, z):
	world.setValue(y+1, x, z, (85,0))
	world.setValue(y+2, x, z, (72,0))
	world.setValue(y+1, x-1, z, (53, 1))
	world.setValue(y+1, x+1, z, (53, 0))

def generateBookshelf(world, y, x, z):
	world.setValue(y+1, x-1, z-1, (47,0))
	world.setValue(y+1, x-2, z-1, (47,0))
	world.setValue(y+2, x-1, z-1, (47,0))
	world.setValue(y+2, x-2, z-1, (47,0))

def generateCouch(world, y, x, z):
	world.setValue(y+1, x+3, z-1, (53, 0))
	world.setValue(y+1, x+2, z-1, (53, 2))
	world.setValue(y+1, x+1, z-1, (53, 1))

def generateChandelier(world, y, x, z, size=1):
	for i in range(1, size+1):
		world.setValue(y-i, x, z, (85,0))
	else:
		world.setValue(y-i-1, x, z, (169,0))

def generateBed(world, y, x, z):
	world.setEntity(y+1, x-1, z+1, (26,11), "bed")
	world.setEntity(y+1, x-2, z+1, (26,3), "bed")

def generateBedNew(world, y, x, z, orientation):
	if orientation == "N":
		world.setEntity(y+1, x, z, (26,8), "bed")
		world.setEntity(y+1, x, z-1, (26,0), "bed")
	elif orientation == "E":
		world.setEntity(y+1, x, z, (26,9), "bed")
		world.setEntity(y+1, x+1, z, (26,1), "bed")
	elif orientation == "S":
		world.setEntity(y+1, x, z, (26,10), "bed")
		world.setEntity(y+1, x, z+1, (26,2), "bed")
	elif orientation == "W": 
		world.setEntity(y+1, x, z, (26,11), "bed")
		world.setEntity(y+1, x-1, z, (26,3), "bed")
	
def generateTable(world, y, x, z):
	world.setValue(y+1, x, z, (85,0))
	world.setValue(y+2, x, z, (72,0))

def generateTorch(world, y, x, z, orientation):
	if orientation == "N":
		world.setValue(y+2, x, z, (50,4))
	elif orientation == "E":
		world.setValue(y+2, x, z, (50,1))
	elif orientation == "S":
		world.setValue(y+2, x, z, (50,3))
	elif orientation == "W":
		world.setValue(y+2, x, z, (50,2))

def generateChest(world, y, x, z, orientation):
	if orientation == "N":
		world.setEntity(y+1, x, z, (54,2), "chest")
	elif orientation == "E":
		world.setEntity(y+1, x, z, (54,5), "chest")
	elif orientation == "S":
		world.setEntity(y+1, x, z, (54,3), "chest")
	elif orientation == "W":
		world.setEntity(y+1, x, z, (54,4), "chest")