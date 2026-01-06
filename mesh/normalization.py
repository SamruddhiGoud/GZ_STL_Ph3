# mesh/normalization.py

import numpy as np

def ensure_z_up(vertices):
    # Assumes STL is already roughly aligned.
    # We only enforce right-handedness via orientation check elsewhere.
    return vertices


def center_hull(vertices):
    centroid = vertices.mean(axis=0)
    return vertices - centroid
