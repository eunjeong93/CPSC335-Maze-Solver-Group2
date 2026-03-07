import random

# *** Maze Generator ***
# Import this file to generate a random maze.
# Mazes can be seeded to create a more deterministic
#   generated maze.

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
            data and maze size
    '''
    max_size = 300

    if size_x > max_size or size_y > max_size: return None

    if size_x <= 0 or size_y <= 0: return None

    """
    Maze Generation Algorithm

    Declare two random points as the start and end of the maze
    While the two random points are invalid:
        Pick two random points
        If the two points are not at the same point and both are on a wall:
            Exit the loop
    
    While a valid path does not exist:
        Generate a random path
        If the path has >= 5% coverage of the space:
            End the loop

    Generate walls around the generated path

    Generate random access paths that connect to only the start or end
    based on the size of the maze space

    Fill in remaining space with walls and return Maze object
    """
    maze_size_option_x = [0, size_x - 1]
    maze_size_option_y = [0, size_y - 1]
    start = (0, 0)
    end = (0, 0)

    while start[0] == end[0] or start[1] == end[1]:
        start = (random.choice(maze_size_option_x), random.choice(maze_size_option_y))
        end = (random.choice(maze_size_option_x), random.choice(maze_size_option_y))
        '''
        0, 299              299, 299


        0, 0                299, 0
        '''

































