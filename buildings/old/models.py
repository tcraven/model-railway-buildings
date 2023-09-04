import math
from cadquery import Assembly
from buildings.old import media
from buildings.old import panels
from buildings.old import Tab
from buildings.old import vertices


class ModelBase:
    def compute_panel_vertices(self):
        self.panels_by_name = { p["name"]: p for p in self.panels }
        for panel in self.panels:
            # Get loops of vertices
            panel["vertices"] = vertices.get_panel_vertex_loops(workplane=panel["workplane"])
        
            # Calculate the width and height of the panels
            (
                panel["width"],
                panel["height"],
                panel["center_offset_x"],
                panel["center_offset_y"]
            ) = vertices.get_width_height(panel_vertices=panel["vertices"])


class WindowTest(ModelBase):

    def __init__(self, name):
        self.name = name
        self.thickness_b = media.get_media_thickness(media_name="2x1.69mm")
        self.thickness_f = media.get_media_thickness(media_name="2x0.56mm")
        self.thickness = media.get_media_thickness(media_name="0.56mm")

        self.panels = []
        self.assembly = None

        self.create_panels()
        self.compute_panel_vertices()
        self.create_assembly()

    def create_panels(self):
        self.panels = [
            {
                "name": "front_base",
                "media_name": "2x1.69mm",
                "workplane": panels.front_with_windows(
                    width=90,
                    height=50,
                    thickness=self.thickness_b,
                    window_margin=5
                )
            },
            {
                "name": "front",
                "media_name": "2x0.56mm",
                "workplane": panels.front_with_windows(
                    width=90,
                    height=50,
                    thickness=self.thickness_f,
                    window_margin=0
                )
            },
            {
                "name": "win_1",
                "media_name": "0.56mm",
                "workplane": panels.window_single_layer(
                    thickness=self.thickness,
                    center_frame_thickness=0.5)
            },
            {
                "name": "win_1_sill",
                "media_name": "0.56mm",
                "workplane": panels.window_sill(thickness=self.thickness)
            },
            {
                "name": "win_2",
                "media_name": "0.56mm",
                "workplane": panels.window_single_layer(
                    thickness=self.thickness,
                    center_frame_thickness=0.75)
            },
            {
                "name": "win_2_sill",
                "media_name": "0.56mm",
                "workplane": panels.window_sill(thickness=self.thickness)
            },
            {
                "name": "win_3",
                "media_name": "0.56mm",
                "workplane": panels.window_single_layer(
                    thickness=self.thickness,
                    center_frame_thickness=1)
            }
        ]

    def create_assembly(self):
        self.assembly = (
            Assembly(name=self.name)
            .add(
                (
                    self.panels_by_name["front_base"]["workplane"]
                ),
                name="front_base"
            )
            .add(
                (
                    self.panels_by_name["front"]["workplane"]
                    .translate((0, 0, self.thickness_b))
                ),
                name="front"
            )
            .add(
                (
                    self.panels_by_name["win_1"]["workplane"]
                    .translate((-20, 0, self.thickness_b - 1 * self.thickness))
                ),
                name="win_1"
            )
            # .add(
            #     (
            #         self.panels_by_name["win_1_2"]["workplane"]
            #         .translate((-20, 0, self.thickness_b - 2 * self.thickness))
            #     ),
            #     name="win_1_2"
            # )
            .add(
                (
                    self.panels_by_name["win_1_sill"]["workplane"]
                    .translate((-20, -12.5, self.thickness_b + 2 * self.thickness))
                ),
                name="win_1_sill"
            )

            .add(
                (
                    self.panels_by_name["win_2"]["workplane"]
                    .translate((20, 0, self.thickness_b - 1 * self.thickness))
                ),
                name="win_2"
            )
            # .add(
            #     (
            #         self.panels_by_name["win_2_2"]["workplane"]
            #         .translate((20, 0, self.thickness_b - 2 * self.thickness))
            #     ),
            #     name="win_2_2"
            # )
            .add(
                (
                    self.panels_by_name["win_2_sill"]["workplane"]
                    .translate((20, -12.5, self.thickness_b + 2 * self.thickness))
                ),
                name="win_2_sill"
            )
        )


# ==================================================
# ==================================================
# ==================================================

