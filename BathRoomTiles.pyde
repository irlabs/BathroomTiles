
# Global imports
import json
from datetime import datetime

# Walls
tileScale = 30 # 30 pixels per 10 cm. / 10 cm tiles

walls = [
	{
		'name': "meubelwand",
		'w': 777, 'h': 795, 'x': 0, 'y': 0,
		'offset': {'x': -2, 'y': -14},
		'excludes': [{
			'w': 60, 'h': 375, 'x': 717, 'y': 420
		}]
	},
	{
		'name': "wc_achter_hoog",
		'w': 270, 'h': 419, 'x': 777, 'y':0,
		'offset': {'x': 1, 'y': -14}
	},
	{
		'name': "wc_achter_boven",
		'w': 270, 'h': 60, 'x': 777, 'y':419,
		'offset': {'x': 1, 'y': 1}
	},
	{
		'name': "wc_achter_laag",
		'w': 300, 'h': 375, 'x': 777, 'y':479,
		'offset': {'x': 1, 'y': -14},
		'excludes': [{
			'w': 30, 'h': 198, 'x': 270, 'y': 0
		}]
	},
	{
		'name': "bad_zijwand",
		'w': 153, 'h': 618, 'x': 1077, 'y':0,
		'offset': {'x': 0, 'y': -14},
		'excludes': [{
			'w': 60, 'h': 420, 'x': 0, 'y': 0
		}]
	},
	{
		'name': "bad_rand",
		'w': 153, 'h': 30, 'x': 1077, 'y':618,
		'offset': {'x': 0, 'y': 1}
	},
	{
		'name': "bad_achter",
		'w': 270, 'h': 618, 'x': 1230, 'y':0,
		'offset': {'x': 1, 'y': -14}
	},
	{
		'name': "bad_wand",
		'w': 870, 'h': 795, 'x': 1500, 'y':0,
		'offset': {'x': 1, 'y': -14},
		'excludes': [{
			'w': 540, 'h': 177, 'x': 0, 'y': 618
		}]
	},
	{
		'name': "douche_wand",
		'w': 246, 'h': 795, 'x': 2370, 'y':0,
		'offset': {'x': 1, 'y': -14}
	},
	{
		'name': "vloer",
		'w': 717, 'h': 540, 'x': 1653, 'y':795,
		'offset': {'x': -1, 'y': 0},
		'excludes': [{
			'w': 387, 'h': 240, 'x': 0, 'y': 0
		}]
	},
	{
		'name': "bad_ombouw_kop",
		'w': 240, 'h': 168, 'x': 1800, 'y':627,
		'offset': {'x': 1, 'y': -11}
	},
	{
		'name': "bad_ombouw_zij",
		'w': 387, 'h': 168, 'x': 1653, 'y':867,
		'offset': {'x': -1, 'y': -11}
	},
]

allColors = [
	{'code': "G1", 'name': "vert fonce", 'r': 92, 'g': 122, 'b': 112},
	{'code': "G2", 'name': "vert uni", 'r': 101, 'g': 129, 'b': 119},
	{'code': "G3", 'name': "vert pale", 'r': 128, 'g': 152, 'b': 137},
	{'code': "G4", 'name': "pistache", 'r': 211, 'g': 230, 'b': 235},
	{'code': "B1", 'name': "blue nuit", 'r': 48, 'g': 72, 'b': 159},
	{'code': "B2", 'name': "blue fonce", 'r': 77, 'g': 101, 'b': 189},
	{'code': "B3", 'name': "blue uni", 'r': 137, 'g': 166, 'b': 233},
	{'code': "Z1", 'name': "noir", 'r': 50, 'g': 50, 'b': 50},
	{'code': "Z2", 'name': "anthracite", 'r': 75, 'g': 75, 'b': 75},
	{'code': "Z3", 'name': "gris perle", 'r': 240, 'g': 240, 'b': 240},
	{'code': "Z4", 'name': "gris pale", 'r': 210, 'g': 210, 'b': 210},
]

