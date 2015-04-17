
# Global imports
add_library('pdf')
add_library('controlP5')

# Import project dependencies
from RectangleGeometry import Rect
from GradientSliders import GradientController

import json
from datetime import datetime

# Walls
tileScale = 30 # 30 pixels per 10 cm. / 10 cm tiles

# Total height = 795
# Total lenght = 2526 (777 + 270 + (153 - 60) + 270 + 870 + 246) (on eye height)
# length on corner: 2280

walls = [
	{
		'name': "meubelwand",
		'w': 777, 'h': 795, 'x': 0, 'y': 0,
		'offset': {'x': -2, 'y': -14},
		'maps': [
			{'type': "surround", 'x1': 0.0, 'x2': 0.308, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.0, 'y2': 1.0}
		],
		'excludes': [{
			'w': 60, 'h': 375, 'x': 717, 'y': 420
		}]
	},
	{
		'name': "wc_achter_hoog",
		'w': 270, 'h': 419, 'x': 777, 'y':0,
		'offset': {'x': 1, 'y': -14},
		'maps': [
			{'type': "surround", 'x1': 0.308, 'x2': 0.414, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.0, 'y2': 0.473}
		],
	},
	{
		'name': "wc_achter_boven",
		'w': 270, 'h': 60, 'x': 777, 'y':419,
		'offset': {'x': 1, 'y': 1},
		'maps': [
			{'type': "surround", 'x1': 0.308, 'x2': 0.414, 'y1': 0.0, 'y2': -0.012},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.473, 'y2': 0.473}
		],
	},
	{
		'name': "wc_achter_laag",
		'w': 300, 'h': 375, 'x': 777, 'y':479,
		'offset': {'x': 1, 'y': -14},
		'maps': [
			{'type': "surround", 'x1': 0.296, 'x2': 0.402, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.473, 'y2': 1.0}
		],
		'excludes': [{
			'w': 30, 'h': 198, 'x': 270, 'y': 0
		}]
	},
	{
		'name': "bad_zijwand",
		'w': 153, 'h': 618, 'x': 1077, 'y':0,
		'offset': {'x': 0, 'y': -14},
		'maps': [
			{'type': "surround", 'x1': 0.391, 'x2': 0.451, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.0, 'y2': 0.777}
		],
		'excludes': [{
			'w': 60, 'h': 420, 'x': 0, 'y': 0
		}]
	},
	{
		'name': "bad_rand",
		'w': 153, 'h': 30, 'x': 1077, 'y':618,
		'offset': {'x': 0, 'y': 1},
		'maps': [
			{'type': "surround", 'x1': 0.391, 'x2': 0.451, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.777, 'y2': 0.777}
		],
	},
	{
		'name': "bad_achter",
		'w': 270, 'h': 618, 'x': 1230, 'y':0,
		'offset': {'x': 1, 'y': -14},
		'maps': [
			{'type': "surround", 'x1': 0.451, 'x2': 0.558, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.0, 'y2': 0.777}
		],
	},
	{
		'name': "bad_wand",
		'w': 870, 'h': 795, 'x': 1500, 'y':0,
		'offset': {'x': 0, 'y': -14},
		'maps': [
			{'type': "surround", 'x1': 0.558, 'x2': 0.903, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.0, 'y2': 1.0}
		],
		'excludes': [{
			'w': 540, 'h': 177, 'x': 0, 'y': 618
		}]
	},
	{
		'name': "douche_wand",
		'w': 246, 'h': 795, 'x': 2370, 'y':0,
		'offset': {'x': 0, 'y': -14},
		'maps': [
			{'type': "surround", 'x1': 0.903, 'x2': 1.0, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.0, 'y2': 1.0}
		],
	},
	{
		'name': "vloer",
		'w': 717, 'h': 540, 'x': 1653, 'y':795,
		'offset': {'x': -3, 'y': 0},
		'maps': [
			{'type': "surround", 'x1': 0.5, 'x2': 0.5, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 1.0, 'y2': 1.0}
		],
		'excludes': [{
			'w': 387, 'h': 240, 'x': 0, 'y': 0
		}]
	},
	{
		'name': "bad_ombouw_kop",
		'w': 240, 'h': 168, 'x': 1800, 'y':627,
		'offset': {'x': 0, 'y': -11},
		'maps': [
			{'type': "surround", 'x1': 0.677, 'x2': 0.772, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.789, 'y2': 1.0}
		],
	},
	{
		'name': "bad_ombouw_zij",
		'w': 387, 'h': 168, 'x': 1653, 'y':867,
		'offset': {'x': -3, 'y': -11},
		'maps': [
			{'type': "surround", 'x1': 0.402, 'x2': 0.677, 'y1': 0.0, 'y2': 0.0},
			{'type': "floor", 'x1': 0.0, 'x2': 0.0, 'y1': 0.789, 'y2': 1.0}
		],
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
colorsIncludingTransparant = []

defaultColors = ["G1", "G2", "G3", "G2", "G3", "G2", "G3"]

voeg = {'name': "voeg donker", 'r': 100, 'g': 100, 'b': 100}

# Slider Values .json
sliderConfigurationFile = "gradient_sliders.json"

# Scale factors
overview_scale = 0.3
detail_scale = 0.6

# Page margins and other elements
pageMargin_x = 25
pageMargin_y = 25
summaryOffset_y = 300
savedNoticeRect = (280, 300, 230, 40)

# Colors
editorBackgroundColor = color(200, 200, 200)
instructionBackgroundColor = color(255, 255, 255)

# Defaults
storeAsArray = True

# Global variables
firstRun = True
savedNoticeAlpha = 255
allTiles = []
usedColors = []

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
	
	setupSliders()
	
def setupSliders():
	global allColors, colorsIncludingTransparant
	global horizontalCtrl, verticalCtrl
	x = 20
	y = 445
	h = 100 # unused
	w = 400
	x2 = 500
	y2 = 433
	w2 = 250
	slider_h = 10
	slider_w = 50
	
	# Add transparent color
	colorsIncludingTransparant = [{'code': "__", 'name': "clear"}]
	for c in allColors:
		colorsIncludingTransparant.append(c)
	
	# See if there is a gradient_sliders.json file to load
	jsonLines = loadStrings(sliderConfigurationFile)
	if jsonLines:
		# Parse the json
		sliderData = json.loads('\n'.join(jsonLines))
		# Load the ControlP5
		cp5 = ControlP5(this)
		
		# Create the horizontal control
		if sliderData.has_key('surround'):
			if sliderData['surround'].has_key('stops'):
				stops = sliderData['surround']['stops']
				horizontalCtrl = GradientController(allColors, cp5, Slider)
				horizontalCtrl.controllerIdentity = 1
				# The order of settings is important
				horizontalCtrl.setPosition(x, y)
				horizontalCtrl.setSize(w, h)
				horizontalCtrl.setSliderSize(slider_w, slider_h)
				horizontalCtrl.addOuterColorStops()
				# See if it needs additional color stops
				if len(stops) > 2:
					for subStop in stops[1:-1]:
						horizontalCtrl.insertColorStop(subStop['position'])
				horizontalCtrl.recalcSubStopPositions()
				horizontalCtrl.addStopPositionSliders()
				# Set the color values
				horizontalCtrl.setSliderValues(stops)
		
		# Create the vertical control
		if sliderData.has_key('floor'):
			if sliderData['floor'].has_key('stops'):
				stops = sliderData['floor']['stops']
				verticalCtrl = GradientController(colorsIncludingTransparant, cp5, Slider)
				verticalCtrl.controllerIdentity = 2
				# The order of settings is important
				verticalCtrl.setPosition(x2, y2)
				verticalCtrl.setSize(w2, h)
				verticalCtrl.setSliderSize(slider_w, slider_h)
				verticalCtrl.addOuterColorStops()
				# See if it needs additional color stops
				if len(stops) > 2:
					for subStop in stops[1:-1]:
						verticalCtrl.insertColorStop(subStop['position'])
				verticalCtrl.recalcSubStopPositions()
				verticalCtrl.addStopPositionSliders()
				# Set the color values
				verticalCtrl.setSliderValues(stops)
			
		if sliderData.has_key('floor'):
			pass
	else:
		print "No slider settings found -- Initialize with default values"
		# Horizontal Gradient Control
		cp5 = ControlP5(this)
		horizontalCtrl = GradientController(allColors, cp5, Slider)
		horizontalCtrl.controllerIdentity = 1
		# The order of settings is important
		horizontalCtrl.setPosition(x, y)
		horizontalCtrl.setSize(w, h)
		horizontalCtrl.setSliderSize(slider_w, slider_h)
		horizontalCtrl.addOuterColorStops()
		horizontalCtrl.insertColorStop(0.5)
		# horizontalCtrl.insertColorStop(0.7)
		horizontalCtrl.addStopPositionSliders()
		
		# Vertical Gradient Control
		verticalCtrl = GradientController(colorsIncludingTransparant, cp5, Slider)
		verticalCtrl.controllerIdentity = 2
		# The order of settings is important
		verticalCtrl.setPosition(x2, y2)
		verticalCtrl.setSize(w2, h)
		verticalCtrl.setSliderSize(slider_w, slider_h)
		verticalCtrl.addOuterColorStops()
		verticalCtrl.insertColorStop(0.5)
		verticalCtrl.addStopPositionSliders()
		
def draw():
	global firstRun, savedNoticeAlpha
	global horizontalCtrl, verticalCtrl
	if (firstRun):
		drawBackground(True)
		drawOutlines(overview_scale)
		drawRandomTiles(overview_scale)
		# drawColorSamples(allColors, 50, 400)
		usedColors = analyzeColors(allTiles)
		drawUsedColors(usedColors)
		firstRun = False
	# Draw saved notice fade-out pane
	if savedNoticeAlpha < 255:
		savedNoticeAlpha += 1
		noStroke()
		fill(red(editorBackgroundColor), green(editorBackgroundColor), blue(editorBackgroundColor), savedNoticeAlpha)
		rect(savedNoticeRect[0], savedNoticeRect[1], savedNoticeRect[2], savedNoticeRect[3])
	# Drawing the Horizontal Gradient Control
	if horizontalCtrl:
		horizontalCtrl.display()
	if verticalCtrl:
		verticalCtrl.display()
	

def drawGrid():
	drawOutlines(overview_scale, False)

def drawBackground(onOverviewPage):
	if onOverviewPage:
		background(editorBackgroundColor)
	else:
		background(instructionBackgroundColor)

def drawRandom():
	drawRandomTiles(overview_scale)

def saveDataAsJson(data, filename):
	jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
	jsonAsList = jsonData.split('\n')
	saveStrings(filename, jsonAsList)	
	
def save():
	global savedNoticeAlpha
	global horizontalCtrl, verticalCtrl
	# 
	# Saving the gradient slider states
	sliderData = {'surround': horizontalCtrl.getSliderValues()}
	sliderData['floor'] = verticalCtrl.getSliderValues()
	saveDataAsJson(sliderData, sliderConfigurationFile)
	# 
	# Saving the .json
	timeName = "tegel_ontwerp_%s" % datetime.strftime(datetime.now(), "%d%b%y_%H.%M.%S")
	data = {'colors': allColors, 'walls': walls, 'allTiles': allTiles, 'sliders': sliderData}
	saveDataAsJson(data, "%s.json" % (timeName))
	# 
	# Creating a pdf
	pdf = createGraphics(width, height, PDF, "%s.pdf" % (timeName));
	beginRecord(pdf)
	# Draw the first page
	# Overview of all walls
	drawTiles(overview_scale, allTiles)
	# Draw the grid
	drawOutlines(overview_scale, False)
	# Summarize the colors
	usedColors = analyzeColors(allTiles)
	# Draw used colors
	drawUsedColors(usedColors)
	# 
	# Draw per wall
	for tiledWall in allTiles[:]:
		# Next page
		pdf.nextPage()
		# White background
		drawBackground(False)
		# Draw the TilerSchema
		drawTilerInstruction(tiledWall, usedColors, detail_scale)
	# Save the pdf
	endRecord()
	# Restore current overview
	drawTiles(overview_scale, allTiles)
	drawUsedColors(usedColors)
	# Draw the "Saved a version" notification
	fill(0)
	noStroke()
	savedNoticeAlpha = 0
	textSize(28)
	text("Saved a version", savedNoticeRect[0], savedNoticeRect[1], savedNoticeRect[2], savedNoticeRect[3])

def keyPressed(event):
	global horizontalCtrl, verticalCtrl
	# cmd + g
	if (keyCode == 71) and (event.isMetaDown()): # 71 = g, meta = cmd
		# Draw Grid
		drawGrid()
	# cmd + r
	if (keyCode == 82) and (event.isMetaDown()): # 82 = r, meta = cmd
		drawBackground(True)
		drawOutlines(overview_scale)
		drawRandom()
		usedColors = analyzeColors(allTiles)
		drawUsedColors(usedColors)
		horizontalCtrl.needsDisplay = True
		verticalCtrl.needsDisplay = True
	# cmd + s
	if (keyCode == 83) and (event.isMetaDown()): # 83 = s, meta = cmd
		print "Saving ..."
		save()
		horizontalCtrl.needsDisplay = True
		verticalCtrl.needsDisplay = True
	if False:
		print "keyCode: %d -  modifiers: %d" % (keyCode, event.getModifiers())
	
def drawColorSamples(fromColors, startX, startY, drawHorizontal = True):
	s = 12
	m = 3
	x = startX
	y = startY
	for color in fromColors:
		stroke (voeg['r'], voeg['g'], voeg['b'])
		fill(color['r'], color['g'], color['b'])
		rect (x, y, s, s)
		if drawHorizontal:
			x += s + m
		else:
			y += s + m
	
def drawOutlines(scale, filled=True):
	for wall in walls:
		# Draw the walls
		if filled:
			stroke(100)
			fill(150)
		else :	
			stroke(0)
			noFill()
		x = (wall['x'] * scale) + pageMargin_x
		y = (wall['y'] * scale) + pageMargin_y
		w = wall['w'] * scale
		h = wall['h'] * scale
		rect(x, y, w, h)
		# Draw the excludes
		if wall.has_key('excludes'):
			for exclude in wall['excludes']:
				if filled:
					stroke(100)
					fill(200)
				else :	
					stroke(50)
					noFill()
				x = ((exclude['x'] + wall['x']) * scale) + pageMargin_x
				y = ((exclude['y'] + wall['y']) * scale) + pageMargin_y
				w = exclude['w'] * scale
				h = exclude['h'] * scale
				rect(x, y, w, h)

def drawUsedColors(uniqueColors):
	# Draw the text
	usedColorTextSize = 10
	textSize(usedColorTextSize)
	noStroke()
	fill(50)
	text("Summary of used colors:", pageMargin_x, summaryOffset_y);
	for i, color in enumerate(uniqueColors):
		text("%s = %s:  \t%d tiles" % (color['code'], color['name'], color['count']), pageMargin_x, summaryOffset_y + ((i + 1) * (usedColorTextSize + 5)));
	# Draw the color swatches
	drawColorSamples(uniqueColors, pageMargin_x + 200, summaryOffset_y + 4, False)

def tileSizeForScale(scale):
	return floor(round(tileScale * scale))

def analyzeColors(tilesArray):
	colorDicts = []
	# Count all unique colors
	for tiledWall in tilesArray:
		for tileRow in tiledWall['tiles']:
			for tileColorCode in tileRow:
				# Get the color
				color = next((c for c in allColors if c['code'] == tileColorCode), None)
				# Is there a color?
				if color:
					# Is this color allready in the array?
					uniqueColor = next((c for c in colorDicts if c['colorCode'] == tileColorCode), None)
					if uniqueColor:
						# Increment the counter
						uniqueColor['count'] += 1
					else:
						# Create a new color dict
						newColor = {}
						newColor['colorCode'] = color['code']
						newColor['name'] = color['name']
						newColor['r'] = color['r']
						newColor['g'] = color['g']
						newColor['b'] = color['b']
						newColor['count'] = 1
						colorDicts.append(newColor)
	# Sort by occurance
	sortedColors = sorted(colorDicts, key = lambda c: c['count'], reverse = True)
	# Add instruction character
	for i, color in enumerate(sortedColors):
		color['code'] = chr(65 + i)
	return sortedColors

def drawTilerInstruction(tiledWall, uniqueColors, scale):
	# 
	tileSize = tileSizeForScale(scale)
	textMargin_x = tileSize * 0.2
	textMargin_y = tileSize * 0.8
	textSize(14)
	noFill()
	# 
	y = 0
	for tileRow in tiledWall['tiles']:
		x = 0
		for tileColorCode in tileRow:
			# Get the color
			color = next((c for c in uniqueColors if c['colorCode'] == tileColorCode), None)
			noFill()
			stroke(30, 30, 30)
			rect(x + pageMargin_x, y + pageMargin_y, tileSize, tileSize)
			if color:
				noStroke()
				fill(0,0,0)
				text(color['code'], x + pageMargin_x + textMargin_x, y + pageMargin_y + textMargin_y)
			x += tileSize
		y += tileSize
	# Draw the title of the wall
	text(tiledWall['wall_name'], x + (pageMargin_x * 2), (pageMargin_y * 2))
	# Draw the outline of the wall
	wall = next((w for w in walls if w['name'] == tiledWall['wall_name']), None)
	offsetx = 0
	offsety = 0
	if wall.has_key('offset'):
		offsetx = wall['offset']['x'] * -scale
		offsety = wall['offset']['y'] * -scale
	offsetx += pageMargin_x
	offsety += pageMargin_y
	w = wall['w'] * scale
	h = wall['h'] * scale
	noFill()
	stroke(255, 0, 0);
	rect(offsetx, offsety, w, h)
	# Draw the excludes
	if wall.has_key('excludes'):
		for exclude in wall['excludes']:
			noFill()
			stroke(255, 60, 60)
			x = (exclude['x'] * scale) + offsetx
			y = (exclude['y'] * scale) + offsety
			w = exclude['w'] * scale
			h = exclude['h'] * scale
			rect(x, y, w, h)

def drawTiles(scale, tilesArray):
	drawBackground(True)
	# 
	tileSize = tileSizeForScale(scale)
	stroke (voeg['r'], voeg['g'], voeg['b'])
	# draw all tiles
	for tiledWall in tilesArray:
		wall = next((w for w in walls if w['name'] == tiledWall['wall_name']), None)
		# Offset of the tiles on the wall
		offsetx = 0
		offsety = 0
		if wall.has_key('offset'):
			offsetx = wall['offset']['x'] * scale
			offsety = wall['offset']['y'] * scale
		wallx = (wall['x'] * scale) 
		wally = (wall['y'] * scale)
		offsetx += wallx
		offsety += wally
		# 
		y = offsety
		for tileRow in tiledWall['tiles']:
			x = offsetx
			for tileColorCode in tileRow:
				# get the color
				color = next((c for c in allColors if c['code'] == tileColorCode), None)
				if color:
					fill(color['r'], color['g'], color['b'])
					rect(x + pageMargin_x, y + pageMargin_y, tileSize, tileSize)
				x += tileSize
			y += tileSize

def drawRandomTiles(scale):
	global allTiles
	allTiles = []
	tileSize = tileSizeForScale(scale)
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
					# Interpolate Mapped Values for middle of the tile
					mapValues = {}
					midX = x + (tileSize / 2.0)
					minX = wallx
					maxX = minX + w
					midY = y + (tileSize / 2.0)
					minY = wally
					maxY = minY + h
					if wall.has_key('maps'):
						for aMap in wall['maps']:
							xComponent = map(midX, minX, maxX, aMap['x1'], aMap['x2'])
							yComponent = map(midY, minY, maxY, aMap['y1'], aMap['y2'])
							mapValues[aMap['type']] = xComponent + yComponent
					# pick random tile
					randomColorCode = randomColorCodeForMapValues(mapValues['surround'], mapValues['floor'])
					randomColor = colorForColorCode(randomColorCode)
					fill(randomColor)
					
					# Store in tilesArray
					if storeAsArray:
						tilesRow.append(randomColorCode)
					else:
						tileDict = {}
						tileDict['c'] = randomColorCode
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
	
def randomColorCodeForMapValues(surroundValue = 0.0, floorValue = 0.0):
	global allColors, colorsIncludingTransparant
	global horizontalCtrl, verticalCtrl
	# 
	# Surround influence
	# Create weighted color list
	surroundWeightedChoices = []
	for c in allColors:
		weight = horizontalCtrl.valueForKeyAtPosition(c['code'], surroundValue)
		if weight > 0.0:
			surroundWeightedChoices.append((c['code'], weight))
	# Floor influence
	floorWeightedChoices = []
	for c in colorsIncludingTransparant:
		weight = verticalCtrl.valueForKeyAtPosition(c['code'], floorValue)
		if weight > 0.0:
			floorWeightedChoices.append((c['code'], weight))
	# Pick a random color code 
	if surroundWeightedChoices:
		randomCode = weightedRandom(surroundWeightedChoices)
		# Add floor random as an arbitrary overlay (if clear do nothing)
		if floorWeightedChoices:
			floorOverlay = weightedRandom(floorWeightedChoices)
			if floorOverlay != "__":
				randomCode = floorOverlay
		return randomCode
	else:
		print "Using the default color. Shouldn't do that"
		colorCode = defaultColors[int(random(len(defaultColors)))]
		return colorCode

def weightedRandom(choices):
	total = sum(w for c, w in choices)
	r = random(total)
	upto = 0
	for c, w in choices:
		if upto + w >= r:
			return c
		upto += w
	assert False, "Shouldn't get here"
	
def colorForColorCode(colorCode):
	col = next((c for c in allColors if c['code'] == colorCode), None)
	return color(col['r'], col['g'], col['b'])
	



