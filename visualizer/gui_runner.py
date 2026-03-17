import pygame
import sys
import maze_generator
import maze_timer
from enum import Enum
import math
import os

sys.path.insert(0, "src")

import BFS_maze
import DFS_maze

# *** Gui Runner Module ***

# Setup
pygame.init()
pygame.font.init()
MAZE_SCALING_FACTOR = 0.4
WINDOW_SIZE = (1200, 700)
MAZE_WINDOW_SIZE = (WINDOW_SIZE[0] * MAZE_SCALING_FACTOR, WINDOW_SIZE[1] * MAZE_SCALING_FACTOR)
screen = pygame.display.set_mode(WINDOW_SIZE)
text_font = pygame.font.Font("freesansbold.ttf", 20)
pygame.display.set_caption("Maze Solver")

# Enums defined for state identification
# Identification Class for Component ID
class Identification(Enum):
    # Buttons
    BFS = 0             # BFS
    DFS = 1             # DFS
    SPEED_INC = 2       # Speed Increment
    SPEED_DEC = 3       # Speed Decrement
    SET_X = 4           # Set X Maze Size ; Unused
    SET_Y = 5           # Set Y Maze Size ; Unused
    SET_X_INC = 6       # X Maze Size Increment
    SET_X_DEC = 7       # X Maze Size Decrement
    SET_Y_INC = 8       # Y Maze Size Increment
    SET_Y_DEC = 9       # Y Maze Size Decrement
    SOLVE = 10          # Solver
    PAUSE = 11          # Pause
    RESET = 12          # Reset
    SIDE_SPLIT = 13     # Place Mazes Side by Side
    SINGLE = 14         # Single Maze on Screen
    VIEW_DATA = 15      # View Data of Previous Runs
    EXPORT = 16         # Export Run Data to External File
    SAMPLE = 17         # Makes Sample Options Appear
    RANDOM = 18         # Randomly Generates a Maze

    # Text
    SPEED_TEXT = 19     # Speed Value
    MAZE_SIZE_X = 20    # Maze X Size
    MAZE_SIZE_Y = 21    # Maze Y Size
    MISCELLANEOUS = 22  # Any non-modified text

    # Mazes
    MAZE_LEFT = 23
    MAZE_RIGHT = 24

class States(Enum):
    START = 100                     # Start State (UNIQUE)              COLOR = BLUE
    END = 101                       # End State (UNIQUE)                COLOR = RED
    WALL = 102                      # Wall State                        COLOR = BLACK
    UNDISCOVERED_PATH = 103         # Undiscovered Path State           COLOR = WHITE
    DISCOVERED_PATH = 104           # Discovered Path State             COLOR = YELLOW
    FINAL_PATH = 105                # Final Path State                  COLOR = GREEN

