import pygame
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import world

class Ant:
    def __init__(self, x, y, direction, mode, world):
        self.x = x
        self.y = y
        self.velocity = random.uniform(3.75, 4.75)
        self.direction = direction
        self.mode = mode
        self.mode_config = {
            "foraging": {
                "leaving": "foraging",
                "seeking": "returning"
            },
            "returning": {
                "leaving": "returning",
                "seeking": "foraging"
            }
        };
        self.max_turn_angle = math.pi / 4 
        self.world = world
        self.max_pheromones = 16000
        self.pheromones = self.max_pheromones
    
    def setMode(self, mode):
        self.mode = mode
        self.pheromones = self.max_pheromones

    def update(self):
        # if ant is foraging and finds food, change mode to returning
        if self.mode == 'foraging' and self.world.food_grid.get_value(self.x, self.y) > 0:
            self.setMode('returning')
            self.turn_around()
            self.world.food_grid.add(self.x, self.y, -150)
        
        # if ant is returning and is at home, change mode to foraging
        elif self.mode == 'returning' and self.world.home.contains(self.x, self.y):
            self.setMode('foraging') 
            self.turn_around()
            self.world.total_food_gathered += 150
        
        self.leave_pheromone()
        self.follow_pheromone()
        self.move()
        
    def move(self):
        self.direction += random.uniform(-0.3, 0.3)
        self.x += math.cos(self.direction) * self.velocity
        self.y += math.sin(self.direction) * self.velocity
        if (self.direction > 2*math.pi):
            self.direction -= 2*math.pi
        elif (self.direction < 0):
            self.direction += 2*math.pi
        self.avoid_edges()

    def draw(self, screen):
        head_x = self.x + 1 * math.cos(self.direction)
        head_y = self.y + 1 * math.sin(self.direction)
        pygame.draw.circle(screen, (255, 255, 255), (int(head_x), int(head_y)), 1)

        body_x = self.x - 2 * math.cos(self.direction + math.pi)
        body_y = self.y - 2 * math.sin(self.direction + math.pi)
        pygame.draw.circle(screen, (255, 255, 255), (int(body_x), int(body_y)), 1.5)

    def leave_pheromone(self):
        ph_type = self.mode_config[self.mode]["leaving"]
        pheromone_grid = self.world.pheromone_grids[ph_type]

        if self.pheromones > 0: 
            amt = min(10, self.pheromones / 100)
            pheromone_grid.add(self.x, self.y, amt)
            self.pheromones -= amt
        
        for i in range(-2, 3):
            for j in range(-2, 3):
                self.pheromones -= amt
                if self.pheromones >= 0:
                    pheromone_grid.add(int(self.x) + i, int(self.y) + j, amt)

    def get_all_paths(self, grid, loc, direction, steps = 5, min_turn = -math.pi / 6, max_turn = math.pi / 6, turn_steps = 10, path = []):
        if steps == 0:
            return [path]

        paths = []
        for i in range(turn_steps):
            next_turn = min_turn + (max_turn - min_turn) * i / turn_steps
            next_dir = direction + next_turn
            next_loc = (loc[0] + math.cos(next_dir) * self.velocity, loc[1] + math.sin(next_dir) * self.velocity)
            next_score = grid.get(int(next_loc[0]), int(next_loc[1]))
            new_paths = self.get_all_paths(grid, next_loc, next_dir, steps - 1, min_turn, max_turn, turn_steps, path + [next_turn])
            paths += new_paths
        return paths

    def get_score(self, grid, path):
        score = 0
        x = self.x
        y = self.y
        direction = self.direction
        for turn in path:
            multiplier = 1 - abs(turn) / self.max_turn_angle
            direction += turn
            dx = math.cos(direction) * self.velocity
            dy = math.sin(direction) * self.velocity
            x += dx
            y += dy
            score += grid.get(int(x), int(y)) * multiplier
            if self.mode == 'returning' and self.world.home.contains(x, y):
                score += 1000
            if self.mode == 'foraging' and self.world.food_grid.get_value(x, y) > 0:
                score += 1000
        return score

    def get_scored_paths(self, grid, paths):
        scored_paths = []
        for path in paths:
            score = self.get_score(grid, path) 
            if score > 0:
                scored_paths.append((score, path))
        return scored_paths

    def find_best_path(self, grid, loc, dir, score = 0, steps = 5, min_turn = -math.pi / 6, max_turn = math.pi / 6, turn_steps = 10):
        paths = self.get_all_paths(grid, loc, dir, steps, min_turn, max_turn, turn_steps)
        scored_paths = self.get_scored_paths(grid, paths)
        if len(scored_paths) == 0:
            return None
        scored_paths.sort(key = lambda x: x[0], reverse = True)
        best_path = scored_paths[0][1]
        return best_path

    def follow_pheromone(self):
        ph_type = self.mode_config[self.mode]["seeking"]
        grid = self.world.pheromone_grids[ph_type]
        steps = 3 
        turn_steps = 4 
        path = self.find_best_path(grid, (self.x, self.y), self.direction, 0, steps, -self.max_turn_angle, self.max_turn_angle, turn_steps)
        if path is None:
            return
        self.direction += path[0]

    def turn(self, radians):
        self.direction += radians
        if (self.direction > 2*math.pi):
            self.direction -= 2*math.pi
        elif (self.direction < 0):
            self.direction += 2*math.pi

    def turn_around(self):
        self.turn(math.pi)

    def avoid_edges(self):
        if self.x < 0:
            self.x = 0
            self.turn(random.random() * 2 * math.pi)
        elif self.x >= self.world.width:
            self.x = self.world.width - 1
            self.turn(random.random() * 2 * math.pi)
        if self.y < 0:
            self.y = 0
            self.turn(random.random() * 2 * math.pi)
        elif self.y >= self.world.height:
            self.y = self.world.height - 1
            self.turn(random.random() * 2 * math.pi)
