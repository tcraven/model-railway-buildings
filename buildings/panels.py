import math
from cadquery import Workplane
from buildings import Tab

"""
In three dimensions, we use the following terms:
x = length, y = width, z = height

All panels are created in the XY plane => they have width and height
"""

def rect(
    width, height, thickness, tab_left, tab_right, tab_bottom, tab_top
):
    panel = (
        Workplane("XY")
        .box(width, height, thickness)
        .translate((0, 0, 0.5 * thickness))
    )
    panel_with_tabs = _add_tabs(
        panel=panel,
        tab_defs_dict={0: tab_left, 1: tab_right, 2: tab_bottom, 3: tab_top})

    return panel_with_tabs


def rect_with_hole(
    width, height, thickness, tab_left, tab_right, tab_bottom, tab_top,
    extra_hole=None
):
    panel = (
        rect(
            width=width, height=height, thickness=thickness,
            tab_left=tab_left, tab_right=tab_right, tab_bottom=tab_bottom,
            tab_top=tab_top
        )

        # Cut out hole
        .faces(">Z")
        .sketch()
        .rect(width - 20, height - 20)
        .vertices()
        .chamfer(5)
        .finalize()
        .cutThruAll()
    )

    result = panel

    if extra_hole is not None:
        hole_box = (
            Workplane("XY")
            .box(extra_hole["width"], extra_hole["height"], thickness * 2)
            .translate((extra_hole["x"], extra_hole["y"], 0))
        )
        result = panel - hole_box

    return result


def front_with_windows(width, height, thickness, window_margin=0):
    panel = (
        Workplane("XY")
        .box(width, height, thickness)
        .translate((0, 0, 0.5 * thickness))
    )

    window_width = 14 + 2 * window_margin
    window_height = 23 + 2 * window_margin

    win0 = (
       Workplane("XY")
        .box(window_width, window_height, 10)
        .translate((-20, 0, 0))
    )
    win1 = (
        Workplane("XY")
        .box(window_width, window_height, 10)
        .translate((20, 0, 0))
    )

    front_with_windows_panel = panel - win0 - win1
    return front_with_windows_panel


def window_sill(thickness):
    width = 14 + 3
    height = 2
    return (
        Workplane("XY")
        .box(
            width,
            height,
            thickness)
        .translate((0, 0, 0.5 * thickness))
    )


def window_layer_1(thickness):
    window_margin = 5
    window_width = 14
    window_height = 23
    frame_thickness = 0.5

    panel = (
        Workplane("XY")
        .box(
            window_width + 2 * window_margin,
            window_height + 2 * window_margin,
            thickness)
        .translate((0, 0, 0.5 * thickness))
    )

    hole_1 = (
        Workplane("XY")
        .box(
            window_width - 2 * frame_thickness,
            0.5 * window_height - 2 * frame_thickness,
            10)
        .translate((0, -0.25 * window_height, 0))
    )

    hole_2 = (
        Workplane("XY")
        .box(
            window_width - 4 * frame_thickness,
            0.5 * window_height - 3 * frame_thickness,
            10)
        .translate((
            0,
            0.25 * window_height - 1.5 * frame_thickness,
            0))
    )

    center_frame = (
        Workplane("XY")
        .box(
            frame_thickness,
            0.5 * window_height - 2 * frame_thickness,
            thickness)
        .translate((
            0,
            0.25 * window_height - 1.5 * frame_thickness,
            0.5 * thickness))
    )

    window_panel = panel - hole_1 - hole_2 + center_frame
    return window_panel


def window_layer_2(thickness):
    window_margin = 5
    window_width = 14
    window_height = 23
    frame_thickness = 0.5

    panel = (
        Workplane("XY")
        .box(
            window_width + 2 * window_margin,
            window_height + 2 * window_margin,
            thickness)
        .translate((0, 0, 0.5 * thickness))
    )

    hole_1 = (
        Workplane("XY")
        .box(
            window_width - 2 * frame_thickness,
            0.5 * window_height - 0 * frame_thickness,
            10)
        .translate((
            0,
            0.25 * window_height,
            0))
    )

    hole_2 = (
        Workplane("XY")
        .box(
            window_width - 4 * frame_thickness,
            0.5 * window_height - 4 * frame_thickness,
            10)
        .translate((
            0,
            -0.25 * window_height + 1 * frame_thickness,
            0))
    )

    center_frame = (
        Workplane("XY")
        .box(
            frame_thickness,
            0.5 * window_height - 4 * frame_thickness,
            thickness)
        .translate((
            0,
            -0.25 * window_height + 1 * frame_thickness,
            0.5 * thickness))
    )

    window_panel = panel - hole_1 - hole_2 + center_frame
    return window_panel