# Button class for GUI
class Button:
    # Button text will default to white
    def __init__(self, x_position, y_position, width, height, text, color, hover_color, action, button_id):
        self.x_position = x_position
        self.y_position = y_position

        self.width = width
        self.height = height

        self.text = text

        self.color = color
        self.hover_color = hover_color

        self.action = action

        self.button_id = button_id

        self.text_offset_x = self.x_position + (self.width // 2) - text_font.size(self.text)[0] // 1.45 + 7
        self.text_offset_y = self.y_position + (self.height // 2) - text_font.size(self.text)[1] // 2

    def display(self):
        pygame.draw.rect(screen, self.color, (self.x_position, self.y_position, self.width, self.height), 0, 5)
        text = text_font.render(F"{self.text}", True, white)
        screen.blit(text, [self.text_offset_x, self.text_offset_y])

    def hover(self):
        color = self.hover_color
        pygame.draw.rect(screen, color, (self.x_position, self.y_position, self.width, self.height), 0, 5)
        text = text_font.render(F"{self.text}", True, white)
        screen.blit(text, [self.text_offset_x, self.text_offset_y])
    
    def command(self):
        color = red
        pygame.draw.rect(screen, color, (self.x_position, self.y_position, self.width, self.height), 0, 5)
        text = text_font.render(F"{self.text}", True, white)
        screen.blit(text, [self.text_offset_x, self.text_offset_y])
        self.action()

# Text Class to place text on GUI
class Text:
    def __init__(self, x_position, y_position, text, id):
        self.x_position = x_position
        self.y_position = y_position
        self.text = text
        self.id = id

    def display(self):
        text = text_font.render(F"{self.text}", True, black)
        screen.blit(text, [self.x_position, self.y_position])       

# Maze Class to place maze
class Maze:
    def __init__(self, x_position, y_position, maze_size_x, maze_size_y, maze_id):
        self.x_position = x_position
        self.y_position = y_position
        self.maze_size_x = maze_size_x
        self.maze_size_y = maze_size_y
        self.maze_id = maze_id
        
        # Pre-calculate cell dimensions
        self.cell_size_x = maximum_maze_window / self.maze_size_x
        self.cell_size_y = maximum_maze_window / self.maze_size_y
        
        # Persistent storage for Cell objects
        self.cells = []
        self.generate_empty_grid()
    
    def __len__(self):
        return len(self.cells)
    
    def __getitem__(self, index):
        return self.cells[index]

    def generate_empty_grid(self):
        self.cells = []
        for y in range(self.maze_size_y):
            for x in range(self.maze_size_x):
                # Calculate screen position once
                screen_x = self.x_position + (x * self.cell_size_x)
                screen_y = self.y_position + (y * self.cell_size_y)
                self.cells.append(Cell(x, y, States.UNDISCOVERED_PATH, screen_x, screen_y))
    
    def update_cells(self, index, state):
        if index >= len(self.cells): return

        self.cells[index].state = state

    def display(self):
        # Draw background/border
        pygame.draw.rect(screen, white, (self.x_position, self.y_position, maximum_maze_window, maximum_maze_window))
        pygame.draw.rect(screen, black, (self.x_position, self.y_position, maximum_maze_window, maximum_maze_window), 2)
        
        # Display the pre-calculated cells
        for cell in self.cells:
            cell.display(self.cell_size_x, self.cell_size_y)

class Cell:
    def __init__(self, x_coord, y_coord, state, screen_x, screen_y):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.state = state
        self.screen_x = screen_x
        self.screen_y = screen_y

    def display(self, w, h):
        color = white # Default
        if self.state == States.WALL: color = black
        elif self.state == States.START: color = blue
        elif self.state == States.END: color = red
        elif self.state == States.DISCOVERED_PATH: color = yellow
        elif self.state == States.FINAL_PATH: color = neon_green

        pygame.draw.rect(screen, color, (self.screen_x, self.screen_y, w, h))
        pygame.draw.rect(screen, black, (self.screen_x, self.screen_y, w, h), 1)

# Other Variables placed here to use the defined classes
# Colors
blue, white, gray = (0, 0, 255), (255, 255, 255), (128, 128, 128)
light_purple, black, red = (127, 0, 255), (0, 0, 0), (255, 0, 0)
light_gray, yellow, neon_green = (192, 192, 192), (255, 255, 0), (57, 255, 20)

# Variable Values
x_array_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y_array_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
time_scale_values = [0.5, 1, 2, 3]
 
# Intialize
x_maze_size = x_array_sizes[0] 
y_maze_size = y_array_sizes[0]
time_scale = 1
maximum_maze_window = 400
algo_current = Identification.BFS
algo_mode = Identification.SINGLE
maze_current = Maze(WINDOW_SIZE[0], WINDOW_SIZE[1], x_maze_size, y_maze_size, Identification.BFS)
maze_raw = 0
maze_mode = Identification.RANDOM
sample_maze_list = []
sample_current = "maze1"
active_solvers = []
show_data_overlay = False
results_text_objects = []
timer = maze_timer.MazeTimer()
is_paused = False
path_found = False
maze_x_offset = (WINDOW_SIZE[0] / 2) -  (maximum_maze_window / 2)
maze_y_offset = 70
maze_start = (0, 0)
maze_end = (0, 0)
needs_update = True
result = False
path = []
path_length = 0
final_visited = []
runtime = 0
total_visited = []


def gui_setup():
    '''
    Description: Runs the setup and the program.
    '''
    global needs_update, maze_current
    clock = pygame.time.Clock()
    running = True
    button_arr = load_buttons()
    text_arr = load_text_into_screen()
    
    var_text_arr = []
    maze_arr = []
    sample_buttons = load_sample_maze_buttons()

    while running:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        if needs_update:
            var_text_arr = load_variable_text_into_screen()
            maze_arr = maze_setup(x_maze_size, y_maze_size)
            if maze_mode == Identification.SAMPLE:
                sample_buttons = load_sample_maze_buttons()
            needs_update = False

        screen.fill(light_gray)

        for t in text_arr: t.display()
        for vt in var_text_arr: vt.display()
        for m in maze_arr: m.display()

        for b in button_arr:
            if b.x_position < mouse_pos[0] < b.x_position + b.width and b.y_position < mouse_pos[1] < b.y_position + b.height:
                b.hover()
                if clicked:
                    b.command()
                    needs_update = True
            else:
                b.display()

        for sample in sample_buttons:
            if sample.x_position < mouse_pos[0] < sample.x_position + sample.width and sample.y_position < mouse_pos[1] < sample.y_position + sample.height:
                sample.hover()
                if clicked:
                    sample.command()
                    needs_update = True
            else:
                sample.display()

        if needs_update:
            var_text_arr = load_variable_text_into_screen()
            maze_arr.pop()
            maze_arr.append(maze_current)
            needs_update = False

        # Draw Results Overlay if active
        if show_data_overlay:
            # Draw a background box for readability
            pygame.draw.rect(screen, white, (820, 240, 350, 350))
            pygame.draw.rect(screen, blue, (820, 240, 350, 350), 2)
            for text_obj in results_text_objects:
                text_obj.display()

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

def load_buttons():
    '''
    Description: Loads all gui buttons in an active display.
    '''
    button_width = 130
    button_height = 60

    med_button_width = 130
    med_button_height = 40

    small_button_width = 40
    small_button_height = 40

    bfs_but = Button(30, WINDOW_SIZE[1] - 170, button_width, button_height, "BFS", blue, light_purple, bfs_button, Identification.BFS)
    dfs_but = Button(30, WINDOW_SIZE[1] - 100, button_width, button_height, "DFS", blue, light_purple, dfs_button, Identification.DFS)

    # speed_inc = Button(300, WINDOW_SIZE[1] - 100, small_button_width, small_button_height, "+ ", blue, light_purple, speed_inc_button, Identification.SPEED_INC)
    # speed_dec = Button(200, WINDOW_SIZE[1] - 100, small_button_width, small_button_height, "- ", blue, light_purple, speed_dec_button, Identification.SPEED_DEC)

    # set_x = Button(370, WINDOW_SIZE[1] - 170, button_width, button_height, " SET X", blue, light_purple, set_x_size_button, Identification.SET_X)
    # set_y = Button(370, WINDOW_SIZE[1] - 100, button_width, button_height, " SET Y", blue, light_purple, set_y_size_button, Identification.SET_Y)

    # set_x_inc = Button(570, WINDOW_SIZE[1] - 160, small_button_width, small_button_height, "+ ", blue, light_purple, set_x_inc_button, Identification.SET_X_INC)
    # set_x_dec = Button(480, WINDOW_SIZE[1] - 160, small_button_width, small_button_height, "- ", blue, light_purple, set_x_dec_button, Identification.SET_X_DEC)

    # set_y_inc = Button(570, WINDOW_SIZE[1] - 90, small_button_width, small_button_height, "+ ", blue, light_purple,set_y_inc_button, Identification.SET_Y_INC)
    # set_y_dec = Button(480, WINDOW_SIZE[1] - 90, small_button_width, small_button_height, "- ", blue, light_purple, set_y_dec_button, Identification.SET_Y_DEC)

    run_but = Button(660, WINDOW_SIZE[1] - 170, med_button_width, med_button_height, "SOLVE", blue, light_purple, solve_button, Identification.SOLVE)
    # pause = Button(660, WINDOW_SIZE[1] - 120, med_button_width, med_button_height, "PAUSE", blue, light_purple, pause_button, Identification.PAUSE)
    # reset = Button(660, WINDOW_SIZE[1] - 70, med_button_width, med_button_height, "RESET", blue, light_purple, reset_button, Identification.RESET)

    # side_split = Button(830, WINDOW_SIZE[1] - 170, button_width, button_height, "DUAL", blue, light_purple, side_split_button, Identification.SIDE_SPLIT)
    # single = Button(830, WINDOW_SIZE[1] - 100, button_width, button_height, "   SINGLE", blue, light_purple, single_screen_button, Identification.SIDE_SPLIT)

    data_run = Button(1000, WINDOW_SIZE[1] - 170, button_width, button_height, "       VIEW RUNS", blue, light_purple, data_runs_button, Identification.VIEW_DATA)
    # exp_run = Button(1000, WINDOW_SIZE[1] - 100, button_width, button_height, "   EXPORT", blue, light_purple, export_data_button, Identification.EXPORT)

    # sample_maze = Button(30, 10, med_button_width, med_button_height, "     SAMPLE", blue, light_purple, load_sample_maze_buttons, Identification.SAMPLE)
    # gen_maze = Button(30, 60, med_button_width, med_button_height, "     RANDOM", blue, light_purple, generate_random_maze_button, Identification.RANDOM)

    button_arr = [bfs_but, dfs_but, run_but, data_run]

    return button_arr


def load_text_into_screen():
    '''
    Description: Loads all program text onto the screen.
    '''
    # set_x_text = Text(390, WINDOW_SIZE[1] - 150, "SET X", Identification.MISCELLANEOUS)
    # set_y_text = Text(390, WINDOW_SIZE[1] - 80, "SET Y", Identification.MISCELLANEOUS)
    algo_text = Text(30, WINDOW_SIZE[1] - 200, "ALGORITHM", Identification.MISCELLANEOUS)
    # speed_text = Text(235, WINDOW_SIZE[1] - 130, "SPEED", Identification.MISCELLANEOUS)
    # maze_size_text = Text(450, WINDOW_SIZE[1] - 200, "MAZE SIZE", Identification.MISCELLANEOUS)
    solver_text = Text(682, WINDOW_SIZE[1] - 200, "SOLVER", Identification.MISCELLANEOUS)
    # comparison_text = Text(825, WINDOW_SIZE[1] - 200, "COMPARISON", Identification.MISCELLANEOUS)
    data_manager_text = Text(1035, WINDOW_SIZE[1] - 200, "DATA", Identification.MISCELLANEOUS)

    text_arr = [algo_text, solver_text, data_manager_text]

    return text_arr

def load_variable_text_into_screen():
    '''
    Description: Loads the variable text into the screen.

    These include:
        - SPEED MULTIPLIER
        - MAZE SIZE X
        - MAZE SIZE Y
    '''
    # speed_mult = Text(255, WINDOW_SIZE[1] - 90, str(time_scale) + "X", Identification.SPEED_TEXT)
    # maze_size_x = Text(530, WINDOW_SIZE[1] - 150, str(x_maze_size - 1), Identification.MAZE_SIZE_X)
    # maze_size_y = Text(530, WINDOW_SIZE[1] - 80, str(y_maze_size - 1), Identification.MAZE_SIZE_Y)

    var_text_arr = []

    algo_left = "Breadth-First Search"
    algo_right = "Depth-First Search"

    algo_name = algo_left if (algo_current == Identification.BFS) else algo_right
    algo_id = Identification.MAZE_LEFT if (algo_current == Identification.BFS) else Identification.MAZE_RIGHT
    algo_single = Text((WINDOW_SIZE[0] / 2) - (maximum_maze_window / 4), 40, algo_name, algo_id)

    algo_dual_left = Text(300, 40, algo_left, Identification.MAZE_LEFT)
    algo_dual_right = Text(800, 40, algo_right, Identification.MAZE_RIGHT)

    if algo_mode == Identification.SINGLE:
        var_text_arr.append(algo_single)
    else:
        var_text_arr.append(algo_dual_left)
        var_text_arr.append(algo_dual_right)

    return var_text_arr
    
def maze_setup(maze_size_x, maze_size_y):
    '''
    Description: Sets up a maze of size x and y in the visualizer
    window.

    :param maze_size_x: The length of the x direction of the maze
    :param maze_size_y: The length of the y direction of the maze
    '''
    maze_id = Identification.BFS if (algo_current == Identification.BFS) else Identification.DFS
    maze_arr = []

    maze = Maze((WINDOW_SIZE[0] / 2) -  (maximum_maze_window / 2), 70, maze_size_x, maze_size_y, maze_id)
    maze_left = Maze(200, 70, maze_size_x, maze_size_y, Identification.MAZE_LEFT)
    maze_right = Maze(700, 70, maze_size_x, maze_size_y, Identification.MAZE_RIGHT)

    if algo_mode == Identification.SIDE_SPLIT:
        maze_arr.append(maze_left)
        maze_arr.append(maze_right)
    else:
        maze_arr.append(maze)

    return maze_arr

def maze_update_display(maze) -> Maze:
    '''
    Description: Updates an existing display in the window.
    '''
    return [maze]

def load_sample_maze_buttons():
    '''
    Description: Loads the buttons that allows the selection of built-in sample mazes.

    :param maze_arr: A list of maze file names
    '''
    global sample_maze_list
    file_path = "src"
    maze_names = []
    maze_processed = []

    for file in os.listdir(file_path):
        if file.endswith(".txt"):
            sample_maze_list.append(file)

    for maze in sample_maze_list:
        maze_names.append(os.path.splitext(maze)[0])
    
    for i in range(0, len(maze_names)):
        filename = sample_maze_list[i]
        print(maze_names[i])

        sample_maze_button = Button(
            30, 60 * (i + 2), 100, 40, 
            maze_names[i], blue, light_purple, 
            lambda f=filename: sample_button(f), 
            Identification.MISCELLANEOUS
        )
        maze_processed.append(sample_maze_button)

    return maze_processed

def load_results_for_display():
    '''
    Description: Reads the results file and returns a list of Text objects 
    to be rendered on the GUI.
    '''
    display_data = []
    file_path = "maze_results.txt"
    
    if not os.path.exists(file_path):
        return [Text(850, 250, "No data found.", Identification.MISCELLANEOUS)]

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            # Grab the header and the last 10 entries
            header = lines[0].strip().split(',')
            recent_runs = lines[-10:] 
            
            y_offset = 250
            # Display Header
            header_str = f"{header[1]:<10} | {header[2]:<8} | {header[3]:<8}"
            display_data.append(Text(830, y_offset, header_str, Identification.MISCELLANEOUS))
            
            # Display Rows
            for line in reversed(recent_runs): # Newest first
                if line == lines[0]: continue # Skip header if it's in the last 10
                cols = line.strip().split(',')
                y_offset += 30
                row_str = f"{cols[1]:<10} | {cols[2]:<8} | {cols[3]:<8}s"
                display_data.append(Text(830, y_offset, row_str, Identification.MISCELLANEOUS))
                
    except Exception as e:
        print(f"Error reading file: {e}")
        
    return display_data

def data_runs_button():
    global show_data_overlay, results_text_objects
    show_data_overlay = not show_data_overlay # Toggle
    if show_data_overlay:
        results_text_objects = load_results_for_display()

# Algorithms Selection
def bfs_button():
    global algo_current

    if algo_current == Identification.BFS: return

    algo_current = Identification.BFS

def dfs_button():
    global algo_current

    if algo_current == Identification.DFS: return

    algo_current = Identification.DFS

# Maze Size Selection
def set_x_inc_button():
    global x_maze_size

    if x_maze_size == x_array_sizes[len(x_array_sizes) - 1]: return

    x_maze_size = x_array_sizes[x_array_sizes.index(x_maze_size) + 1]

def set_x_dec_button():
    global x_maze_size

    if x_maze_size == x_array_sizes[0]: return

    x_maze_size = x_array_sizes[x_array_sizes.index(x_maze_size) - 1]

def set_y_inc_button():
    global y_maze_size

    if y_maze_size == y_array_sizes[len(y_array_sizes) - 1]: return

    y_maze_size = y_array_sizes[y_array_sizes.index(y_maze_size) + 1]

def set_y_dec_button():
    global y_maze_size

    if y_maze_size == y_array_sizes[0]: return

    y_maze_size = y_array_sizes[y_array_sizes.index(y_maze_size) - 1]

# Maze Solver
def solve_button():
    global maze_current, x_maze_size, y_maze_size, needs_update
    global maze_x_offset, maze_y_offset, maze_raw
    global result, path, path_length, final_visited, runtime

    start, end = (0, 0), (0, 0)
    for i in range(len(maze_raw)):
        for j in range(len(maze_raw[i])):
            if maze_raw[i][j] == 'S': start = (j, i)
            if maze_raw[i][j] == 'E': end = (j, i)

    # Load data to searching algorithms
    if algo_current == Identification.BFS:
        result, path, path_length, final_visited, runtime, total_visited = BFS_maze.bfs(maze_raw, start, end)
    else:
        result, path, path_length, final_visited, runtime, total_visited = DFS_maze.dfs(maze_raw, start, end)

    # Place all settings into the GUI
    x_maze_size = len(maze_raw[0])
    y_maze_size = len(maze_raw)

    num_discovered = 0
    num_undiscovered = 0
    
    cell_arr = []

    print("Result of Search: " + str(result))
    print("Path from S to E:" + str(path))
    print("Path Length: " + str(path_length))
    print("Final Visited: " + str(final_visited))
    print("Total Runtime: " + str(runtime) + " seconds.")
    print("Total Visited: " + str(len(total_visited)))


    # Map Result to Cell Values

    for i in range(len(maze_raw)):
        for j in range(len(maze_raw[i])):
            cell_state = States.UNDISCOVERED_PATH

            if maze_raw[i][j] == '#':
                cell_state = States.WALL
            elif maze_raw[i][j] == ".":
                if (i, j) in path:
                    cell_state = States.FINAL_PATH
                elif total_visited[i][j] == True:
                    cell_state = States.DISCOVERED_PATH
                    num_discovered += 1
                elif total_visited[i][j] == False:
                    cell_state = States.UNDISCOVERED_PATH
                    num_undiscovered += 1
            elif maze_raw[i][j] == "S":
                cell_state = States.START
            elif maze_raw[i][j] == "E":
                cell_state = States.END

            # print(str(cell_state) + " with value " + str(maze_raw[i][j]))
            cell_width_x = maximum_maze_window / len(maze_raw[0])
            cell_width_y = maximum_maze_window / len(maze_raw)

            cell_offset_x = maze_x_offset + j * cell_width_x
            cell_offset_y = maze_y_offset + i * cell_width_y

            cell_arr.append(Cell(j, i, cell_state, cell_offset_x, cell_offset_y))

    maze_id = Identification.BFS if algo_current == Identification.BFS else Identification.DFS

    maze_current = Maze(maze_x_offset, maze_y_offset, len(maze_raw[0]), len(maze_raw), maze_id)
    maze_current.cells = cell_arr
    needs_update = True

def pause_button():
    global is_paused
    if not is_paused:
        is_paused = True
        timer.pause()
    else:
        is_paused = False
        timer.resume()

def reset_button():
    global active_solvers, is_paused, maze_current
    
    # 1. Kill any active simulation
    active_solvers = []
    is_paused = False
    
    # 2. Reset the timer
    timer.stop()
    timer.accumulated_time = 0 
    
    # 3. Clean the maze colors
    soft_reset_maze(maze_current)
    
def soft_reset_maze(maze_obj):
    '''
    Clears the search progress (yellow/green) but keeps 
    the walls and start/end points intact.
    '''
    for cell in maze_obj.cells:
        # Check if the cell is part of a previous search
        if cell.state in [States.DISCOVERED_PATH, States.FINAL_PATH]:
            cell.state = States.UNDISCOVERED_PATH

def speed_inc_button():
    global time_scale

    if time_scale == time_scale_values[len(time_scale_values) - 1]: return

    time_scale = time_scale_values[time_scale_values.index(time_scale) + 1]

def speed_dec_button():
    global time_scale

    if time_scale == time_scale_values[0]: return

    time_scale = time_scale_values[time_scale_values.index(time_scale) - 1]

# Maze Window Management
def side_split_button():
    global algo_mode

    if algo_mode == Identification.SIDE_SPLIT: return

    algo_mode = Identification.SIDE_SPLIT

def single_screen_button():
    global algo_mode

    if algo_mode == Identification.SINGLE: return

    algo_mode = Identification.SINGLE

# Data Management
def load_sample_maze_button():
    global maze_mode
    global sample_maze_list

    if maze_mode == Identification.SAMPLE: return
    
    file_path = "src"

    for file in os.listdir(file_path):
        if file.endswith(".txt") and file not in sample_maze_list:
            sample_maze_list.append(file)

    maze_mode = Identification.SAMPLE

def generate_random_maze_button():
    global maze_current

    maze_current.generate_empty_grid() 

    maze_generator.generate_random_maze(maze_current)

def sample_button(filename):
    global maze_current, x_maze_size, y_maze_size, needs_update
    global maze_x_offset, maze_y_offset, maze_raw

    maze_mode = Identification.SAMPLE
    # If load_maze_from_file returns a 2D list (grid_data) 
    # instead of a Maze object, this will crash the solver.
    maze_raw = maze_generator.load_maze_from_file(filename)

    start, end = (0, 0), (0, 0)
    for i in range(len(maze_raw)):
        for j in range(len(maze_raw[i])):
            if maze_raw[i][j] == 'S': start = (j, i)
            if maze_raw[i][j] == 'E': end = (j, i)

    info_tuple = (0, 0, 0, 0, 0)

    # Load data to searching algorithms

    # Place all settings into the GUI
    x_maze_size = len(maze_raw[0])
    y_maze_size = len(maze_raw)
    
    cell_arr = []

    # Map Result to Cell Values

    for i in range(len(maze_raw)):
        for j in range(len(maze_raw[i])):
            cell_state = States.UNDISCOVERED_PATH

            if maze_raw[i][j] == '#':
                cell_state = States.WALL
            elif maze_raw[i][j] == ".":
                cell_state = States.UNDISCOVERED_PATH
            elif maze_raw[i][j] == "S":
                cell_state = States.START
            elif maze_raw[i][j] == "E":
                cell_state = States.END

            # print(str(cell_state) + " with value " + str(maze_raw[i][j]))
            cell_width_x = maximum_maze_window / len(maze_raw[0])
            cell_width_y = maximum_maze_window / len(maze_raw)

            cell_offset_x = maze_x_offset + j * cell_width_x
            cell_offset_y = maze_y_offset + i * cell_width_y

            cell_arr.append(Cell(j, i, cell_state, cell_offset_x, cell_offset_y))

    maze_id = Identification.BFS if algo_current == Identification.BFS else Identification.DFS
    maze_current = Maze(maze_x_offset, maze_y_offset, len(maze_raw[0]), len(maze_raw), maze_id)
    maze_current.cells = cell_arr
    needs_update = True

def data_runs_button():
    print("VIEW DATA")

def export_data_button():
    print("EXPORT")


if __name__ == '__main__':
    gui_setup()