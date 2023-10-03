class NodeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class _Node:
    def __init__(self, name, colour) -> None:
        self.name = name
        self.colour = colour
    def __repr__(self) -> str:
        return f"{self.name}"

class UndirectedGraph:
    """A class to represent an undirected, simple, unweighted graph."""

    def __init__(self) -> None:
        self.nodelist = []
        self.connections = {}

    def add_node(self, node_name):
        """
        Adds one or more nodes to the list.

        Parameters
        ----------
        node_name: str/list of strings
            One (represented by the name of the node in string format) or more (list of node names) nodes to be added to the undirected graph.
        """
        if type(node_name) == list:
            for node in node_name:
                if node in [existing_nodes.name for existing_nodes in self.nodelist]:
                    raise Exception(f'{node} exist(s) in the nodelist. Try again.')
                else:
                    self.nodelist.append(_Node(node, None))
                    self.connections[node] = []
        else:
            for nodeIndex in range (0, len(self.nodelist)):
                if self.nodelist[nodeIndex].name == node_name:
                    raise Exception(f'{self.nodelist[nodeIndex].name} already exists in the nodelist. Try Again')
            node = _Node(node_name, None)
            self.nodelist.append(node)
            self.connections[node] = []

    def add_random_nodes(self, number_of_nodes):
        """Adds random nodes to the graph(with letters as the name).
        
        Parameters
        ----------
        length: int
            Number of nodes to be added.
        """
        if len(self.connections) !=0:
            asc = max([ord(keys) for keys in self.connections])
            asc+=1
        else:
            asc = 65
        for iters in range (0, number_of_nodes):
            node = _Node(chr(asc), None)
            self.nodelist.append(node)
            self.connections[node.name] = []
            asc+=1

    def test_adjacency(self, fro, to):
        """
        Checks if two nodes are adjacency to each other.

        Parameters
        ----------
        fro: str
            Node from which an edge is outgoing
        to: str
            Node on which the outgoing edge is incident on
        """
        if fro not in [nodes.name for nodes in self.nodelist] and to not in [nodes.name for nodes in self.nodelist]:
            raise Exception(f'{fro} and {to} are both not in the list of defined nodes')
        elif fro not in [nodes.name for nodes in self.nodelist]:
            raise Exception(f'{fro} is not in the list of defined nodes')
        elif to not in [nodes.name for nodes in self.nodelist]:
            raise Exception(f'{to} is not in the list of defined nodes')
        else:
            if to not in self.connections or fro not in self.connections:
                return False
            if to in self.connections[fro]:
                return True
            else:
                return False
        
    def add_edge(self, fro, to):
        """
        Adds an edge between two nodes.

        Parameters
        ----------
        fro: str
            The node from which the edge is to be drawn.
        to: str
            The node towards which the edge is to be drawn.
        """
        count_to = 0
        count_fro = 0
        for nodeIndex in range (0, len(self.nodelist)):
            if self.nodelist[nodeIndex].name == fro:
                count_fro+=1
            elif self.nodelist[nodeIndex].name == to:
                count_to+=1

        if count_to == 0 or count_fro == 0:
            raise Exception('Node not a part of defined graph. Try a different node or define it then try again.')
        
        elif self.test_adjacency(fro, to):
            raise Exception('Nodes are already connected.')
        
        if fro not in self.connections:
            self.connections[fro] = [to]
        else:
            self.connections[fro].append(to)

        if to not in self.connections:
            self.connections[to] = [fro]
        else:
            self.connections[to].append(fro)

    def remove_edge(self, fro, to):
        if fro not in self.connections[to] or to not in self.connections[fro]:
            raise Exception('Edges are not connected')
        else:
            self.connections[to].remove(fro)
            self.connections[fro].remove(to)
    
    def degree(self, node):
        """
        Fetches the degree of a node in the graph.

        Parameters
        ----------
        node: str
            The vertex/node whose degree is to be fetched.

        Returns
        -------
        degree_node: int
            Degree of the node.
        """
        count_node = 0
        for nodeIndex in range (0, len(self.nodelist)):
            if self.nodelist[nodeIndex].name == node:
                count_node+=1
        if count_node == 1:
            degree_node = len(self.connections[node])
            return degree_node
        else:
            raise NodeError('Node not present in graph, try again.')              
        
    def display_connections(self):
        return self.connections
    
    def construct_adjacency_matrix(self):
        """
        Builds and returns the adjacency matrix of the graph object.

        Parameters
        ----------
        self: references the object of the UndirectedGraph class.

        Returns
        -------
        adj_mat: list
            Adjacency Matrix of the graph.
        """
        from pandas import DataFrame

        adj_mat = []
        adj_mat_df = DataFrame(index=[nodes for nodes in self.connections], columns=[nodes for nodes in self.connections])
        for rows in adj_mat_df.index:
            for cols in self.connections[rows]:
                adj_mat_df[rows][cols] = 1
        adj_mat_df.fillna(0, inplace=True)
        for rows in adj_mat_df.index:
            row = []
            for cols in adj_mat_df.columns:
               row.append(adj_mat_df[cols][rows])
            adj_mat.append(row)

        return adj_mat
      
    def complement(self):
        """
        Returns the complement graph of the graph object.

        Parameters
        ----------
        None

        Returns
        -------
        complement_graph: UndirectedGraph object.
            The complement Graph (object) of the specified graph. This is an object of the UndirectedGraph and thus
            the methods of the UndirectedGraph class are also available to this instance.

        """      
        from pandas import DataFrame

        adj_mat = []
        df_adjMat = DataFrame(index=[nodes for nodes in self.connections], columns=[nodes for nodes in self.connections])
        for rows in df_adjMat.index:
            for cols in self.connections[rows]:
                df_adjMat[rows][cols] = 0

        for rows in df_adjMat.index:
            for cols in df_adjMat.index:
                if rows == cols:
                    df_adjMat[rows][cols] = 0

        df_adjMat.fillna(1, inplace=True)
        for rows in df_adjMat.index:
            row = []
            for cols in df_adjMat.columns:
                row.append(df_adjMat[cols][rows])
            adj_mat.append(row)
        
        complement_graph= graph_reconstruction(adj_mat)
        return complement_graph

