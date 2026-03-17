import random
import time
import os
import gui_runner

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
    '''
    def __init__(self, maze_size_x, maze_size_y):
        self.maze_size_x = maze_size_x
        self.maze_size_y = maze_size_y

        self.maze_cells = []

    def add_cell(self, cell):
        self.maze_cells.append(cell)

def generate_random_maze(maze_obj):
    '''
    Implementation of Recursive Backtracker for maze generation.
    '''
    # 1. Start by setting every cell to a WALL
    for cell in maze_obj.cells:
        cell.state = gui_runner.States.WALL

    stack = []
    start_cell = maze_obj.cells[0]
    start_cell.state = gui_runner.States.START
    stack.append(start_cell)

    while stack:
        current = stack[-1]
        neighbors = get_unvisited_neighbors(current, maze_obj.cells, 
                                            maze_obj.maze_size_x, maze_obj.maze_size_y)

        if neighbors:
            next_cell = random.choice(neighbors)
            
            # Remove the wall between current and next
            remove_wall(current, next_cell, maze_obj.cells, maze_obj.maze_size_x)
            
            # Move to next cell
            next_cell.state = gui_runner.States.UNDISCOVERED_PATH
            stack.append(next_cell)
        else:
            stack.pop()

    # Set the bottom-right cell as the END
    maze_obj.cells[-1].state = gui_runner.States.END

def get_unvisited_neighbors(cell, grid, maze_size_x, maze_size_y):
    '''
    Returns a list of neighbors that are currently UNDISCOVERED_PATH.
    '''
    neighbors = []
    x, y = cell.x_coord, cell.y_coord

    # Directions: Up, Down, Left, Right (jumping 2 units to leave walls in between)
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze_size_x and 0 <= ny < maze_size_y:
            # Find the cell object in your flat list based on coordinates
            target_cell = grid[ny * maze_size_x + nx]
            if target_cell.state == gui_runner.States.UNDISCOVERED_PATH:
                neighbors.append(target_cell)
    
    return neighbors

def remove_wall(current, next_cell, grid, maze_size_x):
    '''
    Changes the state of the cell between 'current' and 'next_cell' to a path.
    '''
    wall_x = (current.x_coord + next_cell.x_coord) // 2
    wall_y = (current.y_coord + next_cell.y_coord) // 2
    
    wall_cell = grid[wall_y * maze_size_x + wall_x]
    wall_cell.state = gui_runner.States.UNDISCOVERED_PATH # Or a specific PATH state

def load_maze_from_file(file_name):
    '''
    Description: Loads an existing maze from a file and parses it into 
    a format compatible with the Maze class.
    '''
    # Add extension if missing and handle paths safely
    if not file_name.endswith(".txt"):
        file_name += ".txt"
    
    # Use os.path.join for cross-platform compatibility
    path = os.path.join("src", file_name)
    maze_data = []

    try:
        with open(path, "r") as file:
            for line in file:
                maze_data.append(list(line.strip()))
    except Exception as e:
        print(f"Error loading maze: {e}")
        return None

    return maze_data

