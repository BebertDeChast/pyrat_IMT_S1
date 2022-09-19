##############################################################
# The turn function should always return a move to indicate where to go
# The four possibilities are defined here
##############################################################

import queue as q
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

def create_structure() -> q.Queue:
    # Create an empty FIFO
    return q.Queue()


def push_to_structure(structure: q.Queue, element: any) -> None:
    # Add an element to the FIFO
    structure.put(element)


def pop_from_structure(structure: q.Queue) -> any:
    # Extract an element from the FIFO
    return structure.get()


def neighbors(maze_map, player_location: tuple) -> list:
    """
    Find the neighbors of a given location
    Variables :
        player_location : tuple[int,int]
        maze_map : dict[tuple[int,int], dict[tuple[int,int], int]]

    Returns list[tuple[int, int]]
    """
    return list(maze_map[player_location].keys())


def traversal(start_vertex: tuple, graph):
    """
    BFS traversal
    Variables :
        start_vertex : tuple(int,int)
        graph : dict{tuple(int,int) : dict{tuple(int,int) : int}}

    Returns list[tuple(int,int)], dict{tuple(int,int): tuple(int,int)}
    """
    # First we create either a LIFO or a FIFO
    queuing_structure = create_structure()
    # Add the starting vertex with None as parent
    push_to_structure(queuing_structure, (start_vertex, None))
    # Initialize the outputs
    explored_vertices = []
    routing_table = {}
    # Iterate while some vertices remain
    while queuing_structure.qsize() > 0:

        # This will return the next vertex to be examined, and the choice of queuing structure will change the resulting order
        (current_vertex, parent) = pop_from_structure(queuing_structure)

        # Tests whether the current vertex is in the list of explored vertices
        if current_vertex not in explored_vertices:
            # Mark the current_vertex as explored
            explored_vertices.append(current_vertex)

            # Update the routing table accordingly
            routing_table[current_vertex] = parent

            # Examine neighbors of the current vertex
            for neighbor in neighbors(graph, current_vertex):
                # We push all unexplored neighbors to the queue
                if neighbor not in explored_vertices:
                    push_to_structure(queuing_structure, (neighbor, current_vertex))

    return explored_vertices, routing_table


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
        path.append(current_location)
    return path[::-1]


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
    explored, routing_table=traversal(player_location, maze_map)
    path = find_route(routing_table,player_location,pieces_of_cheese[0])
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
