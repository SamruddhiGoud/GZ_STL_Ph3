# main.py

from mesh.stl_reader import read_stl
from mesh.validation import check_manifold, fix_orientation, remove_degenerate, bounding_box_report
from solver.phase2_solver import run_hydrostatics

import matplotlib.pyplot as plt


def load_and_prepare_mesh(filepath):
    print(f"\nLoading STL: {filepath}")
    vertices, faces = read_stl(filepath)

    print(f"Vertices: {len(vertices)}, Faces: {len(faces)}")
    bounding_box_report(vertices)

    faces = remove_degenerate(vertices, faces)
    check_manifold(vertices, faces)
    faces = fix_orientation(vertices, faces)

    return vertices, faces


def get_user_inputs():
    print("\n--- User Inputs ---")

    KG = float(input("Enter KG (vertical center of gravity): "))
    draft = float(input("Enter draft (fixed waterline z): "))

    start = float(input("Heel start angle (deg): "))
    end = float(input("Heel end angle (deg): "))
    step = float(input("Heel step (deg): "))

    heel_angles = []
    a = start
    while a <= end + 1e-6:
        heel_angles.append(a)
        a += step

    return KG, draft, heel_angles


if __name__ == "__main__":
    stl_path = "data/kcs.stl"   # change to wigley.stl later, then kcs.stl

    vertices, faces = load_and_prepare_mesh(stl_path)

    KG, draft, heel_angles = get_user_inputs()

    results, deck_immersion_angle = run_hydrostatics(
        vertices,
        faces,
        KG=KG,
        draft=draft,
        heel_angles_deg=heel_angles
    )

    # ---------------- PLOTTING ----------------

    angles = []
    GZ_values = []

    for heel in heel_angles:
        angles.append(heel)
        GZ_values.append(results[heel]["GZ"])

    plt.figure()
    plt.plot(angles, GZ_values, marker='o')
    plt.xlabel("Heel Angle (deg)")
    plt.ylabel("GZ (m)")
    plt.title("GZ Curve (Phase 3 – STL Input)")
    plt.grid(True)

    if deck_immersion_angle is not None:
        plt.axvline(x=deck_immersion_angle, linestyle='--')
        plt.text(deck_immersion_angle, max(GZ_values)*0.9,
                 "Deck edge immersion", rotation=90, verticalalignment='center')

    plt.show()

    print("\n--- Completed Hydrostatics ---")