def visualise(graph_obj):

    """
    [Experimental] Returns a graph visualisation in the form of a png image and uses Pillow (A fork of the Python Imaging LIbrary, or PIL)
    to generate the image.

    Parameters
    ----------
    adj_mat: list
        The adjacency matrix of the graph to be visualised.
    node_names: list, optional
        A list of strings representing the names of nodes (order should match the adjacency matrix).

    Returns
    -------
    PIL Image Object
        Use <variable name for the returned image>.show() to display the image in full-screen.

    """
    from PIL import Image, ImageDraw
    import numpy as np

    node_names = [node.name for node in graph_obj.nodelist]
    adj_mat = graph_obj.construct_adjacency_matrix()
    adjacency_matrix = np.array(adj_mat)

    width, height = 400, 400
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    num_nodes = len(adjacency_matrix)
    vertex_positions = [(width // 2 + width // 4 * np.cos(2 * np.pi * i / num_nodes),
                        height // 2 + height // 4 * np.sin(2 * np.pi * i / num_nodes))
                    for i in range(num_nodes)]

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if adjacency_matrix[i, j] == 1:
                draw.line([vertex_positions[i], vertex_positions[j]], fill="black", width=2)

    radius = 20
    for i, position in enumerate(vertex_positions):
        x, y = position
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], outline="black", fill="white")
        name_x = x - radius
        name_y = y + radius + 5  # Adjust the offset to position the name properly
        draw.text((name_x, name_y), node_names[i], fill="black")

    return image


def graph_reconstruction(adj_mat):

    """
    Used to reconstruct a graph from an adjacency matrix (in the form of a Python 2d List)
    
    Parameters
    ----------
    adj_mat: The 2d List/square adjacency matrix representing the connections of the graph.

    Returns
    -------
    graph: UndirectedGraph object
        The graph represented by the adjacency matrix.
    """
    from pandas import DataFrame

    graph = UndirectedGraph()
    graph.add_random_nodes(len(adj_mat))
    df_connections = DataFrame(data=adj_mat)
    df_connections.index = [nodes for nodes in graph.connections] 
    df_connections.columns = [nodes for nodes in graph.connections]

    graph.nodelist = [_Node(node, None) for node in df_connections.index]
    for i in df_connections.columns:
        for j in df_connections.index:
            if df_connections[i][j] == 1:
                graph.connections[i].append(j)
    return graph


def havelHakimi(degree_seq):
    """
    Returns a degree sequence of length 3 from a degree sequence of indefinite length.

    Parameters
    ----------
    degree_seq: Python list

    Returns
    -------
    degree_seq (of length 3): Python list -> final degree sequence of length 3
    """
    degree_seq.sort(reverse=True)
    if len(degree_seq) == 3:
        return degree_seq
    else:
        s = degree_seq.pop(0)
        for indices in range (0, s):
            degree_seq[indices] = degree_seq[indices]-1
        
        return havelHakimi(degree_seq)

