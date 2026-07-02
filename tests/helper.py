import pygame
import numpy as np

def display_shape(screen, current_vertices, w_values, edges, colours, number_of_line_segments, max_distance_from_origin):
    for edge in range(len(edges)):
        start_pos = current_vertices[edges[edge][0]]
        for i in range(number_of_line_segments + 1):
            t = i / number_of_line_segments
            coordinates_t = current_vertices[edges[edge][0]] + t * (current_vertices[edges[edge][1]] - current_vertices[edges[edge][0]])
            colours_t = lerp_colours_hsv(w_values[edges[edge][0]] + t * (w_values[edges[edge][1]] - w_values[edges[edge][0]]), max_distance_from_origin)
            pygame.draw.line(screen, colours_t, start_pos, coordinates_t, 3)
            start_pos = coordinates_t

def main():
    colours = lerp_colours(w_values, max_distance_from_origin, mode='hsv')
    display_shape(screen, current_vertices, w_values, edges, colours, number_of_line_segments, max_distance_from_origin) 

if __name__ == "__main__":
    main()
