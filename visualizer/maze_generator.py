import random
import time
from collections import deque

# *** Maze Generator ***
# Import this file to generate a random maze.

class Maze:
    '''
    Maze class for creating Maze objects
    that contain maze information for retrieval.
    
    Maze data contains:
        'S' which represents the start position,
        'E' which represents the end position,
        '#' which represents a wall,
        '.' which represents a path
    
    Maze data is stored in a three tuple format:
    (point_type, x_coord, y_coord)
        point_type: 'S' | 'E' | '#' | '.'
        x_coord: Integer; 1 <= x <= max_size
        y_coord: Integer; 1 <= x <= max_size

    Maze data also contains a path array,
    which stores the valid path in the generated maze.
    '''



def generate_random_maze(size_x, size_y):
    '''
    Generates a random maze of size_x * size_y.
    Maze sizes are kept above a certain size to allow sufficient
    space for the path.

    :param size_x: The x length of the maze; 7 <= x <= 300
    :param size_y: The y length of the maze; 7 <= x <= 300
    :returns: A maze object containing generated maze
            data and maze size; Returns None if x or y
            length is invalid
    '''
    min_size = 7
    max_size = 300

    if size_x > max_size or size_y > max_size: return None

    if size_x <= min_size or size_y <= min_size: return None

    """
    Maze Generation Algorithm

    Generate a border around the maze
    Declare two random points as the start and end of the maze
    While the two random points are invalid:
        Pick two random points
        If the two points are not on the same point and not directly adjacent to each other:
            End the loop
    
    While a valid path does not exist:
        Generate a random path
        If the path has >= 5% and < 30% coverage of the space:
            End the loop
    
    Store valid path

    While the amount of generated walls is not valid:
        Generate walls around the generated path
        If the amount of walls have <= 40% of path coverage:
            End the loop

    Generate random access paths that connect to only the start or end
    based on the size of the maze space

    Fill in remaining space with walls and return Maze object
    """
    max_maze_x = size_x - 1
    max_maze_y = size_y - 1
    # Border generation

def generate_path(size_x, size_y, start_pos, end_pos):
    '''
    Description: Generates a random path given a start and end
    position, along with the size of the maze.

    :param size_x: The size of the x maze direction;
    :param size_y: The size of the y maze direction;
    :param start_pos: The start position of the maze in 2-tuple format
    :param end_pos: The end position of the maze in 2-tuple format
    :returns path_arr: An array of 2-tuples that contains the path data
    '''

    """
    Path Generation Algorithm

    Start from the start position
    While current point is not equal to the end position
        Choose a random adjacent point that is in the same row or column but not both
        
        If the chosen point is adjacent to more than 1 point:
            End the current iteration
        Otherwise:
            Set the current position to the chosen point 
    """
    """
    A path CANNOT have 4+ path cells directly adjacent to each other.

    W = Wall
    C = Current
    N = Next
    O = Not Allowed

    Yes Example         No Example      Yes Example

    W N O               C C             C C C C
    W C N               C C                 C
    W N O

    Cell Position Map
    [x - 1, y + 1][x + 0, y + 1][x + 1, y + 1]
    [x - 1, y + 0][x + 0, y + 0][x + 1, y + 0]
    [x - 1, y - 1][x + 0, y - 1][x + 1, y - 1]

    Current Position = (x, y)
    Adjacent Possible Positions:
        Corner Blocked
            - (Left-Top):       (x + 1, y), (x, y - 1)
            - (Left-Bottom):    (x, y + 1), (x + 1, y)
            - (Right-Top):      (x - 1, y), (x, y - 1)
            - (Right-Bottom):   (x - 1, y), (x, y + 1)
        Single Blocked
            - (Left):           (x, y), (x + 1, y), (x, y - 1)
            - (Right):          (x, y), (x - 1, y), (x, y - 1)
            - (Top):            (x - 1, y), (x + 1, y), (x, y - 1)
            - (Bottom):         (x, y + 1), (x - 1, y), (x + 1, y)
    Adjacent Not Possible Positions
        Corner Blocked
            - (Left-Top):       (x - 1, y), (x, y + 1)
            - (Left-Bottom):    (x - 1, y), (x, y - 1)
            - (Right-Top):      (x, y + 1), (x + 1, y)
            - (Right-Bottom):   (x + 1, y), (x, y - 1)
        Single Blocked
            - (Left):           (x - 1, y)
            - (Right):          (x + 1, y)
            - (Top):            (x, y + 1)
            - (Bottom):         (x, y - 1)
    """
    path_arr = [] # Store path data in an array of 2-tuples
    current_pos = start_pos # Intialize current position to start (x, y)
    path_arr.append(current_pos) # Include the start position into the path
    next_positions = []

    while current_pos != end_pos:   
        # Get Adjacent Cells
        left = (current_pos[0] - 1, current_pos[1])
        right = (current_pos[0] + 1, current_pos[1])
        top = (current_pos[0], current_pos[1] + 1)
        bottom = (current_pos[0], current_pos[1] - 1)

        print("Current Posit:\t" + str(current_pos))
        print("Adjacent Left:\t" + str(left))
        print("Adjacent Righ:\t" + str(right))
        print("Adjacent Top:\t" + str(top))
        print("Adjacent Bott:\t" + str(bottom))

        # Check each cell if it already exists in the path array
        # Also check if the path is single wall adjacent
        if left not in path_arr or left[0] > 1: next_positions.append(left)

        if right not in path_arr or right[0] < size_x: next_positions.append(right)

        if top not in path_arr or top[1] < size_y: next_positions.append(top)

        if bottom not in path_arr or bottom[1] > 1: next_positions.append(bottom)

        # Check for single adjacent positions
        # Look ahead by one position in order to check for directly adjacent possible positions
        new_next = []
        for next_pos in next_positions:
            next_left = (next_pos[0] - 1, next_pos[1])
            next_right = (next_pos[0] + 1, next_pos[1])
            next_top = (next_pos[0], next_pos[1] + 1)
            next_bot = (next_pos[0], next_pos[1] - 1)

            if next_left or next_right or next_top or next_bot not in path_arr:
                new_next.append(next_pos)

        # Randomly pick between the remaining next positions
        current_pos = random.choice(new_next)
        path_arr.append(current_pos)
        print("New Position:\t" + str(current_pos))
        print()

        # Clear next positions for the next iteration
        next_positions.clear()
    
    return path_arr

if __name__ == '__main__':
    arr = generate_path(7, 7, (1, 3), (4, 5))

    for coord in arr: print(coord)


    

