def generate_graph(size, type_of_graph):

    """
    Generates a special graph based on keyword and the size of the graph required.

    Parameters
    ----------
    size: int or tuple(for bipartite graphs)
    type_of_graph: str
        Currently allows the generation of complete and cycle graphs. Use 'complete' as the keyword for complete graphs,
        'cycle' for cycle graphs.
    """

    def generate_complete_graph(size):
        complete_graph = UndirectedGraph()
        complete_graph.add_random_nodes(size)
        from copy import deepcopy
        nodelist2 = [n.name for n in complete_graph.nodelist]
        nodelist3 = []
        for node in complete_graph.nodelist:
            nodelist3 = deepcopy(nodelist2)
            nodelist3.remove(node.name)
            complete_graph.connections[node.name] = [nodes for nodes in nodelist3]

        del nodelist2, nodelist3
        return complete_graph
    
    def generate_cycle_graph(size):

        cycle_graph = UndirectedGraph()
        cycle_graph.add_random_nodes(size)
        for indices in range(0, len(cycle_graph.nodelist)-1):
            cycle_graph.nodelist[indices]
            cycle_graph.add_edge(cycle_graph.nodelist[indices].name, cycle_graph.nodelist[indices+1].name)
        cycle_graph.add_edge(cycle_graph.nodelist[len(cycle_graph.nodelist)-1].name, cycle_graph.nodelist[0].name)

        return cycle_graph
    
    def generate_bipartite_graph(size):
        if type(size) != tuple:
            raise Exception('Size for a bipartite graph has to be a tuple of form (NumberOfNodes_set1, NumberOfNodes_set2)')
        else:
            bipartite_graph = UndirectedGraph()
            set1_length = size[0]
            set2_length = size[1]
            bipartite_graph.add_random_nodes(set1_length+set2_length)
            set1 = [bipartite_graph.nodelist[index] for index in range(0, set1_length)]
            set2 = [bipartite_graph.nodelist[index] for index in range(set1_length, set1_length+set2_length)]
            from random import randint
            counter = randint(3, set1_length*set2_length)

            while counter > 0:
                fro = set1[randint(0, set1_length-1)].name
                to = set2[randint(0, set2_length-1)].name
                while bipartite_graph.test_adjacency(fro, to):
                    fro = set1[randint(0, set1_length-1)].name
                    to = set2[randint(0, set2_length-1)].name
                bipartite_graph.add_edge(fro, to)
                counter-=1
            return bipartite_graph
    
    keywords = {
        'complete': generate_complete_graph,
        'cycle': generate_cycle_graph,
        'bipartite': generate_bipartite_graph
    }

    return keywords[type_of_graph](size)

def is_bipartite(graph_obj):
    """
    Checks if a graph is bipartite or not. Returns true if bipartite, false if not bipartite.

    Parameters
    ----------
    graph_obj: UndirectedGraph object
        The graph which needs to be checked for its bipartite nature(or otherwise).
    
    Returns
    -------
    bool: True or False
        True if bipartite, False if not bipartite.
    """
    from copy import deepcopy
    adj_dictionary = {}
    connections = graph_obj.connections
    nodelist = graph_obj.nodelist

    for key in connections:
        adj_dict_key = next((k for k in nodelist if k.name == key))
        adj_dictionary[adj_dict_key] = []
        # adj_dictionary[adj_dict_key] = [next(connections[v] for v in nodelist if v.name == n for n in connections[key])]
        for node_name in connections[adj_dict_key.name]:
            adj_dictionary[adj_dict_key].append(next(deepcopy(n) for n in nodelist if n.name == node_name))
    
    keys = list(adj_dictionary)
    
    first_node = keys[0]
    first_node.colour = 'red'
    for neighbour in adj_dictionary[first_node]:
        neighbour.colour = 'green'
        
    for i in range (1, len(keys)):
        print(keys[0], [c.colour for c in adj_dictionary[keys[0]]])
        if graph_obj.test_adjacency(keys[i-1].name, keys[i].name):
            if keys[i-1].colour == 'red':
                keys[i].colour = 'green'
                print(keys[i], '-->key')
                for neighbour in adj_dictionary[keys[i]]:
                    neighbour.colour = 'red'

            elif keys[i-1].colour == 'green':
                keys[i].colour = 'red'

                for neighbour in adj_dictionary[keys[i]]:
                    neighbour.colour = 'green'
        else:
            print('hi')
            keys[i].colour = keys[i-1].colour
            
            if keys[i].colour == 'red':
                for neighbour in adj_dictionary[keys[i]]:
                        neighbour.colour = 'green'
            else:
                for neighbour in adj_dictionary[keys[i]]:
                        neighbour.colour = 'red'    

    nodes_red = []
    nodes_green = []
    for key in adj_dictionary:
        for value in adj_dictionary[key]:
            print(key, value, key.colour, value.colour)
            if value.colour == 'green':
                nodes_green.append(value)
            elif value.colour == 'red':
                nodes_red.append(value)
 
    for red_node in nodes_red:
        for green_node in nodes_green:
            if red_node.name == green_node.name:
                del adj_dictionary, nodes_green, nodes_red
                return False
    
    del adj_dictionary, nodes_green, nodes_red
    return True


