# solver/hydrostatics/volume.py

import numpy as np

def volume_and_centroid(vertices, faces):
    V = 0.0
    C = np.zeros(3)

    for f in faces:
        v0 = vertices[f[0]]
        v1 = vertices[f[1]]
        v2 = vertices[f[2]]

        v = np.dot(v0, np.cross(v1, v2)) / 6.0
        tet_centroid = (v0 + v1 + v2) / 4.0

        V += v
        C += v * tet_centroid

    V_abs = abs(V)

    if V_abs < 1e-12:
        raise ValueError("Computed volume is zero or very small.")

    centroid = C / V

    return V_abs, centroid
