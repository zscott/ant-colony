
import pygame
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import ant

class Home:
    def __init__(self, ants, width, height, ants_per_second = 10, max_ants = 200):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.radius = 10
        self.ants_per_second = ants_per_second
        self.max_ants = max_ants
        self.ants = ants
        self.width = width
        self.height = height
        self.timestamp_milliseconds = pygame.time.get_ticks()

    def update(self, world):
        if len(self.ants) > self.max_ants:
            return

        current_milliseconds = pygame.time.get_ticks()
        ant_generation_count = (current_milliseconds - self.timestamp_milliseconds) / 1000 * self.ants_per_second
        if ant_generation_count >= 1:
            for i in range(int(ant_generation_count)):
                if len(self.ants) < self.max_ants:
                    direction = random.uniform(0, 2*math.pi)
                    self.ants.append(ant.Ant(self.x, self.y, direction, 'foraging', world))
            self.timestamp_milliseconds = current_milliseconds

    def draw(self, screen):
        pygame.draw.circle(screen, (165, 42, 42), (self.x, self.y), self.radius)

    def contains(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.radius
