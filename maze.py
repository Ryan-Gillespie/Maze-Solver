# Imports
import random
from wrappers import timer
from math import sqrt

class Maze:
    """ Class that contains the algorithm to generate a maze """

    def __init__(self, height, width):
        """ Constructor for Maze object. initializes width and height """
        self.height = height
        self.width = width

        self.maze = []
        self.entrance = None
        self.exit = None
        self.generate_maze()
    
    @timer
    def generate_maze(self):
        """ Generates a maze using randomized prim's algorithm """
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
    
    def surroundingCells(self, rand_wall):
        """ Utility function that gets the surrounding cells of a given random wall """
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
