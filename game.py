from scene import *
import math
import random
import timeit
import time
import ui
from threading import Timer
from objc_util import ObjCInstance
#bug with threading, perhaps stop updating?

from gameUI import UI
import tile as tiles
import levelData
import enemies
import betterPathfinding as bpf
import intro
import textEngine

class main(Scene):	
	def setup(self):	
		v = ObjCInstance(self.view)
		for x in v.subviews():
			if str(x.description()).find('UIButton') >= 0:
				x.setHidden(True)	
		self.transition = ShapeNode(ui.Path.rounded_rect(0,0,1500,900, 16), parent = self, position = (self.size.w*2, self.size.h/2), color = '#000000', z_position = 105)
		self.levelDic = {1: levelData.level1(), 2: levelData.level2(), 3: levelData.level3(), 4: levelData.level4(), 5: levelData.level5()}
		self.currentLevel = 0
		self.doUpdate = False
		self.uiState = "menu"
		#states are
		#		menu
		#		playing
		#		dead
		#		pause
		#		help
		#		intro
	#	self.startGame(2)
		self.text = intro.tut(parent = self, z_position = 99)
		self.menu = intro.menu(parent = self, z_position = 100, alpha = 0)
		self.show_menu()
		self.deathScene = intro.death(parent = self, z_position = 99, alpha = 0)
		self.pauseMenu = intro.pause(parent = self, z_position = 98)
		self.helpMenu = intro.help(parent = self, z_position = 98, alpha = 1)
		
		self.doNotDelete = [self.menu, self.deathScene, self.transition, self.pauseMenu, self.text, self.helpMenu]
	
	def textUpdate(self):		
		self.text.t.update()
		if self.text.t.textReceiver[0] == True:
			eval(str(self.text.t.textReceiver[1]))
			self.text.t.textReceiver = (False, "")
	
	def show_menu(self):
		self.uiState = "menu"
		self.menu.alpha = 1
		self.doUpdate = False
		self.menu.setup()
	
	def start(self):
		self.startGame(self.currentLevel + 1)
	
	def startGame(self, level):
		if level == 1:
			self.text.t.ALLTEXTINFO = []
			self.text.intro()
			self.text.alpha = 1
		else:
			self.text.alpha = 0
		self.uiState = "playing"
		for child in self.children: # is deleting wrong things
			if child not in self.doNotDelete and child != self.transition and child != self.doNotDelete:
				child.run_action(Action.remove())
		self.doUpdate = True
		l = self.levelDic.get(level)
		self.background = SpriteNode(l.bgImg, parent = self, scale = l.bgScale, position = l.bgPos, z_position = 0) # 1.36
		self.background.anchor_point = (0, 1)
		self.background.texture.filter_mode = FILTERING_NEAREST
		self.set_parents()
		self.set_values(l)
		self.ui = UI(parent = self)
		self.pointer = pointer('pzl:Gray3', parent = self, scale = 1, z_position = 19)
		self.towerParent = Node(parent = self)

		self.userState = "passive"
		self.debug = False
		self.currentTowerUI = None
		self.tick = 0
		self.waterSpawnList = []
		# states are:
		#		passive
		# 	placing
		# 	upgrading
		#		settings
		# 	help
		
		self.get_building_areas(self.levelDic.get(level))
		self.pfMain = bpf.pf(parent = self, z_position = 10)
		self.pfMain.gen_static_area()
		#self.water = enemies.water(parent = self.waterParent, position = (928,640))
		#self.debug_mode()
	
	def set_parents(self):
		self.waterParent = Node(parent = self, z_position = 45)
	
	def set_values(self, l):
		self.maxHealth = 100
		self.currentHealth = 100
		self.healthPercentage = round(self.currentHealth * 100/self.maxHealth)
		
		self.money = l.money
		self.currentWave = 0
		self.maxWave = l.maxWave
		self.power = 100
		self.totalPower = 0
		self.batList = []
		
	def get_building_areas(self, level):
		self.buildArea = []
		self.staticArea = []
		self.towerArea = []
		self.waterPath = []
		self.idealWaterPath = []
		self.level = level
		self.staticArea = self.level.staticArea
		self.buildArea = self.level.buildArea
		self.waterPath = self.level.pathArea
		
	def touch_began(self, touch):
		self.text.t.touch_b(touch)
		if self.doUpdate == False:
			if self.uiState == "menu":
				self.menu.touch_b(touch)
			if self.uiState == "dead":
				self.deathScene.touch_b(touch)
			if self.uiState == "pause":
				self.pauseMenu.touch_b(touch)
			if self.uiState == "help":
				self.helpMenu.touch_b(touch)
			return
		self.pointer.scale = 1
		#self.pointer.alpha = 0.8
		self.pointer.touch_update(touch)
		self.pointer.touch_start(touch)
		
	def touch_moved(self, touch):
		self.text.t.touch_m(touch)
		if self.doUpdate == False:
			return
		self.pointer.touch_update(touch)
	
	def touch_ended(self, touch):
		self.text.t.touch_e(touch)
		if self.doUpdate == False:
			if self.uiState == "menu":
				self.menu.touch_e(touch)
			if self.uiState == "dead":
				self.deathScene.touch_e(touch)
			if self.uiState == "pause":
				if self.pauseMenu.menu_bg.scale == 1:
					self.pauseMenu.touch_e(touch)
				elif self.pauseMenu.menu_bg.scale == 0:
					self.pauseMenu.show()
			if self.uiState == "help":
				self.helpMenu.touch_e(touch)
			return
		self.pointer.alpha = 0
		if self.debug == True: self.pointer.texture = Texture('pzl:Gray3')
		if self.userState == "placing":
			if touch.location in self.background.frame:
				self.pointer.place_tower(touch)
			self.userState = "passive"
	
	def update(self):
		if self.doUpdate == True:
			self.gameUpdate()
		#print(self.uiState)
		self.textUpdate()
	
	def towerUpdateNest(self):
		if self.ui.startWaveButton.alpha == 0:
			self.money += self.level.waves.get(self.currentWave).get("end")
			self.ui.moneyDisplay.text = "$" + str(self.money)
			for tower in self.towerParent.children:
				if tower.type == "siren" and tower.playerHRegen != 0:
					self.currentHealth += tower.playerHRegen
					self.ui.update_health()
				if tower.type == "hole":
					if tower.currentWaterAmount != None and tower.wCap != None:
						tower.currentWaterAmount = max(tower.currentWaterAmount - tower.wCap/4, 0)
	
	def towerUpdate(self):
		if len(self.waterSpawnList) == 0 and len(self.waterParent.children) == 0: #self.waterParent.children
			self.towerUpdateNest()
			if self.currentWave + 1 > self.maxWave:
				self.ui.startWaveTextTop.text = "NEXT"
				self.ui.startWaveTextBottom.text = "MAP"
				self.ui.waveCurrent.text = str(self.maxWave)
			self.ui.startWaveButton.alpha = 1
		else:
			if self.ui.startWaveButton.alpha == 1:
				#will only run once
				self.towerUpdateNest()
				self.towerUpdateNest()
				self.towerUpdateNest()
				self.towerUpdateNest()
				self.towerUpdateNest()
				self.towerUpdateNest()
			self.ui.startWaveButton.alpha = 0
							
	def gameUpdate(self):
		self.doUpdate = True
		self.power = min(self.power, self.totalPower)
		self.power = max(0, self.power)
		self.money = int(self.money)
		if self.currentHealth <= 0:
			self.deathScene.reset()
			self.deathScene.begin()
			self.uiState = "dead"
			self.doUpdate = False
		self.towerUpdate()		
		self.ui.update_health()
		self.spawn_water()
		for water in self.waterParent.children:
			if self.tick % water.speed == 0:
				water.move()
		
		if len(self.waterParent.children) != 0: #slight optimization, checking to make sure that only to attack when water on screen
			for tower in self.towerParent.children:
				tower.check_can_attack()
				tower.reload()
				tower.update()
				if tower.type != "hole" and tower.type != "generator":
					tower.update_health()

			
		if self.userState == "upgrading":
			self.update_upgrade_UI()
		self.tick += 1
		if self.tick > 60:
			self.tick = 0
		#print(self.userState)
		
	def update_upgrade_UI(self):
		if self.ui.RIGHTUIUPGRADE.alpha == 1:
			#upgrade ui is showing
			if self.currentTowerUI.health == 0:
				#tower is dead
				self.currentTowerUI.run_action(Action.remove())
				self.ui.RIGHTUIDEFUALT.alpha = 1
				self.ui.RIGHTUIUPGRADE.alpha = 0
				self.currentTowerUI.attackImg.alpha = 0.5
				self.currentTowerUI = None
				self.userState = "passive"
				return
				
			if self.ui.ctHealthParent.alpha == 1:
				if self.currentTowerUI.maxHealth == None:
					#tower is invincible, mainly for holes
					self.ui.ctHealthFG.path = ui.Path.rounded_rect(0,0,120,12,3)
				else:
					self.ui.ctHealthFG.path = ui.Path.rounded_rect(0,0,120 * (self.currentTowerUI.health)/(self.currentTowerUI.maxHealth),12,3)
			
			if self.ui.ctReloadParent.alpha == 1:
				self.ui.ctReloadFG.path = ui.Path.rounded_rect(0,0,120 * (self.currentTowerUI.cReload)/(self.currentTowerUI.reloadTime),12,3)
			
			if self.ui.ctWaterParent.alpha == 1:
				self.ui.ctWaterFG.path = ui.Path.rounded_rect(0,0,120 * (self.currentTowerUI.currentWaterAmount)/(self.currentTowerUI.wCap),12,3)
				
			if self.ui.ctBatteryParent.alpha == 1:
				if self.totalPower == 0:
					self.ui.ctBatteryFG.path = ui.Path.rounded_rect(0,0,0,12,3)
				else:
					self.ui.ctBatteryFG.path = ui.Path.rounded_rect(0,0,120 * (self.power)/(self.totalPower),12,3)
			
			if self.ui.ctPowerParent.alpha == 1:
				self.ui.ctPowerFG.path = ui.Path.rounded_rect(0,0,120 * (self.currentTowerUI.eGain/3),12,3)
			
	def debug_mode(self):
		self.money = 100000
		self.debug = True
		for x in range(0, 31):
			for y in range(0, 30):
				pos = LabelNode("(" + str(x * 32) + ", " + str(y * 32) + ")" , position = (x * 32,y * 32), parent = self, z_position = 1, font = ('Avenir Next Condensed', 7))
				box = ui.Path.rect(0,0,32,32)
				box.line_width = 1
				box2 = ShapeNode(box, parent = pos, fill_color = "clear", stroke_color = '#ffffff')
				if pos.position in self.staticArea:
					box2.stroke_color = '#ff0000'
					pos.color = '#ff0000'
				elif pos.position in self.buildArea:
					box2.stroke_color = '#00ff16'
					pos.color = '#00ff16'
				if pos.position in self.waterPath:
					box2.stroke_color = '#00deff'
					pos.color = '#00deff'
					pos.text = str(self.waterPath.index(pos.position))
				if pos.position in self.idealWaterPath:
					box2.stroke_color = '#ffffff'
					pos.color = '#ffffff'
	
	def display_upgrade_UI(self, tower):
		#print(self.userState)
		self.currentTowerUI = tower
		self.ui.RIGHTUIDEFUALT.alpha = 0
		self.ui.RIGHTUIUPGRADE.alpha = 1
		
		#set basic ui
		self.currentTowerUI.attackImg.alpha = 0.5
		self.ui.currentTowerIMGTitle.text = tower.info.get(tower.level).get("Name")
		self.ui.currentTowerIMGToolTip.text = tower.info.get(tower.level).get("Tooltip")
		self.ui.currentTowerIMG.texture = tower.texture
		self.ui.currentTowerIMG.scale = 80/max(tower.size)
		self.ui.sellDisplay.text = "SELL: $" + str(int(tower.totalMoneySpent/1.5))
		
		#set up display stats
		
		if tower.reloadTime == None:
			self.ui.ctReloadParent.alpha = 0
		else:
			self.ui.ctReloadParent.alpha = 1
		if tower.eCap == None and tower.eNeeded == None:
			self.ui.ctBatteryParent.alpha = 0
		else:
			self.ui.ctBatteryParent.alpha = 1
		if tower.eGain == None:
			self.ui.ctPowerParent.alpha = 0
		else:
			self.ui.ctPowerParent.alpha = 1
		if tower.wCap == None:
			self.ui.ctWaterParent.alpha = 0
		else:
			self.ui.ctWaterParent.alpha = 1
		
		#set up ugrade paths
		
		try:
			self.ui.uP2Parent.alpha = 1
			#test to see if the right path is avaliable (bottom)
			u = (tower.level[0], tower.level[1] + 1)
			self.ui.uP2Title.text = str(tower.info.get(u).get("Name"))
			self.ui.uP2.texture = Texture((tower.upgradeImages.get(u)))
			self.ui.uP2.scale = 96/max(self.ui.uP2.size)
			self.ui.uP2Cost.text = '$' + str(tower.upgradeCost.get(u))
		except:
			self.ui.uP2Parent.alpha = 0
		try:
			self.ui.uP1Parent.alpha = 1
			#test to see if the left path is avaliable (top)
			u = (tower.level[0] + 1, tower.level[1])
			self.ui.uP1Title.text = str(tower.info.get(u).get("Name"))
			self.ui.uP1.texture = Texture((tower.upgradeImages.get(u)))
			self.ui.uP1.scale = 96/max(self.ui.uP1.size)
			self.ui.uP1Cost.text = '$' + str(tower.upgradeCost.get(u))
		except:
			self.ui.uP1Parent.alpha = 0
		self.update_upgrade_UI()
	
	def spawn_water(self):
		if len(self.waterSpawnList) == 0:
			return
		else:
			#print(len(self.waterSpawnList))
			eval(self.waterSpawnList[0])
			self.waterSpawnList.pop(0)
	
	def next_wave(self):
		info = self.level.waves.get(self.currentWave)
		for index in range(info.get("amount") * info.get("speed")): #create a list like [1, 0, 0, 0, 1, 0, 0, 0, 1] where one is when water is spawned. 
			if index % info.get("speed") == 0:
				self.waterSpawnList.append('enemies.water(parent = self.waterParent, position = self.level.spawnLocation[random.randint(0, len(self.level.spawnLocation) - 1)], health = self.level.waves.get(self.currentWave).get("health"), speed = self.level.waves.get(self.currentWave).get("speed"))')
			else:
				self.waterSpawnList.append("False")
		#print(len(self.waterSpawnList))
		
		
