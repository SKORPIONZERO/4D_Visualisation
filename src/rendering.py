"""
rendering.py

"""
import config
import polytopes
import pygame

def draw_polytope(screen: pygame.Surface, polytope: polytopes.Polytope):
    screen.fill(config.BACKGROUND)
    for vertex in range(len(polytope.projected_vertices)):
        pygame.draw.circle(screen, config.BLUE, (int(polytope.projected_vertices[vertex][0]), int(polytope.projected_vertices[vertex][1])), 5)
    for edge in range(len(polytope.edges)):
        pygame.draw.line(screen, config.WHITE, polytope.projected_vertices[polytope.edges[edge][0]], polytope.projected_vertices[polytope.edges[edge][1]], 2)

def draw_w_labels(screen: pygame.Surface, polytope: polytopes.Polytope ,font: pygame.font.Font)