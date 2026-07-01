"""
config.py

Fixed constants used across the project: window size, colors, etc.
"""
import pygame

WIDTH, HEIGHT = 1200, 800
FPS = 60
BASE_ROTATION_SPEED = 0.01  # radians per frame
DISTANCE_4D = 3.0  # Distance from the 4D object to the 4D camera
DISTANCE_3D = 4.0  # Distance from the 3D projection to the 3D camera
UNIT_DISTANCE = 1.0  # Distance from the center to the vertices of the polytope
OBJECT_SCALE = 100  # Scale factor for rendering the projected vertices
NUMBER_OF_LINE_SEGMENTS = 10  # Number of line segments for rendering edges
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
