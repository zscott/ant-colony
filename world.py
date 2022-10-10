import home
import grid
import random

class World:
    def __init__(self, ants, width, height):
        self.ants = ants
        self.width = width
        self.height = height
        self.pheromone_grids = self.init_pheromone_grids()
        self.food_grid = self.init_food_grid()
        self.home = self.init_home()
        self.total_food_gathered = 0

    def init_pheromone_grids(self):
        pheromone_grids = {}
        pheromone_grids['foraging'] = grid.Grid(self.width, self.height, 0.96, (255, 0, 0))
        pheromone_grids['returning'] = grid.Grid(self.width, self.height, 0.96, (0, 0, 255))
        return pheromone_grids

    def init_food_grid(self):
        food_grid = grid.Grid(self.width, self.height, 1.0, (0, 255, 0))
        for i in range(3):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            for j in range(2000):
                x2 = random.randint(x-15, x+15)
                y2 = random.randint(y-15, y+15)
                if x2 >= 0 and x2 < self.width and y2 >= 0 and y2 < self.height:
                    food_grid.add(x2, y2, 50)
        return food_grid

    def init_home(self):
        return home.Home(self.ants, self.width, self.height)

    def draw(self, screen):
        for key in self.pheromone_grids:
            self.pheromone_grids[key].draw(screen)
        self.food_grid.draw(screen)
        self.home.draw(screen)
        self.draw_ants(screen)
         
    def draw_ants(self, screen):
        for ant in self.ants:
            ant.draw(screen)

    def update_ants(self):
        for ant in self.ants:
            ant.update()

    def update(self):
        for key in self.pheromone_grids:
            self.pheromone_grids[key].update()
        self.home.update(self)
        self.update_ants()
