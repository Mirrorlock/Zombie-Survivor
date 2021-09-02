import pygame, sys
from Classes import *
from process import *

username = input("Enter your username: ")

pygame.init()
pygame.font.init()
pygame.mixer.init()

music = pygame.mixer
SCREENWIDTH, SCREENHEIGHT = 640, 360

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.FULLSCREEN,32)
ADASDFSADFASDFSADFASDFASFD
width_health, height_health = 200, 30


clock = pygame.time.Clock()
FPS = 30

background = pygame.image.load("images/Stage.jpg")

totalFrames = 0
music.music.load("Music/music3.mp3")
music.music.play()
music.music.queue("Music/music2.mp3")
music.music.queue("Music/music5.mp3")
bug = Bug(SCREENWIDTH/2, SCREENHEIGHT - 84, "images/characterco (2).png", 300, username) 



while True:
	process(bug, FPS, totalFrames, SCREENHEIGHT, SCREENWIDTH, music)

	
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

	for obj in Objects.List:
		obj.move()

	for text_holder in Write.normal_list:
		screen.blit(text_holder.screen_text, (text_holder.x,text_holder.y))

	pygame.display.flip()
	#DRAW
	
	



	clock.tick(FPS)

