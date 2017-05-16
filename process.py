import pygame, sys, Classes, random, time

all_months = ["January", "February", "March", "April", "June", "July", "August", "September", "Octomber", "November", "December"]
current_time = None
killed = None
written = 0
health_obj = None
last_ticks = 0




#######################

def process(bug, FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH, music):
	global current_time, written, killed
	if(current_time is not None and not Classes.Bug.dead):
		current_time.off_screen()

	if(killed is not None and not Classes.Bug.dead):
		killed.off_screen()
	
	if(Classes.BaseClass.music_need and Classes.Bug.dead):
		music.music.load("Music/game_over.mp3")
		music.music.play()
		Classes.BaseClass.music_need = 0


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
		
		
		texts = show_texts(SCREENWIDTH)
		current_time = texts[0]
		killed = texts[1]
		

		health_packs(SCREENHEIGHT, SCREENWIDTH)
		spawn(FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH)
		collisions(bug, SCREENHEIGHT, SCREENWIDTH, totalFrames, FPS, current_time)
		



	else:
		
		
		if(not written):
			f = open("Result.txt", 'a+')
			t = time.localtime()
			f.write("\n-> On {0} {1}, {2} at {3}:%.2d: %s survived: %s \n".format(all_months[t[1]], t[2], t[0], t[3]) %(t[4], bug.username, current_time.text))
			f.close()
			written = 1


		# while(True):
		# 	if(press_any_button()):
				
		# 		break
		if(press_spc_button()):
			pygame.quit()
			sys.exit()
	
	
		



###################################

	
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

def collisions( bug, SCREENHEIGHT, SCREENWIDTH, totalFrames, FPS, current_time):


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



		

		if(pygame.sprite.spritecollide(enemy, Classes.Bug.List, False)): #bug is hit
			if not enemy.hitting:
				if(bug.character_health > enemy.hitpoints):
					
					bug.character_health -= enemy.hitpoints
					
					
				else:
					bug.character_health = 0
					#GAME OVER#
					game_over = Classes.Write( 'GAME OVER', size = 90, color = (153, 15, 15),font_type = 'Informal Roman', bold = True)							
					game_over.on_screen(x = SCREENWIDTH/2 - game_over.text_size[0]/2,
										y = SCREENHEIGHT/2 - game_over.text_size[1]/2 - 60)
					

					

					your_time = Classes.Write(text = "TIME SURVIVED: %s" %(current_time.text),  
											size = int(game_over.size/2), color =  game_over.color, 
											font_type = game_over.font_type)
					your_time.on_screen(x = SCREENWIDTH/2 - your_time.text_size[0]/2, 
										y = game_over.y + game_over.text_size[1] + 15)

					p_continue = Classes.Write(text = "Press <ESCAPE> to quit",  
											size = int(your_time.size/2), color =  game_over.color, 
											font_type = game_over.font_type)	
					p_continue.on_screen(x = SCREENWIDTH/2 - p_continue.text_size[0]/2, 
										y = your_time.y + your_time.text_size[1] + 15)

					Classes.Bug.dead = True
					bug.velx, bug.vely = 0, 0
					
					#GAME OVER#

				if(bug.is_hit):
						bug.del_health()

				bug.show_health()
				bug.is_hit = True
				

					
				enemy.hitting = 1
		else:	
			enemy.hitting = 0

	for obj in Classes.Objects.List:
		if(pygame.sprite.spritecollide(obj, Classes.Bug.List, False) ):
			
				if(bug.character_health + obj.healing <= bug.begging_health):	
					bug.character_health += obj.healing
					
				else:
					bug.character_health = bug.begging_health
				
				if(bug.is_hit):
					bug.del_health()	
					bug.show_health()
				obj.destroy(Classes.Objects)


def press_spc_button():
	keys_for_func = pygame.key.get_pressed()
	keypressed = False

	if(keys_for_func[pygame.K_ESCAPE]):
		keypressed = True
	
	return keypressed

def show_texts(SCREENWIDTH):

	t = pygame.time.get_ticks()

	
	text = "%.2d:%.2d:%.2d" %((t/(1000*60))%60, (t/1000)%60, (t%1000)/10)

	show_time = Classes.Write(text = text, size = 45, color =  (255, 255, 255), font_type = "Informal Roman")
	show_time.on_screen(x = SCREENWIDTH/2 - show_time.text_size[0]/2, y = -10)
	
	killed = str(Classes.Bug.killed)
	show_killed = Classes.Write(text = "%s kills" %(killed), size = 30, color = show_time.color, font_type = show_time.font_type)
	show_killed.on_screen(x = SCREENWIDTH - show_killed.text_size[0], y = -10)
	
	return (show_time, show_killed)


def health_packs(SCREENHEIGHT, SCREENWIDTH):
	global last_ticks
	ticks = pygame.time.get_ticks()	

	if(ticks - last_ticks >= 15000):
		health_pack = Classes.Objects("images/Packs/health_pack.png", SCREENHEIGHT, SCREENWIDTH)
		last_ticks = pygame.time.get_ticks() 
	








