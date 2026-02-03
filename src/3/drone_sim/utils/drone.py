from utils import *
from constants import *
from map import Map

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
        self.max_speed = DRONE_MAX_SPEED
        self.max_force = DRONE_MAX_FORCE
        
        self.check_radius_cell = math.ceil(OBSTACLE_DISTANCE_THRESHOLD / CELL_SIZE) + 1
        
    def limit_vector(self, vector, limit):
        magnitude = vector[0] ** 2 + vector[1] ** 2
        if magnitude > limit:
            f = limit / magnitude
            return [vector[0] * f, vector[1] * f]
        return vector
    
    def to_target(self, target):
        desired_dir = [target[0] - self.position[0], target[1] - self.position[1]]
        distance = math.sqrt(desired_dir[0] ** 2 + desired_dir[1] ** 2)
        
        desired_dir = norm_vector(desired_dir)
        desired_velocity = [dir * self.max_speed for dir in desired_dir]

        steer = [desired_velocity[0] - self.velocity[0], desired_velocity[1] - self.velocity[1]]
        steer = self.limit_vector(steer, self.max_force)
        return steer 
    

    def avoid_obstacle(self, game_map : Map):
        steer = [0.0, 0.0]
        obstacle_threshold = OBSTACLE_DISTANCE_THRESHOLD

        cell_radius = self.check_radius_cell

        for dy_grid in range(-cell_radius, cell_radius + 1):
            for dx_grid in range(-cell_radius, cell_radius + 1):
                gx = int(self.position[0] // CELL_SIZE) + dx_grid
                gy = int(self.position[1] // CELL_SIZE) + dy_grid

                if game_map.is_in_frame_grid(gx, gy):
                    obs_px, obs_py = game_map.to_pixel_coords(gx, gy)
                    
                    is_obstacle_cell = game_map.obstacles[gx][gy] == 1

                    # Consider both explicit obstacles and map boundaries as repulsive sources
                    if is_obstacle_cell or not game_map.is_in_frame_pixel(obs_px, obs_py):
                        doi = distance(self.position, (obs_px, obs_py))

                        if 0 < doi < obstacle_threshold:
                            eta =  ETA_WEIGHT
                            
                            dir_vector = [self.position[0] - obs_px, self.position[1] - obs_py]
                            magnitude_dir = math.sqrt(dir_vector[0]**2 + dir_vector[1]**2)

                            if magnitude_dir > 0:
                                unit_dir_vector = [v / magnitude_dir for v in dir_vector]
                            else:
                                unit_dir_vector = [0.0, 0.0] 

                            repulsion_term = (1 / doi - 1 / obstacle_threshold)
                            if repulsion_term < 0:
                                repulsion_term = 0
                            
                            force_magnitude = eta * (repulsion_term ** 2)
                            
                            steer[0] += force_magnitude * unit_dir_vector[0]
                            steer[1] += force_magnitude * unit_dir_vector[1]

        if steer[0] != 0 or steer[1] != 0:
            steer = norm_vector(steer)
            steer = [v * self.max_speed for v in steer]
            steer = [v - self.velocity[i] for i, v in enumerate(steer)] #
            steer = self._limit_vector(steer, self.max_force)
        return steer
    
    def cohesion(self, drones):
        pos_sum = [0.0, 0.0]
        count = 0

        for drone in drones:
            if drone != self:
                pos_sum[0] += drone.position[0]
                pos_sum[1] += drone.position[1]
                count += 1

        if count > 0:
            avg_pos = [pos_sum[0] / count, pos_sum[1] / count]
            velocities = [avg_pos[0] - self.position[0], avg_pos[1] - self.position[1]]

            velocities = norm_vector(velocities)
            velocities = [v * self.max_speed for v in velocities]
            steer = [velocities[0] - self.velocity[0], velocities[1] - self.velocity[1]]
            steer = self.limit_vector(velocities, self.max_force)
            return steer
        return [0, 0]


    def draw(self, screen):
        pos_int = [int(self.position[0]), int(self.position[1])]
        pygame.draw.circle(screen, self.color, pos_int, self.radius)

        vel_mag = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if vel_mag > 0.1:
            factor = 2 * self.radius / vel_mag
            line_end = (int(self.position[0] + self.velocity[0] * factor),
                        int(self.position[1] + self.velocity[1] * factor))
            pygame.draw.line(screen, WHITE, pos_int, line_end, 1)
