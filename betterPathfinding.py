# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used
import numpy
from heapq import *
import timeit
from scene import *


def heuristic(a, b):
	return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
	
def astar(array, start, goal):

	neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
	
	close_set = set()
	came_from = {}
	gscore = {start:0}
	fscore = {start:heuristic(start, goal)}
	oheap = []
	
	heappush(oheap, (fscore[start], start))
	
	while oheap:
	
		current = heappop(oheap)[1]
		
		if current == goal:
			data = []
			totalF = 0
			while current in came_from:
				data.append(current)
				current = came_from[current]
				totalF += fscore.get(current)
			return data, totalF
			
		close_set.add(current)
		for i, j in neighbors:
			neighbor = current[0] + i, current[1] + j
			tentative_g_score = gscore[current] + heuristic(current, neighbor)
			if 0 <= neighbor[0] < array.shape[0]:
				if 0 <= neighbor[1] < array.shape[1]:
					if array[neighbor[0]][neighbor[1]] == -1: #== 1
						continue
				else:
					# array bound y walls
					continue
			else:
				# array bound x walls
				continue
				
			if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
				continue
				
			if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
				came_from[neighbor] = current
				gscore[neighbor] = tentative_g_score
				fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal) + array[neighbor[0]][neighbor[1]] * 1000# add health? of tower if the path goes through a tower
				heappush(oheap, (fscore[neighbor], neighbor))
				
	return None
	
'''Here is an example of using my algo with a numpy array,
   astar(array, start, destination)
   astar function returns a list of points (shortest path)'''

class pf(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.natMaze = []
		
	def gen_static_area(self):
		a = timeit.default_timer()
		#to be called at the start of each level, generates the natural walls
		for y in range(128, 864, 32):
			rowList = []#929
			for x in range(0, 929, 32): #929
				if (x,y) in self.parent.staticArea:
					rowList.append(-1)
				else:
					rowList.append(0)
			self.natMaze.append(rowList)
		self.natMaze = self.natMaze[::-1]
		b = timeit.default_timer()
		return self.natMaze
		
	def convert_pos_to_usable(self, pos):
		return (int(-pos[1]/32 + 26), int(pos[0]/32))
		
	def add_tower(self, position, tower):
		#run only if the amount of towers has changed (optimizing), use to gen the tower areas
		row, column = self.convert_pos_to_usable(position)
		#print(self.decode_single((row, column)))
		self.natMaze[row].pop(column)
		a = 0 if tower.health is None else tower.health
		self.natMaze[row].insert(column, a)
		
	def remove_tower(self, position):
		row, column = self.convert_pos_to_usable(position)
		#print(self.decode_single((row, column)))
		self.natMaze[row].pop(column)
		self.natMaze[row].insert(column, 0)
		
	def path(self, start, end):
		maze = numpy.array(self.natMaze)
		start2 = self.convert_pos_to_usable(start)
		end2 = self.convert_pos_to_usable(end)
		path, totalF = astar(maze, start2, end2)
		returnPath = self.decode_path(path)[::-1]
		#for x in range(0, 31):
		#	for y in range(0, 30):
		#		if (x*32,y*32) in returnPath:
		#			pos = LabelNode("(" + str(x * 32) + ", " + str(y * 32) + ")" , position = (x * 32,y * 32), parent = self.parent, z_position = 20, font = ('Avenir Next Condensed', 7))
		#			box = ui.Path.rect(0,0,32,32)
		#			box.line_width = 1
		#			box2 = ShapeNode(box, parent = pos, fill_color = "clear", stroke_color = '#ffffff')
		#			box2.stroke_color = '#ffffff'
		#			pos.color = '#ffffff'
		#print(returnPath)
		return returnPath, totalF
	
	def decode_single(self, encoded): # should be in row, column format
		return (encoded[1]*32, -32 * encoded[0] + 832)
	
	def decode_path(self, path):
		#return a path that is readable by the enemies.py script
		newPath = []
		for encoded in path:
			newPath.append(self.decode_single(encoded))
		return newPath
		
#(row#, column#)
