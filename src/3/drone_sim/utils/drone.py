from utils import *
from constants import *

import random 
import pygame
import math

class Drone:
    def __init__(self, x, y, drone_id):
        self.id = drone_id
        self.position = [float(x), float(y)]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.velocity = norm_vector(self.velocity)
        self.velocity = [v * DRONE_MAX_SPEED for v in self.velocity]
        self.color = BLUE
        self.radius = 2
        
        self.check_radius_cell = math.ceil(OBSTACLE_DISTANCE_THRESHOLD / CELL_SIZE) + 1
        
    def avoid_obstacle(self, game_map):
        steer = [0.0, 0.0]
        obstacle_threshold = OBSTACLE_DISTANCE_THRESHOLD

        cell_radius = self.check_radius_cell
        
        obs_px, obs_py = game_map._to 


    def draw(self, screen):
        pos_int = [int(self.position[0]), int(self.position[1])]
        pygame.draw.circle(screen, self.color, pos_int, self.radius)

        vel_mag = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if vel_mag > 0.1:
            factor = 2 * self.radius / vel_mag
            line_end = (int(self.position[0] + self.velocity[0] * factor),
                        int(self.position[1] + self.velocity[1] * factor))
            pygame.draw.line(screen, WHITE, pos_int, line_end, 1)
