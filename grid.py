
import pygame
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class Grid:
    def __init__(self, width, height, decay, color):
        self.width = width
        self.height = height
        self.decay = decay
        self.color = color
        self.grid = np.zeros((width, height))

    def values(self):
        return self.grid
    
    def get_value(self, x, y):
        if x < 0 or x >= self.width:
            return 0
        if y < 0 or y >= self.height:
            return 0
        return self.grid[int(x), int(y)]

    def get(self, x, y):
        return self.get_value(x, y)

    def draw(self, screen):
        surf = pygame.Surface((self.width, self.height))
        surf.fill(self.color)
        surf.set_alpha(255)
        surfarray = pygame.surfarray.pixels_alpha(surf)
        surfarray[:, :] = np.minimum(self.grid, 100) * 2.55
        del surfarray
        screen.blit(surf, (0, 0))

    def update(self):
        self.grid = self.grid * self.decay
        for i in range(self.width):
            for j in range(self.height):
                if self.grid[i, j] < 2:
                    self.grid[i, j] = 0

    def add(self, x, y, amount):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        x = int(x)
        y = int(y)
        self.grid[x, y] = self.grid[x, y] + amount
        if self.grid[x, y] > 100:
            self.grid[x, y] = 100
        if self.grid[x, y] < 0:
            self.grid[x, y] = 0
    