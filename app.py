import pygame
import math
from queue import deque, PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Simulator")

colors = {
    'closed'    : '#FF0000',    # red
    'open'      : '#00FF00',    # green
    'blue'      : '#0000FF',    # blue
    'yellow'    : '#FFFF00',    # yellow
    'blank'     : '#363e4d',    # white
    'barrier'   : '#000000',    # black
    'path'      : '#800080',    # path
    'start'     : '#FF8000',    # orange
    'grey'      : '#808080',    # grey
    'goal'      : '#40E0D0'     # turquoise
}

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = self.row * width
        self.y = self.col * width
        self.color = colors['blank']
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def get_color(self):
        return self.color
    
    def set_color(self, color):
        self.color = color
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def find_neighbors(self, grid):
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

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    

def reconstruct_path(prev_map, current, start, draw):
    while current in prev_map:
        current = prev_map[current]
        if current is start:
            return True
        current.color = colors['path']
        draw()

def depth_first(draw, grid, start, goal):
    stack = [start]
    prev_map = {}
    
    while len(stack) > 0:
        # safety net to exit the loop if need be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # get current node
        current = stack.pop()
        if current is not start and current is not goal:
            current.color = colors['open']

        # we've reached goal state
        if current == goal:
            reconstruct_path(prev_map, current, start, draw)
            goal.color = colors['goal']
            return True
        
        for neighbor in current.neighbors:
            if neighbor.color != colors['open'] and neighbor.color != colors['closed']:
                prev_map[neighbor] = current
                stack.append(neighbor)
        
        draw()

        if current != start and current != goal:
            current.color = colors['closed']
    
    return False

def breadth_first(draw, grid, start, goal):
    queue = [start]
    queue_hash = {start}
    prev_map = {}
    i = 0

    def get_heuristic(node):
        return euclidean_dist(node.get_pos(), goal.get_pos())
    
    while len(queue) > 0:
        # safety net to exit the loop if need be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # get current node
        current = queue.pop(0)
        if current is not start and current is not goal:
            current.color = colors['open']

        # we've reached goal state
        if current == goal:
            reconstruct_path(prev_map, current, start, draw)
            goal.color = colors['goal']
            return True

        current.neighbors.sort(key=get_heuristic)
        for neighbor in current.neighbors:
            if neighbor not in queue_hash:
                prev_map[neighbor] = current
                queue.append(neighbor)
                queue_hash.add(neighbor)
                if neighbor is not start and current is not goal:
                    neighbor.color = colors['open']
        draw()

        if current != start and current != goal:
            current.color = colors['closed']
    return False

def best_first(draw, grid, start, goal):
    stack = [start]
    prev_map = {}
    
    def get_heuristic(node):
        return euclidean_dist(node.get_pos(), goal.get_pos())
    
    while len(stack) > 0:
        # safety net to exit the loop if need be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # get current node
        current = stack.pop()
        if current is not start and current is not goal:
            current.color = colors['open']

        # we've reached goal state
        if current == goal:
            reconstruct_path(prev_map, current, start, draw)
            return True

        current.neighbors.sort(reverse=True, key=get_heuristic)
        for neighbor in current.neighbors:
            if neighbor.color != colors['open'] and neighbor.color != colors['closed']:
                prev_map[neighbor] = current
                stack.append(neighbor)
        
        draw()

        if current != start and current != goal:
            current.color = colors['closed']
    
    return False



def run_algo(draw, grid, start, goal):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    # hashmap to keep track of the node's previous node
    previous_map = {}
    # g score set
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # f score set
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = euclidean_dist(start.get_pos(), goal.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        # safety net to exit the loop if need be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2] # get the node with the lowest f score
        open_set_hash.remove(current)

        # if we've reached the goal
        if current == goal:
            reconstruct_path(previous_map, current, start, draw)
            goal.color = colors['goal']
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                previous_map[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + euclidean_dist(neighbor.get_pos(), goal.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = colors['open']
        
        draw()

        if current != start and current != goal:
            current.color = colors['closed']
    
    return None


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i, j, gap, rows))
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, colors['grey'], (0, i * gap), (width, i*gap))
    for j in range(rows):
        pygame.draw.line(win, colors['grey'], (j * gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(colors['blank'])

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)

    pygame.display.update()

def get_clicked_node(pos, rows, width):
    gap = width // rows
    x, y = pos
    return x // gap, y // gap

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    goal = None

    run = True
    started = False

    algos = [run_algo, best_first, depth_first, breadth_first]
    cur_algo = 0

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue
            
            if pygame.mouse.get_pressed()[0]: # left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != goal:
                    start = node
                    node.color = colors['start']
                elif not goal and node != start:
                    goal = node
                    node.color = colors['goal']
                elif node != goal and node != start:
                    node.color = colors['barrier']
                
            elif pygame.mouse.get_pressed()[2]: # right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, ROWS, width)
                node = grid[row][col]
                node.color = colors['blank']
                if start == node:
                    start = None
                elif goal == node:
                    goal = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started and start and goal: # Start button pressed
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

                elif event.key == pygame.K_r and not started: # reset key pressed
                    start = None
                    goal = None
                    for row in grid:
                        for node in row:
                            node.color = colors['blank']
                
                elif event.key == pygame.K_c and not started: # clear key pressed
                    for row in grid:
                        for node in row:
                            if node is not start and node is not goal and node.color is not colors['barrier']:
                                node.color = colors['blank']
                
                elif event.key == pygame.K_LCTRL:
                    cur_algo += 1
                    if cur_algo >= len(algos):
                        cur_algo = 0
            

    pygame.quit()

main(WIN, WIDTH)