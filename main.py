import pygame;
import sys;
import os;
import time;
import random;
import math;
import numpy as np;
import matplotlib.pyplot as plt;
import ant;
import grid;
import home;
import world;

pygame.init()

width = 300 
height = 300
footer_font = pygame.font.SysFont('Arial', 12)
footer_height = footer_font.get_height()
screen_width = width
screen_height = height + footer_height

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 32)
pygame.display.set_caption("Ant Simulation")

ants = []
world = world.World(ants, width, height)

def draw_footer():
    footer = footer_font.render("Total food gathered: " + str(world.total_food_gathered), True, (255, 255, 255))
    screen.blit(footer, (0, height))

def draw_world():
    world.draw(screen)

def update_world():
    world.update()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    draw_world()
    draw_footer()
    update_world()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
