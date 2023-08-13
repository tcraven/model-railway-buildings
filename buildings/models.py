import math
from cadquery import Assembly
from buildings import panels
from buildings import Tab
from buildings import vertices


class ModelBase:
    def compute_panel_vertices(self):
        self.panels_by_name = { p["name"]: p for p in self.panels }
        for panel in self.panels:
            # if panel["name"] != "left":
            #     continue

            # Get loops of vertices
            panel["vertices"] = vertices.get_panel_vertex_loops(panel=panel["workplane"])
        
            # Calculate the width and height of the panels
            (
                panel["width"],
                panel["height"],
                panel["center_offset_x"],
                panel["center_offset_y"]
            ) = vertices.get_width_height(panel_vertices=panel["vertices"])


class Box(ModelBase):

    def __init__(self, length, width, height, thickness, name):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.thickness = thickness
        self.panels = []
        self.assembly = None

        self.create_panels()
        self.compute_panel_vertices()
        self.create_assembly()

    def create_panels(self):
        self.panels = [
            {
                "name": "bottom",
                "workplane": panels.rect(
                    width=self.length - 2 * self.thickness,
                    height=self.width - 2 * self.thickness,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.OUT,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.OUT,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "top",
                "workplane": panels.rect(
                    width=self.length - 2 * self.thickness,
                    height=self.width - 2 * self.thickness,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.OUT,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.OUT,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "back",
                "workplane": panels.rect(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "front",
                "workplane": panels.rect(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "left",
                "workplane": panels.rect(
                    width=self.height,
                    height=self.width,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.IN,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.IN
                )
            },
            {
                "name": "right",
                "workplane": panels.rect(
                    width=self.height,
                    height=self.width,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.IN,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.IN
                )
            }
        ]

    def create_assembly(self):
        # Panels are rotated so that their top face is pointed outwards, and
        # translated so that the tabs fit together
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
                    self.panels_by_name["top"]["workplane"]
                    .translate((0, 0, self.height - self.thickness))
                ),
                name="top"
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
                    .rotate((0, 0, 0), (0, 1, 0), -90)
                    .translate((-(0.5 * self.length - self.thickness), 0, 0.5 * self.height))
                ),
                name="left"
            )
            .add(
                (
                    self.panels_by_name["right"]["workplane"]
                    .rotate((0, 0, 0), (0, 1, 0), 90)
                    .translate((0.5 * self.length - self.thickness, 0, 0.5 * self.height))
                ),
                name="right"
            )            
        )


class BoxWithHoles(Box):
    def create_panels(self):
        self.panels = [
            {
                "name": "bottom",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=self.width - 2 * self.thickness,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.OUT,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.OUT,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "top",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=self.width - 2 * self.thickness,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.OUT,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.OUT,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "back",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "front",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "left",
                "workplane": panels.rect_with_hole(
                    width=self.height,
                    height=self.width,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.IN,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.IN
                )
            },
            {
                "name": "right",
                "workplane": panels.rect_with_hole(
                    width=self.height,
                    height=self.width,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.IN,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.IN
                )
            }
        ]


class House_1(Box):

    def __init__(self, length, width, height, gable_height, thickness, name):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.gable_height = gable_height
        self.thickness = thickness
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

        self.panels = [
            {
                "name": "bottom",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=self.width - 2 * self.thickness,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.OUT,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.OUT,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "front_roof",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=roof_len - 1 - 2 * self.thickness * math.tan(math.radians(roof_a)),
                    # height=roof_len - 3 * self.thickness,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "back_roof",
                "workplane": panels.rect_with_hole(
                    width=self.length - 2 * self.thickness,
                    height=roof_len - 1 - 2 * self.thickness * math.tan(math.radians(roof_a)),
                    # height=roof_len - 3 * self.thickness,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "back",
                "workplane": panels.rect(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "front",
                "workplane": panels.rect(
                    width=self.length - 2 * self.thickness,
                    height=self.height,
                    thickness=self.thickness,
                    tab_length=30,
                    tab_top=Tab.IN,
                    tab_left=Tab.OUT,
                    tab_bottom=Tab.IN,
                    tab_right=Tab.OUT
                )
            },
            {
                "name": "left",
                "workplane": panels.gable_wall(
                    width=self.width,
                    height=self.height,
                    gable_height=self.gable_height,
                    thickness=self.thickness,
                    wall_tab_length=30,
                    gable_tab_length=30
                )
            },
            {
                "name": "right",
                "workplane": panels.gable_wall(
                    width=self.width,
                    height=self.height,
                    gable_height=self.gable_height,
                    thickness=self.thickness,
                    wall_tab_length=30,
                    gable_tab_length=30
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
                        -0.25 * self.width + self.thickness * math.sin(math.radians(roof_a)),
                        self.height + 0.5 * self.gable_height - self.thickness * math.cos(math.radians(roof_a))
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
        )