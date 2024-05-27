import pygame
import time
import sys
import random
from graph import Graph
from eades_algorithm import Eades

#Constants used in the Eades algorithm.
c1 = 1
c2 = 16
c3 = 30000
c4 = 0.1

#Create a graph using the 'Graph' class.
vertices_count = 6
my_graph = Graph(vertices_count)
my_graph.add_vertices(['A', 'B', 'C', 'D', 'E', 'F'])
my_graph.add_edge('A', 'B', 2)
my_graph.add_edge('B', 'C', 1)
my_graph.add_edge('C', 'D', 1)
my_graph.add_edge('C', 'E', 1)
my_graph.add_edge('B', 'F', 1)
cost_matrix = my_graph.get_cost_matrix()
adj_matrix = my_graph.get_adj_matrix() # Matriz de adjacência.
screen_width = 700
screen_height = 700
my_eades = Eades(vertices_count, screen_width, screen_height)
vertices_pos = my_eades.get_vertices_pos()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

circles = []
for v in range(vertices_count):
	circle = pygame.draw.circle(screen, RED, vertices_pos[v], 5)
	circles.append(circle)


running = True
loop = 0
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		while loop < 1000:
			loop += 1
			#Invoke the Eades algorithm.
			vertices_pos = my_eades.run_eades(adj_matrix, c1, c2, c3, c4)
			screen.fill(BLACK)
			for v in range(len(adj_matrix)):
				for w in range(len(adj_matrix)):
					if v != w and  adj_matrix[v][w] == 1:
						pygame.draw.line(screen, WHITE, vertices_pos[v], vertices_pos[w])
				circle = circles[v].move_ip(vertices_pos[v])
				pygame.draw.circle(screen, RED, vertices_pos[v], 5)
			pygame.display.flip()
			time.sleep(0.01)
pygame.quit()
sys.exit()
