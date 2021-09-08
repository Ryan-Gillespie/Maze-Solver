import pygame
import math
from queue import deque, PriorityQueue
from Pathfinder import *
from maze import Maze;

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Simulator")

colors = {
    'closed'    : '#FF0000',    # red
    'open'      : '#00FF00',    # green
    'blue'      : '#0000FF',    # blue
    'yellow'    : '#FFFF00',    # yellow
    'blank'     : '#363e4d',    # nice looking dark color
    'barrier'   : '#000000',    # black
    'path'      : '#800080',    # path
    'start'     : '#FF8000',    # orange
    'grey'      : '#808080',    # grey
    'goal'      : '#40E0D0'     # turquoise
}

class Node:
    """ 
    Node object used to represent a cell in the grid for pathfinding purposes 
    
    row and col are the indicies of the node.
    x and y are the screen-based coordinates of the node.
    color is used to indicate what type of cell this is (wall, travelled, etc.).
    width is the width of the cell.
    """
    def __init__(self, row, col, width, total_rows):
        """ Initializes a new Node """
        self.row = row
        self.col = col
        self.x = self.row * width
        self.y = self.col * width
        self.color = colors['blank']
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        """ Gets the row and col of a node in the form ( row, col ) """
        return self.row, self.col

    def get_color(self):
        """ Gets the color of the current node """
        return self.color
    
    def set_color(self, color):
        """ Sets the color of the current node """
        self.color = color
    
    def draw(self, win):
        """ draws the current node. """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def find_neighbors(self, grid):
        """ Gets all adjacent neighbors to the current cell. Used as a successor function
        
        Will do nothing if current node is a barrier node. 
        Will not append a neighbor if that neighbor is a barrier. """
        self.neighbors = []
        # if we're a barrier node
        if self.color == colors['barrier']:
            return
        # down case
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].get_color() == colors['barrier']:
            self.neighbors.append(grid[self.row + 1][self.col])
        # right case
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].get_color() == colors['barrier']:
            self.neighbors.append(grid[self.row][self.col + 1])
        # up case
        if self.row > 0 and not grid[self.row - 1][self.col].get_color() == colors['barrier']:
            self.neighbors.append(grid[self.row - 1][self.col])
        # right case
        if self.col > 0 and not grid[self.row][self.col - 1].get_color() == colors['barrier']:
            self.neighbors.append(grid[self.row][self.col - 1])

def make_grid(rows, width):
    """ Initializes the grid """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i, j, gap, rows))
    
    return grid

def draw_grid(win, rows, width):
    """ Draws the lines seperating the cells """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, colors['grey'], (0, i * gap), (width, i*gap))
    for j in range(rows + 1):
        pygame.draw.line(win, colors['grey'], (j * gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    """ Draws the grid and all cells to the screen """
    win.fill(colors['blank'])

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)

    pygame.display.update()

def get_clicked_node(pos, rows, width):
    """ Converts screen coordinates to indicies of the grid """
    gap = width // rows
    x, y = pos
    return x // gap, y // gap

def main(win, width):
    """ Main loop of the application """
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    goal = None

    run = True
    started = False

    algos = [a_star, best_first, depth_first, breadth_first]
    cur_algo = 0

    # main loop - draw the grid and then run every pygame event
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue
            
            # left click
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, ROWS, width)
                if col >= ROWS or row >= ROWS:
                    continue
                node = grid[row][col]
                if not start and node != goal:
                    start = node
                    node.color = colors['start']
                elif not goal and node != start:
                    goal = node
                    node.color = colors['goal']
                elif node != goal and node != start:
                    node.color = colors['barrier']
                
            # right click
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, ROWS, width)
                node = grid[row][col]
                node.color = colors['blank']
                if start == node:
                    start = None
                elif goal == node:
                    goal = None
            
            if event.type == pygame.KEYDOWN:
                # Start button pressed
                if event.key == pygame.K_SPACE and not started and start and goal: 
                    # clear previous runs
                    started = True
                    for row in grid:
                        for node in row:
                            if node is not start and node is not goal and node.color is not colors['barrier']:
                                node.color = colors['blank']
                    
                    # update the neighbors of each node
                    for row in grid:
                        for node in row:
                            node.find_neighbors(grid)
                    # run the search
                    algos[cur_algo](lambda: draw(win, grid, ROWS, width), grid, start, goal)
                    started = False

                # reset key pressed
                elif event.key == pygame.K_r and not started: 
                    start = None
                    goal = None
                    for row in grid:
                        for node in row:
                            node.color = colors['blank']
                
                # clear key pressed
                elif event.key == pygame.K_c and not started: 
                    for row in grid:
                        for node in row:
                            if node is not start and node is not goal and node.color is not colors['barrier']:
                                node.color = colors['blank']
                
                # left key pressed, cycle algorithm right
                elif event.key == pygame.K_RIGHT: 
                    cur_algo += 1
                    if cur_algo >= len(algos):
                        cur_algo = 0
                
                # right key pressed, cycle algorithm left
                elif event.key == pygame.K_LEFT: 
                    cur_algo -= 1
                    if cur_algo <= 0:
                        cur_algo = len(algos) - 1
                
                # enter key pressed, generate maze
                elif event.key == pygame.K_RETURN:
                    maze = Maze(ROWS, ROWS)
                    for i in range(len(grid)):
                        for j in range(len(grid[i])):
                            if maze.maze[i][j] == 'w':
                                grid[i][j].set_color(colors['barrier'])
                            else:
                                grid[i][j].set_color(colors['blank'])
                    start = grid[maze.entrance[0]][maze.entrance[1]]
                    goal = grid[maze.exit[0]][maze.exit[1]]
                    start.set_color(colors['start'])
                    goal.set_color(colors['goal'])
            
    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)