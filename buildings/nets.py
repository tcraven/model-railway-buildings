import os
import rectpack


# Leave a margin of 5mm around each rectangle, so that adjacent
# rectangles will be 10mm apart
PACK_OBJECT_MARGIN = 5


def compute_layout(panels, media_info):
    """
    Computes the layout of the panels across multiple pages, and
    sets the layout dict in each panel of the object.
    """
    # panel: name, workplane, vertices, width, height
    # vertices: dict of loop_index, vertices

    panels_by_id = { panel["name"]: panel for panel in panels }
    
    rectangles_by_id = {}
    for panel in panels:
        rectangles_by_id[panel["name"]] = {
            "width": panel["width"] + 2 * PACK_OBJECT_MARGIN,
            "height": panel["height"] + 2 * PACK_OBJECT_MARGIN,
            "id": panel["name"]
        }

    # Run the packing algorithm and get the positions, bin index and
    # rotation of each rectangle
    packer = rectpack.newPacker()
    for rectangle in rectangles_by_id.values():
        packer.add_rect(
            width=rectangle["width"],
            height=rectangle["height"],
            rid=rectangle["id"])

    # Bins are the size of the drawing area of a page    
    for i in range(10):
        packer.add_bin(width=media_info["width"], height=media_info["height"])
    
    packer.pack()

    for rect in packer.rect_list():
        bin_index, x, y, width, height, rect_id = rect
        rectangle = rectangles_by_id[rect_id]
        rotated_90 = (rectangle["width"] != width)
        panel = panels_by_id[rect_id]

        offset_x = panel["center_offset_x"]
        offset_y = panel["center_offset_y"]
        if rotated_90:
            offset_x, offset_y = offset_y, offset_x

        panel["layout"] = {
            "x": x + 0.5 * (width + offset_x),
            "y": y + 0.5 * (height + offset_y),
            "bin_index": bin_index,
            "r": 90 if rotated_90 else 0
        }
    
    return packer.rect_list()


def export_svg(object, media_info, output_dirpath, include_layout_boxes):
    with open("page.svg.template", "r") as f:
        template_str = f.read()

    # If the media has a mulitply value, create multiple copies of each panel
    # to be added to the layout
    panels = []
    for panel in object.panels:
        multiply = media_info.get("multiply")
        if not multiply:
            panels.append(panel)
            continue
        
        for i in range(multiply):
            copied_panel = panel.copy()
            copied_panel["name"] += f"_{i}"
            panels.append(copied_panel)

    # Compute the layout
    packer_rect_list = compute_layout(panels=panels, media_info=media_info)

    bin_indexes = [panel["layout"]["bin_index"] for panel in panels]
    page_count = max(bin_indexes) + 1

    for page_index in range(page_count):
        page_number = page_index + 1

        panel_svg_strings = []
        
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
        for panel in panels:
            if panel["layout"]["bin_index"] != page_index:
                continue
            x = panel["layout"]["x"]
            y = panel["layout"]["y"]
            r = panel["layout"]["r"]
            vertex_loops_dict = panel["vertices"]
            for vertices in vertex_loops_dict.values():
                panel_svg_strings.append(
                    f'<g transform="translate({x},-{y}) rotate({r})">'
                    f'{polygon_svg_str(vertices=vertices)}'
                    '</g>'
                )

        panels_svg_str = "\n".join(panel_svg_strings)
        svg_str = template_str.replace("{{polygons}}", panels_svg_str)

        output_filepath = os.path.join(
            output_dirpath, f"page-{page_number}-cut.svg")

        with open(output_filepath, "w") as f:
            f.write(svg_str)


def polygon_svg_str(vertices):
    # <polygon points="100,100 150,25 150,75 200,0" fill="none" stroke="black" />
    polygon_svg_str = (
        '<polygon points="'
        f'{" ".join([",".join([str(x), str(y)]) for x, y in vertices])}'
        '" fill="none" stroke="black" />'
    )
    return polygon_svg_str

"""
<g transform="translate(49.0,-39.0)">
    {{polygon}}
</g>
"""
