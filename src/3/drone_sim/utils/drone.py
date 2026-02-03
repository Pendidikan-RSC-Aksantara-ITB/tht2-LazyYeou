from .utils import *
from .constants import *
from .map import Map

import random 
import pygame
import math

class Drone:
    def __init__(self, x, y, drone_id, target):
        self.id = drone_id
        self.position = [float(x), float(y)]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.velocity = norm_vector(self.velocity)
        self.velocity = [v * DRONE_MAX_SPEED for v in self.velocity]
        self.color = BLUE
        self.radius = CELL_SIZE // 2
        self.max_speed = DRONE_MAX_SPEED
        self.max_force = DRONE_MAX_FORCE
        self.acceleration = [0.0, 0.0]
        self.fov_radius = 2.0
        self.target = target
        
        self.check_radius_cell = math.ceil(OBSTACLE_DISTANCE_THRESHOLD / CELL_SIZE) + 1
        
    def limit_vector(self, vector, limit):
        magnitude = vector[0] ** 2 + vector[1] ** 2
        if magnitude > limit:
            f = limit / magnitude
            return [vector[0] * f, vector[1] * f]
        return vector
    
    def apply_force(self, force):
        self.acceleration[0] += force[0]
        self.acceleration[1] += force[1]
    
    def to_target(self, target):
        desired_dir = [target[0] - self.position[0], target[1] - self.position[1]]
        distance = math.sqrt(desired_dir[0] ** 2 + desired_dir[1] ** 2)
        
        desired_dir = norm_vector(desired_dir)
        desired_velocity = [dir * self.max_speed for dir in desired_dir]

        steer = [desired_velocity[0] - self.velocity[0], desired_velocity[1] - self.velocity[1]]
        steer = self.limit_vector(steer, self.max_force)
        return steer 
    

    def avoid_obstacle(self, game_map : Map):
        force = [0.0, 0.0]
        obstacle_threshold = OBSTACLE_DISTANCE_THRESHOLD 
        cell_radius = self.check_radius_cell

        for dx_grid in range(-cell_radius, cell_radius + 1):
            for dy_grid in range(-cell_radius, cell_radius + 1):
                gx = int(self.position[0] // CELL_SIZE) + dx_grid
                gy = int(self.position[1] // CELL_SIZE) + dy_grid

                if game_map.is_in_frame_grid(gx, gy):
                    obs_px, obs_py = game_map.to_pixel_coords(gx, gy)
                    
                    is_obstacle_cell = game_map.obstacles[gx][gy] == 1
                    
                    if is_obstacle_cell:
                        dist_val = distance(self.position, (obs_px, obs_py))
                        
                        if dist_val < 0.1:
                            dist_val = 0.1

                        if dist_val < obstacle_threshold:
                            dir_vector = [self.position[0] - obs_px, self.position[1] - obs_py]
                            
                            mag = math.sqrt(dir_vector[0]**2 + dir_vector[1]**2)
                            unit_dir = [dir_vector[0]/mag, dir_vector[1]/mag]

                            repulsion_strength = (1.0 / dist_val - 1.0 / obstacle_threshold) ** 2
                            total_repulsion = repulsion_strength * ETA_WEIGHT
                            
                            force[0] += unit_dir[0] * total_repulsion
                            force[1] += unit_dir[1] * total_repulsion
        return force
    
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
    
    def alignment(self, drones ):
        sum_vel = [0.0, 0.0]
        count = 0
        
        for drone in drones:
            if drone != self:
                if distance(self.position, drone.position) < self.fov_radius:
                    sum_vel[0] += drone.velocity[0]
                    sum_vel[1] += drone.velocity[1]
                    count += 1
        
        if count > 0:
            avg_vel = [sum_vel[0] / count, sum_vel[1] / count]
            avg_vel = norm_vector(avg_vel)
            avg_vel = [v * self.max_speed for v in avg_vel]
            steer = [avg_vel[0] - self.velocity[0], avg_vel[1] - self.velocity[1]]
            steer = self.limit_vector(steer, self.max_force)
            return steer
        return [0.0, 0.0]

    def separation(self, drones ):
        steer = [0.0, 0.0]
        count = 0
        
        for drone in drones:
            if drone != self:
                d = distance(self.position, drone.position)
                if 0 < d < BOIDS_SEPARATION_DISTANCE:
                    diff_x = self.position[0] - drone.position[0]
                    diff_y = self.position[1] - drone.position[1]
                    factor = 1.0 / (d * d) 
                    steer[0] += diff_x * factor
                    steer[1] += diff_y * factor
                    count += 1
        
        if count > 0:
            steer = norm_vector(steer)
            steer = [v * self.max_speed for v in steer]
            steer = [v - self.velocity[i] for i, v in enumerate(steer)] 
            steer = self.limit_vector(steer, self.max_force)
        return steer



    def update(self, drones, game_map: Map):
        self.acceleration = [0.0, 0.0] 

        # boids
        cohesion_force = self.cohesion(drones)
        alignment_force = self.alignment(drones)
        separation_force = self.separation(drones)

        self.apply_force([f * BOIDS_COHESION_WEIGHT for f in cohesion_force])
        self.apply_force([f * BOIDS_ALIGNMENT_WEIGHT for f in alignment_force])
        self.apply_force([f * BOIDS_SEPARATION_WEIGHT for f in separation_force])

        #obstacle
        obstacle_force = self.avoid_obstacle(game_map)
        self.apply_force([f * ETA_WEIGHT for f in obstacle_force])

        target_force = self.to_target(self.target)
        self.apply_force([f * ATTRACT_TO_TARGET for f in target_force])

        # update velocity
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.velocity = self.limit_vector(self.velocity, self.max_speed)

        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # boundary
        if self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] = abs(self.velocity[0]) * 0.5 
        elif self.position[0] > game_map.screen_w:
            self.position[0] = game_map.screen_w
            self.velocity[0] = -abs(self.velocity[0]) * 0.5

        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] = abs(self.velocity[1]) * 0.5
        elif self.position[1] > game_map.screen_h:
            self.position[1] = game_map.screen_h
            self.velocity[1] = -abs(self.velocity[1]) * 0.5

        # local minima handling
        if game_map.is_obstacle(self.position[0], self.position[1]):
            if math.sqrt(self.velocity[0]**2 + self.velocity[1]**2) > 0.1:
                self.position[0] -= self.velocity[0] * 2 
                self.position[1] -= self.velocity[1] * 2
            else: 
                self.position[0] += random.uniform(-10, 10)
                self.position[1] += random.uniform(-10, 10)
                self.velocity = [v * -0.5 for v in self.velocity] 

    def draw(self, screen):
        pos_int = [int(self.position[0]), int(self.position[1])]
        pygame.draw.circle(screen, self.color, pos_int, self.radius)

        vel_mag = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if vel_mag > 0.1:
            factor = 2 * self.radius / vel_mag
            line_end = (int(self.position[0] + self.velocity[0] * factor),
                        int(self.position[1] + self.velocity[1] * factor))
            pygame.draw.line(screen, WHITE, pos_int, line_end, 1)