class pointer(SpriteNode):
	def __init__(self, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		self.texture.filtering_mode = FILTERING_NEAREST
		self.touchPos = (0,0)
		self.anchor_point = (0.5, 0.5)
		self.placeTower = None
		self.alpha = 0
		self.canPlace = False
	
	def place_tower(self, touch): #placing towers
		if self.canPlace == False:
			return
		if self.check_UI(touch):
			return 
		
		if self.placeTower == "hole":
			tower = tiles.hole(parent = self.parent.towerParent, position = self.touchPos)
		elif self.placeTower == "wall":
			tower = tiles.wall(parent = self.parent.towerParent, position = self.touchPos)
		elif self.placeTower == "siren":
			tower = tiles.siren(parent = self.parent.towerParent, position = self.touchPos)
		elif self.placeTower == "tank":
			tower = tiles.tank(parent = self.parent.towerParent, position = self.touchPos)
		elif self.placeTower == "battery":
			tower = tiles.battery(parent = self.parent.towerParent, position = self.touchPos)
		elif self.placeTower =="generator":
			tower = tiles.generator(parent = self.parent.towerParent, position = self.touchPos)
			
		if tower.upgradeCost.get((0,0)) <= self.parent.money:
			self.parent.pfMain.add_tower(self.touchPos, tower)
			self.parent.money -= tower.upgradeCost.get((0,0))
			self.parent.ui.moneyDisplay.text = "$" + str(self.parent.money)
			tower.totalMoneySpent += tower.upgradeCost.get((0,0))
			#self.parent.path = self.parent.pfMain.path((800,672), (192,256))
		else:
			tower.remove_from_parent()
			tower.run_action(Action.remove())
			return 
		
		if self.placeTower != "generator" and self.placeTower != "hole": #IMPORTANT
			self.parent.towerArea.append(self.touchPos)
	
	def check_ui_buttons(self, touch):
		if touch.location in self.parent.ui.settings.frame.inset(-16,-16):
			self.parent.uiState = "pause"
			self.parent.doUpdate = False
		if touch.location in self.parent.ui.help.frame.inset(-16, -16):
			self.parent.uiState = "help"
			self.parent.doUpdate = False
			self.parent.helpMenu.show()
	
	def touch_start(self, touch): #beginning of touch
		self.check_ui_buttons(touch)
		#figure out if the player is trying to place a tower, or tap an already existing tower
		if self.parent.userState != "upgrading":
			if self.check_UI(touch) == True:
				#the player is tapping the UI, probably trying to place a tower
				self.check_place_start(touch)
			else:
				#the player is tapping on the playing area 
				self.check_upgrade_start(touch)
		else:
			# user is in the UI menu of a tower
			self.check_tower_UI(touch)
		if touch.location in self.parent.ui.startWaveButton.frame and self.parent.ui.startWaveButton.alpha == 1:
			self.parent.ui.waveCurrent.text = str(int(self.parent.ui.waveCurrent.text) + 1)
			self.parent.currentWave += 1
			if self.parent.currentWave > self.parent.maxWave:
				#raise AttributeError("gj u win")
				if self.parent.currentLevel + 1 == 5:		
					self.parent.transition.run_action(Action.sequence(Action.move_to(self.parent.size.w/2, self.parent.size.h/2, 1.5, TIMING_SINODIAL), Action.wait(0.15), Action.call(self.parent.show_menu), Action.wait(0.15), Action.move_to(-self.parent.size.w, self.parent.size.h/2, 1), Action.move_to(self.parent.size.w*2, self.parent.size.h/2,0)))
					self.parent.currentLevel = 0
				else:	
					self.parent.transition.run_action(Action.sequence(Action.move_to(self.parent.size.w/2, self.parent.size.h/2, 1.5, TIMING_SINODIAL), Action.wait(0.25), Action.call(self.parent.start), Action.wait(0.25), Action.move_to(-self.parent.size.w, self.parent.size.h/2, 1.5), Action.move_to(self.parent.size.w*2, self.parent.size.h/2, 0)))
					self.parent.doUpdate = False
					self.parent.currentLevel += 1
			else:
				self.parent.next_wave()
			#self.parent.level.run_wave(int(self.parent.ui.waveCurrent.text))
			#water = enemies.water(parent = self.parent.waterParent, position = (928,640))
	
	def check_tower_UI(self, touch):
		if touch.location in self.parent.ui.rightBack.frame:
			#user is probably trying to upgrade
			if touch.location in self.parent.ui.uP1BG.frame and self.parent.ui.uP1Parent.alpha == 1:
				self.try_upgrade_tower((1,0), self.parent.currentTowerUI)
			elif touch.location in self.parent.ui.uP2BG.frame and self.parent.ui.uP2Parent.alpha == 1:
				self.try_upgrade_tower((0,1), self.parent.currentTowerUI)
			if touch.location in self.parent.ui.sellButton.frame:
				self.parent.pfMain.remove_tower(self.parent.currentTowerUI.position)
				self.parent.money += int(self.parent.currentTowerUI.totalMoneySpent/1.5)
				if self.parent.currentTowerUI.type == "battery":
					self.parent.totalPower -= self.parent.currentTowerUI.eCap
					self.parent.batList.remove(self.parent.currentTowerUI)
				self.parent.currentTowerUI.remove_from_parent()
				#self.parent.currentTowerUI.run_action(Action.remove())
				self.parent.userState = "passive"
				self.parent.ui.moneyDisplay.text = "$" + str(self.parent.money)
				self.parent.ui.RIGHTUIUPGRADE.alpha = 0
				self.parent.ui.RIGHTUIDEFUALT.alpha = 1
				self.parent.currentTowerUI.attackImg.alpha = 0
				try:
					self.parent.towerArea.remove(self.parent.currentTowerUI.position)
				except:
					pass
		else:
			#user is tapping elsewhere
			if touch.location not in self.parent.ui.bottomBack.frame:
				self.parent.ui.RIGHTUIUPGRADE.alpha = 0
				self.parent.currentTowerUI.attackImg.alpha = 0
				self.parent.ui.RIGHTUIDEFUALT.alpha = 1
				self.parent.userState = 'passive'
			self.check_upgrade_start(touch)
			
	def try_upgrade_tower(self, upgradePath, tower):
		newLevel = (tower.level[0] + upgradePath[0], tower.level[1] + upgradePath[1])
		if tower.upgradeCost.get((newLevel)) <= self.parent.money:
			self.parent.money -= tower.upgradeCost.get((newLevel))
			self.parent.ui.moneyDisplay.text = "$" + str(self.parent.money)
			tower.upgrade(upgradePath)
			self.parent.pfMain.add_tower(tower.position, tower)
			tower.totalMoneySpent += tower.upgradeCost.get(newLevel)
			self.parent.display_upgrade_UI(tower)
	
	def check_upgrade_start(self, touch):
		for tower in self.parent.towerParent.children:
			if self.parent.debug == True:
				yeet = ui.Path.rect(0,0, tower.frame.w, tower.frame.h)
				yeet2 = ShapeNode(yeet, parent = self.parent, z_position = 100, fill_color = "clear", stroke_color = "#000000", position = tower.position)
			if touch.location in tower.frame:
				#show upgrading UI
				self.parent.userState = "upgrading"
				self.parent.display_upgrade_UI(tower)
				return True
			
	def check_place_start(self, touch): #check if the user is trying to drag a building
		for wallBG in self.parent.ui.SELECTAREA:
			square = ui.Path.rect(0, 0, wallBG.frame.w, wallBG.frame.h)
			yeet = ShapeNode(square, parent = self.parent, z_position = 100, fill_color = 'clear', stroke_color = '#ff0000', position = wallBG.point_to_scene(wallBG.position))
			yeet.anchor_point = (0.5, 0)
			if self.parent.debug == False:
				yeet.alpha = 0
			if touch.location in yeet.frame.inset(0, -16):
				self.alpha = 0.8
				self.parent.userState = "placing"
				self.texture = (wallBG.children[0].texture)
				if wallBG == self.parent.ui.holeBg:
					self.placeTower = "hole"
					self.scale = 0.92
				elif wallBG == self.parent.ui.wallBg:
					self.placeTower = "wall"
				elif wallBG == self.parent.ui.sirenBg:
					self.placeTower = "siren"
					self.scale = 0.25
				elif wallBG == self.parent.ui.tankBg:
					self.scale = 0.52
					self.placeTower = "tank"
				elif wallBG == self.parent.ui.batteryBg:
					self.scale = 0.125
					self.placeTower = "battery"
				elif wallBG == self.parent.ui.genBg:
					self.scale = 0.125
					self.placeTower = "generator"
				return True
			else:
				self.alpha = 0
		
	def touch_update(self, touch): #movement of touch
		self.scale = 32/max(self.size)
		self.touchPrevPos = self.touchPos
		self.touchPos = (round((touch.location.x/32))*32, round((touch.location.y/32))*32)
		#test = SpriteNode('pzl:Gray3', parent = self.parent, position = self.touchPos)
		self.position = (self.touchPos[0], self.touchPos[1])
	
		self.canPlace = True
		for child in self.parent.towerParent.children:
			if self.touchPos in child.frame:
				self.canPlace = False
				break
		if self.touchPos in self.parent.staticArea:
			self.canPlace = False
		if self.check_UI(touch) == True:
			self.canPlace = False
			self.alpha = 0
			if self.parent.userState == "placing":
				self.parent.userState = "passive"
				if self.parent.debug == True: self.texture = Texture('pzl:Gray3')
			return
		elif self.parent.debug == True: self.alpha = 0.8
		if self.canPlace == True:
			self.color = '#00ff16'
		else: self.color = '#ff7272'
	
	def check_UI(self, touch):
		if self.parent.ui.bottomBack.frame.contains_point(self.touchPos) and not self.parent.ui.bottomBack.frame.contains_point(self.touchPrevPos):
			return True
		if self.parent.ui.rightBack.frame.contains_point(self.touchPos) and not self.parent.ui.rightBack.frame.contains_point(self.touchPrevPos):
			return True
		return False

if __name__ == '__main__':
	run(main(), frame_interval = 1, show_fps = False)