colors = ["G1", "G2", "G3", "G2", "G3", "G2", "G3"]

voeg = {'name': "voeg donker", 'r': 100, 'g': 100, 'b': 100}

overview_scale = 0.3
pageMargin_x = 25
pageMargin_y = 25

firstRun = True
storeAsArray = True

allTiles = []

class Rect(object):
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
	def containsRect(self, aRect):
		if (self.x < aRect.x) and ((self.x + self.w) > (aRect.x + aRect.w)) and (self.y < aRect.y) and ((self.y + self.h) > (aRect.y + aRect.h)):
			return True
		return False
	
	def containsPoint(self, x, y):
		if (x > self.x) and (x < self.x + self.w) and (y > self.y) and (y < self.y + self.h):
			return True
		return False	
		
	def insideRectButNotIn(self, allRect, exRect):
		topLeft = allRect.containsPoint(self.x, self.y) and (not exRect.containsPoint(self.x, self.y))
		topRight = allRect.containsPoint(self.x + self.w, self.y) and (not exRect.containsPoint(self.x + self.w, self.y))
		bottomLeft = allRect.containsPoint(self.x, self.y + self.h) and (not exRect.containsPoint(self.x, self.y + self.h))
		bottomRight = allRect.containsPoint(self.x + self.w, self.y + self.h) and (not exRect.containsPoint(self.x + self.w, self.y + self.h))
		if topLeft or topRight or bottomLeft or bottomRight:
			return True
		return False
		
	def description(self):
		return "Rect(%f, %f, %f, %f)" % (self.x, self.y, self.w, self.h)

def setup():
	
	# size(872, 445)
	# size(900, 600)
	# noLoop()

	A4Landscape_w = 29.7
	A4Landscape_h = 21.0
	cmInch = 2.54
	dpi = 72

	docW = (A4Landscape_w / cmInch) * dpi 
	docH = (A4Landscape_h / cmInch) * dpi
	size(floor(round(docW)), floor(round(docH)));
		
def draw():
	global firstRun
	if (firstRun):
		drawBackground(True)
		drawOutlines(overview_scale)
		drawTiles(overview_scale)
		colorSamples()
		firstRun = False

def drawGrid():
	drawOutlines(overview_scale)

def drawBackground(onOverviewPage):
	if onOverviewPage:
		background(200, 200, 200)
	else:
		background(255, 255, 255)

def drawRandom():
	drawTiles(overview_scale)

def saveDataAsJson(data, filename):
	jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
	jsonAsList = jsonData.split('\n')
	saveStrings(filename, jsonAsList)	
	
def save():
	# Saving the .json
	timeName = "tegel_ontwerp_%s" % datetime.strftime(datetime.now(), "%d%b%y_%H.%M.%S")
	jsonFile = "%s.json" % (timeName)
	data = {'colors': allColors, 'walls': walls, 'allTiles': allTiles}
	saveDataAsJson(data, jsonFile)

def keyPressed(event):
	# cmd + g
	if (keyCode == 71) and (event.isMetaDown()): # 71 = g, meta = cmd
		# Draw Grid
		drawGrid()
	# cmd + r
	if (keyCode == 82) and (event.isMetaDown()): # 82 = r, meta = cmd
		print "New Random"
		drawRandom()
	# cmd + s
	if (keyCode == 83) and (event.isMetaDown()): # 83 = s, meta = cmd
		print "Saving ..."
		save()
	if False:
		print "keyCode: %d -  modifiers: %d" % (keyCode, event.getModifiers())
	
