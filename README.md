# CPSC335-Maze-Solver-Group2

### Group Members and Roles
- Ariel Ahn — BFS Engineer
- Nicholas Karamanlis — DFS Engineer
- David Le — GUI / Visualization Engineer

### Project Description
This project is a Python GUI application that solves a maze using Breadth-First Search (BFS) and Depth-First Search (DFS). The program allows the user to load or generate a maze, choose an algorithm, and visualize the final path from the start cell (S) to the exit cell (E).

### Features
- Solve a maze using BFS
- Solve a maze using DFS
- Display the maze in a GUI
- Highlight the final path clearly
- Show algorithm used
- Show path length
- Show number of visited/explored cells
- Show runtime

### How to Run
1. Make sure Python 3 is installed.
2. Open the project folder in a terminal.
3. Run the GUI file with:
   python gui.py

### Notes
- BFS is implemented using a queue and is designed to find the shortest path in number of steps when a path exists.
- DFS is implemented to correctly find a path when one exists, though the path may not be the shortest.