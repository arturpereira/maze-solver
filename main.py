from graphics import Window
from maze import Maze
import sys

def main():
    num_rows = 6
    num_cols = 8
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)
    sys.setrecursionlimit(10000)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 42)
    is_solvable = maze.solve()
    if not is_solvable:
        print("Maze can not be solved!")
    else:
        print("Maze solved!")
    
    win.wait_for_close()
    
if __name__ == "__main__":
    main()