def colorSamples():
	bx = 50
	y = 400
	s = 20
	m = 2
	x = bx
	# for color in colors:
	# 	stroke (voeg['r'], voeg['g'], voeg['b'])
	# 	fill(color['r'], color['g'], color['b'])
	# 	rect (x, y, s, s)
	# 	x += s + m
	y += s + m
	x = bx
	for color in allColors:
		stroke (voeg['r'], voeg['g'], voeg['b'])
		fill(color['r'], color['g'], color['b'])
		rect (x, y, s, s)
		x += s + m
		
	
def drawOutlines(scale):
	for wall in walls:
		# Draw the wall
		stroke(100)
		fill(150)
		x = (wall['x'] * scale) + pageMargin_x
		y = (wall['y'] * scale) + pageMargin_y
		w = wall['w'] * scale
		h = wall['h'] * scale
		rect(x, y, w, h)
		# Draw the excludes
		if wall.has_key('excludes'):
			for exclude in wall['excludes']:
				stroke(100)
				fill(200)
				x = ((exclude['x'] + wall['x']) * scale) + pageMargin_x
				y = ((exclude['y'] + wall['y']) * scale) + pageMargin_y
				w = exclude['w'] * scale
				h = exclude['h'] * scale
				rect(x, y, w, h)

def drawTiles(scale):
	global allTiles
	allTiles = []
	tileSize = floor(tileScale * scale)
	count = 0
	for wall in walls[:]:
		# Per wall draw tiles
		tilesOnWall = {}
		tilesOnWall['wall_name'] = wall['name']
		# 
		w = wall['w'] * scale
		h = wall['h'] * scale
		# Calculate the offset
		offsetx = 0
		offsety = 0
		if wall.has_key('offset'):
			offsetx = wall['offset']['x'] * scale
			offsety = wall['offset']['y'] * scale
		wallx = (wall['x'] * scale) 
		wally = (wall['y'] * scale)
		offsetx += wallx
		offsety += wally
		# create an thisWall Rect
		thisWall = Rect(wall['x'] * scale, wall['y'] * scale, w, h)
		# print "All Wall: %s" % (thisWall.description())
		# 
		# stroke the voeg color
		stroke (voeg['r'], voeg['g'], voeg['b'])
		# stroke (200, 100, 100) # red voeg for testing
		noFill()
		tilesArray = []
		# 
		y = offsety
		while y < (h + wally):
			x = offsetx
			tilesRow = []
			while x < (w + wallx):
				# check if not inside an exclude
				shouldInclude = False
				tile = Rect(x, y, tileSize, tileSize)
				if wall.has_key('excludes'):
					for exclude in wall['excludes']:
						ex = (exclude['x'] + wall['x']) * scale
						ey = (exclude['y'] + wall['y']) * scale
						ew = exclude['w'] * scale
						eh = exclude['h'] * scale
						excludeShape = Rect(ex,ey,ew,eh)
						if tile.insideRectButNotIn(thisWall, excludeShape):
							shouldInclude = True
				else:
					shouldInclude = True
				# Only draw the tiles if not inside an exclude
				if shouldInclude:
					# pick random tile
					colorCode = colors[int(random(len(colors)))]
					color = next((c for c in allColors if c['code'] == colorCode), None)
					fill(color['r'], color['g'], color['b'])
					
					# Store in tilesArray
					if storeAsArray:
						tilesRow.append(colorCode)
					else:
						tileDict = {}
						tileDict['c'] = colorCode
						tileDict['x'] = round((x - wallx) / scale)
						tileDict['y'] = round((y - wally) / scale)
						tilesArray.append(tileDict)
					
					# Draw on the screen
					rect(x + pageMargin_x, y + pageMargin_y, tileSize, tileSize)
					count += 1
				else:
					# Store in tilesArray
					if storeAsArray:
						tilesRow.append(None)
				x += tileSize
			# Store in tilesArray
			if storeAsArray:
				tilesArray.append(tilesRow)
			y += tileSize
		tilesOnWall['tiles'] = tilesArray
		allTiles.append(tilesOnWall)
	# print "total tiles: %d" % count		
