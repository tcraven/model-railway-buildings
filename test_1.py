import re
from cadquery import Assembly, Workplane
from cadquery import exporters


THICKNESS = 2
TAB_MARGIN = 20
MIN_TAB_LEN = 10


def panel_sketch(
    length,
    width,
    tabs_outside_x=True,
    tabs_outside_y=True,
    thickness=THICKNESS,
    tab_margin=TAB_MARGIN,
    min_tab_len=MIN_TAB_LEN
):
    x_tab_len = max(length - 2 * tab_margin, min_tab_len)
    y_tab_len = max(width - 2 * tab_margin, min_tab_len)
    rect_mode_x = "a" if tabs_outside_x else "s"
    rect_mode_y = "a" if tabs_outside_y else "s"

    if tabs_outside_x:
        length = length - 2 * thickness
    if tabs_outside_y:
        width = width - 2 * thickness

    return (
        Workplane("XY")
        .sketch()
        
        # Panel
        .rect(length, width)
        
        # Select the top and bottom edges and add the tabs
        .edges(">Y or <Y")
        .rect(x_tab_len, 2 * thickness, mode=rect_mode_y)
        
        # Select the left and right edges and add the tabs
        .reset()
        .edges(">X or <X")
        .rect(2 * thickness, y_tab_len, mode=rect_mode_x)
        
        # Remove the internal wires
        .clean()
    )


def panel(panel_sketch, thickness=THICKNESS):
    return (
        panel_sketch
        .finalize()
        .extrude(thickness)
    )


def _box_panel_sketches(length, width, height):
    top_ps = panel_sketch(
        length=length,
        width=width,
        tabs_outside_x=True,
        tabs_outside_y=True)

    bottom_ps = panel_sketch(
        length=length,
        width=width,
        tabs_outside_x=True,
        tabs_outside_y=True)

    front_ps = panel_sketch(
        length=length,
        width=height,
        tabs_outside_x=True,
        tabs_outside_y=False)

    back_ps = panel_sketch(
        length=length,
        width=height,
        tabs_outside_x=True,
        tabs_outside_y=False)

    left_ps = panel_sketch(
        length=height,
        width=width,
        tabs_outside_x=False,
        tabs_outside_y=False)

    right_ps = panel_sketch(
        length=height,
        width=width,
        tabs_outside_x=False,
        tabs_outside_y=False)

    return top_ps, bottom_ps, front_ps, back_ps, left_ps, right_ps


def _get_vertices_from_panel_sketch(panel_sketch):
    # Export CadQuery panel sketch to SVG using top down view
    svg_str = exporters.svg.getSVG(
        shape=exporters.utils.toCompound(
            panel(panel_sketch=panel_sketch)),
        opts={
            "width": 300,
            "height": 300,
            "marginLeft": 10,
            "marginTop": 10,
            "projectionDir": (0, 0, -1),  # Top
            "showAxes": False,
            "showHidden": False
        }
    )
    # print(svg_str)

    # Get the <path /> elements from the SVG string
    # <path d="M43.0,33.0 L25.0,33.0 " />
    # => "M43.0,33.0 L25.0,33.0 "
    path_strings = re.findall("<path d=\"(.+)\"", svg_str)

    # [['43.0,-33.0', '43.0,-15.0'], ...]
    path_edges = [p.strip()[1:].split(" L") for p in path_strings]

    # Extract the vertices, ordering them correctly (clockwise?)
    paths_dict = {}
    for edge_index, pe in enumerate(path_edges):
        for j in [0, 1]:
            if pe[j] not in paths_dict:
                paths_dict[pe[j]] = []
            paths_dict[pe[j]].append(edge_index)
    
    edges = []
    last_edge = None
    for key, val in paths_dict.items():
        from_index, to_index = sorted(val)
        # print(from_index, to_index)
        if to_index - from_index > 1:
            from_index, to_index = to_index, from_index
            last_edge = (from_index, to_index, key)
        else:
            edges.append((from_index, to_index, key))
    edges.append(last_edge)

    vertices = []
    for e in edges:
        x, y = e[2].split(",")
        vertices.append((float(x), float(y)))

    return vertices


def _polygon_svg_str(vertices):
    # <polygon points="100,100 150,25 150,75 200,0" fill="none" stroke="black" />
    polygon_svg_str = (
        '<polygon points="'
        f'{" ".join([",".join([str(x), str(y)]) for x, y in vertices])}'
        '" fill="none" stroke="black" />'
    )
    return polygon_svg_str


def box_faces(length, width, height):
    top_ps, bottom_ps, front_ps, back_ps, left_ps, right_ps \
        = _box_panel_sketches(length=length, width=width, height=height)

    return [
        {
            "name": "top",
            "vertices": _get_vertices_from_panel_sketch(panel_sketch=top_ps)
        },
        {
            "name": "bottom",
            "vertices": _get_vertices_from_panel_sketch(panel_sketch=bottom_ps)
        },
        {
            "name": "front",
            "vertices": _get_vertices_from_panel_sketch(panel_sketch=front_ps)
        },
        {
            "name": "back",
            "vertices": _get_vertices_from_panel_sketch(panel_sketch=back_ps)
        },
        {
            "name": "left",
            "vertices": _get_vertices_from_panel_sketch(panel_sketch=left_ps)
        },
        {
            "name": "right",
            "vertices": _get_vertices_from_panel_sketch(panel_sketch=right_ps)
        }
    ]


def box_assembly(length, width, height):
    top_ps, bottom_ps, front_ps, back_ps, left_ps, right_ps \
        = _box_panel_sketches(length=length, width=width, height=height)

    # Panels are rotated so that their top face is pointed outwards, and
    # translated so that the tabs fit together
    bottom_p = (
        panel(panel_sketch=bottom_ps)
        .rotate((0, 0, 0), (1, 0, 0), 180)
        .translate((0, 0, THICKNESS))
    )

    top_p = (
        panel(panel_sketch=top_ps)
        .translate((0, 0, height - THICKNESS))
    )
    left_p = (
        panel(panel_sketch=left_ps)
        .rotate((0, 0, 0), (0, 1, 0), -90)
        .translate((-(0.5 * length - THICKNESS), 0, 0.5 * height))
    )
    right_p = (
        panel(panel_sketch=right_ps)
        .rotate((0, 0, 0), (0, 1, 0), 90)
        .translate((0.5 * length - THICKNESS, 0, 0.5 * height))
    )
    front_p = (
        panel(panel_sketch=front_ps)
        .rotate((0, 0, 0), (1, 0, 0), -90)
        .translate((0, 0.5 * width - THICKNESS, 0.5 * height))
    )
    back_p = (
        panel(panel_sketch=back_ps)
        .rotate((0, 0, 0), (1, 0, 0), 90)
        .translate((0, -(0.5 * width - THICKNESS), 0.5 * height))
    )

    return (
        Assembly(name="tom-box")
        .add(bottom_p, name="bottom")
        .add(top_p, name="top")
        .add(left_p, name="left")
        .add(right_p, name="right")
        .add(front_p, name="front")
        .add(back_p, name="back")
    )

assembly = box_assembly(length=90, width=70, height=50)
# faces = box_faces(length=90, width=70, height=50)

# show_object(assembly)
# print(faces)
# for f in faces:
#     print(_polygon_svg_str(vertices=f["vertices"]))

# assembly.save(
#     path="./mesh.gltf",
#     exportType="GLTF",
#     mode="fused")
