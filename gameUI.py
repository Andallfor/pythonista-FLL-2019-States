from scene import *
import sound
import random
import math
import ui

class UI(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.anchor_point = (0,0)
		
		self.settings = SpriteNode('iow:settings_24', parent = self, position = (996, self.parent.size.h - 24), z_position = 100)
		self.settingsOutline = ShapeNode(ui.Path.rounded_rect(0,0,26,26,2), stroke_color = '#ffffff', position = (995, self.parent.size.h - 24), parent = self, z_position = 100, fill_color = 'clear')
		self.help = SpriteNode('iow:help_24', parent = self, position = (1055, self.parent.size.h - 24), z_position = 100)
		self.helpOutline = ShapeNode(ui.Path.rounded_rect(0,0,26,26,2), stroke_color = '#ffffff', position = (1054, self.parent.size.h - 24), parent = self, z_position = 100, fill_color = 'clear')
		
		self.bottomBackShape = ui.Path.rect(0,0, 1300, 120)
		self.bottomBack = ShapeNode(self.bottomBackShape, parent = self, position = (-1,-1))
		self.bottomBack.anchor_point = (0,0)
		self.bottomBack.color = '#000000'
		self.z_position = 41

		self.rightBackShape = ui.Path.rect(0,0, 176, 1000)
		self.rightBack = ShapeNode(self.rightBackShape, parent = self, position = (self.parent.size.w + 1, 0))
		self.rightBack.anchor_point = (1,0)
		self.rightBack.color = '#000000'
		self.z_position = 41
		
		#IMPORTANT: THIS IS THE UPGRADING UI
		self.RIGHTUIUPGRADE = Node(parent = self, z_position = 5, alpha = 0)
		
		outline = ui.Path.rounded_rect(0,0,96,96,8)
		self.currentTowerIMGOutline = ShapeNode(outline, parent = self.RIGHTUIUPGRADE, fill_color = '#dbdbdb', z_position = 51, position = (1024, self.parent.size.h/10*8.5))
		self.currentTowerIMG = SpriteNode('images/tank_red.png',parent = self.RIGHTUIUPGRADE, position = (1024, self.parent.size.h/10*8.5), z_position = 52)
		self.currentTowerIMG.scale = 80/max(self.currentTowerIMG.frame.w, self.currentTowerIMG.frame.h)
		self.currentTowerIMGTitle = LabelNode("TITLE", parent = self.RIGHTUIUPGRADE, position = (1024, self.parent.size.h/10*8.5+72), font = ('Copperplate', 20))
		self.currentTowerIMGToolTip = LabelNode("Give desc here", parent = self.RIGHTUIUPGRADE, position = (1024, self.parent.size.h/10*8.5-64), font = ('Avenir Next Condensed', 11))
		
		self.ctHealthParent = Node(parent = self.RIGHTUIUPGRADE)
		self.ctHealthIMG = SpriteNode('images/heart.png', scale = 0.03125, parent = self.ctHealthParent, position = (953, self.parent.size.h/10*7.5))
		self.ctHealthBG = ShapeNode(ui.Path.rounded_rect(0,0,128,16,3), position = (968, self.parent.size.h/10*7.5), parent = self.ctHealthParent, anchor_point = (0,0.5))
		self.ctHealthFG = ShapeNode(ui.Path.rounded_rect(0,0,120,12,3), position = (972, self.parent.size.h/10*7.5), parent = self.ctHealthParent, anchor_point = (0,0.5), fill_color = '#ff0000')
		self.ctReloadParent = Node(parent = self.RIGHTUIUPGRADE)
		self.ctReloadIMG = SpriteNode('images/attack.png', scale = 0.06, parent = self.ctReloadParent, position = (953, self.parent.size.h/10*7.5-24))
		self.ctReloadBG = ShapeNode(ui.Path.rounded_rect(0,0,128,16,3), position = (968, self.parent.size.h/10*7.5-24), parent = self.ctReloadParent, anchor_point = (0,0.5))
		self.ctReloadFG = ShapeNode(ui.Path.rounded_rect(0,0,120,12,3), position = (972, self.parent.size.h/10*7.5-24), parent = self.ctReloadParent, anchor_point = (0,0.5), fill_color = '#ff8500')
		self.ctPowerParent = Node(parent = self.RIGHTUIUPGRADE)
		self.ctPowerIMG = SpriteNode('spc:BoltGold', parent = self.ctPowerParent, position = (953, self.parent.size.h/10*7.5-48), scale = 0.6)
		self.ctPowerBG = ShapeNode(ui.Path.rounded_rect(0,0,128,16,3), position = (968, self.parent.size.h/10*7.5-48), parent = self.ctPowerParent, anchor_point = (0,0.5))
		self.ctPowerFG = ShapeNode(ui.Path.rounded_rect(0,0,120,12,3), position = (972, self.parent.size.h/10*7.5-48), parent = self.ctPowerParent, anchor_point = (0,0.5), fill_color = '#ffd335')
		self.ctBatteryParent = Node(parent = self.RIGHTUIUPGRADE)
		self.ctBatteryIMG = SpriteNode('images/barrelBlack_side.png', scale = 0.3, position = (953, self.parent.size.h/10*7.5-72), parent = self.ctBatteryParent)
		self.ctBatteryBG = ShapeNode(ui.Path.rounded_rect(0,0,128,16,3), position = (968, self.parent.size.h/10*7.5-72), parent = self.ctBatteryParent, anchor_point = (0,0.5))
		self.ctBatteryFG = ShapeNode(ui.Path.rounded_rect(0,0,120,12,3), position = (972, self.parent.size.h/10*7.5-72), parent = self.ctBatteryParent, anchor_point = (0,0.5), fill_color = '#00ce0b')
		self.ctWaterParent = Node(parent = self.RIGHTUIUPGRADE)
		self.ctWaterIMG = SpriteNode('images/barrelGreen_side.png', parent = self.ctWaterParent, position = (953, self.parent.size.h/10*7.5-48), scale = 0.3)
		self.ctWaterBG = ShapeNode(ui.Path.rounded_rect(0,0,128,16,3), position = (968, self.parent.size.h/10*7.5-48), parent = self.ctWaterParent, anchor_point = (0,0.5))
		self.ctWaterFG = ShapeNode(ui.Path.rounded_rect(0,0,0,12,3), position = (972, self.parent.size.h/10*7.5-48), parent = self.ctWaterParent, anchor_point = (0,0.5), fill_color = '#61c1ff')
		
		self.uP1Parent = Node(parent = self.RIGHTUIUPGRADE, z_position = 5)
		self.uP1BG = ShapeNode(ui.Path.rounded_rect(0,0,128,152,4), parent = self.uP1Parent, fill_color = '#dbdbdb', position = (1024, self.parent.size.h/10*5.4), z_position = 51)
		self.uP1Title = LabelNode("Title", parent = self.uP1Parent, font = ('Copperplate', 15), position = (1024, self.parent.size.h/10*5.4+64), color = '#000000', z_position = 52)
		self.uP1Cost = LabelNode("Cost", parent = self.uP1Parent, font = ('Copperplate', 25), position = (1024, self.parent.size.h/10*5.4-64), color = '#000000', z_position = 52)
		self.uP1 = SpriteNode('images/tank_darkLarge.png', parent = self.uP1Parent, position = (1024, self.parent.size.h/10*5.4), z_position = 53)
		self.uP1.scale = 104/max(self.uP1.size)
		self.uP2Parent = Node(parent = self.RIGHTUIUPGRADE)
		self.uP2BG = ShapeNode(ui.Path.rounded_rect(0,0,128,152,4), parent = self.uP2Parent, fill_color = '#dbdbdb', position = (1024, self.parent.size.h/10*3.2))
		self.uP2 = SpriteNode('images/tank_sand.png', parent = self.uP2Parent, position = (1024, self.parent.size.h/10*3.2))
		self.uP2.scale = 104/max(self.uP2.size)
		self.uP2Title = LabelNode("Title", parent = self.uP2Parent, font = ('Copperplate', 15), position = (1024, self.parent.size.h/10*3.2+64), color = '#000000')
		self.uP2Cost = LabelNode("Cost", parent = self.uP2Parent, font = ('Copperplate', 25), position = (1024, self.parent.size.h/10*3.2-64), color = '#000000')
		
		self.sellButton = ShapeNode(ui.Path.rounded_rect(0,0,128,48,8), parent = self.RIGHTUIUPGRADE, fill_color = '#ffffff', position = (1024, self.parent.size.h/10*1.75))
		self.sellDisplay = LabelNode("SELL: $" + "yeet", parent = self.sellButton, color = '#000000', font = ('DIN Condensed', 30))
		
		#IMPORTANT: THIS IS THE RIGHT MENU, DEFUALT PARENT
		self.RIGHTUIDEFUALT = Node(parent = self, alpha = 1, z_position = 4)
		
		self.attackParent = Node(parent = self.RIGHTUIDEFUALT, position = (1036, self.parent.size.h/10*9))
		self.attackTitle = LabelNode("Attack", parent = self.attackParent, z_position = 42)
		self.attackSubtitle = LabelNode("_____", parent = self.attackParent, position = (0, -4), z_position = 42)
		self.holeBg = SpriteNode('images/towerDefense_tile181.png', parent = self.attackParent, position = (0, -68), z_position = 42)
		self.holeImg = SpriteNode('images/treeBrown_twigs.png', parent = self.holeBg, position = (0, 16), z_position = 43)
		self.holeCost = LabelNode("$10", parent = self.attackParent, position = (0, -96), z_position = 43)
		self.attackParent2 = Node(parent = self.attackParent, position = (0, -117))
		self.tankBg = SpriteNode('images/towerDefense_tile181.png', parent = self.attackParent2, z_position = 42, position = (0, -68))
		self.tankImg = SpriteNode('images/tank_red.png', parent = self.tankBg, position = (0, 16), z_position = 43, scale = 0.7)
		self.tankCost = LabelNode("$200", parent = self.attackParent, position = (0, -217), z_position = 43)
		
		self.defenseParent = Node(parent = self.RIGHTUIDEFUALT, position = (1036, self.parent.size.h/10*6))
		self.defenseTitle = LabelNode("Defense", parent = self.defenseParent, z_position = 42)
		self.defenseSubtitle = LabelNode("_____", parent = self.defenseParent, position = (0, -4), z_position = 42)
		self.wallBg = SpriteNode('images/towerDefense_tile181.png', parent = self.defenseParent, position = (0, -68), scale = 1, z_position = 42)
		self.wallImg = SpriteNode('images/barricadeWood.png', parent = self.wallBg, scale = 1, position = (0, 16), z_position = 43)
		self.wallCost = LabelNode("$20", parent = self.defenseParent, position = (0, -96), z_position = 43)
		self.defenseParent2 = Node(parent = self.defenseParent, position = (0, -117), z_position = 4)
		self.sirenBg = SpriteNode('images/towerDefense_tile181.png', parent = self.defenseParent2, position = (0, -68), scale = 1, z_position = 1)
		self.sirenImg = SpriteNode('images/Campfire.png', parent = self.sirenBg, scale = 0.25, position = (0, 16), z_position = 43)
		self.sirenCost = LabelNode("$250", parent = self.defenseParent2, position = (0, -96), z_position = 43)
		
		self.supportParent = Node(parent = self.RIGHTUIDEFUALT, position = (1036, self.parent.size.h/10*3))
		self.supportTitle = LabelNode("Support", parent = self.supportParent, z_position = 42)
		self.supportSubtitle = LabelNode("_____", parent = self.supportParent, position = (0, -4), z_position = 42)
		self.genBg = SpriteNode('images/towerDefense_tile181.png', parent = self.supportParent, position = (0, -68), scale = 1, z_position = 42)
		self.genImg = SpriteNode('images/gear.png', parent = self.genBg, scale = 0.25, position = (0, 16), z_position = 43)
		self.genCost = LabelNode("$150", parent = self.supportParent, position = (0, -96), z_position = 43)
		self.supportParent2 = Node(parent = self.supportParent, position = (0, -117), z_position = 4)
		self.batteryBg = SpriteNode('images/towerDefense_tile181.png', parent = self.supportParent2, position = (0, -68), scale = 1, z_position = 1)
		self.batteryImg = SpriteNode('images/regBat.png', parent = self.batteryBg, scale = 0.125, position = (0, 16), z_position = 43)
		self.batteryCost = LabelNode("$100", parent = self.supportParent2, position = (0, -96), z_position = 43)

		self.healthParent = Node(parent = self, position = (self.parent.size.w/2, 74))
		healthLine = ui.Path.rounded_rect(0, 0, 500, 20, 8)
		heathBGLine = ui.Path.rounded_rect(0, 0, 525, 30, 16) #16
		self.healthBG = ShapeNode(heathBGLine, fill_color = '#ffffff', parent = self.healthParent, z_position = 42)
		self.healthDisplay = ShapeNode(healthLine, fill_color = '#ff3e3e', parent = self.healthParent, position = (-self.healthBG.size.w/2 + 12.5,0), z_position = 43)
		self.healthDisplay.anchor_point = (0,0.5)
		self.healthPercent = LabelNode(str(self.parent.healthPercentage) + "%", parent = self.healthParent, z_position = 44)
		self.healthPercent.color = '#000000'
		self.healthTitle = LabelNode("HEALTH:", parent = self.healthParent, position = (-350, 0), z_position = 42)
		
		self.moneyParent = Node(parent = self, position = (self.parent.size.w/2, 34), z_position = 42)
		self.moneyTitle = LabelNode("MONEY: ", parent = self.moneyParent, position = (-350, 0))
		self.moneyDisplay = LabelNode("$" + str(self.parent.money), parent = self.moneyParent, position = (-286, 0))
		self.moneyDisplay.anchor_point = (0,0.5)
		self.moneyDisplay.color = "FFBD1B"
		
		self.waveParent = Node(parent = self, position = (self.parent.size.w/14, 74), z_position = 42)
		self.waveTitle = LabelNode("WAVE:", parent = self.waveParent)
		self.waveCurrent = LabelNode(str(self.parent.currentWave), parent = self.waveParent, position = (0, -10))
		self.waveCurrent.anchor_point = (0.5, 1)
		self.waveDivider = LabelNode("—", parent = self.waveParent, position = (-1, -21))
		self.waveDivider.anchor_point = (0.5, 1)
		self.waveMax = LabelNode(str(self.parent.maxWave), parent = self.waveParent, position = (-1, -34))
		self.waveMax.anchor_point = (0.5, 1)
		
		self.startWaveButton = ShapeNode(ui.Path.rounded_rect(0,0,80,80,4), parent = self, position = (self.parent.size.w/14*11.3, 64), z_position = 50)
		self.startWaveTextTop = LabelNode("NEXT", parent = self.startWaveButton, font = ('Courier', 20), color = '#000000', position = (0, 8))
		self.startWaveTextBottom = LabelNode("WAVE", parent = self.startWaveButton, font = ('Courier', 20), color = '#000000', position = (0, -8))
		
				
		for child in self.children:
			try:
				child.texture.filtering_mode = FILTERING_NEAREST
			except:
				try:
					for child2 in child.children:
						child2.texture.filtering_mode = FILTERING_NEAREST
				except:
					pass
		
		self.SELECTAREA = [self.holeBg, self.wallBg, self.sirenBg, self.tankBg, self.batteryBg, self.genBg]
		
	def update_health(self):
		self.parent.healthPercentage = min(100, max(round(self.parent.currentHealth * 100/self.parent.maxHealth),0)) #caps health at 0 and at 100
		self.healthDisplay.path = ui.Path.rounded_rect(0,0,self.parent.healthPercentage*5,20,8)
		self.healthPercent.text = str(self.parent.healthPercentage) + "%"
		
	# Not used
	def build_area(self):
		buildArea = []
		staticArea = []
		holderPos = (0,0)
		for x in range(0, int(self.parent.size.w + 16), 16):
			for y in range(0, int(self.parent.size.h + 16), 16):
				if x >= 960:
					holderPos = (x, holderPos[1])
				if y <= 112:
					holderPos = (holderPos[0], y)
				staticArea.append(holderPos)
		return staticArea
