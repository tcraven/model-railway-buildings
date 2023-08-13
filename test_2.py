import re
from cadquery import Assembly, Workplane
from cadquery import exporters


THICKNESS = 2
TAB_MARGIN = 20
MIN_TAB_LEN = 10


def panel_sketch(
    length,
    width,
    roof_width,
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

    #if tabs_outside_x:
    #    length = length - 2 * thickness
    #if tabs_outside_y:
    #    width = width - 2 * thickness

    return (
        Workplane("XY")
        .sketch()
        
        # Panel
        #.rect(length, width)
        .polygon(
            [
                (-0.5 * length, 0.5 * width),
                (0, 0.5 * width + roof_width),
                (0.5 * length, 0.5 * width),
                (0.5 * length, -0.5 * width),
                (-0.5 * length, -0.5 * width),
            ],
            mode="a"
        )
        
        # Select bottom edge and add the tab
        .edges()
        .rect(x_tab_len, 2 * thickness, mode=rect_mode_y)
        
        # Select the left and right edges and add the tabs
        #.reset()
        #.edges(">X or <X")
        #.rect(2 * thickness, y_tab_len, mode=rect_mode_x)
        
        .reset()
        
        
        # Remove the internal wires
        .clean()
    )


def panel(panel_sketch, thickness=THICKNESS):
    return (
        panel_sketch
        .finalize()
        .extrude(thickness)
    )

show_object(panel_sketch(length=60, width=40, roof_width=20))
