"""
colouring.py

This module contains functions for colouring the edges 
of a polytope based on the w-coordinate values of its vertices.
"""
import numpy as np
import colorsys

import config

def lerp_colours_rgb(value: float, max_value: float, min_value: float | None = None) -> tuple[int, int, int]:
    """
    Linearly interpolate between two RGB colours based on a value.
    """
    R1, G1, B1 = config.BLUE
    R2, G2, B2 = config.RED
    if min_value is None:
        min_value = -max_value
    # Normalize value to a value between 0 and 1
    normalized_v = (value - min_value) / (max_value - min_value)
    # Map normalized_v to a color gradient between 2 colors, e.g., from blue to red.
    R_t = int(R1 + (R2 - R1) * normalized_v)
    G_t = int(G1 + (G2 - G1) * normalized_v)
    B_t = int(B1 + (B2 - B1) * normalized_v)
    return (R_t, G_t, B_t)

def lerp_colours_hsv(value: float, max_value: float, min_value: float | None = None) -> tuple[int, int, int]:
    """
    Linearly interpolate between two colours in HSV space based on a value.
    """
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

def lerp_colours(values: list, max_value: float, min_value: float | None = None, mode: int = config.LERP_MODES['hsv']) -> list:
    """
    Linearly interpolate between colours based on an array of values.
    """
    if mode == config.LERP_MODES['rgb']:
        return [lerp_colours_rgb(value, max_value, min_value) for value in values]
    elif mode == config.LERP_MODES['hsv']:
        return [lerp_colours_hsv(value, max_value, min_value) for value in values]
    else:
        raise ValueError("Invalid mode. Please choose 'rgb' or 'hsv'.")
