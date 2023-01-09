from scene import *

#20 by 23

def get_area(topLeft, bottomRight): # values must be divisable by 32
	returnList = []
	for x in range(topLeft[0], bottomRight[0] + 1, 32):
		for y in range(bottomRight[1], topLeft[1] + 1, 32):
			returnList.append((x,y))
	return returnList

class level1():
	def __init__(self):
		self.bgImg = 'images/stage1.jpeg'
		self.bgScale = 1.361
		self.bgPos = (-10, 845) # -10, 845
		self.staticArea = self.get_level_static()
		self.buildArea = self.get_level_build()
		self.pathArea = self.get_level_path()
		self.waves = self.get_waves()
		self.spawnLocation = [(928,640), (928,320)]
		self.endLocation = [(0,256), (0,224), (0,192)]
		self.bgScale = 1.361
		self.maxWave = 10
		self.money = 175
	
	def get_waves(self):
		waves = {
			1: {"amount": 5, "health": 1, "speed": 8, "space": 2, "end": 50},
			2: {"amount": 5, "health": 1, "speed": 8, "space": 1, "end": 100},
			3: {"amount": 7, "health": 1, "speed": 7, "space": 2, "end": 50},
			4: {"amount": 10, "health": 1, "speed": 7, "space": 1, "end": 150},
			5: {"amount": 12, "health": 1, "speed": 6, "space": 1, "end": 100},
			6: {"amount": 15, "health": 1, "speed": 5, "space": 1, "end": 100},
			7: {"amount": 20, "health": 1, "speed": 5, "space": 2, "end": 250},
			8: {"amount": 10, "health": 3, "speed": 3, "space": 1, "end": 150},
			9: {"amount": 25, "health": 4, "speed": 7, "space": 2, "end": 700},
			10: {"amount": 23, "health": 5, "speed": 4, "space": 1, "end": 500}
			}
		return waves
	
	def get_level_static(self):
		holder = []
		holder.extend(get_area((0,832), (96,288)))
		holder.extend(get_area((128, 832), (928, 800)))
		holder.extend(get_area((608,768), (768,544)))
		holder.extend(get_area((800, 768), (928, 704)))
		holder.extend(get_area((0, 160), (192,128)))
		holder.extend(get_area((224, 672), (480, 128)))
		holder.extend(get_area((512, 416), (768, 128)))
		holder.extend(get_area((800, 256), (928, 128)))
		holder.extend(get_area((896, 576), (928, 384)))
		return holder
	
	def get_level_build(self):
		holder = []
		holder.extend(get_area((0,256), (96,192)))
		holder.extend(get_area((128,768), (192,192)))
		holder.extend(get_area((224,768), (576,704)))
		holder.extend(get_area((512,672), (576,448)))
		holder.extend(get_area((608,512), (768,448)))
		holder.extend(get_area((800,672), (928,608)))
		holder.extend(get_area((800,352), (928,288)))
		holder.extend(get_area((800,576), (864,384)))
		return holder
	
	def get_level_path(self):
		holder = []
		holder.extend(get_area((0,224), (160,224)))
		holder.extend(get_area((160,736), (160,256)))
		holder.extend(get_area((192,736), (544,736)))
		holder.extend(get_area((544,704), (544,480))[::-1])
		holder.extend(get_area((576,480), (832,480)))
		holder.extend(get_area((832,640), (832,512)))
		holder.extend(get_area((864,640), (928,640)))
		holder.extend(get_area((832,448), (832,320))[::-1])
		holder.extend(get_area((864,320), (928,320)))
		return holder

