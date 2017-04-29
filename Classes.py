import pygame
from random import *


class BaseClass(pygame.sprite.Sprite):
	
	allsprites = pygame.sprite.Group()
	
	
	
	def __init__(self, x, y, image_string):
			
		pygame.sprite.Sprite.__init__(self)
		BaseClass.allsprites.add(self)
		
		self.image = pygame.image.load(image_string)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		
		

	def destroy(self, ClassName):
		ClassName.List.remove(self)
		BaseClass.allsprites.remove(self)
		del self
		
class Bug(BaseClass):
	killed = 0
	going_right = True
	dead = False
	List =  pygame.sprite.Group()
	def __init__(self,x, y, image_string, character_health ):
		BaseClass.__init__(self,x, y, image_string )
		
		self.is_hit = False
		self.character_health = character_health
		
		self.begging_health = self.character_health
		
			
		Bug.List.add(self)
		
		self.velx, self.vely = 0, 7
		self.jumping, self.go_down = False, False

	def motion(self, SCREENWIDTH, SCREENHEIGHT):
		
		predicted_location = self.rect.x + self.velx
		
		if predicted_location < 0:
			self.velx = 0
		elif( predicted_location + self.rect.width > SCREENWIDTH):
			self.velx = 0
		
		
		
		self.rect.x += self.velx
		
		self.__jump(SCREENHEIGHT)
		
	def __jump(self, SCREENHEIGHT):
		
		
		if self.jumping:

			if self.rect.y < 0:
				self.jumping = False
			else:
				self.rect.y -= self.vely

			
		if self.go_down:
			
			predicted_location = self.rect.y + self.vely
			
			if predicted_location + self.rect.height > SCREENHEIGHT:	
				self.go_down = False
			else:
				self.rect.y += self.vely		
	
	
	def show_health(self, width, height, inner_x, inner_y):


		inner_width = width - 2*inner_x
		inner_height = height - 2*inner_y

		percents = (self.character_health/self.begging_health)

		self.health_bar = Surfaces(0, 0, width, height, color = (255, 255, 255), alpha = 128)
		self.inner_bar = Surfaces(inner_x, inner_y, abs(inner_width*percents), inner_height, color = (206, 6, 6), alpha = 255)
		
		if(self.is_hit):
			self.text_health.off_screen()	


		self.text_health = Write("%d / %d" %(self.character_health, self.begging_health), 12, (255, 255, 255), 'Times New Roman')
		self.text_health.on_screen(x = width/2 - self.text_health.text_size[0]/2,
							  y = height/2 - self.text_health.text_size[1]/2)
		
	def del_health(self):
		self.health_bar.delete()
		self.inner_bar.delete()
				
			
			
class Enemy(BaseClass):

		
		
		List = pygame.sprite.Group()
		frequency_spawning = 4*30 #FPS hardcode
		def __init__(self, x, y, image_string, SCREENHEIGHT, totalFrames, FPS):
			BaseClass.__init__(self, x, y, image_string)
			Enemy.List.add(self)
			
			self.hitpoints = 30
			
			
			self.pic_num = 1
			self.hitting = 0

			self.frames_frozen = None
			self.velx_bef_freeze = None
			self.frames_set_on_fire = None
			self.set_on_fire = False
			self.frozen = False
			
			self.health = 100
			self.half_health = self.health / 2.0
			
			self.rect.y = randint(0, SCREENHEIGHT-self.rect.height)
			
			
			seconds = int(abs(totalFrames/FPS))
			max_speed = int(abs(seconds/10))

			self.velx = randint(max_speed+1, max_speed+2)


			
		def move(self, SCREENWIDTH, FPS, totalFrames):
			
			
			if(self.set_on_fire and not self.frozen):
				
				if((totalFrames-self.frames_set_on_fire)/FPS >= 5): #If 5 secs have passed since burned#
					self.set_on_fire = False
					self.image = pygame.image.load('images/characterco enemy.png')
					if(self.velx < 0):
						self.image = pygame.transform.flip(self.image, True, False)
					return 


				if(self.pic_num == 6):	
					self.pic_num = 1

				self.image = pygame.image.load("images/on_fire/characterco-enemy_on_fire(%d).png" %(self.pic_num))
				if(self.velx < 0):
					self.image = pygame.transform.flip(self.image, True, False)

				self.pic_num += 1

			if(self.frozen):
				if((totalFrames-self.frames_frozen)/FPS >= 5): #If 5 sec have passed since freeze#
					
					self.frozen = False
					self.image = pygame.image.load('images/characterco enemy.png')
					self.velx = self.velx_bef_freeze
					if(self.velx < 0):
						self.image = pygame.transform.flip(self.image, True, False)

					return 

			if(self.rect.x + self.rect.width > SCREENWIDTH or self.rect.x < 0):
				self.image = pygame.transform.flip(self.image, True, False)
				self.velx = -self.velx
			
			self.rect.x += self.velx
			
		
			
		@staticmethod	
		def update_all(SCREENWIDTH, FPS, totalFrames):
			for enemy in Enemy.List: 
			
				enemy.move(SCREENWIDTH, FPS, totalFrames)
			
				if enemy.health <= 0:
					enemy.destroy(Enemy)

class BugProjectile(pygame.sprite.Sprite):
	
	List = pygame.sprite.Group()
	normal_list = []
	fire = True

	def __init__(self, x, y, if_true_fire, image_string, FPS):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load(image_string)
		
		self.if_true_fire = if_true_fire
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		
		self.one_second = 0.5 * FPS
		
	
		try:
			last_element = BugProjectile.normal_list[-1]
			difference   = abs(self.rect.x - last_element.rect.x)
			if difference < self.rect.width + 100:
				return
		
		except Exception:
			pass
		

		BugProjectile.normal_list.append(self)
		BugProjectile.List.add(self)
		self.velx = None
	
	@staticmethod
	def movement():
	
		for projectile in BugProjectile.List:
			projectile.rect.x += projectile.velx
			
	def destroy(self):
		BugProjectile.List.remove(self)
		BugProjectile.normal_list.remove(self)
		del self

class Write:
	normal_list = []

	def __init__(self, text, size, color , font_type, bold = False):

		self.text = str(text)
		
		
		self.color = color
		self.font_type = font_type

		self.font = pygame.font.SysFont(font_type, size)

		self.font.set_bold(bold)

		self.text_size = self.font.size(self.text)

		self.text = self.font.render(self.text, False, color)
		 

	def on_screen(self, x, y):
		self.x = x
		self.y = y
		Write.normal_list.append(self)
	
	def off_screen(self):
		Write.normal_list.remove(self)
		del self

class Surfaces:

	normal_list = []
	def __init__(self, x, y, width, height,  color = (255, 255, 255), alpha = 0):
		
		self.surface = pygame.Surface((width, height))
		self.x = x
		self.y = y
		
		self.surface.fill(color)
		self.surface.set_alpha(alpha)
		
		
		
		Surfaces.normal_list.append(self)
	
	def delete(self):
		Surfaces.normal_list.remove(self)
		del self
		