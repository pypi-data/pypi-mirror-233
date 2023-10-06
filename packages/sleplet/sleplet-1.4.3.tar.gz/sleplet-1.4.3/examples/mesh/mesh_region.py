import argparse

import cmocean
import numpy as np

import sleplet

MESHES = [
    "bird",
    "cheetah",
    "cube",
    "dragon",
    "homer",
    "teapot",
]


def main(mesh_name: str) -> None:
    """Plots the tiling of the Slepian line."""
    # initialise mesh and Slepian mesh
    mesh = sleplet.meshes.Mesh(mesh_name)

    # create region masking
    field = np.zeros(mesh.vertices.shape[0])
    field[mesh.region] = 1

    name = f"{mesh_name}_region"
    sleplet.plotting.PlotMesh(mesh, name, field, region=True).execute(cmocean.cm.haline)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mesh tiling")
    parser.add_argument(
        "function",
        type=str,
        choices=MESHES,
        help="mesh to plot",
        default="homer",
        const="homer",
        nargs="?",
    )
    args = parser.parse_args()
    main(args.function)
