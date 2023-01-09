from scene import *
import math
import ui
import sound
import textEngine
from threading import Timer
A = Action


class help(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.size = get_screen_size()
		self.masterParent = Node(parent = self, scale = 0)
		bg_shape = ui.Path.rounded_rect(0, 0, 240, 256, 8)
		bg_shape.line_width = 4
		shadow = ((0, 0, 0, 0.35), 0, 0, 24)			
		self.menu_bg = ShapeNode(bg_shape, (1,1,1,0.9), '#15a4ff', shadow=shadow, parent=self.masterParent, position = self.size/2)
		self.menu_bg.anchor_point = (0.5, 0.5)
		
		self.title = SpriteNode('images/helpTitle.png', parent = self.menu_bg, scale = 0.25, position = (0, 88))
		
		self.help1 = ButtonNode("Towers 1", parent = self.menu_bg, position = (0, 32))
		self.help2 = ButtonNode("Towers 2", parent = self.menu_bg, position = (0, -24))
		self.help3 = ButtonNode("Electricity", parent = self.menu_bg, position = (0, -82))
		
		self.btn = [self.help1, self.help2, self.help3]
		self.display = SpriteNode('images/helpTitle.png', parent = self.menu_bg, alpha = 1, position = (0, -64), scale = 0)
		self.display.anchor_point = (0.5, 0.5)
		
	def show(self):
		self.masterParent.run_action(Action.scale_to(1, 0.25, TIMING_SINODIAL))

	def hide(self):
		self.masterParent.run_action(Action.scale_to(0, 0.25, TIMING_SINODIAL))
		self.parent.doUpdate = True
		self.parent.uiState = "playing"
	
	def touch_b(self, touch):
		for btn in self.btn:
			if self.menu_bg.point_from_scene(touch.location) in btn.frame:
				btn.texture = Texture('pzl:Button2')
	
	def touch_e(self, touch):
		if self.display.scale == 1.1:
			self.display.run_action(Action.scale_to(0,0.25, TIMING_SINODIAL))
			return
		if touch.location not in self.menu_bg.frame and self.masterParent.scale == 1:
			self.hide()
			return
		for btn in self.btn:
			btn.texture = Texture('pzl:Button1')
			if self.menu_bg.point_from_scene(touch.location) in btn.frame:
				if btn.title == "Towers 1":
					self.display.texture = Texture('images/Help1.png')
				if btn.title == "Towers 2":
					self.display.texture = Texture('images/Help2.png')
				if btn.title == "Electricity":
					self.display.texture = Texture('images/HelpE.png')
				
				self.display.run_action(Action.scale_to(1.1,0.25, TIMING_SINODIAL))

class tut(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.t = textEngine.textEngine(defaultFont = 'Fira Mono', parent = self)
		self.t.addTextBox("tut", 'images/Textbar.png')
		self.t.createPreset("a", {"position": (128, 256), "textWrap": 760, "endWait": "tap", "size": 19})
	
	def intro(self):
		self.t.write("tut", "Hello? Is this thing on? Oh good... it’s you!                                                                                                                                                                          				                                                                                                                                                                             	                                                                                                                                                                              	                                                                                                                                                                             (Tap to continue)", preset = "a", interval = 2)
		self.t.write("tut", "Listen, HQ is being over run, and we’re tight on resources. This is where you come in. We need you to defend while we get defenses back online. The enemy? Oh it’s dangerous. It’s powerful... it’s WATER.", preset = "a")
		self.t.write("tut", "But don’t worry, we know where it comes from. Whenever you press that “NEXT WAVE” button, the water appears at the right side and tries to get to the left side.", preset = "a")
		self.t.write("tut", "After a certain amount of waves, the water will give up, and you can advance to the next stage.", preset = "a")
		self.t.write("tut", "See those six towers to the right? Those are the units HQ sent for you. Drag them out, and place them on the track. If the unit glows green, then it can be placed, if red, then it cannot be placed. Tap on them to upgrade them.", preset = "a")
		self.t.write("tut", 'The units will be explained in more depth in those two buttons at the top right. The first will take you to settings, and the second will give you more information.', preset = "a")
		self.t.write("tut", "Remember to use that help button in the top right. It explains many key concepts, such as electricity!", preset = "a")
		self.t.write("tut", "Good luck commander. We’re all counting on you.", preset = "a")


class stageSelection(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.size = get_screen_size()
		self.position = (-self.size.w, 0)
		self.s1 = MapNode('images/stage1.jpeg', "Placid Park", '#beffb0', (self.size.w/10 * 1.5, self.size.h/10*5), 1, parent = self, scale = 1.25)
		self.s2 = MapNode('images/Stage2.png', "Beach Barrage", '#fcffb0', (self.size.w/10 * 4, self.size.h/10*5), 2, parent = self, scale = 1.25)
		self.s3 = MapNode('images/Stage3.png', "Pathway Plaza", '#ffbd76', (self.size.w/10 * 6.5, self.size.h/10*5), 3, parent = self, scale = 1.25)
		self.s4 = MapNode('images/Stage4.png', "Downtown Delirium", '#ff5858', (self.size.w/10 * 2.75, self.size.h/10*2.8), 4, parent = self, scale = 1.25)
		self.s5 = MapNode('images/Stage5.png', "Aqua Annihilation", '#000000', (self.size.w/10 * 5.25, self.size.h/10*2.8), 5, parent = self, scale = 1.25)
		
		self.mapList = [self.s1, self.s2, self.s3, self.s4, self.s5]
	
	def show(self):
		self.run_action(Action.move_to(0,0, 1, TIMING_SINODIAL))
		self.parent.masterParent.run_action(Action.move_to(self.size.w*2, 0, 1, TIMING_SINODIAL))
	
	def hide(self):
		self.run_action(Action.move_to(-self.size.w, 0, 1, TIMING_SINODIAL))
		self.parent.masterParent.run_action(Action.move_to(0,0,1, TIMING_SINODIAL))
	
	def touch_b(self, touch):
		for button in self.mapList:
			if button.point_from_scene(touch.location) in button.bg.frame:
				button.bg.scale = 1.1
	
	def touch_e(self, touch):
		for button in self.mapList:
			button.bg.scale = 1
		for button in self.mapList:
			if button.point_from_scene(touch.location) in button.bg.frame:
				self.parent.parent.currentLevel	= button.level - 1
				self.parent.parent.transition.run_action(Action.sequence(Action.move_to(self.size.w/2, self.size.h/2, 1, TIMING_SINODIAL), Action.wait(0.15), Action.call(self.parent.hide), Action.call(self.parent.parent.start), Action.wait(0.15), Action.move_to(-self.size.w, self.size.h/2, 1), Action.move_to(self.size.w*2, self.size.h/2,0)))
		else:
			self.hide()

class pause(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.size = get_screen_size()
		bg_shape = ui.Path.rounded_rect(0, 0, 240, 200, 8)
		bg_shape.line_width = 4
		shadow = ((0, 0, 0, 0.35), 0, 0, 24)
		self.background = ShapeNode(ui.Path.rounded_rect(0,0,1200,900, 16), parent = self, color = '#000000', alpha = 0, position = self.size/2)			
		self.menu_bg = ShapeNode(bg_shape, (1,1,1,0.9), '#15a4ff', shadow=shadow, parent=self, position = self.size/2)
		self.menu_bg.scale = 0
		self.menuButton = ButtonNode("Menu", parent = self.menu_bg, position = (0, 0))
		self.resetButton = ButtonNode("Reset", parent = self.menu_bg, position = (0, -64))
		self.buttonList = [self.menuButton, self.resetButton]
		self.title = SpriteNode('images/Paused.png', parent = self.menu_bg, position = (0, 64), scale = 0.35)
	
	def show(self):
		self.menu_bg.run_action(Action.scale_to(1, 0.25, TIMING_SINODIAL))
		self.background.alpha = 0.15		
		self.parent.uiState = "pause"
		self.parent.doUpdate = False
	
	def hide(self):
		self.menu_bg.run_action(Action.scale_to(0, 0.25, TIMING_SINODIAL))
		self.background.alpha = 0
		self.parent.uiState = "playing"
		self.parent.doUpdate = True
	
	def touch_b(self, touch):
		for button in self.buttonList:
			if self.menu_bg.point_from_scene(touch.location) in button.frame:
				button.texture = Texture('pzl:Button2')
	
	def touch_e(self, touch):
		for button in self.buttonList:
			button.texture = Texture('pzl:Button1')
			if self.menu_bg.point_from_scene(touch.location) in button.frame:
				if button.title == "Reset":			
					self.parent.transition.run_action(Action.sequence(Action.move_to(self.size.w/2, self.size.h/2, 1.25, TIMING_SINODIAL), Action.wait(0.2), Action.call(self.parent.start), Action.wait(0.2), Action.move_to(-self.size.w, self.size.h/2, 1.25), Action.move_to(self.size.w*2, self.size.h/2,0)))
				if button.title == "Menu":
					self.parent.transition.run_action(Action.sequence(Action.move_to(self.size.w/2, self.size.h/2, 1, TIMING_SINODIAL), Action.wait(0.15), Action.call(self.parent.show_menu), Action.wait(0.15), Action.move_to(-self.size.w, self.size.h/2, 1), Action.move_to(self.size.w*2, self.size.h/2,0)))
		self.hide()
			
class death(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.size = get_screen_size()
	
	def begin(self):
		self.reset()
		self.resetButton.run_action(Action.sequence(Action.wait(2.5), Action.move_to(self.size.w/2, self.size.h/2 - 116, 2, TIMING_SINODIAL)))
		self.menuButton.run_action(Action.sequence(Action.wait(2.5), Action.move_to(self.size.w/2, self.size.h/2 - 188, 2, TIMING_SINODIAL)))
		
		self.buttonList = [self.resetButton, self.menuButton]
	
	def reset(self):
		for child in self.children:
			child.run_action(Action.remove())
		self.parent.transition = ShapeNode(ui.Path.rounded_rect(0,0,1500,900, 16), parent = self.parent, position = (self.size.w*2, self.size.h/2), color = '#000000', z_position = 100)
		self.background = ShapeNode(ui.Path.rounded_rect(0,0,1200,900, 16), parent = self, position = self.size/2, color = '#000000', alpha = 0)		
		self.deathImg = SpriteNode('images/Gravestone.png', parent = self, position = (self.size.w/2, self.size.h*2), scale = 0.5)
		self.nxtTime = SpriteNode('images/Yeet.png', parent = self.deathImg, scale = 1, position = (0, -304))
		
		self.background.run_action(Action.sequence(Action.wait(0.25), Action.fade_to(0.55, 2)))
		self.deathImg.run_action(Action.sequence(Action.wait(0.25), Action.move_to(self.size.w/2, self.size.h/2 + 128, 3, TIMING_SINODIAL)))
		
		self.resetButton = ButtonNode("Reset", parent = self, position = (-self.size.w, self.size.h/2 - 116))
		self.menuButton = ButtonNode("Menu", parent = self, position = (self.size.w*2, self.size.h/2 - 188))	
		self.alpha = 1
		
	def touch_b(self, touch):
		for button in self.buttonList:
			if touch.location in button.frame:
				button.texture = Texture('pzl:Button2')
	
	def touch_e(self, touch):
		for button in self.buttonList:
			button.texture = Texture('pzl:Button1')
			if touch.location in button.frame:
				if button.title == "Reset":		
					self.parent.transition.run_action(Action.sequence(Action.move_to(self.size.w/2, self.size.h/2, 1.25, TIMING_SINODIAL), Action.wait(0.2), Action.call(self.hide), Action.call(self.parent.start), Action.wait(0.2), Action.move_to(-self.size.w, self.size.h/2, 1.25), Action.move_to(self.size.w*2, self.size.h/2,0)))
				if button.title == "Menu":
					self.parent.transition.run_action(Action.sequence(Action.move_to(self.size.w/2, self.size.h/2, 1, TIMING_SINODIAL), Action.wait(0.15), Action.call(self.parent.show_menu), Action.wait(0.15), Action.move_to(-self.size.w, self.size.h/2, 1), Action.call(self.hide), Action.move_to(self.size.w*2, self.size.h/2,0)))
	
	def hide(self):
		self.alpha = 0
					
class menu(Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.size = get_screen_size()
	
	def setup(self):
		for child in self.children:
			child.run_action(Action.remove())
		self.masterParent = Node(parent = self, z_position = 15)
		self.background_color = '#87ceeb'	
		self.background = ShapeNode(ui.Path.rect(0,0,1112, 834), parent = self, position = (self.size/2), color = '#87ceeb')
		bg_shape = ui.Path.rounded_rect(0, 0, 240, 4 * 64 + 140, 8)
		bg_shape.line_width = 4
		shadow = ((0, 0, 0, 0.35), 0, 0, 24)
		self.menu_bg = ShapeNode(bg_shape, (1,1,1,0.9), '#15a4ff', shadow=shadow, parent=self.masterParent, position = (self.size.w/2, self.size.h/3))
		self.title = LabelNode("WATER WARRIORS", parent = self.masterParent, position = (self.size.w/2, self.size.h/1.25), font = ('Menlo', 75))
		self.title.color = '#000000'
		
		self.bg2 = SpriteNode("images/crateWood.png", parent = self, alpha = 0, position = (self.size.w*2, self.size.h/2 - 96), z_position = 5)
		self.bg2.filter_mode = FILTERING_NEAREST
		self.transition = ShapeNode(ui.Path.rounded_rect(0,0,1500,900, 16), parent = self, position = (self.size.w*2, self.size.h/2), color = '#000000', z_position = 20)
		
		self.mapSelectionMenu = stageSelection(parent = self, z_position = 100, alpha = 1)
		
		self.buttons = []
		for i, title in enumerate(["Start", "Info", "Map Selection", "Credits"]):
			btn = ButtonNode(title, parent=self.masterParent)
			btn.position = (self.size.w/2, self.size.h/2 - i * 96)
			self.buttons.append(btn)
		
	def touch_b(self, touch):
		if self.bg2.position == (self.size.w/2, self.size.h/2 - 96):
			self.bg2.run_action(Action.move_to(self.size.w*2, self.size.h/2 - 96, 1.5, TIMING_SINODIAL))
			self.masterParent.run_action(Action.move_to(0,0,1.5, TIMING_SINODIAL))
		elif self.mapSelectionMenu.position == (0,0):
			self.mapSelectionMenu.touch_b(touch)
		elif self.bg2.position == (self.size.w*2, self.size.h/2 - 96):
			touch_loc = touch.location
			for btn in self.buttons:
				if touch_loc in btn.frame:
					btn.texture = Texture('pzl:Button2')
			
	def hide(self):
		self.masterParent.alpha = 0
		self.menu_bg.alpha = 0
		self.background.alpha = 0
		self.title.alpha = 0
		for button in self.buttons:
			button.alpha = 0	
	
	def touch_e(self, touch):
		if self.mapSelectionMenu.position == (0,0):
			self.mapSelectionMenu.touch_e(touch)
		elif self.bg2.position == (self.size.w*2, self.size.h/2 - 96):
			touch_loc = touch.location
			for btn in self.buttons:
				btn.texture = Texture('pzl:Button1')
				if touch.location in btn.frame:
					if btn.title == "Start":
						self.parent.currentLevel = 0
						self.transition.run_action(Action.sequence(Action.move_to(self.size.w/2, self.size.h/2, 1, TIMING_SINODIAL), Action.call(self.hide), Action.call(self.parent.start), Action.wait(0.1), Action.move_to(-self.size.w, self.size.h/2, 1), Action.fade_to(0,0.25)))
						#self.dismiss_modal_scene()
						return
					if btn.title == "Info":
						self.bg2.texture = Texture('images/Info.png')
					if btn.title == "Map Selection":
						self.mapSelectionMenu.show()
						return
					if btn.title == "Credits":
						self.bg2.texture = Texture('images/Credits.png')
					
					self.bg2.scale = 1.1
					self.bg2.alpha = 1
					self.masterParent.run_action(Action.move_to(-self.size.w, 0, 1.5, TIMING_SINODIAL))
					self.bg2.run_action(Action.move_to(self.size.w/2, self.size.h/2 - 96, 1.5, TIMING_SINODIAL))
		

class ButtonNode(SpriteNode):
	def __init__(self, title, *args, **kwargs):
		SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Avenir Next', 20)
		self.title_label = LabelNode(title, font=button_font, color='black', position=(0, 1), parent=self)
		self.title = title

class MapNode(Node):
	def __init__(self, map, name, borderColor, pos, pairedLevel, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		bg_shape = ui.Path.rounded_rect(0, 0, 240, 160, 8)
		bg_shape.line_width = 4
		shadow = ((0, 0, 0, 0.35), 0, 0, 24)
		self.level = pairedLevel
		self.bg = ShapeNode(bg_shape, (1,1,1,0.9), borderColor, shadow=shadow, parent=self, position = pos)
		#self.bg.anchor_point = (0.5, 0.5)
		self.img = SpriteNode(map, parent = self.bg, position = (0, 12))
		self.img.scale = 160/max(self.img.size)
		self.title = LabelNode(name, parent = self.bg, position = (0, -64), color = '#000000', font = ('Anonymous Pro', 20))
