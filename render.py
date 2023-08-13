import os
import shutil
from buildings import models
from buildings import nets

# 2mm corrugated card sheets are width="269.4mm" height="205.9mm"
MEDIA_INFO_BY_NAME = {
    "2mm": {
        "thickness": 1.69,      # Exact material thickness in mm
        "width": 265,
        "height": 165
    },
    "4mm": {
        "thickness": 1.69 * 2,  # Two layers of 2mm card
        "width": 265,
        "height": 165,
        "multiply": 2       # Omit two copies of each panel in the net
                            # since we need are two layers to glue together
    }
}


def main():
    media_name = "4mm"
    media_info = MEDIA_INFO_BY_NAME[media_name]
    

    # Generate box building data
    # b = models.Box(
    # b = models.BoxWithHoles(
    b = models.House_1(
        name="house-1",
        length=90,
        width=70,
        height=50,
        gable_height=30,  # 30,
        thickness=media_info["thickness"]
    )

    model_name = b.name
    output_dirpath = f"./output/{model_name}"
    shutil.rmtree(output_dirpath, ignore_errors=True)
    media_dirpath = os.path.join(output_dirpath, f"media-{media_name}")
    os.makedirs(media_dirpath, exist_ok=True)
    mesh_path = os.path.join(output_dirpath, "mesh.gltf")

    # Export GLTF mesh
    b.assembly.save(
        path=mesh_path,
        exportType="GLTF",
        mode="fused")

    # Export SVG pages
    nets.export_svg(
        object=b,
        media_info=media_info,
        output_dirpath=media_dirpath,
        include_layout_boxes=False)

    print("OK")


if __name__ == "__main__":
    main()
