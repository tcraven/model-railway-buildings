import math
from cadquery import Workplane
from buildings import Tab

"""
In three dimensions, we use the following terms:
x = length, y = width, z = height

All panels are created in the XY plane => they have width and height
"""

def rect(
    width, height, thickness, tab_length, tab_top, tab_left,
    tab_bottom, tab_right
):
    return (
        Workplane("XY")
        .sketch()
        .rect(width, height)

        # Create tabs
        .edges(">Y")
        .rect(tab_length, 2 * thickness, mode=_rect_mode(tab=tab_top))
        .reset()
        .edges("<Y")
        .rect(tab_length, 2 * thickness, mode=_rect_mode(tab=tab_bottom))
        .reset()
        .edges(">X")
        .rect(2 * thickness, tab_length, mode=_rect_mode(tab=tab_right))
        .reset()
        .edges("<X")
        .rect(2 * thickness, tab_length, mode=_rect_mode(tab=tab_left))
        .reset()

        # Remove the internal wires
        .clean()
        .finalize()
        .extrude(thickness)
    )


def rect_2(
    width, height, thickness, tab_length, tab_top, tab_left,
    tab_bottom, tab_right
):
    result = (
        Workplane("XY")
        .sketch()
        .rect(width, height)
    )

    # Select edges and add the tabs
    result = _add_tab(
        result=result,
        edges_query=">Y",
        tab_mode=tab_top,
        tab_length=tab_length,
        edge_length=width,
        thickness=thickness)
    # .edges(">Y")
    # .rect(tab_length, 2 * thickness, mode=_rect_mode(tab=tab_top))
    # .reset()

    result = _add_tab(
        result=result,
        edges_query="<Y",
        tab_mode=tab_bottom,
        tab_length=tab_length,
        edge_length=width,
        thickness=thickness)
    # .edges("<Y")
    # .rect(tab_length, 2 * thickness, mode=_rect_mode(tab=tab_bottom))
    # .reset()
        
    result = _add_tab(
        result=result,
        edges_query=">X",
        tab_mode=tab_right,
        tab_length=tab_length,
        edge_length=height,
        thickness=thickness)
    # .edges(">X")
    # .rect(2 * thickness, tab_length, mode=_rect_mode(tab=tab_right))
    # .reset()
    
    result = _add_tab(
        result=result,
        edges_query="<X",
        tab_mode=tab_left,
        tab_length=tab_length,
        edge_length=height,
        thickness=thickness)
    # .edges("<X")
    # .rect(2 * thickness, tab_length, mode=_rect_mode(tab=tab_left))
    # .reset()

    return (
        result

        # Remove the internal wires
        .clean()
        .finalize()
        .extrude(thickness)
    )


def rect_with_hole(
    width, height, thickness, tab_length, tab_top, tab_left,
    tab_bottom, tab_right
):
    return (
        rect(
            width=width, height=height, thickness=thickness,
            tab_length=tab_length, tab_top=tab_top, tab_left=tab_left,
            tab_bottom=tab_bottom, tab_right=tab_right
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


def gable_wall(
    width, height, gable_height, thickness, wall_tab_length, gable_tab_length
):
    roof_a = math.atan2(gable_height, 0.5 * width) * 180 / math.pi
    face_index = -1

    def face_loc_fn(loc):
        nonlocal face_index
        face_index += 1
        
        if face_index == 0:
            a = roof_a
            tab_len = gable_tab_length
        if face_index == 1:
            a = -roof_a
            tab_len = gable_tab_length
        if face_index == 2:
            a = 90
            tab_len = wall_tab_length
        if face_index == 3:
            a = 0
            tab_len = wall_tab_length
            # # Return shape with no overlap - no cut
            # return (
            #     Workplane(loc)
            #     .box(1, 1, 1)
            #     .translate((0, -5, 0))
            #     .val()
            # )
        if face_index == 4:
            a = 90
            tab_len = wall_tab_length

        return (
            Workplane(loc)
            .box(tab_len, thickness * 2, thickness)
            .rotateAboutCenter((0, 0, 1), a)
            .val()
        )

    return (
        Workplane("XY")
        .sketch()
        .polygon(
            [
                (-0.5 * width, 0.5 * height),
                (0, 0.5 * height + gable_height),
                (0.5 * width, 0.5 * height),
                (0.5 * width, -0.5 * height),
                (-0.5 * width, -0.5 * height),
            ],
            mode="a"
        )
        .finalize()
        .extrude(thickness)
        .faces("#Z")
        .cutEach(face_loc_fn)

        # .faces(">Z")
        # .center(10, -10)
        # .rect(16, 20)
        # .cutThruAll()

        # .faces(">Z")
        # .center(0, 10)
        # .circle(8)
        # .cutThruAll()

        # try .item(0) on faces?
    )


def _rect_mode(tab):
    return "a" if tab == Tab.OUT else "s"