class level2():
	def __init__(self):
		self.bgImg = 'images/Stage2.png'
		self.bgScale = 1
		self.bgPos = (-16, 848)
		self.staticArea = self.get_level_static()
		self.buildArea = self.get_level_build()
		self.pathArea = self.get_level_path()
		self.waves = self.get_waves()
		self.spawnLocation = [(928, 384), (928, 352), (928, 320)]
		self.endLocation = [(0, 768), (0, 736), (0,704), (0,672), (0, 224), (0, 192), (0, 160)]
		self.maxWave = 15
		self.money = 250
	
	def get_level_static(self):
		holder = []
		holder.extend(get_area((0,640), (512,256)))
		holder.extend(get_area((544,512), (544,256)))
		holder.extend(get_area((576,480), (576,256)))
		holder.extend(get_area((0,832), (928,800)))
		holder.extend(get_area((704,768), (928,416)))
		holder.extend(get_area((640,480), (640, 416)))
		holder.extend(get_area((672,512), (672,416)))
		holder.extend(get_area((0,128), (640,128)))
		holder.extend(get_area((672,288), (928,128)))
		return holder
	
	def get_level_build(self):
		holder = []
		holder.extend(get_area((0,768), (672,672)))
		holder.extend(get_area((544,640), (672,544)))
		holder.extend(get_area((576,544), (640, 512)))
		holder.extend(get_area((608,480), (608,416)))
		holder.extend(get_area((608,384), (928,320)))
		holder.extend(get_area((608,288), (640,256)))
		holder.extend(get_area((0,224), (640,160)))	
		return holder
	
	def get_level_path(self):
		holder = []
		return holder
	
	def get_waves(self):
		waves = {
			1: {"amount": 5, "health": 5, "speed": 7, "space": 2, "end": 75},
			2: {"amount": 7, "health": 5, "speed": 7, "space": 2, "end": 75},
			3: {"amount": 3, "health": 10, "speed": 4, "space": 1, "end": 100},
			4: {"amount": 20, "health": 3, "speed": 6, "space": 1, "end": 150},
			5: {"amount": 10, "health": 10, "speed": 6, "space": 1, "end": 75},
			6: {"amount": 11, "health": 11, "speed": 5, "space": 1, "end": 80},
			7: {"amount": 12, "health": 12, "speed": 5, "space": 1, "end": 85},
			8: {"amount": 13, "health": 13, "speed": 4, "space": 2, "end": 90},
			9: {"amount": 14, "health": 14, "speed": 4, "space": 1, "end": 150},
			10: {"amount": 15, "health": 15, "speed": 3, "space": 1, "end": 200},
			11: {"amount": 10, "health": 10, "speed": 2, "space": 3, "end": 250},
			12: {"amount": 10, "health": 25, "speed": 8, "space": 1, "end": 500},
			13: {"amount": 20, "health": 15, "speed": 6, "space": 1, "end": 250},
			14: {"amount": 20, "health": 7, "speed": 2, "space": 1, "end": 1000},
			15: {"amount": 30, "health": 20, "speed": 5, "space": 1, "end": 1500}
			}
		return waves

class level3():
	def __init__(self):
		self.bgImg = 'images/Stage3.png'
		self.bgScale = 1
		self.bgPos = (-16, 848)
		self.staticArea = self.get_level_static()
		self.buildArea = self.get_level_build()
		self.pathArea = self.get_level_path()
		self.waves = self.get_waves()
		self.spawnLocation = [(928, 640), (928, 608), (928, 512), (928, 480), (928, 448), (928, 352), (928, 320)]
		self.endLocation = [(0, 768), (0, 736), (0, 512), (0,480), (0, 448), (0, 224), (0, 192)]
		self.maxWave = 20
		self.money = 350
	
	def get_level_static(self):
		holder = []
		holder.extend(get_area((0,832), (928, 800)))
		holder.extend(get_area((416,768), (928,736)))
		holder.extend(get_area((704,704), (928, 672)))
		holder.extend(get_area((704,576), (928,544)))
		holder.extend(get_area((704,416), (928,384)))
		holder.extend(get_area((704,288), (928,256)))
		holder.extend(get_area((416,224), (928,192)))
		holder.extend(get_area((0,160), (928,128)))
		holder.extend(get_area((0,416), (320,256)))
		holder.extend(get_area((0,704), (320,544)))
		holder.extend(get_area((416,608), (608,352)))
		return holder
		
	def get_level_build(self):
		holder = []
		holder.extend(get_area((0,768), (320,736)))
		holder.extend(get_area((0,512), (320,448)))
		holder.extend(get_area((0,224), (320,192)))
		holder.extend(get_area((352,768), (384,192)))
		holder.extend(get_area((416,704), (608,640)))
		holder.extend(get_area((416,320), (608,256)))
		holder.extend(get_area((640,704), (672,256)))
		holder.extend(get_area((704,640), (928,608)))
		holder.extend(get_area((704,512), (928,448)))
		holder.extend(get_area((704,352), (928,320)))
		return holder
	
	def get_waves(self):
		waves = {
			1: {"amount": 20, "health": 1, "speed": 6, "space": 1, "end": 150},
			2: {"amount": 25, "health": 2, "speed": 6, "space": 1, "end": 150},
			3: {"amount": 26, "health": 2, "speed": 6, "space": 1, "end": 150},
			4: {"amount": 27, "health": 2, "speed": 6, "space": 1, "end": 200},
			5: {"amount": 20, "health": 5, "speed": 3, "space": 0, "end": 250},
			6: {"amount": 20, "health": 2, "speed": 5, "space": 1, "end": 250},
			7: {"amount": 22, "health": 2, "speed": 5, "space": 1, "end": 250},
			8: {"amount": 24, "health": 2, "speed": 5, "space": 1, "end": 250},
			9: {"amount": 26, "health": 2, "speed": 5, "space": 1, "end": 250},
			10: {"amount": 30, "health": 10, "speed": 7, "space": 1, "end": 300},
			11: {"amount": 20, "health": 4, "speed": 6, "space": 1, "end": 300},
			12: {"amount": 24, "health": 4, "speed": 5, "space": 1, "end": 300},
			13: {"amount": 28, "health": 4, "speed": 4, "space": 1, "end": 300},
			14: {"amount": 32, "health": 4, "speed": 4, "space": 1, "end": 350},
			15: {"amount": 50, "health": 6, "speed": 4, "space": 2, "end": 400},
			16: {"amount": 40, "health": 5, "speed": 3, "space": 1, "end": 400},
			17: {"amount": 45, "health": 5, "speed": 3, "space": 1, "end": 400},
			18: {"amount": 45, "health": 6, "speed": 3, "space": 1, "end": 400},
			19: {"amount": 50, "health": 7, "speed": 2, "space": 1, "end": 500},
			20:	 {"amount": 10, "health": 200, "speed": 4, "space": 0, "end": 1000}
			}
		return waves
	
	def get_level_path(self):
		return []
	
	
