import pygame
from object import Object
import math

pygame.init()
scrx = 1500
scry = 750
initx = 0
inity = 0
window = pygame.display.set_mode((scrx,scry))
size = 4
pygame.display.set_caption('Physics Engine')
obj_list = []
#puts a reallllly massive object in the screen to begin with
obj_list.append(Object(window,scrx/2,scry/2,1000))
make_new = False
run = True


def draw_arrow(initx,inity):
	'''
	draw a new object and an arrow in the dirrection and 
	magnitude of the new velocity vector
	'''
	x,y = pygame.mouse.get_pos()
	pygame.draw.circle(window, (255,0,0), (x,y), size)
	pygame.draw.line(window,(255,255,255), (x,y),(initx,inity))
		
	angle = 0
	if initx -x != 0:
		angle = math.atan((inity - y)/(initx-x))
		angle = math.degrees(angle)
		
	angle1 = angle - 30
	angle2 = angle + 30

	lenx = x-initx
	leny = y-inity
	length = ((lenx)**2 + (leny)**2)**.5

	length = length/8

	if angle == 0 and inity - y > 0: #its above it 
		nx1 = initx + (length*math.sin(math.radians(-150)))
		ny1 = inity + (length*math.cos(math.radians(-150)))
		nx2 = initx + (length*math.sin(math.radians(150)))
		ny2 = inity + (length*math.cos(math.radians(150)))
	elif angle == 0 and inity - y < 0: #its below it 
		nx1 = initx + (-length*math.sin(math.radians(-150)))
		ny1 = inity + (-length*math.cos(math.radians(-150)))
		nx2 = initx + (-length*math.sin(math.radians(150)))
		ny2 = inity + (-length*math.cos(math.radians(150)))
	elif initx - x < 0:
		nx1 = initx + (length*math.cos(math.radians(angle1)))
		ny1 = inity + (length*math.sin(math.radians(angle1)))
		nx2 = initx + (length*math.cos(math.radians(angle2)))
		ny2 = inity + (length*math.sin(math.radians(angle2)))
	else:
		nx1 = initx + (-length*math.cos(math.radians(angle1)))
		ny1 = inity + (-length*math.sin(math.radians(angle1)))
		nx2 = initx + (-length*math.cos(math.radians(angle2)))
		ny2 = inity + (-length*math.sin(math.radians(angle2)))
		
	pygame.draw.line(window,(255,255,255), (nx1,ny1),(initx,inity))
	pygame.draw.line(window, (255,255,255), (nx2,ny2),(initx,inity))
	

def handle_col(obj_list):
	'''
	Handles collisions between objects by maintaining the 
	density of the objects (obviously not a completly 
	realistic way to handle the colisions, but it was the easiest
	way to allow objects to collide and combine mass and radius
	propotional to the density of both objects)
	'''
	for obj1 in obj_list:
		for obj2 in obj_list:
			if obj1==obj2:
				pass
			else:
				distx = obj1.pos.xpos-obj2.pos.xpos
				disty = obj1.pos.ypos-obj2.pos.ypos
				dist = ((distx)**2 + (disty)**2)**.5
				if dist <= obj1.h+obj2.h:
					obj1.mass += obj2.mass
					if obj1.dense >= obj2.dense:
						obj1.h = ((obj1.mass)/(obj1.dense *math.pi))**.5 
						obj1.vel.xspeed = ((obj1.mass*obj1.vel.xspeed)+((obj2.mass*obj2.vel.xspeed)))/(obj1.mass+obj2.mass)
						obj1.vel.yspeed = ((obj1.mass*obj1.vel.yspeed)+((obj2.mass*obj2.vel.yspeed)))/(obj1.mass+obj2.mass)
						obj_list.remove(obj2)
					else:
						pass


while run:
	pygame.time.delay(40)
	window.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONUP:
			make_new = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			initx,inity = pygame.mouse.get_pos()
			pygame.mouse.get_rel()

	#draw arrow for every time a new object is created
	if pygame.mouse.get_pressed()[0]:
		draw_arrow(initx,inity)

	#if the mouse is pressed create a new object
	if make_new:
		x,y = pygame.mouse.get_pos()
		n = Object(window,x,y,1,size,1)
		n.init_accel()
		obj_list.append(n)
		make_new = False

	#movment for every iteration
	for obj in obj_list:
		obj.calc_accel(obj_list)
		obj.move()
		if obj.pos.xpos > scrx or obj.pos.xpos < 0 or obj.pos.ypos < 0 or obj.pos.ypos > scry:
			obj_list.remove(obj)
		else:
			obj.draw()

	handle_col(obj_list)
	pygame.display.update()

pygame.quit()