def house_front(
    width, height, thickness, tab_left, tab_right, tab_bottom, tab_top
):
    panel = rect(
        width=width, height=height, thickness=thickness,
        tab_left=tab_left, tab_right=tab_right, tab_bottom=tab_bottom,
        tab_top=tab_top
    )
    
    win0 = (
       Workplane("XY")
        .box(12, 16, 10)
        .translate((-30, -5, 0))
    )
    win1 = (
        Workplane("XY")
        .box(12, 28, 10)
        .translate((0, 1, 0))
    )
    win2 = (
        Workplane("XY")
        .box(12, 16, 10)
        .translate((30, -5, 0))
    )

    house_front = panel - win0 - win1 - win2

    return house_front


def _gable_panel(width, height, gable_height, thickness):
    return (
        Workplane("XY")
        .sketch()
        .polygon(
            [
                (-0.5 * width, 0.5 * height),
                (-0.5 * width, -0.5 * height),
                (0.5 * width, -0.5 * height),
                (0.5 * width, 0.5 * height),
                (0, 0.5 * height + gable_height)
            ],
            mode="a"
        )
        .finalize()
        .extrude(thickness)
    )


def gable_wall(
    width, height, gable_height, thickness, tab_left, tab_bottom, tab_right,
    tab_top_right, tab_top_left
):
    panel = _gable_panel(
        width=width,
        height=height,
        gable_height=gable_height,
        thickness=thickness)

    panel_with_tabs = _add_tabs(
        panel=panel,
        tab_defs_dict={
            0: tab_left, 1: tab_bottom, 2: tab_right, 3: tab_top_right,
            4: tab_top_left
        })

    return panel_with_tabs


def gable_wall_with_chimney(
    width, height, gable_height, thickness, chimney_width, chimney_height,
    tab_left, tab_bottom, tab_right, tab_top_right, tab_top_left
):
    panel = _gable_panel(
        width=width,
        height=height,
        gable_height=gable_height,
        thickness=thickness)

    chimney = (
        Workplane("XY")
        .box(chimney_width, chimney_height * 2, thickness)
        .translate((0, 0.5 * height + gable_height, 0.5 * thickness))
    )

    panel_with_chimney = panel + chimney

    # 0 - left, 1 - top_left, 2 - bottom, 3 - chimney_left, 4 - right,
    # 5 - top_right, 6 - chimney_top, 7 - chimney_right
    panel_with_tabs = _add_tabs(
        panel=panel_with_chimney,
        tab_defs_dict={
            0: tab_left, 1: tab_top_left, 2: tab_bottom, 3: None,
            4: tab_right, 5: tab_top_right, 6: None, 7: None
        })

    return panel_with_tabs


def roof_panel(
    width, gable_width, gable_height, rafter_length, thickness,
    overhang_length, cut_slots=True
):

    roof_len = math.sqrt(
        0.25 * gable_width * gable_width +
        gable_height * gable_height) + overhang_length

    panel = (
        Workplane("XY")
        .box(width, roof_len, thickness)
        .translate((0, 0, 0.5 * thickness))
    )
    if not cut_slots:
        return panel

    rafter_width = 0.56 * 4
    rafter_count = 9
    for i in range(rafter_count):
        x = -0.5 * (width - thickness) + (width - thickness) * (i / (rafter_count - 1))
        top_slot = (
            Workplane("XY")
            .box(rafter_width, 2 * rafter_length, 10)
            .translate((x, 0.5 * roof_len, 0))
        )
        bottom_slot = (
            Workplane("XY")
            .box(rafter_width, 2 * rafter_length, 10)
            .translate((x, -0.5 * roof_len, 0))
        )
        panel = panel - top_slot - bottom_slot

    return panel


def rafter_extension(
    gable_width, gable_height, length, thickness
):
    roof_a = math.atan2(gable_height, 0.5 * gable_width) * 180 / math.pi
    d = thickness * math.tan(math.radians(roof_a))

    return (
        Workplane("XY")
        .sketch()
        .polygon(
            [
                (0, 0),
                (length + d, 0),
                (length, thickness),
                (0, thickness)
            ],
            mode="a"
        )
        .finalize()
        .extrude(thickness)
    )


