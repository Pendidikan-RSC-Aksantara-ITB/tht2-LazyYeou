from constants import *
from utils import *
import pygame
import random

class Map:
    def __init__(self, grid_size, screen_w, screen_h):
        self.grid_size = grid_size
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cell_size = screen_h // grid_size + 1
        