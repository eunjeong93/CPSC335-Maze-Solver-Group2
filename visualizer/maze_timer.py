import time

# *** Maze Timer ***
start_time_arr = []
end_time_arr = []

global_start_time = 0
global_end_time = 0

def time_maze_run(maze_state):
    '''
    Description: Times a maze run by initializing a global timer.
    When the maze is paused, this function can be called again
    to temporarily stop the timer. An incomplete run will be
    deleted. If this function is called without starting a run,
    the function call will automatically return without taking
    any action.

    :param maze_state: The current maze state;
                    First call maze_state = 1 to start the timer,
                    Then call maze_state = 0 to end the timer
    '''
    if maze_state == 1:
        if global_start_time != 0 and global_end_time == 0:
            start_time_arr.pop()
            return None
        # Repeat measurement for more precise measurement
        for i in range(3):
            global_start_time += time.perf_counter()
        
        global_start_time /= 3
        start_time_arr.append(global_start_time)
    elif maze_state == 0:
        if global_start_time == 0 and global_end_time == 0:
            return None
        for i in range(3):
            global_end_time += time.perf_counter()

        global_end_time /= 3
        end_time_arr.append(global_end_time)

        global_start_time, global_end_time = 0
