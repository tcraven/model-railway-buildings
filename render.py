import os
import shutil
from buildings import models
from buildings import nets


def main():
    # Generate box building data
    # b = models.House_1(
    #     name="house-1",
    #     length=90,
    #     width=70,
    #     height=50,
    #     gable_height=30,
    #     chimney_width=15,
    #     chimney_height=12
    # )

    # b = models.Roof(
    #     name="roof-1",
    #     width=100,
    #     gable_width=70,
    #     gable_height=30,
    #     rafter_length=10,
    #     overhang_length=5
    # )

    b = models.WindowTest(
        name="window-test-1"
    )

    model_name = b.name
    output_dirpath = f"./output/{model_name}"
    shutil.rmtree(output_dirpath, ignore_errors=True)
    os.makedirs(output_dirpath, exist_ok=True)
    mesh_path = os.path.join(output_dirpath, "mesh.gltf")

    # Export GLTF mesh
    b.assembly.save(
        path=mesh_path,
        exportType="GLTF",
        mode="fused")

    # Export SVG pages
    nets.export_svg(
        object=b,
        output_dirpath=output_dirpath,
        include_layout_boxes=False)

    print("OK")


if __name__ == "__main__":
    main()
