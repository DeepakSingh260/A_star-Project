import pygame
import random
import time
myList = [80,160,240,320,400,480,560,640,720]

maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("comicsans",50)
WIN = pygame.display.set_mode((800,800))
snakes = pygame.transform.scale(pygame.image.load('snake.png'),(80,80))
tail_image = pygame.transform.scale(pygame.image.load('tail.png'),(80,80))
fruites = pygame.transform.scale(pygame.image.load('fruit.png'),(80,80))
change= 1	
gameOver_img = pygame.transform.scale(pygame.image.load('download.png'),(148,72))

maze
def tailsFun(Maze , tails,fruits):
	print("abs")

	for i in range(len(tails)-1):
		if round(fruits[0].x/80) == round(tails[i].y/80)  and round(fruits[0].x/80)==round(tails[i].x/80):
			continue
		Maze[round(tails[i].y/80)][round(tails[i].x/80)]=1

	return Maze	


class  node:
	
	def __init__(self , parent ,position):
		self.parent = parent
		self.position = position

		self.f =0
		self.g = 0
		self.h = 0

	def __eq__(self,other):
		return self.position == other.position

def a_star(maze , start , end):
	
	start_node = node(None , start)
	start_node.f = start_node.g=start_node.h =0
	end_node = node(None , end)
	end_node.f = end_node.h = end_node.g = 0

	OpenList = []
	ClosedList = []

	OpenList.append(start_node)
	while len(OpenList)>0:

		current_Node = OpenList[0]
		current_index =0

		for index , item in enumerate(OpenList):
			if item.f< current_Node.f:
				current_Node = item
				current_index = index

		OpenList.pop(current_index)
		ClosedList.append(current_Node)

		if current_Node == end_node:

			path  = []

			current = current_Node
			while current is not None:
				path.append(current.position)
				current = current.parent

			return path[::-1]	


		#child
		children =[]

		for new_position in [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)]:

			node_position = (current_Node.position[0]+new_position[0],
				current_Node.position[1]+new_position[1])

			
			if node_position[0] >len(maze)-1 or node_position[0]<0 or node_position[1] > (len(maze[len(maze)-1])-1) or node_position[1]<0:
				
				continue

			if maze[node_position[0]][node_position[1]]!=0:
				continue

			newNode = node(current_Node,node_position)
			children.append(newNode)


		for child in children:

			for closedChild in ClosedList:
				if closedChild == child:
					continue



			child.g = current_Node.g+1
			child.h = ((child.position[0]-end_node.position[0])**2+(child.position[1]-end_node.position[1])**2)
			child.f = child.g + child.h

			for open_node in OpenList:
				if child == open_node and child.g > open_node.g	:
					continue

			OpenList.append(child)	

class Snake:

	def __init__(self,x,y):
		self.x=x
		self.y= y
		self.xchange = 0
		self.ychange = 0


	def change(self,xchange,ychange):
		self.xchange=xchange
		self.ychange=ychange	
	def move(self,x,y):
		self.x=x
		self.y=y



	def draw(self,win):
		if self.xchange == 0:
			win.blit(pygame.transform.rotate(snakes,180),(self.x,self.y))

		if self.xchange == -32:
			win.blit(pygame.transform.rotate(snakes,180),(self.x,self.y))

		if self.xchange == 32:
			win.blit(snakes,(self.x,self.y))
		if self.ychange == -32:
			win.blit(pygame.transform.rotate(snakes,90),(self.x,self.y))
		if self.ychange == 32:
			win.blit(pygame.transform.rotate(snakes,270),(self.x,self.y))			
	def get_mask(self):
		return pygame.mask.from_surface(snakes)

class Tail:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
	def move(self,x,y):
		self.x=x
		self.y=y

	def draw(self,win):	
		win.blit(tail_image,(self.x,self.y))

	def match(self,snake):

		snake_mask = snake.get_mask()
		tail_mask = pygame.mask.from_surface(tail_image)

		tail_offest = (self.x - round(snake.x),self.y - round(snake.y))

		if snake_mask.overlap(tail_mask,tail_offest):
			return True	

		
		return False	


