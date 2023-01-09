# ADAPTED ASTAR CODE
#just use push direction? like at each path, have push
# may not work for stuff with lots of turns
from scene import *
import math

class Node():
	"""A node class for A* Pathfinding"""
	
	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position
		
		self.g = 0
		self.h = 0
		self.f = 0
		
	def __eq__(self, other):
		return self.position == other.position
	
class pathfind(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.static = []
		self.maze = []
		for x in range(0, 929, 32):
			rowList = []
			for y in range(0, 833, 32):
				rowList.append((x,y))
				if (x,y) in self.parent.parent.parent.staticArea or (x,y) in self.parent.parent.parent.towerArea:
					self.static.append((x,y))
			self.maze.append(rowList[::-1])
		self.maze = self.maze[::-1]
		
	def path_to(self, start, end):
		start2, end2 = self.get_points(start,end)
		return self.astar(self.maze,start2,end2)
	
	def get_points(self, start, end):
		rowIndex = 0
		columnIndex = 0
		for row in self.maze:
			for column in row:
				if column == start:
					start2 = (rowIndex, columnIndex)
				if column == end:
					end2 = (rowIndex, columnIndex)
				columnIndex += 1
			rowIndex += 1
			columnIndex = 0
		return start2, end2
		
	def astar(self, maze, start, end):
		"""Returns a list of tuples as a path from the given start to the given end in the given maze"""
		index10 = 0
		# Create start and end node
		start_node = Node(None, start)
		start_node.g = start_node.h = start_node.f = 0
		end_node = Node(None, end)
		end_node.g = end_node.h = end_node.f = 0
		
		# Initialize both open and closed list
		open_list = []
		closed_list = []
		
		# Add the start node
		open_list.append(start_node)
		
		# Loop until you find the end
		while len(open_list) > 0:
			index10 += 1
			if index10 >= 300:# return to best answer
				return None
		
		# Get the current node
			current_node = open_list[0]
			current_index = 0
			for index, item in enumerate(open_list):
				if item.f < current_node.f:
					current_node = item
					current_index = index
					
			# Pop current off open list, add to closed list
			open_list.pop(current_index)
			closed_list.append(current_node)
			
			# Found the goal
			if current_node == end_node:
				path = []
				current = current_node
				while current is not None:
					#path.append(current.position)
					path.append(maze[current.position[0]][current.position[1]])
					current = current.parent
				if self.parent.parent.parent.debug == True:
					for child in path:
						test = SpriteNode('pzl:Green7', parent = self.parent.parent.parent, position = child, alpha = 1)
				return path[::-1] # Return reversed path
				
			# Generate children
			#REDO
			children = []
			for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
			
				# Get node position
				node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
				if self.parent.parent.parent.debug == True: test = SpriteNode('pzl:Blue7', parent = self.parent.parent.parent, position = maze[node_position[0]][node_position[1]], alpha = 0.5)
				# Make sure within range
				if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
					continue
					
				# Make sure walkable terrain
				if maze[node_position[0]][node_position[1]] in self.static:
					continue
					
				# Create new node
				new_node = Node(current_node, node_position)
				
				# Append
				children.append(new_node)
				
				
			# Loop through children
			for child in children:
			
				# Child is on the closed list
				for closed_child in closed_list:
					if child == closed_child:
						continue
						
				# Create the f, g, and h values
				child.g = current_node.g + 1
				child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
				child.f = child.g + child.h
				
				# Child is already in the open list
				for open_node in open_list:
					if child == open_node and child.g > open_node.g:
						continue
						
				# Add the child to the open list
				open_list.append(child)