def rafter(
    gable_width, gable_height, overhang_width, end_height, thickness
):
    roof_a = math.atan2(gable_height, 0.5 * gable_width) * 180 / math.pi
    tan_a = math.tan(math.radians(roof_a))
    t_width = 0.5 * (gable_width + overhang_width)
    t_height = t_width * tan_a
    # overhang_height = end_width * tan_a + end_height

    return (
        Workplane("XY")
        .sketch()
        .polygon(
            [
                (0, 0),
                (t_width, -t_height),
                (t_width, -t_height - end_height),
                (0, -end_height),
                (-t_width, -t_height - end_height),
                (-t_width, -t_height)
            ],
            mode="a"
        )
        .finalize()
        .extrude(thickness)
    )


def rake_edge(
    gable_width, gable_height, overhang_width, end_height, end_width,
    thickness
):
    roof_a = math.atan2(gable_height, 0.5 * gable_width) * 180 / math.pi
    tan_a = math.tan(math.radians(roof_a))
    t_width = 0.5 * (gable_width + overhang_width)
    t_height = t_width * tan_a
    overhang_height = end_width * tan_a + end_height

    return (
        Workplane("XY")
        .sketch()
        .polygon(
            [
                (0, 0),
                (t_width, -t_height),
                (t_width, -t_height - end_height),
                (t_width - end_width, -t_height - end_height),
                (0, -overhang_height),
                (-t_width + end_width, -t_height - end_height),
                (-t_width, -t_height - end_height),
                (-t_width, -t_height)
            ],
            mode="a"
        )
        .finalize()
        .extrude(thickness)
    )


def rake_edge_with_tabs(
    gable_width, gable_height, overhang_width, end_height, end_width,
    thickness
):
    panel = rake_edge(
        gable_width=gable_width,
        gable_height=gable_height,
        overhang_width=overhang_width,
        end_height=end_height,
        end_width=end_width,
        thickness=thickness)
    
    tab_top_left = {"type": Tab.IN, "width": 30, "height": thickness, "offset": 0, "thickness": thickness}
    tab_top_right = {"type": Tab.IN, "width": 30, "height": thickness, "offset": 0, "thickness": thickness}
    tab_left = {"type": Tab.IN, "width": 0.5 * end_height, "height": thickness, "offset": 0.25 * end_height, "thickness": thickness}
    tab_right = {"type": Tab.IN, "width": 0.5 * end_height, "height": thickness, "offset": -0.25 * end_height, "thickness": thickness}
    # 0 - top_right, 1 - right, 6 - left, 7 - top_left
    panel_with_tabs = _add_tabs(
        panel=panel,
        tab_defs_dict={
            0: tab_top_right, 1: tab_right, 2: None, 3: None,
            4: None, 5: None, 6: tab_left, 7: tab_top_left
        })

    return panel_with_tabs


def _add_tabs(panel, tab_defs_dict):
    face_index = -1

    def union_face_fn(face):
        nonlocal face_index
        face_index += 1
        normal = face.normalAt()
        a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
        
        tab_def = tab_defs_dict[face_index]
        if tab_def is None or tab_def["type"] != Tab.OUT:
            return (
                Workplane("XY")
                .box(0.2, 0.2, 0.2)
                .translate((0, 0, 0.5))
                .val()
            )
        
        return (
            Workplane(face)
            .box(tab_def["width"], 2 * tab_def["height"], tab_def["thickness"])
            .translate((
                tab_def["offset"] * math.cos(math.radians(a)),
                tab_def["offset"] * math.sin(math.radians(a)),
                0
            ))
            .rotateAboutCenter(
                (0, 0, 1), a)
            .val()
        )

    union_shapes = (
        panel
        .faces("#Z")
        .each(union_face_fn, combine=False)
    )

    face_index_2 = -1

    def cut_face_fn(face):
        nonlocal face_index_2
        face_index_2 += 1
        normal = face.normalAt()
        a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
        
        tab_def = tab_defs_dict[face_index_2]
        if tab_def is None or tab_def["type"] != Tab.IN:
            return (
                Workplane("XY")
                .box(0.1, 0.1, 0.1)
                .translate((0, 0, 0.5))
                .val()
            )
        
        return (
            Workplane(face)
            .box(tab_def["width"], 2 * tab_def["height"], tab_def["thickness"])
            .translate((
                tab_def["offset"] * math.cos(math.radians(a)),
                tab_def["offset"] * math.sin(math.radians(a)),
                0
            ))
            .rotateAboutCenter(
                (0, 0, 1), a)
            .val()
        )

    cut_shapes = (
        panel
        .faces("#Z")
        .each(cut_face_fn, combine=False)
    )

    result = panel - cut_shapes + union_shapes

    return result
