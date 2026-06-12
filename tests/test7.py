import pygame
import math
import numpy as np

from tests.test4 import BACKGROUND

WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND = (30, 30, 30)
NEON_BLUE = (0, 150, 255)
ORANGE = (255, 100, 0)
GREEN = (0, 255, 0)

def setup():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("4D Tesseract Rotation Test - Orthographic Projection")
    clock = pygame.time.Clock()
    return screen, clock

def main():
    screen, clock = setup()
    running = True
    start = pygame.Vector2([screen.get_width() / 2, screen.get_height() / 2])
    line_vectors=[]
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                for w in [-1, 1]:
                    line_vectors.append([x, y, z, w])
    theta_changing = False
    theta = 0
    while running:
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    theta_changing = not theta_changing
        clock.tick(60)
        if theta_changing:
            theta = (theta + 0.01) % (2 * math.pi)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