class Roof(ModelBase):
    
    def __init__(
        self, name, width, gable_width, gable_height, rafter_length,
        overhang_length
    ):
        self.name = name
        self.width = width
        self.gable_width = gable_width
        self.gable_height = gable_height
        self.rafter_length = rafter_length
        self.overhang_length = overhang_length

        self.thickness = media.get_media_thickness(media_name="1.69mm")
        self.panels = []
        self.assembly = None

        self.create_panels()
        self.compute_panel_vertices()
        self.create_assembly()
    
    def create_panels(self):
        self.panels = [
            {
                "name": "roof",
                "media_name": "1.69mm",
                "workplane": panels.roof_panel(
                    width=self.width,
                    gable_width=self.gable_width,
                    gable_height=self.gable_height,
                    rafter_length=self.rafter_length,
                    thickness=self.thickness,
                    overhang_length=self.overhang_length
                )
            },
            {
                "name": "roof_2",
                "media_name": "0.56mm",
                "workplane": panels.roof_panel(
                    width=self.width,
                    gable_width=self.gable_width,
                    gable_height=self.gable_height,
                    rafter_length=self.rafter_length,
                    thickness=self.thickness,
                    overhang_length=self.overhang_length,
                    cut_slots=False
                )
            }
        ]
        for i in range(18 * 4):
            self.panels.append({
                "name": f"rafter_{i}",
                "media_name": "0.56mm",
                "workplane": panels.rafter_extension(
                    gable_width=self.gable_width,
                    gable_height=self.gable_height,
                    length=self.rafter_length,
                    thickness=self.thickness)
            })

    
    def create_assembly(self):
        self.assembly = (
            Assembly(name=self.name)
            .add(
                (
                    self.panels_by_name["roof"]["workplane"]
                    # .rotate((0, 0, 0), (1, 0, 0), 180)
                    # .translate((0, 0, self.thickness))
                ),
                name="roof"
            )
        )


# ==================================================
# ==================================================
# ==================================================


