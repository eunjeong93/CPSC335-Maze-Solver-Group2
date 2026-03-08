import random

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

    :param size_x: The x length of the maze; x <= 300
    :param size_y: The y length of the maze; x <= 300
    :returns: A maze object containing generated maze
            data and maze size; Returns None if x or y
            length is invalid
    '''
    max_size = 300

    if size_x > max_size or size_y > max_size: return None

    if size_x <= 0 or size_y <= 0: return None

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
        If the path has >= 5% coverage of the space:
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
            It is recommended to generate the border and then
            reduce the maze size by 2
    :param size_y: The size of the y maze direction;
            It is recommended to generate the border and then
            reduce the maze size by 2
    :param start_pos: The start position of the maze in 2-tuple format
    :param end_pos: The end position of the maze in 2-tuple format
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
    current_pos = start_pos
    next_x_pos = 0
    next_y_pos = 0
    while current_pos != end_pos:
        # Check if the current_pos is next to a left or right wall
        if current_pos[0] == 0: next_x_pos = current_pos[0] + 1
        elif current_pos[0] == size_x: next_x_pos = current_pos[0] - 1
        else:
            next_x_pos = random.choice(current_pos[0] + 1, current_pos[0] - 1)

        # Check if the current_pos is next to a top or bottom wall
        if current_pos[1] == 0: next_y_pos = current_pos[1] + 1
        elif current_pos[1] == size_y: next_y_pos = current_pos[1] - 1
        else:
            next_y_pos = random.choice(current_pos[1] + 1, current_pos[1] - 1)


    

































