# mesh/validation.py

import numpy as np
from collections import defaultdict

def check_manifold(vertices, faces):
    edge_count = defaultdict(int)

    for tri in faces:
        edges = [
            tuple(sorted((tri[0], tri[1]))),
            tuple(sorted((tri[1], tri[2]))),
            tuple(sorted((tri[2], tri[0]))),
        ]
        for e in edges:
            edge_count[e] += 1

    bad_edges = [e for e, c in edge_count.items() if c != 2]

    if bad_edges:
        raise ValueError(f"Non-manifold or open edges detected: {len(bad_edges)} problematic edges")

    print("✔ Manifold check passed")


def compute_signed_volume(vertices, faces):
    vol = 0.0
    for tri in faces:
        v0, v1, v2 = vertices[tri]
        vol += np.dot(v0, np.cross(v1, v2))
    return vol / 6.0


def fix_orientation(vertices, faces):
    vol = compute_signed_volume(vertices, faces)
    if vol < 0:
        print("⚠ Inverted mesh detected. Flipping face orientation.")
        faces = faces[:, [0, 2, 1]]
    else:
        print("✔ Orientation check passed")
    return faces


def remove_degenerate(vertices, faces, eps=1e-12):
    keep = []
    removed = 0

    for tri in faces:
        v0, v1, v2 = vertices[tri]
        area = np.linalg.norm(np.cross(v1 - v0, v2 - v0)) * 0.5
        if area > eps:
            keep.append(tri)
        else:
            removed += 1

    if removed > 0:
        print(f"⚠ Removed {removed} degenerate triangles")

    return np.array(keep, dtype=np.int64)


def bounding_box_report(vertices):
    mins = vertices.min(axis=0)
    maxs = vertices.max(axis=0)
    dims = maxs - mins

    print("Bounding Box:")
    print(f"  X: {mins[0]:.3f} → {maxs[0]:.3f} (L = {dims[0]:.3f})")
    print(f"  Y: {mins[1]:.3f} → {maxs[1]:.3f} (B = {dims[1]:.3f})")
    print(f"  Z: {mins[2]:.3f} → {maxs[2]:.3f} (D = {dims[2]:.3f})")

    return mins, maxs
