# Rectangle Geometry
# 
# Rect object
# 	containsRect
#	containsPoint
#	insideRectButNotIn

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
	
	def containsPoint(self, x_or_tuple, y = None):
		if y is None:
			# given tuple
			x = x_or_tuple[0]
			y = x_or_tuple[1]
		else:
			# given x and y
			x = x_or_tuple
		if (x > self.x) and (x < self.x + self.w) and (y > self.y) and (y < self.y + self.h):
			return True
		return False	
		
	def insideRectButNotIn(self, allRect, exRect):
		# Make self just a tiny bit smaller, to compansate for edge cases (literally edge-cases)
		tinyM = 0.1
		pointTL = (self.x + tinyM, self.y + tinyM)
		pointTR = (self.x + self.w - tinyM, self.y + tinyM)
		pointBL = (self.x + tinyM, self.y + self.h - tinyM)
		pointBR = (self.x + self.w - tinyM, self.y + self.h - tinyM)
		topLeft = allRect.containsPoint(pointTL) and (not exRect.containsPoint(pointTL))
		topRight = allRect.containsPoint(pointTR) and (not exRect.containsPoint(pointTR))
		bottomLeft = allRect.containsPoint(pointBL) and (not exRect.containsPoint(pointBL))
		bottomRight = allRect.containsPoint(pointBR) and (not exRect.containsPoint(pointBR))
		if topLeft or topRight or bottomLeft or bottomRight:
			return True
		return False
		
	def description(self):
		return "Rect(%f, %f, %f, %f)" % (self.x, self.y, self.w, self.h)

