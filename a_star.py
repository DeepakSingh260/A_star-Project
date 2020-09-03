import pygame 
pygame.init()
import time
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


win = pygame.display.set_mode((800,800))
height = 80
width = 80
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


		for i in ClosedList:
			maze[i.position[0]][i.position[1]]=2

		draw(maze)						 		

		
def draw(maze):
	WIN = pygame.display.set_mode((800,800))
	xpos =0
	ypos = 0

	for i in maze:
		for j in i:
			
			if j == 0:

				pygame.draw.rect(WIN , (255,255,255),(xpos , ypos,width,height))
				xpos+=width
			elif j==1 :
				pygame.draw.rect(WIN , (0,0,0),(xpos,ypos,width,height))
				xpos+=width

			elif j==2:
				pygame.draw.rect(WIN , (255,0,0),(xpos,ypos,width,height))
				xpos+=width	

			elif j==3:
				pygame.draw.rect(WIN,(0,255,0),(xpos,ypos,width,height))
				xpos+=width
					
		ypos+=height
		xpos=0		
		clock = pygame.time.Clock()
		clock.tick(20)

	pygame.display.update()	


 

def main():

	var = False
	draw(maze)
	get_pos = ()

	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			get_pos =pygame.mouse.get_pos()
			var = True

	if var == True:
		for i in range(0,720,80):
			for j in range(0,720,80):
				if get_pos[0]>=i and i+80>=get_pos[0] and get_pos[1]>=j	and j+80>=get_pos[1]:
					maze[round(j/80)][round(i/80)] = 1
					var = False
					draw(maze)
					break

	draw(maze)
	
	start = (0,0)					
	end = (2,9)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				Path = a_star(maze,start,end)
				for path in Path:
					maze[path[0]][path[1]]=3
				draw(maze)	

if __name__ == '__main__':
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		main()
