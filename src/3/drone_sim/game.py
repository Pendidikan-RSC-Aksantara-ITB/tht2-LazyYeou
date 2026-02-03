import pygame
import random
import math
from utils.constants import *
from utils.utils import *
from utils.drone import Drone
from utils.map import Map


def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AMBA Drone Swarm Simulation")
    clock = pygame.time.Clock()

    game_map = Map(GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
    target_pos = [random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)]
    while game_map.is_obstacle(target_pos[0], target_pos[1]):
        target_pos = [random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)]
        
    drones = []

    # 1. SETUP DRONES
    for i in range(NUM_DRONES):
        initial_x = random.uniform(0, SCREEN_WIDTH //5)
        initial_y = random.uniform(0, SCREEN_HEIGHT // 5)
        # Ensure we don't spawn inside an obstacle
        while game_map.is_obstacle(initial_x, initial_y):
            initial_x = random.uniform(0, SCREEN_WIDTH // 5)
            initial_y = random.uniform(0, SCREEN_HEIGHT // 5)

        # FIXED: Removed target_pos (passed in update instead)
        drone = Drone(initial_x, initial_y, i, target_pos)
        drones.append(drone)

    simulation_active = True
    start_time = pygame.time.get_ticks()
    elapsed_time_seconds = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_active = not simulation_active
                    # Adjust start time so the timer doesn't jump when unpausing
                    if simulation_active:
                        start_time = pygame.time.get_ticks() - int(elapsed_time_seconds * 1000)

        # 2. UPDATE PHASE (Physics & Logic)
        if simulation_active:
            current_time = pygame.time.get_ticks()
            elapsed_time_seconds = (current_time - start_time) / 1000.0
            
            # This makes the drones actually move!
            for drone in drones:
                drone.update(drones, game_map)

        # 3. DRAW PHASE (Rendering)
        screen.fill(GRAY)
        
        game_map.draw(screen, target_pos)
        
        for drone in drones:
            drone.draw(screen) 

        # UI / Metrics
        font = pygame.font.Font(None, 24)
        elapsed_time_text = f"Elapsed Time: {elapsed_time_seconds:.2f} s"
        elapsed_time_surface = font.render(elapsed_time_text, True, WHITE)
        screen.blit(elapsed_time_surface, (10, 10))

        if not simulation_active:
            paused_text = font.render("PAUSED", True, YELLOW)
            screen.blit(paused_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()
    print("Simulation ended.")

if __name__ == "__main__":
    run_simulation()