class level4():
	def __init__(self):
		self.bgImg = 'images/Stage4.png'
		self.bgScale = 1
		self.bgPos = (-16, 848)
		self.staticArea = self.get_level_static()
		self.buildArea = self.get_level_build()
		self.pathArea = self.get_level_path()
		self.waves = self.get_waves()
		self.spawnLocation = [(928, 800), (928, 768), (928, 736), (928, 512), (928, 448), (928, 448), (928, 224), (928, 192), (928, 160)]
		self.endLocation = [(0, 800), (0, 768), (0, 736), (0, 512), (0, 448), (0, 448), (0, 224), (0, 192), (0, 160)]
		self.maxWave = 25
		self.money = 500
	
	def get_level_build(self):
		h = []
		h.extend(get_area((0,800), (928,736)))
		h.extend(get_area((0,512), (928,448)))
		h.extend(get_area((0,224), (928,160)))
		h.extend(get_area((288,704), (352,544)))
		h.extend(get_area((288,416), (352,256)))
		h.extend(get_area((576,704), (640,544)))
		h.extend(get_area((576,416), (640,256)))
		return h
	
	def get_level_static(self):
		h = []
		h.extend(get_area((0,832), (928,832)))
		h.extend(get_area((0,128), (928,128)))
		h.extend(get_area((0,416), (256,256)))
		h.extend(get_area((384,416), (544,256)))
		h.extend(get_area((672,416), (928,256)))
		h.extend(get_area((0,704), (224,544)))
		h.extend(get_area((384,704), (544,544)))
		h.extend(get_area((672,704), (928,544)))
		return h

	def get_waves(self):
		waves = {
			1: {"amount": 20, "health": 1, "speed": 6, "space": 1, "end": 150},
			2: {"amount": 25, "health": 2, "speed": 6, "space": 1, "end": 150},
			3: {"amount": 26, "health": 2, "speed": 6, "space": 1, "end": 150},
			4: {"amount": 27, "health": 2, "speed": 6, "space": 1, "end": 200},
			5: {"amount": 20, "health": 5, "speed": 3, "space": 0, "end": 250},
			6: {"amount": 20, "health": 2, "speed": 5, "space": 1, "end": 250},
			7: {"amount": 22, "health": 2, "speed": 5, "space": 1, "end": 250},
			8: {"amount": 24, "health": 2, "speed": 5, "space": 1, "end": 250},
			9: {"amount": 26, "health": 2, "speed": 5, "space": 1, "end": 250},
			10: {"amount": 30, "health": 10, "speed": 7, "space": 1, "end": 300},
			11: {"amount": 20, "health": 4, "speed": 6, "space": 1, "end": 300},
			12: {"amount": 24, "health": 4, "speed": 5, "space": 1, "end": 300},
			13: {"amount": 28, "health": 4, "speed": 4, "space": 1, "end": 300},
			14: {"amount": 32, "health": 4, "speed": 4, "space": 1, "end": 350},
			15: {"amount": 50, "health": 6, "speed": 4, "space": 2, "end": 400},
			16: {"amount": 40, "health": 5, "speed": 3, "space": 1, "end": 400},
			17: {"amount": 45, "health": 5, "speed": 3, "space": 1, "end": 400},
			18: {"amount": 45, "health": 6, "speed": 3, "space": 1, "end": 400},
			19: {"amount": 50, "health": 7, "speed": 2, "space": 1, "end": 500},
			20:	{"amount": 10, "health": 200, "speed": 4, "space": 0, "end": 1000},
			21: {"amount": 50, "health": 10, "speed": 2, "space": 1, "end": 600},
			22: {"amount": 55, "health": 10, "speed": 1, "space": 1, "end": 600},
			23: {"amount": 55, "health": 12, "speed": 1, "space": 1, "end": 600},
			24: {"amount": 60, "health": 12, "speed": 1, "space": 1, "end": 1000},
			25: {"amount": 20, "health": 1000, "speed": 3, "space": 1, "end": 1500}
			}
		return waves
	
	def get_level_path(self):
		return []

