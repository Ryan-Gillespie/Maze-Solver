# Imports
import random

from PriorityQueue import PriorityQueue, Queue, Stack
from wrappers import timer
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

from colorama import init
from colorama import Fore, Back, Style


# globals - will probably move to driver program
wall_color = (0,0,0)
cell_color = (255,255,255)
visiting_color = (50,255,50)
visited_color = (255,0,0)

# Contains the actual maze, the means to generate it, and the means to solve it
class Maze:
    def __init__(self, height, width):
        # initialize variables
        self.height = height
        self.width = width
        self.maze = []

        # generate the maze
        self.generate_maze()

    @timer
    def generate_maze(self):
        # Denote all cells as unvisited
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append('u')
            self.maze.append(line)

        # Randomize starting point and set it a cell
        starting_height = int(random.random() * self.height)
        starting_width = int(random.random() * self.width)
        if starting_height == 0:
            starting_height += 1
        if starting_height == self.height - 1:
            starting_height -= 1
        if starting_width == 0:
            starting_width += 1
        if starting_width == self.width - 1:
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = 'c'
        walls = [[starting_height - 1, starting_width], [starting_height, starting_width - 1],
                 [starting_height, starting_width + 1], [starting_height + 1, starting_width]]

        # Denote walls in maze
        self.maze[starting_height - 1][starting_width] = 'w'
        self.maze[starting_height][starting_width - 1] = 'w'
        self.maze[starting_height][starting_width + 1] = 'w'
        self.maze[starting_height + 1][starting_width] = 'w'

        while walls:
            # Pick a random wall
            rand_wall = walls[int(random.random() * len(walls)) - 1]

            # Check if it is a left wall
            if rand_wall[1] != 0:
                if self.maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and self.maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if self.maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Bottom cell
                        if rand_wall[0] != self.height - 1:
                            if self.maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if self.maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if rand_wall[0] != 0:
                if self.maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and self.maze[rand_wall[0] + 1][rand_wall[1]] == 'c':

                    s_cells = self.surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if self.maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if self.maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                        # Rightmost cell
                        if rand_wall[1] != self.width - 1:
                            if self.maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if rand_wall[0] != self.height - 1:
                if self.maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and self.maze[rand_wall[0] - 1][rand_wall[1]] == 'c':

                    s_cells = self.surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        if rand_wall[0] != self.height - 1:
                            if self.maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[1] != 0:
                            if self.maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])
                        if rand_wall[1] != self.width - 1:
                            if self.maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the right wall
            if rand_wall[1] != self.width - 1:
                if self.maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and self.maze[rand_wall[0]][rand_wall[1] - 1] == 'c':

                    s_cells = self.surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        if rand_wall[1] != self.width - 1:
                            if self.maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])
                        if rand_wall[0] != self.height - 1:
                            if self.maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[0] != 0:
                            if self.maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                    walls.remove(wall)

        # Mark the remaining unvisited cells as walls
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == 'u':
                    self.maze[i][j] = 'w'

        # Set entrance
        for i in range(0, self.width):
            if self.maze[1][i] == 'c':
                self.maze[0][i] = 'c'
                self.entrance = [0, i]
                break

        # set exit
        for i in range(self.width - 1, 0, -1):
            if self.maze[self.height - 2][i] == 'c':
                self.maze[self.height - 1][i] = 'c'
                self.exit = [self.height - 1, i]
                break

    # Find number of surrounding cells
    def surroundingCells(self, rand_wall):
        s_cells = 0
        if self.maze[rand_wall[0] - 1][rand_wall[1]] == 'c':
            s_cells += 1
        if self.maze[rand_wall[0] + 1][rand_wall[1]] == 'c':
            s_cells += 1
        if self.maze[rand_wall[0]][rand_wall[1] - 1] == 'c':
            s_cells += 1
        if self.maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
            s_cells += 1

        return s_cells

    # Save the maze as an image for viewing
    def output_image(self, filename):
        image_array = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                if self.maze[i][j] == 'w':
                    line.append(wall_color)
                elif self.maze[i][j] == 'c':
                    line.append(cell_color)
                elif self.maze[i][j] == 'v':
                    line.append(visiting_color)
                elif self.maze[i][j] == 'd':
                    line.append(visited_color)
            image_array.append(line)

        plt.imshow(np.array(image_array))
        plt.savefig(filename)

    # goal distance estimator (just euclidean distance formula)
    def h(self, curr):
        return sqrt((self.exit[0] - curr[0])**2 + (self.exit[1] - curr[1])**2)

    # get all successor states
    def succ(self, cur):
        succs = []
        if self.maze[cur[0]][cur[1] + 1] == 'c': # right
            succs.append([cur[0], cur[1] + 1])
        if self.maze[cur[0]][cur[1] - 1] == 'c': # left
            succs.append([cur[0], cur[1] - 1])
        if self.maze[cur[0] + 1][cur[1]] == 'c': # up
            succs.append([cur[0] + 1, cur[1]])
        if self.maze[cur[0] - 1][cur[1]] == 'c': # down
            succs.append([cur[0] - 1, cur[1]])
        return succs

    @timer
    def a_star(self):
        # create the PriorityQueue and the closed list and start A*
        open = PriorityQueue()
        closed = PriorityQueue()

        # put the start node in pq
        open.enqueue({'state': self.entrance,
                      'parent': None,
                      'h': self.h(self.entrance),
                      'g': 0,
                      'f': 0})

        # start the A* loop
        while len(open.queue) > 0:
            # pop the first element and add it to closed if it is not visited or it has a lower f than the old one
            s = open.pop()
            closed.enqueue(s)

            # mark current square visited
            self.maze[s['state'][0]][s['state'][1]] = 'v'

            # check if current state is goal state
            if self.h(s['state']) == 0:
                path = []
                st = s

                # reconstruct the path to the current state
                while st is not None:
                    # mark current square as part of the final path
                    self.maze[st['state'][0]][st['state'][1]] = 'd'

                    # traverse up the path
                    path.append(st['state'])
                    st = st['parent']

                # report the results
                # maybe return the length instead as the path is already marked?
                print('Max Queue Length: ' + str(open.max_len))
                return path[::-1]

            # finally add all the succs to the priority queue if they're not on open or closed
            for state in self.succ(s['state']):
                # if new state is not already on open or closed add it to open
                if closed.contains(state):
                    continue

                # calculate heruistics and add it to the open queue
                new_h = self.h(state)
                g = s['g'] + 1
                open.enqueue({'state': state, 'parent': s, 'h': new_h, 'g': g, 'f': new_h + g})

        # if there is no solution, return None
        return None

    @timer
    def breadth_first(self):
        # start with a queue and visited list
        queue = Queue()
        queue.enqueue([self.entrance, None])
        visited = [self.entrance]

        # main loop
        while len(queue) > 0:
            # get the current state
            s = queue.dequeue()

            # mark current square visited
            self.maze[s[0][0]][s[0][1]] = 'v'

            # check to see if we're at the goal
            if self.h(s[0]) == 0:
                path = []
                st = s

                # reconstruct the path to the current state
                while st is not None:
                    # mark current square part of the path
                    self.maze[st[0][0]][st[0][1]] = 'd'
                    # traverse up the path
                    path.append(st[0])
                    st = st[1]

                # report the results
                print('Max Queue Length: ' + str(queue.maxlen))
                return path[::-1]

            # get all the successor states and add them to the queue if necessary
            adjacent = self.succ(s[0])
            for state in adjacent:
                if state not in visited:
                    queue.enqueue([state, s])
                    visited.append(state)

        # return none if the goal is not found
        return None

    @timer
    def depth_first(self):
        # start with a stack and visited list
        stack = Stack()
        stack.push([self.entrance, None])
        visited = [self.entrance]

        # main loop
        while len(stack) > 0:
            # get the current state
            s = stack.pop()

            # mark current square as visited
            self.maze[s[0][0]][s[0][1]] = 'v'

            # check to see if we're at the goal
            if self.h(s[0]) == 0:
                path = []
                st = s

                # reconstruct the path to the current state
                while st is not None:
                    # mark current square part of the path
                    self.maze[st[0][0]][st[0][1]] = 'd'
                    # traverse up the path
                    path.append(st[0])
                    st = st[1]

                # report the results
                print('Max Stack Length: ' + str(stack.maxlen))
                return path[::-1]

            # get all the successor states and add them to the stack if necessary
            adjacent = self.succ(s[0])
            for state in adjacent:
                if state not in visited:
                    stack.push([state, s])
                    visited.append(state)

        # return none if the goal is not found
        return None

    def solve(self, method):
        # reset the maze
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == 'v' or self.maze[i][j] == 'd':
                    self.maze[i][j] = 'c'

        # solve the maze based on the given method
        if method == 'astar':
            self.a_star()
        elif method == 'breadth':
            self.breadth_first()
        elif method == 'depth':
            self.depth_first()

    def __str__(self):
        # initialize colorama
        init()

        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == 'u':
                    print(Fore.WHITE + str(self.maze[i][j]), end=" ")
                elif self.maze[i][j] == 'c':
                    print(Fore.GREEN + str(self.maze[i][j]), end=" ")
                else:
                    print(Fore.RED + str(self.maze[i][j]), end=" ")

            print('\n')
        return ''


if __name__ == '__main__':
    print("Generating Maze")
    maze = Maze(200, 200)
    maze.output_image('maze.png')

    print('Solving Maze')
    print('AStar')
    maze.solve('astar')
    maze.output_image('maze_astar.png')

    print('Breadth First')
    maze.solve('breadth')
    maze.output_image('maze_breadth.png')

    print('Depth First')
    maze.solve('depth')
    maze.output_image('maze_depth.png')
