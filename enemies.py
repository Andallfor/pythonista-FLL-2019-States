from scene import *
import math
import random
import ui
#import pathfinding as pf
import betterPathfinding as pf
import timeit

def get_dist(point1, point2):
	return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

class water(SpriteNode):
	def __init__(self, health, speed, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		self.texture = Texture('images/Water.jpeg')
		self.scale = 0.125
		self.alpha = 1
		self.type = "flowing"
		self.lastPos = self.position
		self.pf = pf.pf(parent = self)
		self.toMove = []
		self.stuck = False
		self.health = health
		self.maxHealth = health
		self.speed = speed
	
	def damage_sides(self, pos):
		row, column = self.parent.parent.pfMain.convert_pos_to_usable(pos)
		corners2 = [
			(row + 1, column),
			(row - 1, column),
			(row, column + 1),
			(row, column - 1)
			]
		for corner in corners2:
			if self.parent == None:
				return
			for toDamage in self.parent.parent.towerParent.children:  #bat kills to quick, doesnt register its dead
				if self.parent == None:
					return
				if self.parent.parent.pfMain.convert_pos_to_usable(toDamage.position) in corners2:
					try:
						if self.parent.parent.pfMain.natMaze[corner[0]][corner[1]] > 0:
							toDamage.health -= self.health/15
							toDamage.update_health()
					except:
						pass
	
	def take_damage(self, damage):
		self.health -= int(damage)
		try:
			if self.health < 0:
					self.parent.parent.money += damage + self.health
			else:
				self.parent.parent.money += max(int(damage),0)
			self.parent.parent.ui.moneyDisplay.text = "$" + str(self.parent.parent.money)
			self.alpha = (self.health/self.maxHealth)
		except:
			pass
		if self.health <= 0:
			#water is dead
			self.run_action(Action.remove())
			
	def move(self):
		try:
			if self.position in self.parent.parent.level.endLocation:
				self.parent.parent.currentHealth -= self.health
				#self.remove_from_parent()
				self.run_action(Action.remove()) #CAUSES PROBLEMS
				return
		except:
			return
		
		if len(self.toMove) != 0:
			row, column = self.parent.parent.pfMain.convert_pos_to_usable(self.toMove[0])
			corners2 = [
				(row + 1, column),
				(row - 1, column),
				(row, column + 1),
				(row, column - 1)
				]
			if self.parent.parent.pfMain.natMaze[row][column] > 0:
				#barrier in the way
				for tower in self.parent.parent.towerParent.children:
					if tower.position == self.toMove[0]:
						tower.health -= self.health/4
						tower.update_health()
				return	
			#	test = ShapeNode(ui.Path.rect(0,0,32,32), parent = self.parent.parent, position = self.position)
			#print((row,column))
			self.lastPos = self.position
			#if there is a specified place to move
			self.position = self.toMove[0]
			self.toMove.pop(0)
			return
			
		
		self.damage_sides(self.position) #error in here
		
		if self.parent == None:
			return
						
		corners = [
		(self.position.x + 32, self.position.y),
		(self.position.x - 32, self.position.y),
		(self.position.x, self.position.y + 32),
		(self.position.x, self.position.y - 32)
		]
		waterPath = self.parent.parent.waterPath
		#self.toMove = self.parent.parent.pfMain.path(self.position, [0,256])
		
		if len(waterPath) == 0:
			pEnds = []
			for end in self.parent.parent.level.endLocation:
				pEnds.append(self.parent.parent.pfMain.path(self.position, end)[::-1])
			self.toMove = min(pEnds)[1]
			return
		
		for pathPos in waterPath: #get closest path tile thats less
			if pathPos in corners:
				#checks if the water path (the ideal location to move) is in one of the moveable areas
				if waterPath.index(pathPos) < waterPath.index(self.position):
					#makes sure that the water is traveling to a lower value tile
					if pathPos in self.parent.parent.staticArea or pathPos in self.parent.parent.towerArea: #ignore generators as towers
						#area is blocked, either by a placed tower, or by un-buildable areas
						testTiles = []
						for tile in self.parent.parent.waterPath:
							if tile == self.position:
								break
							if tile not in self.parent.parent.towerArea:
								testTiles.append(tile)
						closeTiles = {}
						for possibleTiles in testTiles:
							closeTiles.update({get_dist(self.position, possibleTiles): possibleTiles})
						
						path1 = None	
						
						
						try:
							#waterPath is un-obstacted
							close = closeTiles.get(min(closeTiles)) #FIX
							path1 = self.parent.parent.pfMain.path(self.position, close)[0]
						except:
							#waterPath is full
							#default to pathfind to the end tiles
							endTiles = self.parent.parent.level.endLocation[0]
							path1 = self.parent.parent.pfMain.path(self.position, endTiles)[0]
							
							
						self.toMove = path1
							#self.toMove = min(path1,path2)
						break
					else:	
						#area is unblocked, and can move to that position
						self.lastPos = self.position
						self.position = pathPos
						break
