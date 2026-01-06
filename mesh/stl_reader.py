# mesh/stl_reader.py

import struct
import numpy as np


def is_binary_stl(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(80)
        try:
            f.read(4)
            return True
        except:
            return False


def read_binary_stl(filepath):
    with open(filepath, 'rb') as f:
        f.read(80)
        tri_count = struct.unpack('<I', f.read(4))[0]

        vertices = []
        faces = []
        vert_map = {}
        idx = 0

        for _ in range(tri_count):
            data = f.read(50)
            if len(data) != 50:
                raise ValueError("Unexpected end of binary STL file")

            unpacked = struct.unpack('<12fH', data)

            v1 = unpacked[3:6]
            v2 = unpacked[6:9]
            v3 = unpacked[9:12]

            face = []
            for v in (v1, v2, v3):
                key = tuple(v)
                if key not in vert_map:
                    vert_map[key] = idx
                    vertices.append(v)
                    face.append(idx)
                    idx += 1
                else:
                    face.append(vert_map[key])

            faces.append(face)

    return np.array(vertices, dtype=np.float64), np.array(faces, dtype=np.int64)


def read_ascii_stl(filepath):
    vertices = []
    faces = []
    vert_map = {}
    idx = 0

    with open(filepath, 'r') as f:
        lines = f.readlines()

    current_face = []

    for line in lines:
        line = line.strip()
        if line.startswith("vertex"):
            parts = line.split()
            v = (float(parts[1]), float(parts[2]), float(parts[3]))

            if v not in vert_map:
                vert_map[v] = idx
                vertices.append(v)
                current_face.append(idx)
                idx += 1
            else:
                current_face.append(vert_map[v])

            if len(current_face) == 3:
                faces.append(current_face)
                current_face = []

    return np.array(vertices, dtype=np.float64), np.array(faces, dtype=np.int64)


def read_stl(filepath):
    print("Detecting STL format...")

    with open(filepath, 'rb') as f:
        start = f.read(5)

    if start.lower() == b'solid':
        print("→ ASCII STL detected")
        return read_ascii_stl(filepath)
    else:
        print("→ Binary STL detected")
        return read_binary_stl(filepath)
