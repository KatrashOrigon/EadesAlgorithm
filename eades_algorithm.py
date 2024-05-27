import math
import random
import numpy as np

class Eades:

	"""
		Class Eades:

			This class implements the algorithm proposed by Peter Eades (Eades '84) for drawing graphs.

		Attributes:
			__vertices_count (int): The number of vertices in the graph.
			__vertices_pos (numpy.array): An array of tuples containing the positions of the vertices.

		Methods:
			__init__(vertices_count, screen_width, screen_height): Initializes the class with the number of vertices and screen dimensions.
			__vector(point_a, point_b): Calculates the vector pointing from A to B.
			__len_vector(vector): Calculates the modulus of a vector.
			__unit_vector(vector): Calculates the unit vector of a vector.
			__attractive_force(c1, c2, point_a, point_b): Calculates the attractive force between two vertices.
			__repulsive_force(c3, point_a, point_b): Calculates the repulsive force between two vertices.
			__sum_tuples(tuple list): Receives a list of tuples and computes the sum of their x and y components.
			run_eades(adj_matrix, c1, c2, c3, c4): Executes Peter Eades' algorithm to draw the graph.
			set_init_pos(vertices_pos): Sets the initial positions of the vertices.
			get_vertices_pos(): Returns the initial positions of the vertices.
	"""
	
	def __init__(self, vertices_count, screen_width, screen_height):
		"""
		Initializes the graph.
			Parameters:
				vertices_count (int): The number of vertices in the graph.
				screen_width (int): The width of the screen. Required for choosing random values for positions.
				screen_height (int): The height of the screen. Required for choosing random values for positions."
		"""
		self.__vertices_count = vertices_count
		self.__vertices_pos = np.empty(vertices_count, dtype=object)
		# Chooses initial positions randomly.
		dw = int(screen_width * 0.2)
		dh = int(screen_height * 0.2)
		index = 0
		for v in range(vertices_count):
			x = random.randint(dw, screen_width - dw)
			y = random.randint(dh, screen_height - dh)
			self.__vertices_pos[index] = (x, y)
			index += 1

	def __vector(self, point_a, point_b):
		'''
		Calculates the vector pointing from A to B.
			Parameters:
				point_a (tuple of floats), point_b (tuple of floats): the coordinates of points A and B.
			
			Returns:
				(tuple of floats) A tuple containing the vector pointing from A to B.
		'''
		return (point_b[0] - point_a[0], point_b[1] - point_a[1])

	def __len_vector(self, vector):
		'''
		Calculates the modulus of a vector.
			Parameters:
				vector (tuple of floats): coordinates of the vector.
			Returns:
				(float): modulus of the vector.
		'''
		return math.sqrt(vector[0]**2 + vector[1]**2)

	def __unit_vector(self, vector):
		'''
		Calculates the unit vector of a vector.
			Parameters:
				vector (tuple of floats): coordinates of the vector.
			Returns:
				(tuple of floats): the coordinates of the unit vector.
		'''
		return (vector[0] / self.__len_vector(vector), vector[1] / self.__len_vector(vector))

	def __attractive_force(self, c1, c2, point_a, point_b):
		'''
		Calculates the attractive force between two vertices.
			Parameters:
				c1, c2 (floats): see Peter Eades' algorithm (Eades '84).
				point_a, point_b (tuple of floats): tuples with the coordinates of vertices A and B.
			Returns:
				(float) A tuple containing the x and y components of the force.
		'''
		vector_ab = self.__vector(point_a, point_b)
		distance = self.__len_vector(vector_ab)
		unit_vector_ab = self.__unit_vector(vector_ab)
		fa = c1 * math.log(distance/ c2, 10)
		fax = fa * unit_vector_ab[0]
		fay = fa * unit_vector_ab[1]
		return (fax, fay)

	def __repulsive_force(self, c3, point_a, point_b):
		'''
		Calculates the repulsive force between two vertices.
			Parameters:
				c3 (float): see Peter Eades' algorithm (Eades '84).
				point_a, point_b (tuple of floats): tuples with the coordinates of vertices A and B.
			Returns:
				(float) a tuple containing the x and y components of the force..
		'''
		vector_ab = self.__vector(point_a, point_b)
		distance = self.__len_vector(vector_ab)
		unit_vector_ab = self.__unit_vector(vector_ab)
		fr = c3 / (distance * distance)
		frx = fr * - unit_vector_ab[0]
		fry = fr * - unit_vector_ab[1]
		return (frx, fry)

	def __sum_tuples(self, tuple_list):
		'''
		Receives a list of tuples and computes the sum of their x and y components.
		'''
		x = 0
		y = 0
		for tp in tuple_list:
			if tp != None:
				x += tp[0]
				y += tp[1]
		return(x,y)

	def run_eades(self, adj_matrix, c1, c2, c3, c4):
		'''
		The algorithm proposed by Peter Eades (Eades '84).
			Parameters:
				adj_matrix: the adjacency matrix of the graph to be drawn.
				c1, c2, c3, c4 (floats): see Peter Eades' algorithm (Eades '84).
			Returns:
				(array of tuples) an array of tuples containing the new positions of the vertices after calculating the resultant forces on each of them.
		'''
		fa = np.empty(self.__vertices_count, dtype=object) # Sum of the attractive forces for each iteration.
		fr = np.empty(self.__vertices_count, dtype=object) # Sum of the repulsive forces for each iteration.
		for v in range(self.__vertices_count):
			for w in range(v, self.__vertices_count):
				if v != w:
					if adj_matrix[v][w] == 1:
						# The attractive force is calculated only between adjacent vertices
						# because there is a 'spring' between them.
						#
						# Attractive force from v to w.
						attractive = self.__attractive_force(c1, c2, self.__vertices_pos[v], self.__vertices_pos[w])
						fa[v] = self.__sum_tuples([fa[v], attractive])
						# Attractive force from w to v.
						attractive = self.__attractive_force(c1, c2, self.__vertices_pos[w], self.__vertices_pos[v])
						fa[w] = self.__sum_tuples([fa[w], attractive])
					# The repulsive force is calculated between all vertices.
					#
					# Força repulsiva de v para w.
					repulsive = self.__repulsive_force(c3, self.__vertices_pos[v], self.__vertices_pos[w])
					fr[v] = self.__sum_tuples([fr[v], repulsive])
					# Repulsive force from w to v.
					repulsive = self.__repulsive_force(c3, self.__vertices_pos[w], self.__vertices_pos[v])
					fr[w] = self.__sum_tuples([fr[w], repulsive])

		for v in range(self.__vertices_count):
			# Calculates the new positions of the vertices.
			self.__vertices_pos[v] = self.__sum_tuples([self.__vertices_pos[v], fa[v], fr[v]])
		return self.__vertices_pos

	def set_init_pos(self, vertices_pos):
		'''
		Use if you want to initialize the vertices at previously established positions.
			Parameters:
				vertices_pos (array of tuples): an array of tuples containing the initial positions of the vertices.
		'''
		self.__vertices_pos = vertices_pos
		
	def get_vertices_pos(self):
		'''
		Returns an array of tuples containing the positions of the vertices.
		'''		
		return self.__vertices_pos