class House_1(ModelBase):

    def __init__(
        self, length, width, height, gable_height, chimney_width,
        chimney_height, name
    ):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.gable_height = gable_height
        self.chimney_width = chimney_width
        self.chimney_height = chimney_height
        
        # Use 2 x 1.69mm corrugated card for most panels
        self.thickness = media.get_media_thickness(media_name="2x1.69mm")
        self.panels = []
        self.assembly = None

        self.create_panels()
        self.compute_panel_vertices()
        self.create_assembly()

    def create_panels(self):
        roof_len = math.sqrt(
            0.25 * self.width * self.width +
            self.gable_height * self.gable_height)
        roof_a = math.atan2(self.gable_height, 0.5 * self.width) * 180 / math.pi
        chimney_roof_len = 0.5 * self.chimney_width / math.cos(math.radians(roof_a))

        self.panels = [
            {
                "name": "bottom",
                "media_name": "2x1.69mm",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=self.width - 2 * self.thickness,
                    thickness=self.thickness,
                    tab_top={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_left={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_bottom={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_right={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness}
                )
            },
            {
                "name": "front_roof",
                "media_name": "2x1.69mm",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=roof_len - self.thickness,
                    thickness=self.thickness,
                    tab_top={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_left={"type": Tab.OUT, "width": 25, "height": self.thickness, "offset": 0.5 * self.thickness + 0.5 * chimney_roof_len, "thickness": self.thickness},
                    tab_bottom={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_right={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": -0.5 * self.thickness, "thickness": self.thickness},
                    extra_hole={"x": -0.5 * self.length, "y": 0.5 * roof_len, "width": 2 * 2.5 * self.thickness + 2, "height": 30}
                )
            },
            {
                "name": "back_roof",
                "media_name": "2x1.69mm",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=roof_len - 1 - 2 * self.thickness * math.tan(math.radians(roof_a)),
                    thickness=self.thickness,
                    tab_top={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_left={"type": Tab.OUT, "width": 25, "height": self.thickness, "offset": -0.5 * chimney_roof_len, "thickness": self.thickness},
                    tab_bottom={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_right={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    extra_hole={"x": -0.5 * self.length, "y": -0.5 * roof_len, "width": 2 * 2.5 * self.thickness + 2, "height": 27}
                )
            },
            {
                "name": "back",
                "media_name": "2x1.69mm",
                "workplane": panels.rect(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_top={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_left={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_bottom={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_right={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness}
                )
            },
            {
                "name": "front",
                "media_name": "2x1.69mm",
                "workplane": panels.house_front(  # rect(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_top={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_left={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_bottom={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_right={"type": Tab.OUT, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness}
                )
            },
            {
                "name": "left",
                "media_name": "2x1.69mm",
                "workplane": panels.gable_wall_with_chimney(
                    width=self.width,
                    height=self.height,
                    gable_height=self.gable_height,
                    chimney_width=self.chimney_width,
                    chimney_height=self.chimney_height,
                    thickness=self.thickness,
                    tab_left={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_right={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_bottom={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_top_right={"type": Tab.IN, "width": 25, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_top_left={"type": Tab.IN, "width": 25, "height": self.thickness, "offset": 0, "thickness": self.thickness}
                )
            },
            {
                "name": "right",
                "media_name": "2x1.69mm",
                "workplane": panels.gable_wall(
                    width=self.width,
                    height=self.height,
                    gable_height=self.gable_height,
                    thickness=self.thickness,
                    tab_left={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_right={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_bottom={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_top_right={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness},
                    tab_top_left={"type": Tab.IN, "width": 30, "height": self.thickness, "offset": 0, "thickness": self.thickness}
                )
            },
            {
                "name": "chimney_1",
                "media_name": "2x1.69mm",
                "workplane": panels.rect(
                    width=self.chimney_width,
                    height=2 * self.chimney_height,
                    thickness=self.thickness,
                    tab_left=None,
                    tab_bottom=None,
                    tab_right=None,
                    tab_top=None
                )
            },
            {
                "name": "chimney_2",
                "media_name": "1.69mm",
                "workplane": panels.rect(
                    width=self.chimney_width,
                    height=2 * self.chimney_height,
                    thickness=0.5 * self.thickness,
                    tab_left=None,
                    tab_bottom=None,
                    tab_right=None,
                    tab_top=None
                )
            }
        ]

    def create_assembly(self):
        # Panels are rotated so that their top face is pointed outwards, and
        # translated so that the tabs fit together

        roof_a = math.atan2(self.gable_height, 0.5 * self.width) * 180 / math.pi

        self.assembly = (
            Assembly(name=self.name)
            .add(
                (
                    self.panels_by_name["bottom"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), 180)
                    .translate((0, 0, self.thickness))
                ),
                name="bottom"
            )
            .add(
                (
                    self.panels_by_name["front_roof"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), roof_a)
                    .translate((
                        0,
                        -0.25 * self.width                      + 0.5 * self.thickness * math.cos(math.radians(roof_a))     + self.thickness * math.sin(math.radians(roof_a)),
                        self.height + 0.5 * self.gable_height   + 0.5 * self.thickness * math.sin(math.radians(roof_a))     - self.thickness * math.cos(math.radians(roof_a))
                    ))
                ),
                name="front_roof"
            )
            .add(
                (
                    self.panels_by_name["back_roof"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), -roof_a)
                    .translate((
                        0,
                        0.25 * self.width                       - 0.0 * self.thickness * math.cos(math.radians(roof_a)) - self.thickness * math.sin(math.radians(roof_a))     ,
                        self.height + 0.5 * self.gable_height   + 0.0 * self.thickness * math.sin(math.radians(roof_a)) - self.thickness * math.cos(math.radians(roof_a))
                    ))
                ),
                name="back_roof"
            )
            .add(
                (
                    self.panels_by_name["back"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), 90)
                    .translate((0, -(0.5 * self.width - self.thickness), 0.5 * self.height))
                ),
                name="back"
            )
            .add(
                (
                    self.panels_by_name["front"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), -90)
                    .translate((0, 0.5 * self.width - self.thickness, 0.5 * self.height))
                ),
                name="front"
            )
            .add(
                (
                    self.panels_by_name["left"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), 90)
                    .rotate((0, 0, 0), (0, 0, 1), -90)
                    .translate((-(0.5 * self.length - self.thickness), 0, 0.5 * self.height))
                ),
                name="left"
            )
            .add(
                (
                    self.panels_by_name["right"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), 90)
                    .rotate((0, 0, 0), (0, 0, 1), 90)
                    .translate((0.5 * self.length - self.thickness, 0, 0.5 * self.height))
                ),
                name="right"
            )
            .add(
                (
                    self.panels_by_name["chimney_1"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), 90)
                    .rotate((0, 0, 0), (0, 0, 1), 90)
                    .translate((-0.5 * self.length + self.thickness, 0, self.height + self.gable_height))
                ),
                name="chimney_1"
            )
            .add(
                (
                    self.panels_by_name["chimney_2"]["workplane"]
                    .rotate((0, 0, 0), (1, 0, 0), 90)
                    .rotate((0, 0, 0), (0, 0, 1), 90)
                    .translate((-0.5 * self.length + 2 * self.thickness, 0, self.height + self.gable_height))
                ),
                name="chimney_2"
            )
        )