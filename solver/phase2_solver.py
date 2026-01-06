# solver/phase2_solver.py

import numpy as np
from .volume import volume_and_centroid
from .clipping import clip_mesh_at_draft


def rotate_about_x(vertices, theta):
    R = np.array([
        [1, 0, 0],
        [0,  np.cos(theta), -np.sin(theta)],
        [0,  np.sin(theta),  np.cos(theta)]
    ])
    return (R @ vertices.T).T


def get_deck_edge_vertices(vertices, z_tol=1e-3, y_fraction=0.9):
    """
    Identify deck edge vertices:
    - near max Z (top of hull)
    - near extreme |Y| (sides)
    """
    z_max = vertices[:, 2].max()
    y_max = np.abs(vertices[:, 1]).max()

    deck_vertices = []

    for v in vertices:
        if abs(v[2] - z_max) < z_tol and abs(v[1]) > y_fraction * y_max:
            deck_vertices.append(v)

    if len(deck_vertices) == 0:
        return None

    return np.array(deck_vertices)


def run_hydrostatics(vertices, faces, KG, draft, heel_angles_deg):
    results = {}
    deck_immersion_angle = None

    print("\n--- Running Phase 2 Hydrostatics (via STL) ---")

    deck_vertices = get_deck_edge_vertices(vertices)

    for heel_deg in heel_angles_deg:
        theta = np.deg2rad(heel_deg)

        # 1. Rotate hull
        vertices_rot = rotate_about_x(vertices, theta)

        # 2. Clip at fixed draft
        v_sub, f_sub = clip_mesh_at_draft(vertices_rot, faces, draft)

        # 3. Volume and buoyancy centroid
        volume, B = volume_and_centroid(v_sub, f_sub)

        # 4. KN and GZ (sign fixed)
        KN = -B[1]
        GZ = KN - KG * np.sin(theta)

        results[heel_deg] = {
            "volume": volume,
            "B": B,
            "KN": KN,
            "GZ": GZ
        }

        print(f"Heel = {heel_deg:6.2f}° | KN = {KN:+.5f} | GZ = {GZ:+.5f}")

        # 5. Deck edge immersion detection (only first time)
        if deck_vertices is not None and deck_immersion_angle is None:
            deck_rot = rotate_about_x(deck_vertices, theta)
            min_z = deck_rot[:, 2].min()

            if min_z <= draft:
                deck_immersion_angle = heel_deg
                print(f"\n>>> Deck edge immersion detected at ~{deck_immersion_angle:.2f}°")

    return results, deck_immersion_angle
