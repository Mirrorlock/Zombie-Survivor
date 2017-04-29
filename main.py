import pygame, sys
from Classes import *
from process import *


pygame.init()
pygame.font.init()

SCREENWIDTH, SCREENHEIGHT = 640, 360

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.FULLSCREEN,32)

width_health, height_health = 200, 30


clock = pygame.time.Clock()
FPS = 30

background = pygame.image.load("images/Stage.jpg")

totalFrames = 0

bug = Bug(SCREENWIDTH/2, SCREENHEIGHT - 84, "images/characterco (2).png", 300) 

while True:
	process(bug, FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH)

	
	#LOGIC
	bug.motion(SCREENWIDTH, SCREENHEIGHT)
	Enemy.update_all(SCREENWIDTH, FPS, totalFrames)
	BugProjectile.movement()
	totalFrames += 1
	#LOGIC
	
	#DRAW
	screen.blit(background, (0, 0))
	for surface in Surfaces.normal_list:
		screen.blit(surface.surface, (surface.x, surface.y))

	BaseClass.allsprites.draw(screen)
	BugProjectile.List.draw(screen)

	for text_holder in Write.normal_list:
		screen.blit(text_holder.text, (text_holder.x,text_holder.y))

	pygame.display.flip()
	#DRAW
	
	



	clock.tick(FPS)

