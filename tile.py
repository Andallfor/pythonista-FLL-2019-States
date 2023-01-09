from scene import *
import math
import sound
import random

def getDist(point1, point2):
	return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

class tile():
	def __init__(self):
		self.upgradeImages = {(0,0): None, (1,0): None, (2,0): None, (3,0): None, (0,1): None, (0,2): None, (0,3): None}
		self.upgradeStats = {(0,0): None, (1,0): None, (2,0): None, (3,0): None, (0,1): None, (0,2): None, (0,3): None}
		self.currentLevel = (0,0)
		self.info = {(0,0): {"Name": None, "Tooltip": None}, (1,0): {"Name": None, "Tooltip": None}, (2,0): {"Name": None, "Tooltip": None}, (3,0): {"Name": None, "Tooltip": None}, (0,1): {"Name": None, "Tooltip": None}, (0,2): {"Name": None, "Tooltip": None}, (0,3): {"Name": None, "Tooltip": None}}
		self.upgradeCost = {(0,0): None, (1,0): None, (2,0): None, (3,0): None, (0,1): None, (0,2): None, (0,3): None}
		
		self.health, self.maxHealth = None, None
		self.dps = None
		self.eCap, self.eCurrent = None, None
		self.eGain, wPower = None, None
		self.wCap, self.currentWaterAmount = None, None
		self.reloadTime, self.cReload = None, None
		self.eNeeded = None
		
		self.tankHolder = None
		
		#siren stats, seperated bc so many
		self.hRegen, self.playerHRegen = 0, 0 
		self.aRange, self.aSpeed, self.aDmg = 0, 1, 1
		
		self.type = None
		self.level = (0,0)
		self.totalMoneySpent = 0
		
		self.attackRange = 0
		self.attackList = []
		self.attackImg = ShapeNode(ui.Path.oval(0,0,(self.attackRange + self.aRange)*64 + 16, (self.attackRange + self.aRange)*64 + 16), parent = self.parent.parent, alpha = 0, fill_color = '#b5b5b5', stroke_color = '#000000', z_position = 5, position = (self.position)) #paernt = self.parent.parent
		self.attackImg.remove_from_parent()
		self.parent.parent.add_child(self.attackImg)
		
	def shoot_animation(self):
		pass
	def bullet_animation(self):
		pass
	def regular_animation(self):
		pass
	def death(self):
		pass
	def update(self):
		pass
	def upgrade_action(self):
		pass
	def forced_update(self):
		pass
	def set_new_stats(self, stats):
		#best code /s
		newStats = self.upgradeStats.get(stats)
		for newValue in newStats:
			if newValue == "health":
				self.health = newStats.get("health")
				self.maxHealth = newStats.get("health")
			elif newValue == "dps":
				self.dps = newStats.get("dps")
			elif newValue == "eCap":
				if self.eCap == None:
					self.eCap = 0
				self.parent.parent.totalPower += int(newStats.get("eCap") - self.eCap)
				self.eCap = newStats.get("eCap")
			elif newValue == "eGain":
				self.eGain = newStats.get("eGain")
			elif newValue == "wCap":
				self.wCap = newStats.get("wCap")
				self.currentWaterAmount = 0
			elif newValue == "reloadTime":
				self.reloadTime = newStats.get("reloadTime")
				self.cReload = newStats.get("reloadTime")
			elif newValue == "range":
				self.attackRange = newStats.get("range")
				self.attackImg.path = ui.Path.oval(0,0,(self.attackRange + self.aRange)*64 + 16, (self.attackRange + self.aRange)*64 + 16)
			elif newValue == "wPower":
				self.wPower = newStats.get("wPower")
			elif newValue == "eNeeded":
				self.eNeeded = newStats.get("eNeeded")
			elif newValue == "aRange":
				self.aRange = newStats.get("aRange")
			elif newValue == "aDmg":
				self.aDmg = newStats.get("aDmg")
			elif newValue == "aSpeed":
				self.aSpeed = newStats.get("aSpeed")
			elif newValue == "hRegen":
				self.hRegen = newStats.get("hRegen")
			elif newValue == "playerHRegen":
				self.playerHRegen = newStats.get("playerHRegen")

		for tower in self.parent.children:
			if tower.type == "siren":
				tower.forced_update()
								
	def upgrade(self, level):
		newLevel = (self.level[0] + level[0], self.level[1] + level[1])
		self.texture = Texture(self.upgradeImages.get(newLevel))
		self.set_new_stats(newLevel)
		self.level = newLevel
		self.scale = 32/max(self.size)
		self.upgrade_action()
		#self.attackImg.scale = (self.attackRange*64 + 16)/max(self.attackImg.size)
		
	def update_health(self):
		self.health = int(self.health)
		self.health = max(self.health, 0)
		#print(self.health)
		if self.health > 0:
			self.parent.parent.pfMain.add_tower(self.position, self)
		else:
			self.die()
			
	def die(self):	
		self.death()
		try:
			for bullet in self.bImgHolder:
				bullet.run_action(Action.remove())
		except:
			pass
		self.health = 0
		self.parent.parent.pfMain.remove_tower(self.position)
		try:
			self.parent.parent.towerArea.remove(self.position)
		except:
			pass
		self.attackImg.run_action(Action.remove())
		self.remove_from_parent()
		self.run_action(Action.remove())
	
	def check_can_attack(self):
		if self.type == "hole":	
			if self.currentWaterAmount != None:
				self.currentWaterAmount = max(self.currentWaterAmount - 0.01, 0)
			for water in self.parent.parent.waterParent.children:
				if getDist(water.position, self.position) < (self.attackRange) * 32 + 32:
					if self.wCap != None:
						if water.health >= self.wCap - self.currentWaterAmount: # if there's more water then can be absorbed by the hole
							water.take_damage(self.wCap - self.currentWaterAmount)
							self.currentWaterAmount = int(self.wCap) #so the water var isnt paired to the cap var
						elif water.health < self.wCap - self.currentWaterAmount: # if there's less water then the how much the hole can hold
							self.currentWaterAmount += water.health
							water.take_damage(water.health)
					if self.dps != None:
							if self.cReload != None:
								#the hole can attack
								if self.cReload >= self.reloadTime/self.aSpeed:
									# the hole is fully reloaded
									water.take_damage(self.dps)
									self.cReload = 0
					return											
		
		if self.type == "tank":
			#can optimize, remember toAttack?
			if self.parent.parent.power < self.eNeeded or self.cReload < (self.reloadTime/self.aSpeed):
				return
			if self.tankHolder == None or getDist(self.tankHolder.position, self.position) > (self.attackRange + self.aRange) * 32 + 32 or self.tankHolder.health <= 0: #if water is non-existant or out of range
				toCheck = {}
				for water in self.parent.parent.waterParent.children:
					if getDist(water.position, self.position) < (self.attackRange + self.aRange) * 32 + 32:
						toCheck.update({self.parent.parent.level.endLocation[0]: water})
						break
				if len(toCheck) is 0:
					return 
				self.tankHolder = toCheck.get(min(toCheck)) #finds the enemy closest to the end in range
			self.regular_animation(self.tankHolder.position)
			if self.cReload >= (self.reloadTime/self.aSpeed) and self.parent.parent.power >= self.eNeeded:
				self.parent.parent.power -= self.eNeeded
				self.shoot_animation(self.tankHolder.position)
				self.tankHolder.take_damage(self.dps * (self.aDmg + 1))
				self.cReload = 0
		
		if self.type == "generator":
			for water in self.parent.parent.waterParent.children:
				if water.position == self.position:
					#start getting energy
					energy = water.health * self.eGain
					water.take_damage(-1 * water.health * self.wPower)
					#send energy
					least = 100000000
					bat = None
					if len(self.parent.parent.batList) == 0:
						return
					for battery in self.parent.parent.batList:
						if getDist(self.position, battery.position) < least:
							least = getDist(self.position, battery.position)
							bat = battery
					self.parent.parent.power += energy/(getDist(self.position, battery.position)/100)
		
		if self.type == "siren":
			if self.hRegen != 0 and self.powered == True:
				if self.cReload >= self.reloadTime:
					for tower in self.parent.children:
						if getDist(tower.position, self.position) < (self.attackRange) * 32 + 32:
							if tower.health == tower.maxHealth:
								return
							tower.health = min(tower.health + self.hRegen, tower.maxHealth)
							self.parent.parent.power -= self.eNeeded
							for i in range(random.randint(4,6)):
								part = SpriteNode('images/HealthEffect.png', parent = self.parent.parent, position = (random.randint(-16, 16), random.randint(-16, 16)) + tower.position)
								part.scale = 0.03125
								part.run_action(Action.sequence(Action.group(Action.move_by(0, 24, 0.5), Action.fade_to(0.3, 0.5)), Action.remove()))
							self.cReload = 0
				
	def reload(self):
		try:
			if self.cReload < self.reloadTime:
				self.cReload = min(self.cReload + 0.01, self.reloadTime) 
		except:
			pass
			
