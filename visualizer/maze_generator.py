import random
import os
import gui_runner

# *** Maze Generator ***
# Import this file to generate a random maze.

def generate_random_maze(maze_obj):
    # 1. Start everything as a WALL
    for cell in maze_obj.cells:
        cell.state = gui_runner.States.WALL

    stack = []
    start_cell = maze_obj.cells[0]
    start_cell.state = gui_runner.States.START
    stack.append(start_cell)

    while stack:
        current = stack[-1]
        neighbors = get_unvisited_walls(current, maze_obj)

        if neighbors:
            next_cell = random.choice(neighbors)
            # Pass the cell list and width specifically
            remove_wall(current, next_cell, maze_obj.cells, maze_obj.maze_size_x)
            
            next_cell.state = gui_runner.States.UNDISCOVERED_PATH
            stack.append(next_cell)
        else:
            stack.pop()

    # Final touch: ensure start and end are correct
    maze_obj.cells[0].state = gui_runner.States.START
    maze_obj.cells[-1].state = gui_runner.States.END

def get_unvisited_walls(cell, maze_obj):
    neighbors = []
    x, y = cell.x_coord, cell.y_coord
    # Jump by 2 to leave a wall in between
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze_obj.maze_size_x and 0 <= ny < maze_obj.maze_size_y:
            target = maze_obj.cells[ny * maze_obj.maze_size_x + nx]
            # ONLY return it if it's still a WALL (unvisited)
            if target.state == gui_runner.States.WALL:
                neighbors.append(target)
    return neighbors

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
    # Standardize x/y to find the midpoint
    wall_x = (current.x_coord + next_cell.x_coord) // 2
    wall_y = (current.y_coord + next_cell.y_coord) // 2
    
    wall_idx = wall_y * maze_size_x + wall_x
    grid[wall_idx].state = gui_runner.States.UNDISCOVERED_PATH

def apply_maze_data_to_obj(maze_obj, maze_data):
    # maze_data is the 2D list from your load_maze_from_file
    for y, row in enumerate(maze_data):
        for x, char in enumerate(row):
            target_cell = maze_obj.cells[y * maze_obj.maze_size_x + x]
            if char == '#': 
                target_cell.state = gui_runner.States.WALL
            elif char == 'S': 
                target_cell.state = gui_runner.States.START
            elif char == 'E': 
                target_cell.state = gui_runner.States.END
            else:
                target_cell.state = gui_runner.States.UNDISCOVERED_PATH

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

