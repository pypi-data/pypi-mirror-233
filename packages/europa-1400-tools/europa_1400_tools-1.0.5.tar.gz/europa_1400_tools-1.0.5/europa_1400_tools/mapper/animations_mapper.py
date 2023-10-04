from pathlib import Path

import numpy as np

from europa_1400_tools.construct.baf import Baf, Vector3


class AnimationsMapper:
    @staticmethod
    def map_animation(baf: Baf, bgf_to_vertices: dict[Path, np.ndarray]) -> list[Path]:
        """Map animation to object."""

        mapped_bgfs: list[Path] = []
        baf_vertices: list[Vector3] = []

        for model in baf.body.keys[0].models:
            baf_vertices.extend(model.vertices)

        baf_vertices_np = np.array(
            [[vertex.x, vertex.y, vertex.z] for vertex in baf_vertices],
            dtype=np.float32,
        )

        if baf.path.stem.lower() == "sitzung1_kutte":
            pass

        for bgf_path, bgf_vertices_np in bgf_to_vertices.items():
            if bgf_vertices_np.shape[0] != baf_vertices_np.shape[0]:
                continue

            baf_name = baf.path.stem
            bgf_name = bgf_path.stem

            baf_name_parts = [part.lower() for part in baf_name.split("_")]
            bgf_name_parts = [part.lower() for part in bgf_name.split("_")]

            baf_name_parts = [
                "".join([char for char in part]) for part in baf_name_parts
            ]
            bgf_name_parts = [
                "".join([char for char in part]) for part in bgf_name_parts
            ]

            if not any(
                baf_name_part in bgf_name_parts for baf_name_part in baf_name_parts
            ):
                continue

            mapped_bgfs.append(bgf_path)

        return mapped_bgfs