class wall(tile, SpriteNode):
	def __init__(self, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		tile.__init__(self)
		self.anchor_point = (0.5, 0.5)
		self.scale = 0.57
		self.z_position = 20
		self.type = "wall"
		self.upgradeImages.update({
			(0,0): 'images/barricadeWood.png',
			(1,0): 'images/barricadeMetal.png',
			(2,0): 'images/crateWood.png',
			(3,0): 'images/crateMetal.png'
			})
			
		self.upgradeStats.update({
			(0,0): {"health": 150},
			(1,0): {"health": 400},
			(2,0): {"health": 1000},
			(3,0): {"health": 3500}
			})
		
		self.upgradeCost.update({
			(0,0): 20,
			(1,0): 90,
			(2,0): 450,
			(3,0): 1200
			})
		
		self.info.update({
			(0,0): {"Name": 'Picket Fence', "Tooltip": "Good to keep out dogs!"},
			(1,0): {"Name": "Plaster Wall", "Tooltip": "Your basement wall."},
			(2,0): {"Name": "Flood Wall", "Tooltip": "Good ol' concrete."},
			(3,0): {"Name": "THE WALL", "Tooltip": "Keeps out illegal water-migrants!"}
			})
			
		self.texture = Texture(self.upgradeImages.get((0,0)))
		self.set_new_stats((0,0))

		self.texture.filtering_mode = FILTERING_NEAREST

class hole(tile, SpriteNode):
	def __init__(self, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		tile.__init__(self)
		self.anchor_point = (0.5, 0.5)
		self.scale = 0.62
		self.z_position = 20
		self.type = "hole"
		self.currentWaterAmount = 0
		self.attackImg.alpha = 0

		self.upgradeImages.update({
			(0,0): 'images/treeBrown_twigs.png',
			(1,0): 'images/tileSand2.png',
			(2,0): 'images/tileGrass_transitionS.png',
			(3,0): 'images/tileGrass2.png',
			(0,1): 'images/hole.png',
			(0,2): 'images/big hole.png',
			(0,3): 'images/huge hole.png'
			})
			
		self.upgradeStats.update({
			(0,0): {"wCap": 10},
			(0,1): {"wCap": 25},
			(0,2): {"wCap": 75, "dps": 50, "reloadTime": 0.5},
			(0,3): {"wCap": 500, "dps": 300, "reloadTime": 0.1},
			(1,0): {"dps": 5, "reloadTime": 0.025, "wCap": None}, #wcap set to none to prevent it from being seen in this path
			(2,0): {"dps": 10, "reloadTime": 0.25},
			(3,0): {"dps": 1000, "reloadTime": 0.1}
			})
		
		self.upgradeCost.update({
			(0,0): 10,
			(1,0): 100,
			(2,0): 140, 
			(3,0): 700,
			(0,1): 65,
			(0,2): 200,
			(0,3): 500
			})
		
		self.info.update({
			(0,0): {"Name": 'Hole', "Tooltip": "Made with a shovel."},
			(0,1): {"Name": "Big Hole", "Tooltip": "Made with an excavator."},
			(0,2): {"Name": "Spikes", "Tooltip": "Of course spikes will work!"},
			(0,3): {"Name": "Volcanic Flames", "Tooltip": "Imported lava."},
			(1,0): {"Name": "Drain", "Tooltip": "Drains into the ground!"},
			(2,0): {"Name": "Sand + Grass", "Tooltip": "I'm sure this will work..."},
			(3,0): {"Name": "Bio-Retention", "Tooltip": "It's our project!"}
			})
			
		self.texture = Texture(self.upgradeImages.get((0,0)))
		self.set_new_stats((0,0))

class tank(tile, SpriteNode):
	def __init__(self, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		tile.__init__(self)
		self.anchor_point = (0.5, 0.5)
		self.z_position = 20
		self.scale = 0.35
		self.type = "tank"
		self.level = (0,0)
		self.bImgHolder = []
		self.upgradeImages.update({
			(0,0): 'images/tank_red.png',
			(1,0): 'images/tank_bigRed.png',
			(2,0): 'images/tank_darkLarge.png',
			(3,0): 'images/tank_huge.png',
			(0,1): 'images/tank_blue.png',
			(0,2): 'images/tank_sand.png',
			(0,3): 'images/tank_dark.png'
			})
		
		self.upgradeStats.update({
			(0,0): {'dps': 40, "reloadTime": 0.4, "health": 50, "range": 3, "eNeeded": 0},
			(1,0): {'dps': 200, "reloadTime": 0.4, "health": 100, "range":  3, "eNeeded": 5},
			(2,0): {'dps': 500, "reloadTime": 0.5, "health": 150, "range": 5, "eNeeded": 20},
			(3,0): {'dps': 10500, "reloadTime": 0.75, "health": 1000, "range": 8, "eNeeded": 75},
			(0,1): {'dps': 50, "reloadTime": 0.25, "health": 100, "range": 3, "eNeeded": 2},
			(0,2): {'dps': 70, "reloadTime": 0.15, "health": 100, "range": 3, "eNeeded": 5},
			(0,3): {'dps': 200, "reloadTime": 0.02, "health": 500, "range": 3, "eNeeded": 15}
			})
			
		self.upgradeCost.update({
			(0,0): 200,
			(1,0): 500,
			(2,0): 1200,
			(3,0): 2300,
			(0,1): 450,
			(0,2): 1300,
			(0,3): 2000
			})	
			
		self.info.update({
			(0,0): {"Name": "Turret", "Tooltip": "High-end military weapon."},
			(1,0): {"Name": "Big Red", "Tooltip": "Big Red war-machine!"}, 
			(2,0): {"Name": "Big Boi", "Tooltip": "Shoots fire..."},
			(3,0): {"Name": "Plasma Boi", "Tooltip": "When fire is too cold..."},
			(0,1): {"Name": "Peashooter", "Tooltip": "Rapid fire peashooter."},
			(0,2): {"Name": "Gattling Gun", "Tooltip": "Civil War era gun."},
			(0,3): {"Name": "MK 19", "Tooltip": "Modern era gun."}
			})
		
		self.texture = Texture(self.upgradeImages.get((0,0)))
		self.set_new_stats((0,0))
	
	def update(self):
		self.attackImg.path = ui.Path.oval(0,0,(self.attackRange + self.aRange)*64 + 16, (self.attackRange + self.aRange)*64 + 16)
		self.explode()
	
	def regular_animation(self, enemy):
		a = getDist(enemy, (self.position[0] + 32, self.position[1]))
		b = getDist(enemy, self.position)
		c = 32
		firstPart = b**2 + c**2 - a**2
		secondPart = 2*b*c
		if b != 0:
			if enemy[1] < self.position[1]:
				self.rotation = -1* math.acos(firstPart/secondPart) + math.radians(90)
			else:
				self.rotation = math.acos(firstPart/secondPart) + math.radians(90)
	
	def shoot_animation(self, enemy):
		y = -48 * math.sin((self.rotation) - math.radians(90))
		x = -48 * math.cos((self.rotation) - math.radians(90))
		if self.rotation > math.pi:
			y = -y
			x = -x
		texture = 'images/shotLarge.png'
		bullet = 'images/bulletRed2.png'
		exp = 'images/oilSpill_small.png'
		sound = 'arcade:Explosion_7'
		hitSound = 'arcade:Hit_2'
		scale = 1
		if self.level == (0,0):
			texture = 'images/shotLarge.png'
		elif self.level[0] > 0: #big boi gun	
			if self.level[0] == 1:
				texture = 'images/explosionSmoke4.png'
			if self.level[0] == 2:
				exp = 'images/explosion3.png'
				texture = 'images/explosionSmoke4.png'
				sound = 'arcade:Explosion_2'
				hitSound = 'arcade:Explosion_6'
			elif self.level[0] == 3:
				exp = 'images/explosion2.png'
				bullet = 'images/bulletRed2_outline.png'
				texture = 'images/explosionSmoke2.png'
				sound = 'arcade:Explosion_2'
				hitSound = 'arcade:Explosion_4'
				scale = 2.5
		elif self.level[1] > 0: #fast boi gun
			if self.level[1] == 2:
				texture = 'images/shotOrange.png'
				hitSound = 'arcade:Explosion_1'
			elif self.level[1] == 3:
				texture = 'images/shotRed.png'
				bullet = 'images/bulletRed3_outline.png'
				exp = 'images/explosion2.png'
				sound = 'arcade:Explosion_5'
				hitSound = 'arcade:Explosion_2'
				scale = 0.8
		#flash.rotation = int(self.rotation)
		flash = SpriteNode(texture, parent = self, position = (0,0), z_position = 50, scale = 1.1)
		flash.anchor_point = (0.5,1)
		flash.run_action(Action.sequence(Action.fade_to(0,0.2), Action.remove()))
		self.bullet_animation(enemy, bullet, exp, scale, sound, hitSound) #explosion doesnt do anything currently
				
	def bullet_animation(self, enemy, bullet, explosion, scale, shootSound, hitSound):
		bImg = SpriteNode(bullet, parent = self.parent.parent, position = self.position, scale = 0.25)
		bImg.rotation = int(self.rotation) + math.radians(180)
		#bImg.remove_from_parent()
		newPos = (enemy)
		exp = explosion
		bScale = scale
		#sound.play_effect(shootSound)
		hitSound = hitSound
		self.bImgHolder.append({"bullet": bImg, "targetPos": newPos, "exp": exp, "bScale": bScale, "hitSound": hitSound})
		bImg.run_action(Action.sequence(Action.move_to(newPos[0], newPos[1], 0.05)))
	
	def explode(self): #fix, use list or something
	#add bullet to list, as a tuple with the bullet and its target location
	#cycle though it, checking if the bullet has reached the target location, if so then switch to explosion
		for bullet in self.bImgHolder:
			if bullet.get("bullet").position == bullet.get("targetPos"):
				bImg = bullet.get("bullet")
				bImg.texture = Texture(bullet.get("exp"))
				bImg.scale = bullet.get("bScale")/2
			#sound.play_effect(bullet.get("hitSound"))
				bImg.run_action(Action.sequence(Action.fade_to(0,0.15), Action.remove()))
				bImg.run_action(Action.remove())
				self.bImgHolder.remove(bullet)

class battery(tile, SpriteNode):
	def __init__(self, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		tile.__init__(self)
		self.parent.parent.batList.append(self)
		self.type = "battery"
		self.z_position = 20
		self.scale = 0.0625
		self.eCurrent = 0
		self.level = (0,0)
		
		self.upgradeImages.update({
			(0,0): 'images/regBat.png',
			(1,0): 'images/capciator.png',
			(2,0): 'images/dCell.png',
			(3,0): 'images/duracell.png',
			(0,1): 'images/litIon.png',
			(0,2): 'images/fukishmaBat.png',
			(0,3): 'images/radBat.png'
			})
		
		self.upgradeStats.update({
			(0,0): {"health": 10, "dps": 300, "eCap": 250, "range": 3},
			(1,0): {"health": 25, "dps": 250, "eCap": 750, "range": 2},
			(2,0): {"health": 50, "dps": 150, "eCap": 1500, "range": 1},
			(3,0): {"health": 100, "dps": 75, "eCap": 3000, "range": 0},
			(0,1): {"eCap": 200, "dps": 500, "range": 4},
			(0,2): {"eCap": 150, "dps": 1000, "health": 1},
			(0,3): {"eCap": 50, "dps": 3500}
			})
		
		self.upgradeCost.update({
			(0,0): 100,
			(1,0): 200,
			(2,0): 500,
			(3,0): 2000,
			(0,1): 150,
			(0,2): 500,
			(0,3): 1500
			})
		
		self.info.update({
			(0,0): {"Name": "Battery", "Tooltip": "Your average AA."},
			(1,0): {"Name": "Capicator", "Tooltip": "Circuity!"},
			(2,0): {"Name": "D-Cell", "Tooltip": "Big Poppy of batteries."},
			(3,0): {"Name": "Duracell", "Tooltip": "Not sponsored."},
			(0,1): {"Name": "Lithum Ion", "Tooltip": "Chemicals...Fun!"},
			(0,2): {"Name": "Amazon Basics", "Tooltip": "Comes with Prime."},
			(0,3): {"Name": "Galaxy Note 7", "Tooltip": "Don't charge it too much.."}
			})
				
		self.texture = Texture(self.upgradeImages.get((0,0)))
		self.set_new_stats((0,0))
	
	def death(self):
		#self.remove_from_parent()
		#self.parent.parent.add_child(self)
		self.parent.parent.totalPower -= self.eCap
		#self.parent.parent.batList.remove(self)
		explosion = SpriteNode('images/explosion3.png', parent = self.parent.parent, position = self.position, scale = 0.025, alpha = 0.5)
		explosion.run_action(Action.sequence(Action.scale_to((64*self.attackRange + self.dps/2)/max(self.size),0.05), Action.group(Action.scale_to(0.1, 0.3), Action.fade_to(0, 0.3)), Action.remove()))
		if max(self.level) != 3: #if is maxed upgraded, do no damage to friendly buildings
			for tower in self.parent.parent.towerParent.children: #technically redunant, as self.parent.children does the same
				if tower.type != "battery": # doesnt work, changed to have tower health constantly updated, more lag but i cant seem to fix it otherwise
					if abs(getDist(self.position, tower.position)) < self.attackRange * 32 + 16:
						if tower.type == "hole" or tower.type == "generator": #kills hole bc it has a None health value, and causes bugs
							tower.die()
						else:
							tower.health -= (abs(getDist(self.position, tower.position))/100)*self.dps #damage falloff
							#tower.death()
							#tower.update_health()
		for water in self.parent.parent.waterParent.children:
			if abs(getDist(self.position, water.position)) < self.attackRange * 64 + 16:
				water.take_damage((100/abs(getDist(self.position, water.position))) * self.dps)
	

class generator(tile, SpriteNode):
	def __init__(self, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		tile.__init__(self)
		self.type = "generator"
		self.z_position = 20
		self.scale = 0.125
		self.level = (0,0)
		self.upgradeImages.update({
			(0,0): 'images/gear.png',
			(1,0): 'images/waterMill.png',
			(2,0): 'images/greenFact.png',
			(3,0): 'images/geoThermal.png',
			(0,1): 'images/fuk.png',
			(0,2): 'images/factory.png',
			(0,3): 'images/nag.png'
			})
		
		self.upgradeStats.update({
			(0,0): {"eGain": 0.3, "wPower": 0},
			(1,0): {"eGain": 0.5},
			(2,0): {"eGain": 0.7},
			(3,0): {"eGain": 1},
			(0,1): {"eGain": 0.50, "wPower": 0.01},
			(0,2): {"eGain": 1.5, "wPower": 0.1},
			(0,3): {"eGain": 3, "wPower": 0.25}
			})
		
		self.upgradeCost.update({
			(0,0): 150,
			(1,0): 300,
			(2,0): 600,
			(3,0): 1300,
			(0,1): 400,
			(0,2): 800,
			(0,3): 1400
			})
		
		self.info.update({
			(0,0): {"Name": "Generator", "Tooltip": "Old, slow, and loud, but it works."},
			(1,0): {"Name": "Water Mill", "Tooltip": "A tranditional way of getting power."},
			(2,0): {"Name": "Green House", "Tooltip": "A modern way of producing power."},
			(3,0): {"Name": "Geothermal", "Tooltip": "The latest in power production!"},
			(0,1): {"Name": "Amera. Corp", "Tooltip": "Ruining the planet! Est. 1987"},
			(0,2): {"Name": "Fukishima", "Tooltip": "Coast dwellers beware!"},
			(0,3): {"Name": "Chernobyl", "Tooltip": "Explosive power, radiotactive benefts!"}
			})
		
		self.texture = Texture(self.upgradeImages.get((0,0)))
		self.set_new_stats((0,0))

class siren(tile, SpriteNode):
	def __init__(self, *args, **kwargs):
		SpriteNode.__init__(self, *args, **kwargs)
		tile.__init__(self)
		self.type = 'siren'
		self.level = (0,0)
		self.z_position = 20
		self.scale = 0.125	
		self.powered = False
		self.buffedTowers = []
		
		self.upgradeImages.update({
			(0,0): 'images/Campfire.png',
			(1,0): 'images/Bullhorn.png',
			(2,0): 'images/Lighthouse.png',
			(3,0): 'images/RadarDish.png',
			(0,1): 'images/Tent.png',
			(0,2): 'images/Hospital.png',
			(0,3): 'images/Beacon.png'
			})
		
		self.upgradeStats.update({ #if not enough energy, then effects removed from towers
			(0,0): {"health": 25, "aSpeed": 1.1, "aDamage": 1.1, "range": 2, "eNeeded": 0, "aRange": 0}, #aRange is affecting itself
			(1,0): {"health": 30, "aSpeed": 1.5, "aDamage": 1.5, "aRange": 1},
			(2,0): {"health": 35, "aSpeed": 2, "aDamage": 2, "aRange": 1, "eNeeded": 5, "range": 3},
			(3,0): {"health": 40, "aSpeed": 2.5, "aDamage": 2.5, "aRange": 2, "eNeeded": 7, "range": 4},
			(0,1): {"health": 30, "hRegen": 5, "reloadTime": 0.75},
			(0,2): {"health": 35, "hRegen": 10, "reloadTime": 0.75, "eNeeded": 3, "range": 3, "playerHRegen": 5},
			(0,3): {"health": 40, "hRegen": 35, "reloadTime": 0.5, "eNeeded": 10, "playerHRegen": 15}
			})
		
		self.upgradeCost.update({
			(0,0): 250,
			(1,0): 500,
			(2,0): 1000,
			(3,0): 2000,
			(0,1): 700,
			(0,2): 1500,
			(0,3): 3000
			})
		
		self.info.update({
			(0,0): {"Name": "Campfire", "Tooltip": "Provides warmth for your towers."},
			(1,0): {"Name": "Bullhorn", "Tooltip": "Advanced warning system."},
			(2,0): {"Name": "Lighthouse", "Tooltip": "A lighthouse in the middle of land..."},
			(3,0): {"Name": "Satellite Dish", "Tooltip": "Overkill? Maybe."},
			(0,1): {"Name": "Medical Tent", "Tooltip": "Quick access to medical tools."},
			(0,2): {"Name": "Hospital", "Tooltip": '"Afforable" healthcare.'},
			(0,3): {"Name": "Beacon", "Tooltip": "Not copied from Minecraft."}
			})
		
		self.texture = Texture(self.upgradeImages.get((0,0)))
		self.set_new_stats((0,0))
	
	def buff_towers(self):
		if len(self.buffedTowers) != 0:
			for tower in self.buffedTowers:
				tower.aSpeed = max(self.aSpeed, tower.aSpeed)
				tower.aDmg = max(self.aDmg, tower.aDmg)
				tower.aRange = max(self.aRange, tower.aRange)
				tower.attackImg.path = ui.Path.oval(0,0,(self.attackRange + self.aRange)*64 + 16, (self.attackRange + self.aRange)*64 + 16)
		else:
			for tower in self.parent.children:
				if tower.type != 'siren' and tower.type != "hole":
					if getDist(tower.position, self.position) < self.attackRange * 32 + 32:
						tower.aSpeed = max(self.aSpeed, tower.aSpeed)
						tower.aDmg = max(self.aDmg, tower.aDmg)
						tower.aRange = max(self.aRange, tower.aRange)
						tower.attackImg.path = ui.Path.oval(0,0,(self.attackRange + self.aRange)*64 + 16, (self.attackRange + self.aRange)*64 + 16)
						self.buffedTowers.append(tower)
		
	def remove_buff_towers(self):
		for buffed in self.buffedTowers:
			buffed.aSpeed = 1
			buffed.aDmg = 1
			buffed.aRange = 0
			self.buffedTowers.remove(buffed)
	
	def update(self):
		if self.powered == False: #check constantly if there is enough power if there is currently no power
			if self.parent.parent.power >= self.eNeeded:
				self.powered = True
				self.buff_towers()
		elif self.parent.parent.power < self.eNeeded:
			#only remove buff from towers once, as lag prevention
			self.powered = False
			self.remove_buff_towers()
		if self.parent.parent.power >= self.eNeeded:
			self.parent.parent.power -= self.eNeeded/10
	
	def death(self):
		self.remove_buff_towers()
	
	def forced_update(self):
		self.buff_towers()		
