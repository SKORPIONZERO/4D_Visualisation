"""
config.py

Fixed constants used across the project: window size, colors, etc.
"""
import pygame

WIDTH, HEIGHT = 1200, 800
FPS = 60
ROTATION_SPEED = 0.01  # radians per frame
PLANES = ("xy", "xz", "xw", "yz", "yw", "zw")
PLANE_KEYS = {pygame.K_1 + i: plane for i, plane in enumerate(PLANES)}
AXES = {"x": 0,
        "y": 1,
        "z": 2,
        "w": 3}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 100, 0)
BACKGROUND = (30, 30, 30)
