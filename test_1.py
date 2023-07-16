from cadquery import Assembly, Workplane


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


def box_assembly(length, width, height):
    bottom_ps = panel_sketch(
        length=length,
        width=width,
        tabs_outside_x=True,
        tabs_outside_y=True)

    top_ps = panel_sketch(
        length=length,
        width=width,
        tabs_outside_x=True,
        tabs_outside_y=True)

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
        Assembly()
        .add(bottom_p)
        .add(top_p)
        .add(left_p)
        .add(right_p)
        .add(front_p)
        .add(back_p)
    )

assembly = box_assembly(length=90, width=70, height=50)

#show_object(assembly)
