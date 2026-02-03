from constants import *
from utils import *
import pygame
import random

class Map:
    def __init__(self, grid_size, screen_w, screen_h):
        self.grid_size = grid_size
        self.cell_size = screen_h // grid_size 
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.obstacles = [[0 for i in range(self.grid_size)] for i in range(self.grid_size)]

    def to_grid_coord(self, px, py):
        gx = int(px // self.cell_size)
        gy = int(py // self.cell_size)
        return gx, gy
    
    def to_pixel_coords(self, gx, gy):
        px = gx * self.cell_size + self.cell_size / 2
        py = gy * self.cell_size + self.cell_size / 2
        return px, py
    
    def add_obs(self, density):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rand = random.random()
                if rand < density:
                    self.obstacles[x][y] == 1
    
    def in_frame_pixel(self, px, py):
        return 0 <= px < self.screen_w and 0 <= py < self.screen_h
    
    def in_frame_grid(self, gx, gy):
        return 0 <= gx < self.grid_size and 0 <= gy < self.grid_size
    
    def is_obstacle(self, px, py):
        gx, gy = self.to_grid_coord(px, py)
        if self.in_frame_grid(gx, gy):
            return self.obstacles[gx][gy] == 1
        return 0
    
    def draw(self, screen):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

            # obs
            if self.obstacles[x][y] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            
            # target

        