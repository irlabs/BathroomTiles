# Gradient Sliders

# Custom ControlP5 Compound Classes for percentage sliders
# For Processing in Python 

import copy
add_library('controlP5')

class GradientController(object):
	def __init__(self, colorList, cp5, sliderClass):
		self.colorList = self.colorListFromColors(colorList)
		self.cp5 = cp5
		self.Slider = sliderClass
		self.stopCounter = 0
		self.controllerIdentity = 1
		self.x = 0
		self.y = 0
		self.width = 100
		self.height = 100
		self.calculatedHeight = 0
		self.sliderWidth = 50
		self.sliderHeight = 10
		self.backgroundColor = color(220)
		self.margin = 2
		self.allStops = []
		self.callbackActive = True
		self.testLerpSlider = None
		self.needsDisplay = True
	
	def setPosition(self, x, y):
		self.x = x
		self.y = y
		
	def setSize(self, w, h):
		self.width = w
		self.height = h
		
	def setSliderSize(self, w, h):
		self.sliderWidth = w
		self.sliderHeight = h
	
	def addOuterColorStops(self):
		beginStop = self.createColorstop(self.colorList, self.x, self.y, 0.0, False)
		self.allStops.append(beginStop)
		xAtEnd = (self.x + self.width) - self.sliderWidth
		endStop = self.createColorstop(self.colorList, xAtEnd, self.y, 1.0)
		self.allStops.append(endStop)
	
	def insertColorStop(self, position):
		for i, aStop in enumerate(self.allStops):
			if position < aStop['position']:
				insertX = self.positionOfSubStop(i, position, True)[0]
				newStop = self.createColorstop(self.colorList, insertX, self.y, position, False)
				self.allStops.insert(i, newStop)
				break
		self.recalcSubStopPositions()
	
	def addStopPositionSliders(self):
		# Calculate position
		x = self.x + self.sliderWidth + self.margin
		y = self.y + self.calculatedHeight + self.margin
		w = self.width - (2 * (self.sliderWidth + self.margin))
		# Callback
		def positionSliderCallback(event):
			if self.callbackActive:
				if event.getAction() == 32:
					self.positionChanges(event.getController())
				if event.getAction() == 8 or event.getAction() == 16:
					self.stopPositionDidChange(event.getController())
		# Set the slider
		sliderName = "stop_position_%d_%d" % (self.stopCounter, self.controllerIdentity)
		pSlider = self.Slider(self.cp5, sliderName)
		pSlider.setCaptionLabel("")
		pSlider.setSliderMode(0)
		pSlider.setColorForeground(color(150))
		pSlider.setColorBackground(color(70))
		pSlider.setColorActive(color(220))
		pSlider.setSize(w, self.sliderHeight)
		pSlider.setPosition(x, y)
		# For testing: (was 50)
		pSlider.setValue(40)
		pSlider.addCallback(positionSliderCallback)
		self.testLerpSlider = pSlider
		
	def positionChanges(self, aSlider):
		if self.callbackActive:
			# print "change %f" % aSlider.getValue()
			# Move stop
			self.allStops[1]['position'] = aSlider.getValue() / 100.0
			self.recalcSubStopPositions()
		self.needsDisplay = True
		
	def stopPositionDidChange(self, aSlider):
		print "stopPositionDidChange"
		
	def display(self):
		# Sliders are drawn by cp5
		# draw graph
		if self.needsDisplay:
			self.drawGraph(self.allStops)
			self.needsDisplay = False
	
	def getSliderValues(self):
		stopsData = []
		for cStop in self.allStops:
			thisStop = {'position': cStop['position']}
			sliders = {}
			for i, slider in enumerate(cStop['sliders']):
				sliders[self.colorList[i]['code']] = slider.getValue()
			thisStop['values'] = sliders
			stopsData.append(thisStop) 
		return {'stops': stopsData}
	
	def setSliderValues(self, stopsData):
		if len(stopsData) == len(self.allStops):
			self.callbackActive = False
			for i, stopValues in enumerate(stopsData):
				theStop = self.allStops[i]
				theStop['position'] = stopValues['position']
				if stopValues.has_key('values'):
					if len(theStop['sliders']) != len(stopValues['values'].keys()):
						print "WARNING: Possible problem setting slider values - number of colors not matching"
					for key, value in stopValues['values'].iteritems():
						indexOfSlider = next(index for (index, c) in enumerate(self.colorList) if c['code'] == key)
						slider = theStop['sliders'][indexOfSlider]
						slider.setValue(value)
				else:
					print "ERROR: Setting Slider Values Failed - 'values' key missing"
			self.callbackActive = True
		else:
			print "ERROR: Setting Slider Values Failed - number of stops not matching"
		
	def valueForKeyAtPosition(self, key, inFloat):
		# Find the index of the color with key
		colorIndex = 0
		for i, c in enumerate(self.colorList):
			if key == c['code']:
				colorIndex = i
				break 
		# Create allStopPositions
		stopPositions = []
		values = []
		for i, cStop in enumerate(self.allStops):
			# collect stop positions
			v = cStop['sliders'][colorIndex].getValue()
			# set inbetween values
			# if len(stopPositions) > 0:
			# 	# TODO: fix for right position (refactor testLerpSlider)
			# 	testLerpPosition = self.testLerpSlider.getValue() / 100.0
			# 	prevStopPosition = stopPositions[-1]
			# 	nextStopPosition = cStop['position']
			# 	stopPositions.append(lerp(prevStopPosition, nextStopPosition, testLerpPosition))
			# 	# add inbetween value
			# 	values.append(lerp(values[-1], v, 0.5))
			stopPositions.append(cStop['position'])
			# add value of slider with colorIndex
			values.append(v)
		# Find the two stop positions which are right and left of the given position
		prevStopPosition = 0.0
		nextStopPosition = 0.0
		prevValue = 0.0
		nextValue = 0.0
		relativePosition = 0.0
		for i, p in enumerate(stopPositions):
			if inFloat <= p:
				prevP = stopPositions[i - 1]
				relativePosition = (inFloat - prevP) / (p - prevP)
				prevValue = values[i - 1]
				nextValue = values[i]
				break
		else:
			# inFloat is outside bounds of stopPosition range
			# Return the maximum stop position value
			return values[-1]
		return lerp(prevValue, nextValue, relativePosition)
	
	def recalcSubStopPositions(self):
		if len(self.allStops) > 2:
			for i, subStop in enumerate(self.allStops[1:-1]):
				pos = self.positionOfSubStop(i + 1)
				# Reposition sliders of substop
				for slider in subStop['sliders']:
					sliderPos = slider.getPosition()
					slider.setPosition(pos[0], sliderPos.y)
	
	def positionOfSubStop(self, indexOfStop, preInsertPosition = 0, preInsertionMode = False):
		w = self.sliderWidth
		numberOfStops = len(self.allStops)
		thePosition = self.allStops[indexOfStop]['position']
		if preInsertionMode:
			numberOfStops += 1
			thePosition = preInsertPosition
		availableWidth = self.width - ((numberOfStops * w) + ((numberOfStops - 1) * 2 * self.margin))
		leadingSpace = availableWidth * thePosition
		precedingStopsWidth = indexOfStop * (w + (2 * self.margin))
		x = self.x + leadingSpace + precedingStopsWidth
		return (int(x), int(w))
		
	def colorListFromColors(self, colors):
		newList = copy.copy(colors)
		for c in newList:
			if c['code'] == "__":
				c['color'] = None
			else:
				c['color'] = color(c['r'], c['g'], c['b'])
		return newList
		
	def emptyDataStopSet(self):
		colorDataSet = []
		for c in self.colorList:
			colorD = {}
			colorD['color'] = c['color']
			colorD['name'] = c['name']
			colorD['code'] = c['code']
			colorD['values'] = []
			colorD['hidden'] = True
			colorDataSet.append(colorD)
		return colorDataSet

	def drawGraph(self, stopsArray):
		# Collect the data
		# (Assume that every stop has the same amount and order of colors)
		# (The last stop has the color name)
		colorData = self.emptyDataStopSet()
		stopPositions = []
		for cStop in stopsArray:
			# collect stop positions
			# # set inbetween values
			# if len(stopPositions) > 0:
			# 	# TODO: fix for right position (refactor testLerpSlider)
			# 	testLerpPosition = self.testLerpSlider.getValue() / 100.0
			# 	prevStopPosition = stopPositions[-1]
			# 	nextStopPosition = cStop['position']
			# 	stopPositions.append(lerp(prevStopPosition, nextStopPosition, testLerpPosition))
			stopPositions.append(cStop['position'])	
			# collect values and calculate inbetween values
			for i, slider in enumerate(cStop['sliders']):
				v = slider.getValue()
				# Make inbetween semi-stop
				# if len(colorData[i]['values']) > 0:
				# 	inbetween_v = lerp(colorData[i]['values'][-1], v, 0.5)
				# 	colorData[i]['values'].append(inbetween_v)
				colorData[i]['values'].append(v)
				if v > 0:
					colorData[i]['hidden'] = False
		# Get height and y 
		y = self.y
		h = self.calculatedHeight
		# Draw the sub graphs
		for i in range(len(stopsArray) - 1):
			# calculate position
			fromStop = stopsArray[i]
			toStop = stopsArray[i + 1]
			fromStopPos = self.positionOfSubStop(i)
			toStopPos = self.positionOfSubStop(i + 1)
			x = fromStopPos[0] + fromStopPos[1] + self.margin
			w = (toStopPos[0] - self.margin) - x
			# Normalize stop positions
			normalizedStopPositions = []
			for pos in stopPositions:
				norm = map(pos, fromStop['position'], toStop['position'], 1, w - 2)
				normalizedStopPositions.append(norm)
			self.drawSubGraph(x, y, w, h, colorData, normalizedStopPositions, i, i + 1)
					
	def drawSubGraph(self, x, y, w, h, colorData, stopXs, indexFrom, indexTo):
		# Draw background
		fill(self.backgroundColor)
		noStroke()
		rect(x, y, w, h)
		# Draw lines
		for c in colorData:
			if not c['hidden']:
				if c['color']:
					stroke(c['color'])
				else:
					stroke(255)
				for i, v in enumerate(c['values'][indexFrom:indexTo]):
					index = i + indexFrom
					x1 = x + stopXs[index]
					x2 = x + stopXs[index + 1]
					norm_v1 = (h - 2) * (v / 100)
					y1 = y + ((h - 1) - norm_v1)
					norm_v2 = (h - 2) * (c['values'][index + 1] / 100)
					y2 = y + ((h - 1) - norm_v2)
					line(x1, y1, x2, y2)

	def createColorstop(self, colorsInStop, x, y, position = 0.0, showLabel = True):
		# Create callback
		def colorSliderCallback(event):
			if self.callbackActive:
				if event.getAction() == 32:
					self.valueChanges(event.getController())
				if event.getAction() == 8 or event.getAction() == 16:
					self.sliderReleased(event.getController())
				# else:
				# 	print event.getAction()
		# Create colorStop
		colorStop = {}
		colorStop['position'] = position
		colorSliders = []
		for c in colorsInStop:
			sliderName = "%s_%d_%d" % (c['name'], self.stopCounter, self.controllerIdentity)
			cSlider = self.Slider(self.cp5, sliderName)
			if c['color']:
				tileColor = c['color']
			else:
				tileColor = color(255)
			if showLabel:
				cSlider.setCaptionLabel(c['name'])
			else:
				cSlider.setCaptionLabel("")
			cSlider.setColorForeground(tileColor)
			cSlider.setColorCaptionLabel(tileColor)
			if c['color']:
				cSlider.setColorBackground(self.modColor(tileColor, False))
				cSlider.setColorActive(self.modColor(tileColor, True))
			else:
				cSlider.setColorValueLabel(0)
				cSlider.setColorForeground(color(200, 200, 200))
				cSlider.setColorBackground(color(255, 255, 255))
				cSlider.setColorActive(color(230, 230, 230))
			cSlider.setSize(self.sliderWidth, self.sliderHeight)
			cSlider.setPosition(x, y)
			cSlider.setValue(50)
			cSlider.addCallback(colorSliderCallback)
			colorSliders.append(cSlider)
		
			y += self.sliderHeight + self.margin
		# Set the calculated height (if it hasn't been set)
		if not self.calculatedHeight:
			self.calculatedHeight = y - (self.margin + self.y)
		# Load or recalculate values
		self.recalculateStopValues(colorSliders, None)
		self.stopCounter += 1
		colorStop['sliders'] = colorSliders
		return colorStop
	
	def valueChanges(self, aSlider):
		if self.callbackActive:
			for colorStop in self.allStops:
				if aSlider in colorStop['sliders']:
					self.recalculateStopValues(colorStop['sliders'], aSlider)
		self.needsDisplay = True
					
	def sliderReleased(self, aSlider):
		print "slider released -- update render"
		# For testing
		# v = self.valueForKeyAtPosition('G1', 0.7)
		# print v
					
	def recalculateStopValues(self, colorSliders, selectedSlider):
		self.callbackActive = False
		oldValues = [s.getValue() for s in colorSliders]
		adjustment = 100.0 / sum(oldValues)
		for i, aSlider in enumerate(colorSliders):
			aSlider.setValue(oldValues[i] * adjustment)
		self.callbackActive = True
	

	def modColor(self, inColor, darker = True):
		if darker:
			outColor = lerpColor(inColor, color(0), 0.30)
		else:
			outColor = lerpColor(inColor, color(255), 0.40)
		return outColor
