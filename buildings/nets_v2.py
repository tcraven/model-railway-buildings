import copy
import os
import rectpack  # type: ignore
from dataclasses import dataclass
from buildings import vertices_v2
from buildings.panels_v2 import Panel, PanelGroup
from buildings.media_v2 import LayeredMedia, SingleLayerMedia
from buildings.vertices_v2 import Vertex, VertexLoops


@dataclass
class LayoutPanel:
    name: str
    vertex_loops: VertexLoops
    width: float
    height: float
    center_offset_x: float
    center_offset_y: float
    bin_index: int = 0
    x: float = 0
    y: float = 0
    r: float = 0


def compute_layout(
    layout_panels: list[LayoutPanel],
    media: SingleLayerMedia
) -> tuple[list[LayoutPanel], list[tuple]]:
    """
    Computes the layout of the panels across multiple pages, and
    sets the layout dict in each panel of the object.
    """
    # Leave a margin of 5mm around each rectangle, so that adjacent
    # rectangles will be 10mm apart
    PACK_OBJECT_MARGIN = 3

    layout_panels_by_id = {
        layout_panel.name: layout_panel
        for layout_panel in layout_panels
    }
    
    rectangles_by_id = {}
    for layout_panel in layout_panels:
        rectangles_by_id[layout_panel.name] = {
            "width": layout_panel.width + 2 * PACK_OBJECT_MARGIN,
            "height": layout_panel.height + 2 * PACK_OBJECT_MARGIN,
            "id": layout_panel.name
        }

    # Run the packing algorithm and get the positions, bin index and
    # rotation of each rectangle
    packer = rectpack.newPacker()
    for rectangle in rectangles_by_id.values():
        packer.add_rect(
            width=rectangle["width"],
            height=rectangle["height"],
            rid=rectangle["id"])

    # - Bins are the size of the drawing area of a page
    # - They are created up front
    # - We must have enough bins to fit all of the objects otherwise the
    #   objects will overlap
    MAX_BIN_COUNT = 20
    for i in range(MAX_BIN_COUNT):
        packer.add_bin(
            width=media.width,
            height=media.height)
    
    packer.pack()

    for rect in packer.rect_list():
        bin_index, x, y, width, height, rect_id = rect
        rectangle = rectangles_by_id[rect_id]
        is_rotated_90 = (rectangle["width"] != width)
        layout_panel = layout_panels_by_id[rect_id]

        offset_x = layout_panel.center_offset_x
        offset_y = layout_panel.center_offset_y
        if is_rotated_90:
            offset_x, offset_y = offset_y, offset_x


        layout_panel.x = x + 0.5 * (width + offset_x)
        layout_panel.y = y + 0.5 * (height + offset_y)
        layout_panel.bin_index = bin_index
        layout_panel.r = 90 if is_rotated_90 else 0

    
    return layout_panels, packer.rect_list()


def get_layout_panels_by_media(panels: list[Panel]) -> dict[str, list[LayoutPanel]]:
    panels_by_media: dict[str, list[Panel]] = {}
    for panel in panels:
        media = panel.media
        if type(media) is SingleLayerMedia:
            media_name = media.name
            layer_count = 1
        elif type(media) is LayeredMedia:
            media_name = media.media.name
            layer_count = media.layer_count
        else:
            raise Exception("Unknown media")

        if media_name not in panels_by_media:
            panels_by_media[media_name] = []

        if layer_count == 1:
            panels_by_media[media_name].append(panel)
            continue
        
        for index in range(layer_count):
            copied_panel = copy.copy(panel)
            copied_panel.name += f"_{index}"
            panels_by_media[media_name].append(copied_panel)
    
    layout_panels_by_media: dict[str, list[LayoutPanel]] = {}
    for media_name, panels in panels_by_media.items():
        layout_panels_by_media[media_name] = []
        for panel in panels:
            vertex_loops = vertices_v2.get_panel_vertex_loops(
                workplane=panel.workplane)

            width, height, center_offset_x, center_offset_y = \
                vertices_v2.get_width_height(panel_vertices=vertex_loops)

            layout_panel = LayoutPanel(
                name=panel.name,
                vertex_loops=vertex_loops,
                width=width,
                height=height,
                center_offset_x=center_offset_x,
                center_offset_y=center_offset_y
            )
            layout_panels_by_media[media_name].append(layout_panel)

    return layout_panels_by_media


def get_single_layer_media_by_name(
    panels: list[Panel]
) -> dict[str, SingleLayerMedia]:
    media_by_name = {}
    for panel in panels:
        media = panel.media
        if type(media) is SingleLayerMedia:
            media_by_name[media.name] = media
        elif type(media) is LayeredMedia:
            media_by_name[media.media.name] = media.media
        else:
            raise Exception("Unknown media")

    return media_by_name
