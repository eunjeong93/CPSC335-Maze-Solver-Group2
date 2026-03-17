import csv
from datetime import datetime
import os
import time
# *** Maze Timer Module ***

import time

class MazeTimer:
    def __init__(self):
        self.start_time = 0
        self.accumulated_time = 0
        self.is_running = False
        self.is_paused = False

    def start(self):
        self.start_time = time.perf_counter()
        self.accumulated_time = 0
        self.is_running = True
        self.is_paused = False

    def pause(self):
        if self.is_running and not self.is_paused:
            self.accumulated_time += time.perf_counter() - self.start_time
            self.is_paused = True

    def resume(self):
        if self.is_running and self.is_paused:
            self.start_time = time.perf_counter()
            self.is_paused = False

    def stop(self):
        if self.is_running:
            if not self.is_paused:
                self.accumulated_time += time.perf_counter() - self.start_time
            self.is_running = False
            self.is_paused = False
        return round(self.accumulated_time, 4)

    def save_run_data(self, algo_name, maze_size, time_taken, status="Completed"):
        file_path = "maze_results.txt"
        file_exists = os.path.isfile(file_path)
        header = ["Timestamp", "Algorithm", "Size", "Time(s)", "Status"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, algo_name, f"{maze_size[0]}x{maze_size[1]}", time_taken, status]

        with open(file_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(row)
    
def save_run_data(algo_name, maze_size, time_taken, status="Completed"):
    '''
    Saves run results to 'maze_results.txt' in a CSV format.
    '''
    file_path = "maze_results.txt"
    file_exists = os.path.isfile(file_path)
    
    # Headers for the file
    header = ["Timestamp", "Algorithm", "Size", "Time(s)", "Status"]
    
    # Data row
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, algo_name, f"{maze_size[0]}x{maze_size[1]}", time_taken, status]

    try:
        with open(file_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            # Write header only if file is new
            if not file_exists:
                writer.writerow(header)
            writer.writerow(row)
        print(f"Data saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving data: {e}")

