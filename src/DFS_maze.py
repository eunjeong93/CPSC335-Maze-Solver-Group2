import os 
import numpy as np
from collections import deque
import time
import sys 

# how to run: python DFS_maze.py <maze_file_path>

def dfs(maze, start, end):
    """
    Args:
        maze (array): Input maze as a 2D array
        start (tuple): Starting position (row, col)
        end (tuple): Ending position (row, col)

    Returns:
        tuple: A tuple containing (result, path, path_length, final_visited, runtime, total_visited)
        path : fianl path from S to E
        path_length : length of the final path from S to E
        final_visited : 2D array marking the cells that are part of the final path (For visualization)
        runtime : time taken to execute the DFS algorithm
        total_visited : 2D array marking all the cells that were visited during the DFS
    """
    start_time = time.perf_counter()
    rows = len(maze)
    cols = len(maze[0])

    path = []
    parent = {}
    visited = [[False] * cols for _ in range(rows)]
    final_visited = [[False] * cols for _ in range(rows)]
    stack = deque([start])

    visited[start[0]][start[1]] = True
    final_visited[start[0]][start[1]] = True
    while stack:
        r, c = stack.pop()

        if (r, c) == end:
            node = end
            while node != start:
                path.append(node)
                final_visited[node[0]][node[1]] = True
                node = parent[node]
            path.append(start)
            path.reverse()
            end_time = time.perf_counter()
            runtime = end_time - start_time
            return True, path, len(path)-1, final_visited, runtime, visited

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#' and not visited[nr][nc]:
                visited[nr][nc] = True
                parent[(nr, nc)] = (r, c)
                stack.append((nr, nc))
    runtime = time.perf_counter() - start_time
    return False, [], 0, [], runtime, visited

if __name__ == "__main__":
    file_path = sys.argv[1]
    with open(file_path, "r") as file:
        lines = file.readlines()
    maze = np.array([list(line.strip()) for line in lines])
    
    # find S and E position
    start = None
    end = None 
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    # apply DFS algorithm 
    result, path, path_length, final_visited, runtime, total_visited = dfs(maze, start, end)
    visited_count = sum(sum(row) for row in total_visited)
    print("Algorithm: DFS")
    print(f"Shortest Path length: {path_length}")
    print(f"Total Visited Nodes: {visited_count}")
    # print(f"Final Path from S to E: {path}")
    print(f"Runtime: {runtime:.6f} seconds")