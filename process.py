import pygame, sys, Classes, random, time

all_months = ["January", "February", "March", "April", "June", "July", "August", "September", "Octomber", "November", "December"]

def process(bug, FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH, music):
	
	if(Classes.Bug.dead):

			music.music.load("Music/game_over.mp3")
			music.music.play()
			
			f = open("Result.txt", 'a+')
			t = time.localtime()
			f.write("\n-> On {0} {1}, {2} at {3}:%.2d: %s survived: %.2f seconds\n".format(all_months[t[1]], t[2], t[0], t[3]) %(t[4], bug.username, float(totalFrames/FPS)))
			f.close()
	

			# while(True):
			# 	if(press_any_button()):
					
			# 		break
			if(press_spc_button()):
				pygame.quit()
				sys.exit()

	for event in pygame.event.get():
		if(event.type == pygame.QUIT ):
			
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
				
			


			
			
	if(not Classes.Bug.dead):		
		
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
						game_over = Classes.Write( 'GAME OVER', 50, (66, 134, 244),'Wide Latin')							
						game_over.on_screen(x = SCREENWIDTH/2 - game_over.text_size[0]/2,
											y = SCREENHEIGHT/2 - game_over.text_size[1]/2 - 20)
						

						current_time = float(totalFrames/FPS)

						your_time = Classes.Write(text = "TIME SURVIVED: %.2f seconds" %(current_time),  
										 	   size = 13, color =  game_over.color, 
											   font_type = game_over.font_type)
						your_time.on_screen(x = SCREENWIDTH/2 - your_time.text_size[0]/2, 
										 y = game_over.y + game_over.text_size[1] + 15)

						p_continue = Classes.Write(text = "Press <Space> to quit",  
										 	   size = 10, color =  game_over.color, 
											   font_type = game_over.font_type)	
						p_continue.on_screen(x = SCREENWIDTH/2 - p_continue.text_size[0]/2, 
										 y = your_time.y + your_time.text_size[1] + 15)

						Classes.Bug.dead = True
						bug.velx, bug.vely = 0, 0
						
						#GAME OVER#

					if(character.is_hit):
							character.del_health()

					bug.show_health(200, 40, 10, 10)
					character.is_hit = True
					

						
					enemy.hitting = 1
			else:	
				enemy.hitting = 0

def press_spc_button():
	keys_for_func = pygame.key.get_pressed()
	keypressed = False

	if(keys_for_func[pygame.K_SPACE]):
		keypressed = True
	
	return keypressed




	













