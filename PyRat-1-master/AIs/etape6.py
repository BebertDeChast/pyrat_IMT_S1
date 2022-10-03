##############################################################
# The turn function should always return a move to indicate where to go
# The four possibilities are defined here
##############################################################

import heapq as hq
import time
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'


##############################################################
# Please put your code here (imports, variables, functions...)
##############################################################

moves = []
index = 0
max_index = 0

# ? Routing algorithms


def find_direction(player_location, destination):
    difference = (player_location[0] - destination[0], player_location[1] - destination[1])  # Computing the difference to go faster
    if difference[0] == -1:
        return MOVE_RIGHT
    elif difference[0] == 1:
        return MOVE_LEFT
    elif difference[1] == 1:
        return MOVE_DOWN
    elif difference[1] == -1:
        return MOVE_UP
    elif difference[0] == difference[1] == 0:
        raise Exception("find_direction error : Stayed on same location")
    else:
        raise Exception("find_direction input error : Difference of both location is not between -1 and 1.")


def find_neighbors(maze_map, player_location: tuple) -> list:
    """
    Find the neighbors of a given location
    Variables :
        player_location : tuple[int,int]
        maze_map : dict[tuple[int,int], dict[tuple[int,int], int]]

    Returns list[tuple[int, int]]
    """
    return list(maze_map[player_location].keys())


def find_route(routing_table, source_location, target_location):
    """ Use the routing table to find the sequence of locations from source to target
    Variables : 
        routing_table: dict{tuple(int,int): tuple(int,int)}
        source_location: tuple[int, int]
        target_location: tuple[int, int]

    Returns list[tuple(int, int)]
    """
    path = [target_location]
    current_location = target_location
    while current_location != source_location:
        current_location = routing_table[current_location]
        path = [current_location] + path
    return path


def moves_from_locations(locations):
    """Transform a series of locations into corresponding moves to realize it
    Variables: 
        list[tuple(int, int)] 
    Returns void"""
    global moves
    for i in range(len(locations) - 1):
        moves.append(find_direction(locations[i], locations[i + 1]))


def meta_graph_route_to_route(meta_graph_path, routing_tables):
    """
    Transform a path in the meta graph into a path in the maze graph
    Variables:
        meta_graph_path: list(tuple(int,int))
        routing_tables: dict{tuple(int, int), dict{tuple(int,int): tuple(int,int)}}
    Returns:
        route: list(tuple(int,int))
    """
    route = []
    for i in range(len(meta_graph_path) - 1, 0, -1):
        path = find_route(routing_tables[meta_graph_path[i - 1]], meta_graph_path[i - 1], meta_graph_path[i])  # We find the path between each cheese piece
        route = path[1:] + route  # We add it to our route and we remove in the process the first term to prevent it being doubled
    return [meta_graph_path[0]] + route  # We return our route without forgetting to add the starting location in our route, that was removed by the line above


# ? Path Finding


def dijkstra(start_vertex: tuple, graph, target=None):
    """
    Dijkstra Algo
    Variables :
        start_vertex : tuple(int,int),
        graph : dict{tuple(int,int) : dict{tuple(int,int) : int}}

    Returns : 
        routing_table : dict{tuple(int,int): tuple(int,int)},
        distance_table : dict{tuple(int,int): int}
    """
    # Creating structure
    distance_table = {}
    distances_q = []  # the heap
    routing_table = {}
    has_been_explored = {vertex: False for vertex in graph}
    # Initialize with start_vertex
    hq.heappush(distances_q, (0, start_vertex, None))

    # Iterate while some vertices remains in the min heap
    while len(distances_q) != 0:

        # This will return the next vertex to be examined.
        (length, current_vertex, current_parent) = hq.heappop(distances_q)

        if not has_been_explored[current_vertex]:  # We check that this vertex was not already examined
            has_been_explored[current_vertex] = True
            distance_table[current_vertex] = length
            routing_table[current_vertex] = current_parent
            if current_vertex == target:
                return routing_table, distance_table

            neighbors = find_neighbors(graph, current_vertex)
            # Going over the distance with each neighbor
            for neighbor in neighbors:
                if not has_been_explored[neighbor]:
                    new_full_length = length + graph[current_vertex][neighbor]  # get the length from the start passing by the current vertex
                    hq.heappush(distances_q, (new_full_length, neighbor, current_vertex))  # Pushing the neighbor to the heap for further investigation
    return routing_table, distance_table


# ? Structures


