from movement import Coord
from movement import Velocity
import pygame
import math

class Object():
	'''
	An object that can move through space
	'''
	def __init__(self,window,x,y, mass=1,h = 2,accel = 1):
		self.pos = Coord(x,y)
		self.h = h
		self.vel = Velocity()
		self.accel = accel
		self.mass = mass
		self.window = window
		self.dense = self.mass / (math.pi *(self.h**2))


	def init_accel(self):
		'''
		Uses get_rel() to determine initial velovity vector
		of object
		'''

		x,y = pygame.mouse.get_rel()

		dist = ((x)**2 + (y)**2)**.5
			
		if dist != 0 and x != 0:
			force = (abs(dist) * -1)/10
			angle = math.atan(y/x)
			forcex = force*math.cos(angle)
			forcey = force*math.sin(angle)
			
			if x < 0:
				forcex *= -1
				forcey *= -1

			self.vel.xspeed += forcex#/self.mass
			self.vel.yspeed += forcey#/self.mass


	def draw(self):
		'''
		Uses pygame's draw funciton and the atributes of self to draw 
		the object
		'''
		pygame.draw.circle(self.window, (255,0,0), (int(self.pos.xpos), int(self.pos.ypos)), int(self.h))

	def calc_accel(self,obj_list):
		'''
		continually calculates the new acceleration and updates the speed
		of an object as a result of the 
		gravity of all other objects in the environment
		'''
		for obj in obj_list:
			distx = obj.pos.xpos-self.pos.xpos
			disty = obj.pos.ypos-self.pos.ypos
			dist = ((distx)**2 + (disty)**2)**.5
			
			if dist != 0 and distx != 0:
				force = (self.mass*obj.mass)/(dist)**2
				angle = math.atan(disty/distx)
				forcex = force*math.cos(angle)
				forcey = force*math.sin(angle)
				
				if distx < 0:
					forcex *= -1
					forcey *= -1

				self.vel.xspeed += forcex/self.mass
				self.vel.yspeed += forcey/self.mass
			

	def move(self):
		'''
		Uses the speed of an object to update its position
		Also allows for the movement of the objects using the arrow keys if 
		that affect is desired
		'''
		keys = pygame.key.get_pressed()
		if False:
			pass
		else:
			if keys[pygame.K_0]:
				self.vel.yspeed = 0
				self.vel.xspeed = 0
			if keys[pygame.K_DOWN]:
				self.vel.yspeed += self.accel
			if keys[pygame.K_LEFT]:
				self.vel.xspeed -= self.accel
			if keys[pygame.K_RIGHT]:
				self.vel.xspeed += self.accel
			if keys[pygame.K_UP]:
				self.vel.yspeed -= self.accel
		self.pos.xpos += self.vel.xspeed
		self.pos.ypos += self.vel.yspeed


