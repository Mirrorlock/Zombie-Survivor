import pygame, sys, Classes, random, time

def process(bug, FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH):
	
	
	for event in pygame.event.get():
		if(event.type ==  pygame.QUIT or Classes.Bug.dead):
			time.sleep(1.3)
			pygame.quit()
			sys.exit()
		
		
		if event.type == pygame.KEYDOWN:
			if(event.key == pygame.K_e):
				Classes.BugProjectile.fire = not Classes.BugProjectile.fire
			
			if(event.key ==  pygame.K_ESCAPE):
				pygame.quit()
				sys.exit()
			
		
				
				
				
				# your_time = Classes.Write("Your time: %d" %(current_time), 50, (188, 16, 16),'Wide Latin')
				# your_time.on_screen(x = SCREENWIDTH/2 - your_time.text_size[0]/2,
				# 					y = SCREENHEIGHT/2 - your_time.text_size[1]/2 - 20)
				
			


			
			
				

	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_d]:
		Classes.Bug.going_right = True
		bug.image = pygame.image.load("images/characterco (2).png")
		bug.velx = 5
	elif keys[pygame.K_a]:
		Classes.Bug.going_right = False
		bug.image = pygame.image.load("images/characterco_flipped.png")
		bug.velx = -5
	else:
		bug.velx = 0

		
	if keys[pygame.K_w]:
		bug.jumping = True
		
	else:
		
		bug.jumping = False
	
	if keys[pygame.K_s]:
		bug.jumping = False
		bug.go_down = True
	else:
		bug.go_down = False
		
	if keys[pygame.K_SPACE]:

		def direction():
			if Classes.Bug.going_right:
				p.velx = 8
			else:
				p.image = pygame.transform.flip(p.image, True, False)
				p.velx = -8
		
		if(Classes.BugProjectile.fire):		
			p = Classes.BugProjectile(bug.rect.x, bug.rect.y + 40, True, "images/Firebolt.png", FPS )
			direction()
		else:
			p = Classes.BugProjectile(bug.rect.x, bug.rect.y + 40, False, "images/Frostball.png", FPS )
			direction()

		
		
		
	
	spawn(FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH)
	collisions(bug, SCREENHEIGHT, SCREENWIDTH, totalFrames, FPS)
	



	
	
def spawn(FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH):	
	
	if(Classes.Enemy.frequency_spawning - 0.25*FPS > 0):
		if totalFrames % (10*FPS) == 0:
			
			Classes.Enemy.frequency_spawning -= 0.25*FPS
	
	if totalFrames %  Classes.Enemy.frequency_spawning == 0:
		
		r = random.randint(1, 2)
		x = 1
		
		if r == 2:
			x = SCREENWIDTH - 60
			
		enemy = Classes.Enemy(x, 130,  "images/characterco enemy.png", SCREENHEIGHT, totalFrames, FPS)

def collisions( bug, SCREENHEIGHT, SCREENWIDTH, totalFrames, FPS):


	for enemy in Classes.Enemy.List:
		projectiles = pygame.sprite.spritecollide(enemy, Classes.BugProjectile.List, False) # every enemy that has been hit

		for projectile in projectiles:
			

			if projectile.if_true_fire:	# enemy is hit with fire
				enemy.set_on_fire = True
				
				enemy.frames_set_on_fire = totalFrames#When was it hit with fire#

				enemy.health -= enemy.half_health #HEALTH EXTRACT#
				
				projectile.velx = 0
				if(enemy.health <= 0):
					Classes.Bug.killed += 1

			else: # enemy is being frozen 

				if(not enemy.frozen):
					#FREEZE#
					enemy.frozen = True
					enemy.image  = pygame.image.load("images/frozen_enemy.png")
					
					if(enemy.velx <= 0):
						enemy.image = pygame.transform.flip(enemy.image, True, False )
					
					enemy.velx_bef_freeze = enemy.velx #TO RECOVER ITS DIRECTION AND SPEED#
					enemy.velx = 0
					#FREEZE#

				enemy.frames_frozen = totalFrames #when was it frozen#


			projectile.rect.x = 2* projectile.rect.width	
			projectile.destroy()



		for character in Classes.Bug.List:

			if(pygame.sprite.spritecollide(enemy, Classes.Bug.List, False)): #bug is hit
				if not enemy.hitting:
					if(character.character_health > enemy.hitpoints):
						
						character.character_health -= enemy.hitpoints
						
						
					else:
						character.character_health = 0
						#GAME OVER#
						game_over = Classes.Write( 'GAME OVER', 50, (188, 16, 16),'Wide Latin')							
						game_over.on_screen(x = SCREENWIDTH/2 - game_over.text_size[0]/2,
											y = SCREENHEIGHT/2 - game_over.text_size[1]/2 - 20)
						

						current_time = float(totalFrames/FPS)
						your_time = Classes.Write(text = "TIME SURVIVED: %.2f seconds" %(current_time),  
										 	   size = 15, color =  game_over.color, 
											   font_type = game_over.font_type)
						your_time.on_screen(x = SCREENWIDTH/2 - your_time.text_size[0]/2, 
										 y = game_over.y + game_over.text_size[1] + 15)
						Classes.Bug.dead = True
						#GAME OVER#

					if(character.is_hit):
							character.del_health()

					bug.show_health(200, 40, 10, 10)
					character.is_hit = True
					

						
					enemy.hitting = 1
			else:	
				enemy.hitting = 0

		



	













