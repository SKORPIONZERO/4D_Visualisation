"""
projection.py

Contains functions for projecting 4D points to 3D
and then to 2D using perspective projection factors.
"""
import numpy as np

def _project_4D_to_3D(vertex: np.ndarray, distance_4D: float) -> tuple[np.ndarray, float]:
    x, y, z, w = vertex
    factor_4d = distance_4D/(distance_4D-w)
    x, y, z = x * factor_4d, y * factor_4d, z * factor_4d
    return (np.array([x, y, z]), w)

def _project_3D_to_2D(vertex: np.ndarray, distance_3D: float) -> np.ndarray:
    x, y, z = vertex
    factor_3d = distance_3D/(distance_3D-z)
    x, y = x * factor_3d, y * factor_3d
    return np.array([x, y])

def project_4D_to_2D(vertex: np.ndarray, distance_4D: float, distance_3D: float) -> tuple[np.ndarray, float]:
    vertex_3D, w = _project_4D_to_3D(vertex, distance_4D)
    vertex_2D = _project_3D_to_2D(vertex_3D, distance_3D)
    return (vertex_2D, w)

def _project_multiple_4D_to_3D(vertices: np.ndarray, distance_4D: float) -> tuple[np.ndarray, np.ndarray]:
    x, y, z, w = vertices[:, 0], vertices[:, 1], vertices[:, 2], vertices[:, 3]
    factors_4d = distance_4D/(distance_4D-w)
    x, y, z = x * factors_4d, y * factors_4d, z * factors_4d
    return (np.stack([x, y, z], axis = 1), w)

def _project_multiple_3D_to_2D(vertices: np.ndarray, distance_3D: float) -> np.ndarray:
    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    factors_3d = distance_3D/(distance_3D-z)
    x, y = x * factors_3d, y * factors_3d
    return (np.stack([x, y], axis = 1))

def project_multiple_4D_to_2D(vertices: np.ndarray, distance_4D: float, distance_3D: float) -> tuple[np.ndarray, np.ndarray]:
    vertices_3D, w = _project_multiple_4D_to_3D(vertices, distance_4D)
    vertices_2D = _project_multiple_3D_to_2D(vertices_3D, distance_3D)
    return (vertices_2D, w)