class level5():	
	def __init__(self):
		self.bgImg = 'images/Stage5.png'
		self.bgScale = 1
		self.bgPos = (-16, 848)
		self.staticArea = self.get_level_static()
		self.buildArea = self.get_level_build()
		self.pathArea = self.get_level_path()
		self.waves = self.get_waves()
		self.spawnLocation = [(928, 544), (928, 512), (928, 480), (928, 448), (928, 416)]		
		self.endLocation = [(0, 544), (0, 512), (0, 480), (0, 448), (0, 416)]
		self.maxWave = 30
		self.money = 1000
	
	def get_level_static(self):
		h = []
		h.extend(get_area((0,832), (928,576)))
		h.append((576,544))
		h.append((576,416))
		h.extend(get_area((0,384), (928,128)))
		return h
	
	def get_level_build(self):
		h = []
		h.extend(get_area((0,544), (544,416)))
		h.extend(get_area((576,512), (576,448)))
		h.extend(get_area((608,544), (928,416)))
		return h
	
	def get_level_path(self):
		return []
	
	def get_waves(self):
		waves = {
			1: {"amount": 20, "health": 1, "speed": 6, "space": 1, "end": 150},
			2: {"amount": 25, "health": 5, "speed": 6, "space": 1, "end": 150},
			3: {"amount": 26, "health": 10, "speed": 6, "space": 1, "end": 150},
			4: {"amount": 27, "health": 15, "speed": 6, "space": 1, "end": 200},
			5: {"amount": 20, "health": 25, "speed": 3, "space": 0, "end": 250},
			6: {"amount": 20, "health": 20, "speed": 5, "space": 1, "end": 250},
			7: {"amount": 22, "health": 20, "speed": 5, "space": 1, "end": 250},
			8: {"amount": 24, "health": 20, "speed": 5, "space": 1, "end": 250},
			9: {"amount": 26, "health": 22, "speed": 5, "space": 1, "end": 250},
			10: {"amount": 30, "health": 410, "speed": 7, "space": 1, "end": 300},
			11: {"amount": 20, "health": 44, "speed": 6, "space": 1, "end": 300},
			12: {"amount": 24, "health": 44, "speed": 5, "space": 1, "end": 300},
			13: {"amount": 28, "health": 44, "speed": 4, "space": 1, "end": 300},
			14: {"amount": 32, "health": 44, "speed": 4, "space": 1, "end": 350},
			15: {"amount": 50, "health": 46, "speed": 4, "space": 2, "end": 400},
			16: {"amount": 40, "health": 45, "speed": 3, "space": 1, "end": 400},
			17: {"amount": 45, "health": 45, "speed": 3, "space": 1, "end": 400},
			18: {"amount": 45, "health": 46, "speed": 3, "space": 1, "end": 400},
			19: {"amount": 50, "health": 47, "speed": 2, "space": 1, "end": 500},
			20:	{"amount": 10, "health": 4200, "speed": 4, "space": 0, "end": 1000},
			21: {"amount": 50, "health": 510, "speed": 2, "space": 1, "end": 600},
			22: {"amount": 55, "health": 510, "speed": 1, "space": 1, "end": 600},
			23: {"amount": 55, "health": 512, "speed": 1, "space": 1, "end": 600},
			24: {"amount": 60, "health": 512, "speed": 1, "space": 1, "end": 1000},
			25: {"amount": 20, "health": 51000, "speed": 3, "space": 1, "end": 1500},
			26: {"amount": 75, "health": 515, "speed": 1, "space": 1, "end": 1000},
			27: {"amount": 80, "health": 515, "speed": 1, "space": 1, "end": 1100},
			28: {"amount": 80, "health": 520, "speed": 1, "space": 1, "end": 1200},
			29: {"amount": 85, "health": 525, "speed": 1, "space": 1, "end": 2000},
			30: {"amount": 50, "health": 57500, "speed": 3, "space": 1, "end": 5000}
			}
		return waves