def dfs(graph_obj, source_node = None):
    """
    Performs a depth-first search on a specified graph. The default parameter for source_node is None which takes a random call for 
    the source vertex. Else specify the string representing the name of a node.
    
    Parameters
    ----------
    graph_obj: UndirectedGraph object- Graph object on which the depth-first search is performed

    source_node: default=None; else, the name of the node (dtype = str)
        Source node from which the dfs is initialised.

    Raises
    ------
    NodeError
        If specified node is not a part of the graph provided in the parameter.
    """
    if source_node == None:
        import random
        source = graph_obj.nodelist[random.randint(0, len(graph_obj.connections)-1)]
    elif source_node in graph_obj.connections:
        for node in graph_obj.nodelist:
            if node.name == source_node:
                source = node
    else:
        raise NodeError('Node not in nodelist of the specified graph. Try again')

    frontier = []
    frontier.append(source.name)
    traversed = []
    while len(frontier)!=0:
        visitedNode = frontier.pop()
        traversed.append(visitedNode)
        for neighbour in graph_obj.connections[visitedNode]:
            if neighbour not in traversed and neighbour not in frontier:
                frontier.append(neighbour)

    return traversed

def bfs(graph_obj, source_node=None):

    """
    Performs a breadth-first search on a specified graph. The default parameter for source_node is None which pushes the program to take
    a random call for the source vertex. Else specify the string representing the name of a node.
    
    Parameters
    ----------
    graph_obj: UndirectedGraph object- Graph object on which the depth-first search is performed
        Source node from which the dfs is initialised.

    source_node: default=None; else, the name of the node (dtype = str)

    Raises
    ------
    NodeError
        If specified node is not a part of the graph provided in the parameter.
    """


    if source_node == None:
        from random import randint
        source = graph_obj.nodelist[randint(0, len(graph_obj.connections)-1)]
    elif source_node in graph_obj.connections:
        for node in graph_obj.nodelist:
            if node.name == source_node:
                source = node
    else:
        raise NodeError('Node not in nodelist. Try again')

    frontier = []
    frontier.append(source.name)
    traversed = []
    from copy import deepcopy
    while len(frontier)!=0:
        visited = frontier.pop(0)
        traversed.append(visited)
        adj = deepcopy(graph_obj.connections[visited])
        adj.reverse()
        for neighbour in adj:
            if neighbour not in traversed and neighbour not in frontier:
                frontier.append(neighbour)
        
    return traversed

def is_isomorphic(graph_obj1, graph_obj2):
    """
    [Work in progress] Checks if two graphs are isomorphic to each other.(Parameters must be an instance of UndirectedGraphs()).

    Parameters
    ----------
    graph_obj1: UndirectedGraph object
        First graph to be compared.
    graph_obj2: UndirectedGraph object
        Second graph to which the first graph is compared to, to check for isomorphism,

    Returns
    -------
    bool: True/False
        True if isomorphic.
        False if non-isomorphic
    """
    adjacency_matrix1 = graph_obj1.construct_adjacency_matrix()
    adjacency_matrix2 = graph_obj2.construct_adjacency_matrix()
    if len(graph_obj1.connections)!=len(graph_obj2.connections):
        return False
    else:
        no_of_edges1 = 0
        no_of_edges2 = 0
        for row in range(0, len(graph_obj1.connections)):
            for col in range (0, len(graph_obj1.connections)):
                if col>row and adjacency_matrix1[row][col] == 1:
                    no_of_edges1+=1
        for row in range(0, len(graph_obj2.connections)):
            for col in range (0, len(graph_obj2.connections)):
                if col>row and adjacency_matrix2[row][col] == 1:
                    no_of_edges2+=1

        if no_of_edges1!=no_of_edges2:
            return False
        
        else:
            degrees_1 = {}
            degrees_2 = {}
            for i in range(len(graph_obj1.nodelist)):
                degrees_1[str(i)] = 0
                degrees_2[str(i)] = 0

            for row in adjacency_matrix1:
                deg1 = sum(row)
                degrees_1[str(deg1)]+=1
            for row in adjacency_matrix2:
                deg2 = sum(row)
                degrees_2[str(deg2)]+=1

            if degrees_1 != degrees_2:
                return False
            else:
                return True