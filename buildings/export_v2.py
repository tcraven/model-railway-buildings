import os
import shutil
import tempfile
from cadquery import Assembly
from buildings import nets_v2
from buildings import panels_v2
from buildings.nets_v2 import LayoutPanel
from buildings.panels_v2 import PanelGroup
from buildings.vertices_v2 import Vertex


def get_output_dirpath(model_name: str) -> str:
    return f"./output/{model_name}"


def delete_output_dir(output_dirpath: str) -> None:
    shutil.rmtree(output_dirpath, ignore_errors=True)


def export_mesh(output_dirpath: str, panel_group: PanelGroup) -> None:
    assembly = panels_v2.get_assembly(panel_group=panel_group)
    
    os.makedirs(output_dirpath, exist_ok=True)
    mesh_path = os.path.join(output_dirpath, "mesh.gltf")

    # Export GLTF mesh
    assembly.save(
        path=mesh_path,
        exportType="GLTF",
        mode="fused")


def export_mesh_to_xml_string(panel_group: PanelGroup) -> str:
    assembly = panels_v2.get_assembly(panel_group=panel_group)
    mesh_xml_str = None
    with tempfile.TemporaryDirectory() as output_dirpath:
        mesh_path = os.path.join(output_dirpath, "mesh.xml")

        # Export XML mesh to temp file
        assembly.save(
            path=mesh_path,
            exportType="XML",
            mode="fused")
        
        # Read contents of file as string
        with open(mesh_path, "r") as f:
            mesh_xml_str = f.read()

    return mesh_xml_str


def _polygon_svg_str(vertices: list[Vertex]) -> str:
    # <polygon points="100,100 150,25 150,75 200,0" fill="none" stroke="black" />
    polygon_svg_str = (
        '<polygon points="'
        f'{" ".join([",".join([str(x), str(y)]) for x, y in vertices])}'
        '" fill="none" stroke="black" />'
    )
    return polygon_svg_str


def _compute_svg_for_page(
    template_str: str,
    layout_panels: list[LayoutPanel],
    page_index: int,
    packer_rect_list: list[tuple],
    include_layout_boxes: bool
) -> str:
    panel_svg_strings = []
    label_svg_strings = []
            
    # Draw the layout boxes for debugging
    if include_layout_boxes:
        for rect in packer_rect_list:
            bin_index, x, y, width, height, rect_id = rect
            if bin_index != page_index:
                continue
            panel_svg_strings.append(
                f'<rect x="{x}" y="{-(y + height)}" width="{width}" '
                f'height="{height}" '
                'fill="transparent" stroke-width="0.1" stroke="#000" />'
            )

    # Draw the panels
    for index, layout_panel in enumerate(layout_panels):
        if layout_panel.bin_index != page_index:
            continue
        x = layout_panel.x
        y = layout_panel.y
        r = layout_panel.r
        vertex_loops_dict = layout_panel.vertex_loops
        for vs in vertex_loops_dict.values():
            panel_svg_strings.append(
                f'<g transform="translate({x},-{y}) rotate({r})">'
                f'{_polygon_svg_str(vertices=vs)}'
                '</g>'
            )
        
        print(f"{page_index} {index} {layout_panel.name}")
        label_svg_strings.append(
                # f'<g transform="translate({x},-{y}) rotate({r})">'
                # f'{_polygon_svg_str(vertices=vs)}'
                # '</g>'
                f'<text x="{x}" y="{y}">{index}</text>'
            )

    panels_svg_str = "\n".join(panel_svg_strings)
    labels_svg_str = "\n".join(label_svg_strings)
    
    svg_str = (
        template_str
        .replace("{{polygons}}", panels_svg_str)
        .replace("{{labels}}", labels_svg_str)
    )

    return svg_str


def export_svgs(
    panel_group: PanelGroup,
    output_dirpath: str,
    include_layout_boxes=False
) -> None:
    panels = panels_v2.get_all_panels(panel_group=panel_group)
    
    media_by_name = nets_v2.get_single_layer_media_by_name(panels=panels)

    layout_panels_by_media = nets_v2.get_layout_panels_by_media(panels=panels)

    with open("page.svg.template", "r") as f:
        template_str = f.read()

    for media_name, _layout_panels in layout_panels_by_media.items():
        # Compute the layout
        layout_panels, packer_rect_list = nets_v2.compute_layout(
            layout_panels=_layout_panels,
            media=media_by_name[media_name])

        bin_indexes = [layout_panel.bin_index for layout_panel in layout_panels]
        page_count = max(bin_indexes) + 1

        for page_index in range(page_count):
            page_number = page_index + 1

            svg_str = _compute_svg_for_page(
                template_str=template_str,
                layout_panels=layout_panels,
                page_index=page_index,
                packer_rect_list=packer_rect_list,
                include_layout_boxes=include_layout_boxes
            )

            media_dirpath = os.path.join(
                output_dirpath, f"media-{media_name}")

            os.makedirs(media_dirpath, exist_ok=True)

            output_filepath = os.path.join(
                media_dirpath, f"page-{page_number}-cut.svg")

            with open(output_filepath, "w") as f:
                f.write(svg_str)
