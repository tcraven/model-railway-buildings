import cadquery


def get_panel_sketch(width, height, tabs_outside=True, thickness=2, tab_margin=30):
    x_tab_len = width - 2 * tab_margin
    y_tab_len = height - 2 * tab_margin
    rect_mode = "a" if tabs_outside else "s"
    return (
        cadquery
        .Workplane("XY")
        .sketch()
        
        # Panel
        .rect(width, height)
        
        # Select the top and bottom edges and add the tabs
        .edges(">Y or <Y")
        .rect(x_tab_len, 2 * thickness, mode=rect_mode)
        
        # Select the left and right edges and add the tabs
        .reset()
        .edges(">X or <X")
        .rect(2 * thickness, y_tab_len, mode=rect_mode)
        
        # Remove the internal wires
        .clean()
    )