def build_meta_graph(maze_map, cheese_list, starting_location):
    """
    Will build the cheese complete graph using dijkstra
    Variables :
        maze_map: dict{tuple(int, int), dict{tuple(int, int), int}}
        cheese_list: list(pair(int, int))
        starting_location: tuple(int, int)
    Returns :
        meta_graph: dict{tuple(int, int), dict{tuple(int, int): int}}
        meta_routing_table: dict{tuple(int, int), dict{tuple(int,int): tuple(int,int)}}
    """
    meta_routing_table = {}
    meta_graph = {}
    locations = [starting_location] + cheese_list
    for i in range(len(locations)):
        location = locations[i]
        meta_graph[location] = dict()
        routing_table, distance_table = dijkstra(location, maze_map)
        meta_routing_table[location] = routing_table
        for j in range(len(locations)):
            if j != i:
                meta_graph[location][locations[j]] = distance_table[locations[j]]
    return meta_graph, meta_routing_table


def tsp(meta_graph, initial_vertex):
    """
    We take a graph with a set of vertices we want to go through and we look for the best path to go through all of them.
    Return only one best path
    Variables :
        meta_graph: dict{tuple(int, int), dict{tuple(int, int), int}}
        initial_vertex: tuple(int, int)
    Returns : The list of coordinates we must go through
        list(tuple(int,int))
    """

    best_length = -1  # We keep track of our best length to backtrack. -1 is the default value that will be modified
    best_path = []  # We keep track of our best path

    def _tsp(current_vertex, current_length=0, path=[initial_vertex]):
        nonlocal best_length
        nonlocal best_path
        if len(path) == len(meta_graph):  # Recursion ending condition
            if best_length == -1 or best_length > current_length:  # If our length value was not initialized or we found a better value
                best_length = current_length
                best_path = path
            return

        else:  # Continuing recursion
            for neighbor in find_neighbors(meta_graph, current_vertex):
                if neighbor not in path:  # We make sure we don't go through the same vertex twice
                    new_length = current_length + meta_graph[current_vertex][neighbor]
                    if (best_length != -1 and best_length > new_length) or best_length == -1:  # If our length value was initialized and the current value is lower or the length value was not initialized
                        _tsp(neighbor, new_length, path + [neighbor])

    _tsp(initial_vertex)  # Launching the recursion

    return best_path


def give_score(graph, current_vertex, neighbors):
    """
    Associates a score with eache neighbor of the current vertex. The lower the score the better.
    Variables :
        graph : dict{tuple(int, int), dict{tuple(int, int), int}}
        current_vertex : tuple(int, int)
        neighbors : list[tuple(int,int)]
    Outputs : list[tuple(int, tuple(int, int), routing_table)], an heapq containing neighbors associated with their score
    """
    scored_neighbors = []
    for i in range(len(neighbors)):  # We cycle through our neighbors
        neighbor = neighbors[i]
        routing_table, distance_table = dijkstra(current_vertex, graph, neighbor)
        hq.heappush(scored_neighbors, (distance_table[neighbor], neighbor, routing_table))  # For each vertex, we associate to it the distance found
    return scored_neighbors


def greedy(graph, initial_vertex, vertices_to_visit):
    """
    Give the closest vertice to visit and the path to go to it
    Variables :
        graph : dict{tuple(int, int), dict{tuple(int, int), int}}
        initial_vertex : tuple(int, int)
        vertices_to_visit : list[tuple(int, int)]
    Outputs :
        list[tuple(int, int)] : Path to follow to next closest cheese
    """
    current_vertex = initial_vertex
    scores = give_score(graph, current_vertex, vertices_to_visit)
    distance, greedy_choice, routing_table = hq.heappop(scores)
    return find_route(routing_table, current_vertex, greedy_choice)


##############################################################
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.t
# ------------------------------------------------------------
# maze_map : dict(pair(int, int), dict(pair(int, int), int))
# maze_width : int
# maze_height : int
# player_location : pair(int, int)
# opponent_location : pair(int,int)
# pieces_of_cheese : list(pair(int, int))
# time_allowed : float
##############################################################


def preprocessing(maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed):
    result_best = greedy(maze_map, player_location, pieces_of_cheese)
    moves_from_locations(result_best)
    return


##############################################################
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
# ------------------------------------------------------------
# maze_map : dict(pair(int, int), dict(pair(int, int), int))
# maze_width : int
# maze_height : int
# player_location : pair(int, int)
# opponent_location : pair(int,int)
# player_score : float
# opponent_score : float
# pieces_of_cheese : list(pair(int, int))
# time_allowed : float
##############################################################

def turn(maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed):

    global moves
    global index
    if len(moves) == index:
        index = 0
        moves = []
        result_best = greedy(maze_map, player_location, pieces_of_cheese)
        moves_from_locations(result_best)

    future_move = moves[index]
    index += 1
    return future_move
