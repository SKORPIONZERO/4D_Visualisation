import pygame
import numpy as np
import colorsys

def lerp_colours_rgb(value, max_value, min_value=None):
    R1, G1, B1 = BLUE
    R2, G2, B2 = RED
    if min_value is None:
        min_value = -max_value
    # Normalize v to a value between 0 and 1
    normalized_v = (value - min_value) / (max_value - min_value)
    # Map normalized_v to a color gradient between 2 colors, e.g., from blue to red.
    R_t = int(R1 + (R2 - R1) * normalized_v)
    G_t = int(G1 + (G2 - G1) * normalized_v)
    B_t = int(B1 + (B2 - B1) * normalized_v)
    return (R_t, G_t, B_t)

def lerp_colours_hsv(value, max_value, min_value=None):
    if min_value is None:
        min_value = -max_value
    saturation = 1.0
    value_brightness = 1.0
    # Normalize hue to a value between 0 and 1
    normalized_hue = (value - min_value) / (max_value - min_value)
    # Map normalized_hue to a color gradient in HSV space.
    hue = 240 * (1 - normalized_hue)  # From blue (240) to red (0)
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue / 360.0, saturation, value_brightness)
    return (int(r * 255), int(g * 255), int(b * 255))

def lerp_colours(values,max_value, min_value=None, mode='rgb'):
    colours = []
    if mode == 'rgb':
        for v in values:
            colours.append(lerp_colours_rgb(v, max_value, min_value))
    elif mode == 'hsv':
        for v in values:
            colours.append(lerp_colours_hsv(v, max_value, min_value))
    return colours

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
