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
    def __init__(self, main_path):
        pass




def generate_random_maze(size_x, size_y):
    '''
    Generates a random maze of size_x * size_y.
    Maze sizes are kept above a certain size to allow sufficient
    space for the path.

    :param size_x: The x length of the maze; 7 <= x <= 300
    :param size_y: The y length of the maze; 7 <= x <= 300
    :returns: A Maze object containing generated maze
            data and maze size; Returns None if x or y
            length is invalid
    '''
    min_size = 7
    max_size = 100

    if size_x > max_size or size_y > max_size: return None

    if size_x <= min_size or size_y <= min_size: return None

    maximum_maze_area = size_x * size_y

    start_pos = 0
    end_pos = 0
    while start_pos == end_pos:
        start_pos = (random.randint(1, size_x - 1), random.randint(1, size_y - 1))
        end_pos = (random.randint(1, size_x - 1), random.randint(1, size_y - 1))

    main_path = []
    min_path_coverage = maximum_maze_area * 0.1
    max_path_coverage = maximum_maze_area * 0.25
    while len(main_path) < min_path_coverage or len(main_path) > max_path_coverage:
        main_path = generate_path(size_x, size_y, start_pos, end_pos)

    """
    Maze Generation Algorithm

    Generate a border around the maze
    Declare two random points as the start and end of the maze
    While the two random points are invalid:
        Pick two random points
        If the two points are not on the same point:
            End the loop
    
    While a valid path does not exist:
        Generate a random path
        If the path has >= 5% and < 25% coverage of the space (including start and end):
            End the loop
    
    Store valid path

    While total path coverage is < 70% of the entire space
        Generate random access paths that connect to only the start or end
        based on the size of the maze space

    Fill in remaining space with walls and return Maze object
    """
    print(main_path)
    max_maze_x = size_x - 1
    max_maze_y = size_y - 1
    # Border generation

    return main_path

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

        # Check each cell if it already exists in the path array
        # Additionally check for maze bounds
        if left not in path_arr and left[0] > 1: next_positions.append(left)

        if right not in path_arr and right[0] < size_x: next_positions.append(right)

        if top not in path_arr and top[1] < size_y: next_positions.append(top)

        if bottom not in path_arr and bottom[1] > 1: next_positions.append(bottom)

        if len(next_positions) == 0: break

        # Randomly pick between the remaining next positions
        current_pos = random.choice(next_positions)

        path_arr.append(current_pos)

        # Clear next positions for the next iteration
        next_positions.clear()
    
    return path_arr

def generate_single_access_path(size_x, size_y, main_path, *single_path):
    '''
    Description: Randomly picks either the start or end position and
    generates an access path that only connects to one of them. The main_path
    parameter's purpose is to prevent the generation from overlapping too much
    with the main generated path, so this function should be called after the
    main path has been generated.

    :param size_x: The x length of the maze
    :param size_y: The y length of the maze
    :param main_path: The main generated solution path of the maze
                    that connects the start and ending positions.
    :param *single_path: Any number of single paths can be passed as a parameter
                    to prevent overlapping of multiple single access paths.
    :returns: A single access path that connects to either the start or end position.
    '''

def generate_walls_and_borders(size_x, size_y, main_path, *single_path):
    '''
    Description: Generates the walls and border of the maze, where the border
    is 2 units larger than the provided x and y lengths. The walls will be filled
    into the remaining spaces that are non-path cells.

    :param size_x: The x length of the maze
    :param size_y: The y length of the maze
    :param main_path: The main generated solution path of the maze that
                    connects the start and ending positions.
    :param *single_path: Any number of single paths can be passed as a parameter
                    to help determine the remaining spaces in the maze.
    :returns: An array of 2-tuples containing the locations of each wall and the border.
    '''

def export_maze_data_to_text_file(maze):
    '''
    Description: Exports maze data into a text file. The text file will contain
    the translated version of the maze into its correct symbols for searching
    algorithm usage.

    :param maze: A Maze object containing complete maze data.
    :returns: A boolean True if the export was successful; False otherwise
    '''
if __name__ == '__main__':
    sizex = 100
    sizey = 100
    arr = generate_random_maze(sizex, sizey)
    path_coverage = (len(arr) / (sizex * sizey)) * 100

    start = arr[0]
    end = arr[len(arr) - 1]

    print("Main Path Coverage: " + str(path_coverage) + "%")
    for i in range(sizex):
        for j in range(sizey):
            if (i, j) == start:
                print("S", end=" ")
            elif (i, j) == end:
                print("E", end=" ")
            elif (i, j) in arr:
                print(".", end=" ")
            else:
                print("#", end=" ")
        print()


    

































