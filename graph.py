import numpy as np
import random as rnd

class Graph:

	"""
	Class Graph:

		This class represents a graph and provides methods for adding vertices, adding edges,
		and retrieving information about the graph.

	Attributes:
		__vertices_count (int): The number of vertices in the graph.
		__vertices_list (list): A list containing the labels of the vertices.
		__adj_matrix (numpy.array): An adjacency matrix representing the connections between vertices.
		__cost_matrix (numpy.array): A matrix representing the weights of edges between vertices.

	Methods:
		__init__(vertices_count): Initializes the graph with the given number of vertices.
		add_vertices(vertices_list): Adds vertices to the graph.
		add_edge(v, w, weight): Adds an edge between vertices v and w with the given weight.
		get_adj_list(): Returns the adjacency list representation of the graph.
		get_cost_matrix(): Returns the cost matrix representation of the graph.
		get_adj_matrix(): Returns the adjacency matrix representation of the graph.
		get_vertex_label(v_index): Returns the label of the vertex at the given index.
		get_vertices_list(): Returns the list of vertices.
		get_vertex_index(v): Returns the index of the vertex with the given label.
	"""

	def __init__(self, vertices_count):
		self.__vertices_count = vertices_count
		self.__vertices_list = []
		self.__adj_matrix = np.zeros((vertices_count, vertices_count), dtype=int)
		self.__cost_matrix = np.ones((vertices_count, vertices_count), dtype=int) * np.inf
		np.fill_diagonal(self.__cost_matrix, 0)

	def add_vertices(self, vertices_list):
		"""
		Adds vertices to the graph.

		Parameters:
			vertices_list (list): A list containing the labels of the vertices to be added.

		Raises:
			Exception: If the provided list contains duplicate labels.
		"""
		if len(vertices_list) == len(set(vertices_list)):
			self.__vertices_list = vertices_list
		else:
			raise Exception("Provide a list with unique labels.") 
	
	def add_edge(self, v, w, weight):
		"""
		Adds an edge between vertices v and w with the given weight.

		Parameters:
			v (string): The label of the first vertex.
			w (string): The label of the second vertex.
			weight (int): The weight of the edge between v and w.

		"""
		v_index = self.get_vertex_index(v)
		w_index = self.get_vertex_index(w)
		self.__adj_matrix[v_index][w_index] = 1
		self.__cost_matrix[v_index][w_index] = weight
	
	def get_adj_list(self):
		"""
		Returns the adjacency list representation of the graph.

		Returns:
			list: An adjacency list representation of the graph where each element
				  is a list containing the indices of adjacent vertices for each vertex.
		"""
		adj_list = []
		for col in self.__adj_matrix:
			temp_list = []
			index = 0
			for row in col:
				if row == 1:
					temp_list.append(index)
				index += 1
			adj_list.append(temp_list)
		return adj_list
	
	def get_cost_matrix(self):
		"""
		Returns the cost matrix representation of the graph.
		"""
		return self.__cost_matrix

	def get_adj_matrix(self):
		"""
		Returns the adjacency matrix representation of the graph.
		"""
		return self.__adj_matrix

	def get_vertex_label(self, v_index):
		"""
		Returns the label of the vertex at the given index.
		"""
		return self.__vertices_list[v_index]
	
	def get_vertices_list(self):
		"""
		Returns the list of vertices.
		"""
		return self.__vertices_list

	def get_vertex_index(self, v):
		"""
		Returns the index of the vertex with the given label.
		"""
		return self.__vertices_list.index(v)