class Fruit:
	def __init__(self):
		self.x = random.choice(myList)
		self.y= random.choice(myList)

	def draw(self,win):
		win.blit(fruites,(self.x,self.y))



	def match(self,snake):
		snake_mask = snake.get_mask()

		fruit_mask = pygame.mask.from_surface(fruites)
		fruit_offset = (self.x - round(snake.x),self.y - round(snake.y))

		if snake_mask.overlap(fruit_mask,fruit_offset):
			return True

		return False	

def gameLoose(snake,fruits,tails,score):
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_SPACE:
				return False

	window_draw(snake,fruits,tails,score,loose=True)			
	return True							

def window_draw(snake,fruits,tails,score , loose = None):
	Win = pygame.display.set_mode((800,800))
	for fruit in fruits:
		fruit.draw(Win)
	snake.draw(Win)
	for tail in tails:
		tail.draw(Win)
	Score = FONT.render('Score'+str(score),1,(255,255,255))
	Win.blit(Score,(10,10)) 
	if loose:
		Win.blit(gameOver_img,(300,400))	

	pygame.display.update()


def main():
	global win
	win = WIN
	clock = pygame.time.Clock()	
	snake = Snake(400,400)
	fruits = [Fruit()]
	var = 0
	Path = a_star(maze , (round(snake.x/80),round(snake.y/80)),(round(fruits[0].x/80),round(fruits[0].y/80)))

	score =0
	tails =[]
	run =True
	Maze = maze
	while run:
		
		#clock.tick(15)
		# Path = a_star(Maze , (round(snake.x/80),round(snake.y/80)),(round(fruits[0].x/80),round(fruits[0].y/80)))

		lt = []
		List = []
		for fruit in fruits:
			if fruit.match(snake):
				
				lt.append(fruit)
				fruits.append(Fruit())
				for i in range(10):
					for j in range(10):
						Maze[i][j]=0 
				print(Maze)
				Maze= tailsFun(Maze,tails,fruits )
				print(Maze) 
				Path = a_star(Maze , (round(snake.x/80),round(snake.y/80)),(round(fruits[0].x/80),round(fruits[0].y/80)))
				
				var=0
				if snake.xchange == 0:
					tails.append(Tail(snake.x+32*len(tails)+32,snake.y))
				if snake.xchange == 32:
					tails.append(Tail(snake.x-32*len(tails)-32,snake.y))
				if snake.ychange == -32:
					tails.append(Tail(snake.x,snake.y+32*len(tails)+32))
				if snake.ychange == 32:
					tails.append(Tail(snake.x,snake.y-32*len(tails)-32))

		for l in lt:
			fruits.remove(l)
			

		i = len(tails)
		while i>=1:
			if i==1:
				tails[0].move(snake.x,snake.y)
			else :	
				tails[i-1].move(tails[i-2].x,tails[i-2].y)
			i-=1
		if var <len(Path):	
			
			snake.move(Path[var][0]*80,Path[var][1]*80)

		var+=1

		for event in pygame.event.get():

			if event.type  == pygame.QUIT:

				run = False

			if event.type == pygame.KEYDOWN:	

				if event.key == pygame.K_DOWN:
					snake.change(0,32)
					

				if event.key == pygame.K_UP:
					snake.change(0,-32)
					
				
				if event.key == pygame.K_RIGHT:
					snake.change(32,0)
					
					
				if event.key == pygame.K_LEFT:
					snake.change(-32,0)
							

		
		
		# #snake.move()
		# for tail in tails:
		# 	if tail.match(snake):
		# 		score = 0
		# 		i = len(tails)	
		# 		while i>1:
		# 			tails.remove(tails[i-1])
		# 			i=i-1

		# 		tails.remove(tails[0])
		# 		snake.xchange=0
		# 		snake.ychange=0

		# 		while gameLoose(snake,fruits,tails,score):
		# 			pass


		
		window_draw(snake,fruits,tails,score)



main()		