##############################################################
# The turn function should always return a move to indicate where to go
# The four possibilities are defined here
##############################################################


import random as rd
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'


##############################################################
# Please put your code here (imports, variables, functions...)
##############################################################
visited_locations = []


def choose_random_neighbors(player_location, maze_map):
    neighbors = maze_map[player_location]  # Getting all neighbors
    choice = rd.choice(list(neighbors.keys()))  # Choosing a random neighbor
    return choice


def choose_unvisited_neighbors(player_location, maze_map):
    global visited_locations
    neighbors = list(maze_map[player_location].keys())  # Getting all neighbors
    unvisited_neighbors = []
    for i in range(0, len(neighbors)):
        if neighbors[i] not in visited_locations:
            unvisited_neighbors.append(neighbors[i])
    if len(unvisited_neighbors) == 0:
        return rd.choice(neighbors)
    else:
        return rd.choice(unvisited_neighbors)


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


##############################################################
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
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
    pass


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
    global visited_locations
    visited_locations.append(player_location)
    destination = choose_unvisited_neighbors(player_location, maze_map)
    return find_direction(player_location, destination)


maze_map = {(0, 0): {(1, 0): 1}, (0, 1): {(1, 1): 1}, (1, 0): {(1, 1): 6, (0, 0): 1}, (1, 1): {(1, 0): 6, (0, 1): 1}}

player_location = (0, 0)


# print(find_direction(player_location, choose_random_neighbors(player_location, maze_map)))
