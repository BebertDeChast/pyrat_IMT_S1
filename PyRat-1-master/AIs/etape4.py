##############################################################
# The turn function should always return a move to indicate where to go
# The four possibilities are defined here
##############################################################

import heapq as hq
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'


##############################################################
# Please put your code here (imports, variables, functions...)
##############################################################

moves = []
index = 0


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


def add_or_replace(value, name, min_heap, distance_table):
    """
    Performs an add or replace operation on a min heap of the format (value, name). 
    Variables :
        value : int, The value you want to add or replace
        name : String, The name associated to the value
        min_heap : heapq.list, the min_heap
    Outputs an int if it added or replaced, -1 if it did nothing.
    """
    for i in range(len(min_heap)):
        # Cycling in the min heap to find the name and the old value associated with it
        if min_heap[i][1] == name:
            old_value = min_heap[i][0]
            if old_value > value:  # Replacing old value if new value is lower
                min_heap[i] = (value, name)  # ! May need a min_heap.sort() but we don't know yet
                return value

    if old_value == -1:  # In case the name was not found, we push the new name and new value into the heap
        hq.heappush(min_heap, (value, name))
        return value
    return -1


def dijkstra(start_vertex: tuple, graph):
    """
    BFS traversal
    Variables :
        start_vertex : tuple(int,int)
        graph : dict{tuple(int,int) : dict{tuple(int,int) : int}}

    Returns list[tuple(int,int)], dict{tuple(int,int): tuple(int,int)}
    """
    # Creating structure
    distance_table = {v: -1 for v in list(graph.keys())}
    distances_q = []
    explored_vertices = []
    routing_table = {}

    # Initialize with start_vertex
    hq.heappush(distances_q, (0, start_vertex))
    distance_table[start_vertex] = 0
    routing_table = {start_vertex: None}

    # Iterate while some vertices remains in the min heap
    while len(distances_q):

        # This will return the next vertex to be examined.
        (length, current_vertex) = hq.heappop(distances_q)

        if current_vertex not in explored_vertices:  # We check that this vertex was not already examined
            explored_vertices.append(current_vertex)

            neighbors = find_neighbors(graph, current_vertex)
            # Going over the distance with each neighbor
            for neighbor in neighbors:
                if neighbor not in explored_vertices:
                    new_full_length = length + graph[current_vertex][neighbor]  # get the length from the start passing by the current vertex

                    # Now we perform the add & replace with this length value
                    if distance_table[neighbor] == -1 or distance_table[neighbor] > new_full_length:  # We check if no value was added yet or if the new value is better
                        distance_table[neighbor] = new_full_length
                        routing_table[neighbor] = current_vertex
                        hq.heappush(distances_q, (new_full_length, neighbor))  # Pushing the neighbor to the heap for further investigation
    return routing_table


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

    # Example prints that appear in the shell only at the beginning of the game
    # Remove them when you write your own program
    routing_table = dijkstra(player_location, maze_map)
    path = find_route(routing_table, player_location, pieces_of_cheese[0])
    moves_from_locations(path)


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
    # We go up at every turn
    # You should replace this with more intelligent decisions
    global index
    future_move = moves[index]
    index += 1
    return future_move
