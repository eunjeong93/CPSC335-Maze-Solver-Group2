import pygame
import maze_generator

# *** Gui Runner Module ***
MAZE_SCALING_FACTOR = 0.4
WINDOW_SIZE = (1200, 700)
MAZE_WINDOW_SIZE = (WINDOW_SIZE[0] * MAZE_SCALING_FACTOR, WINDOW_SIZE[1] * MAZE_SCALING_FACTOR)
time_scale = 1 # Default set at 1, range 0.5 <= a <= 5 for 1/2 speed to 3x speed
pygame.init()

class Button:
    def __init__(self, rect, label, toggle=False):
        self.rect   = pygame.Rect(rect)
        self.label  = label
        self.toggle = toggle
        self.active = False
        self.font = pygame.font.SysFont('Arial', 40)

    def draw(self, surface, font, text):
        try:
            hover = self.rect.collidepoint(pygame.mouse.get_pos())
            if self.active and self.toggle:
                color = pygame.Color(255, 0, 0) # Red
            elif hover:
                color = pygame.Color(153, 204, 255) # Lighter Blue
            else:
                color = pygame.Color(0, 128, 255) # Light Blue
            pygame.draw.rect(surface, color, self.rect, border_radius=6)
            pygame.draw.rect(surface, (80, 80, 120), self.rect, 1, border_radius=6)
            txt = font.render(text, True, (255, 255, 255))
            surface.blit(txt, txt.get_rect(text))
        except Exception as e:
            print(f"[Button.draw] Error rendering button '{self.label}': {e}")

    def is_clicked(self, event):
        try:
            return (event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and self.rect.collidepoint(event.pos))
        except Exception as e:
            print(f"[Button.is_clicked] Error: {e}")
            return False

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
        but = load_buttons()
        but.draw(screen, "Times New Roman", "TEST")
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
        - SPEED +
            - Sets the speed of the simulation from 0.5X to 5X

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
    button_length = 200
    button_width = 100

    test_button = Button(pygame.Rect(20, 20, button_length, button_width), "test button", False)

    return test_button

def generate_button(button_name, button_text):
    '''
    Description: Generates a button given a button name and text.

    :param button_name: The name of the button object
    :param button_text: The text that is displayed inside the button
    :returns: A Button object
    '''


def test_func():
    print("Hello World!")

def maze_setup(maze_size_x, maze_size_y):
    '''
    Description: Sets up a maze of size x and y in the visualizer
    window.

    :param maze_size_x: The length of the x direction of the maze
    :param maze_size_y: The length of the y direction of the maze
    '''
    

def maze_scale(maze):
    '''
    Description: Scales a maze object data to the maze window within the
    main gui.

    :param maze: Maze object of the Maze class in the maze_generator.py file
    '''

if __name__ == '__main__':
    # arr = maze_generator.generate_path(100, 100, (10, 21), (70, 90))

    # for coord in arr: print(coord)
    gui_setup()