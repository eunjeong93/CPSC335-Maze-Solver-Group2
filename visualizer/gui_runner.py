import pygame
import maze_generator

# *** Gui Runner Module ***
MAZE_SCALING_FACTOR = 0.4
WINDOW_SIZE = (1200, 700)
MAZE_WINDOW_SIZE = (WINDOW_SIZE[0] * MAZE_SCALING_FACTOR, WINDOW_SIZE[1] * MAZE_SCALING_FACTOR)

class Button:
    def __init__(self, x, y, length, width, text, color, hover_color, action):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.create()

    def create(self):
        pygame.Rect(self.x, self.y, self.length, self.width)
    
    def click_action():
        pass

def gui_setup():
    '''
    Description: Runs all functions for setup and begins the program.
    '''
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("white")
        # Place maze code between here
        load_buttons()

        # and here
        pygame.display.flip()
        clock.tick(60)

def load_buttons():
    '''
    Description: Loads all gui buttons in an active display.

    Buttons include:
        *** Maze Size Settings ***
        SET SIZE X [TEXT BOX] - Sets the x size of the maze
        SET SIZE Y [TEXT BOX] - Sets the y size of the maze

        *** Algorithm Setting ***
        BFS - Changes the current maze to use BFS in SINGLE mode
        DFS - Changes the current maze to use DFS in SINGLE mode
        -- Maze MUST be reset to change the algorithm
        -- These buttons are disabled in SPLIT mode

        *** Comparisons ***
        SIDE SPLIT - Changes the current maze window to both BFS and DFS for comparison
        SINGLE - Changes the current maze window to BFS by default.
        RANGE SET [TEXT BOX] [TEXT BOX]
            - Sets the minimum and maximum maze size for incremental maze
                size increases
        REP TIME [TEXT BOX]
            - Takes the range and repeats the maze solver for the amount of
                times set in the range set.
        
        *** Running ***
        RUN CONT
            - Runs the solver repeatedly for the amount of times set
                in the REP TIME text box.
        RUN DISC
            - Runs the solver repeatedly for the amount of times set
                in the REP TIME text box but stops at the end of every
                iteration until this button is pressed again.
            -- Once the max value is hit, then the maze and count is reset.
        PAUSE
            - Pauses the maze solver, regardless of the current maze state.
            -- Press RUN CONT or RUN DISC to resume.
        RESET
            - Resets the maze solver state.

        *** Data Access ***
        DATA
            - Press this button to access the DATA menu
            DATA RUNS
                - Lists the last 20 runs.
                -- Runs contains the Maze object and time to solve,
                    along with the algorithm used
                -- Running in SPLIT mode creates 2 runs
            EXP DATA
                - Exports the data to a specified directory
                - Mazes are exported as a .maze file
                    named with their run, maze size, and algorithm
                - Run, Maze Size, Algorithm, and Time are exported
                to a csv file
    '''
    but = Button(300, 200, 150, 70, "TEST", "green", "red", test_func)

def test_func():
    print("Hello World!")

def maze_setup(maze_size_x, maze_size_y):
    '''
    Description: Sets up a maze of size x and y in the visualizer
    window.

    :param maze_size_x: The length of the x direction of the maze
    :param maze_size_y: The length of the y direction of the maze
    '''
    new_maze = maze_generator.generate_random_maze(maze_size_x, maze_size_y)

def maze_scale(maze):
    '''
    Description: Scales a maze object data to the maze window within the
    main gui.

    :param maze: Maze object of the Maze class in the maze_generator.py file
    '''

if __name__ == '__main__':
    gui_setup()