from typing import List
from cell import Cell
from graphics import Window
import time
import random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        
        if seed:
            random.seed(seed)
        
        self._create_cells()
        
        if self._cells:
            self._break_entrance_and_exit()
            self._break_walls_r(0,0)
            self._reset_cells_visited()
        
    def _create_cells(self):
        for i in range(self._num_cols):
            row = []
            for j in range(self._num_rows):
                row.append(Cell(self._win))
            self._cells.append(row)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i,j)
                
                
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        cell:Cell = self._cells[i][j]
        x1 = self._x1 + self._cell_size_x * i
        y1 = self._y1 + self._cell_size_y * j
        x2 = self._x1 + self._cell_size_x * (i + 1)
        y2 = self._y1 + self._cell_size_y * (j + 1)
        cell.draw(x1, y1, x2, y2)
        
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
        
    def _break_entrance_and_exit(self):
        if self._cells:
            entry = self._cells[0][0]
            entry.has_top_wall = False
            self._draw_cell(0, 0)
            
            exit = self._cells[self._num_cols - 1][self._num_rows - 1]
            exit.has_bottom_wall = False
            self._draw_cell(self._num_cols - 1, self._num_rows - 1)
    
    def _break_walls_r(self, i, j): # i is col, j is row
        self._cells[i][j].visited = True
        while True:
            possible_directions = []
            
            to_visit = []
            to_visit.append((i-1, j)) # left
            to_visit.append((i, j-1)) # up
            to_visit.append((i+1, j)) # right
            to_visit.append((i, j+1)) # down

            for col, row in to_visit:
                if (
                    col >= 0 
                    and row >= 0 
                    and col < self._num_cols 
                    and row < self._num_rows 
                    and self._cells[col][row].visited == False
                ):
                    possible_directions.append((col, row))
                    
            if len(possible_directions) == 0:
                self._draw_cell(i, j)
                return
            
            pick = possible_directions[random.randrange(len(possible_directions))]
            
            if pick[0] == i - 1:
                self._cells[i][j].has_left_wall = False
            elif pick[1] == j - 1:
                self._cells[i][j].has_top_wall = False
            elif pick[0] == i + 1:
                self._cells[i][j].has_right_wall = False
            else:
                self._cells[i][j].has_bottom_wall = False
                
            self._break_walls_r(pick[0], pick[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
    
    def solve(self):
        return self._solve_r(0, 0)
           
    def _solve_r(self, i, j):
        self._animate()
        current_cell:Cell = self._cells[i][j]
        current_cell.visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        directions = []
        directions.append((i-1, j)) # left
        directions.append((i, j-1)) # up
        directions.append((i+1, j)) # right
        directions.append((i, j+1)) # down
        
        for d in directions:
            col, row = d[0], d[1]
            if col in range(self._num_cols) and row in range(self._num_rows):
                target = self._cells[col][row]
                if (
                    (col == i - 1 and not current_cell.has_left_wall) 
                    or (row == j - 1 and not current_cell.has_top_wall)
                    or (col == i + 1 and not current_cell.has_right_wall)
                    or (row == j + 1 and not current_cell.has_bottom_wall)
                    and not target.visited
                ):  
                    current_cell.draw_move(target)
                    if self._solve_r(col, row):
                        return True
                    current_cell.draw_move(target, undo=True)
        return False