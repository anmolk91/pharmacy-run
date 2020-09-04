import math
class Graph:

    vertices = []
    edges = []
    adjacency_matrix = []
    distance_matrix = []
    path = []

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.adjacency_matrix = self.generate_adjacency_matrix(edges)

    def generate_adjacency_matrix(self, edges):
        """
            generates adjacency matrix for the graph
        """
        adjacency_matrix_init = [[0 for i in self.vertices] for j in self.vertices]
        for edge in edges:
            index_one = self.vertices.index(edge['vertice_one'])
            index_two = self.vertices.index(edge['vertice_two'])
            adjacency_matrix_init[index_one][index_two] = int(edge['weight'])
            adjacency_matrix_init[index_two][index_one] = int(edge['weight'])
            
        for i in range(len(self.vertices)):
            index = int(i)
            adjacency_matrix_init[index][index] = math.inf

        return adjacency_matrix_init

    def find_shortest_path(self, source_index):
        """
            finds the shortest path using Djikstra algorithm
        """
        return self.djikstra_algo(source_index)

    def find_shortest_vertices_distance(self, distance_list, spt_set):
        min = math.inf
        min_index = -1
        for v in range(len(self.vertices)):
            if distance_list[v] < min and spt_set[v] == False:
                min = distance_list[v]
                min_index = v

        return min_index;


    def djikstra_algo(self, source_index):

        distance_list = [math.inf] * len(self.vertices)
        distance_list[source_index] = 0
        spt_set = [False] * len(self.vertices)

        parent = [-1] * len(self.vertices)

        for i in range(len(self.vertices)):
            min_node_index = self.find_shortest_vertices_distance(distance_list, spt_set)
            spt_set[min_node_index] = True
            for j in range(len(self.vertices)):
                if self.adjacency_matrix[min_node_index][j] > 0 and spt_set[j] == False and distance_list[j] > distance_list[min_node_index] + self.adjacency_matrix[min_node_index][j]:
                    distance_list[j] = distance_list[min_node_index] + self.adjacency_matrix[min_node_index][j]
                    parent[j] = min_node_index
        
        self.generate_path(parent, source_index)
        return distance_list

    def generate_path(self, parent, source_index):
        for i in range(len(parent)):
            if i != source_index:
                path = []
                path.append(self.vertices[i])
                self.create_path(parent, i, path)
                path.reverse()
                self.path.append(path)
            else:
                self.path.append([])


    def create_path(self, parent, index, path_list):
        if parent[index] == -1:
            return
        path_list.append(self.vertices[parent[index]])
        self.create_path(parent, parent[index], path_list)