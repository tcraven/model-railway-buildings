import copy
import math
from dataclasses import dataclass, field
from typing import Optional, Union
from cadquery import Assembly, Color, Workplane
from buildings import transforms_v2
from buildings.media_v2 import Media
from buildings.transforms_v2 import Transform
from buildings.tabs import Tab, TabDirection


def empty(type):
    return field(default_factory=type)


@dataclass
class Panel:
    name: str
    media: Media
    workplane: Workplane
    transform: Transform = empty(Transform)


@dataclass
class Cutout:
    workplane: Workplane
    subtract_from: list[str]
    transform: Transform = empty(Transform)


@dataclass
class PanelGroup:
    name: str
    panels: list[Panel] = empty(list)
    cutouts: list[Cutout] = empty(list)
    children: list["PanelGroup"] = empty(list)
    transform: Transform = empty(Transform)


def get_all_panels(panel_group: PanelGroup, name_prefix: str = "") -> list[Panel]:
    """
    Get a list of all panels for all nested child PanelGroups. The returned
    panels are copies of the originals with names formed from the panel
    hierarchy to ensure that all panels have a unique name.
    """
    panels = []
    for index, panel in enumerate(panel_group.panels):
        copied_panel = copy.copy(panel)
        copied_panel.name = f"{name_prefix}{panel_group.name}_p{index}_{panel.name}"
        panels.append(copied_panel)
    
    for index, pg in enumerate(panel_group.children):
        child_name_prefix = f"{name_prefix}{panel_group.name}_c{index}_"
        panels.extend(get_all_panels(panel_group=pg, name_prefix=child_name_prefix))
    
    return panels


def get_all_transformed_workplanes(panel_group: PanelGroup) -> list[Workplane]:
    """
    Get a list of transformed workplanes from the PanelGroup by transforming
    all child panels and panel groups.
    """
    # print("get_transfored_workplanes", panel_group)
    transformed_workplanes = []
    for panel in panel_group.panels:
        wp = transforms_v2.apply_transform(
            workplane=panel.workplane,
            transform=panel.transform
        )
        transformed_workplanes.append(wp)
    
    for pg in panel_group.children:
        wps = get_all_transformed_workplanes(panel_group=pg)
        for wp in wps:
            wp = transforms_v2.apply_transform(
                workplane=wp,
                transform=pg.transform
            )
            transformed_workplanes.append(wp)
    
    return transformed_workplanes


def apply_cutouts_from_children(panel_group: PanelGroup) -> None:
    """
    Get the cutouts from the direct children and apply them.
    """
    panels_by_name = {panel.name: panel for panel in panel_group.panels}

    for child_pg in panel_group.children:
        for cutout in child_pg.cutouts:
            cutout_wp = cutout.workplane
            cutout_wp = transforms_v2.apply_transform(
                workplane=cutout_wp,
                transform=cutout.transform
            )
            cutout_wp = transforms_v2.apply_transform(
                workplane=cutout_wp,
                transform=child_pg.transform
            )
            for panel_name in cutout.subtract_from:
                if panel_name not in panels_by_name:
                    print(
                        "apply_cutouts_from_children: panel name: "
                        f"{panel_name} not found in panel group: "
                        f"{panel_group.name}")
                    continue

                panel = panels_by_name[panel_name]

                # panel.workplane = panel.workplane - cutout_wp

                # Cut the cutout from the panel as follows:
                # - Apply the panel local transform
                # - Cut the cutout from the panel
                # - Apply the reverse panel local transform to return it
                #   to its original position
                panel_wp = panel.workplane
                panel_wp = transforms_v2.apply_transform(
                    workplane=panel_wp,
                    transform=panel.transform)
                panel_wp = panel_wp - cutout_wp
                panel_wp = transforms_v2.apply_reverse_transform(
                    workplane=panel_wp,
                    transform=panel.transform)
                panel.workplane = panel_wp

    return None


def add_child_panel_group(parent: PanelGroup, child: PanelGroup) -> None:
    """
    When a child is added, cutouts are applied to the parent panel workplanes
    as necessary.
    """
    parent.children.append(child)
    apply_cutouts_from_children(panel_group=parent)


def get_child_panel_group(panel_group: PanelGroup, name: str) -> PanelGroup:
    for child_pg in panel_group.children:
        if child_pg.name == name:
            return child_pg
        
    raise Exception(f"Child panel group not found: {name}")


def get_assembly(panel_group: PanelGroup) -> Assembly:
    workplanes = get_all_transformed_workplanes(panel_group=panel_group)
    panels = get_all_panels(panel_group=panel_group)
    panel_names = [p.name for p in panels]
    panel_media_descs = [p.media.description for p in panels]

    # This works because the panels are processed in the same order by both
    # functions
    named_workplanes = zip(panel_names, panel_media_descs, workplanes)

    assembly = Assembly(name=panel_group.name)
    for panel_name, panel_media_desc, workplane in named_workplanes:
        if "corrugated" in panel_media_desc:
            color = Color(0.83, 0.64, 0.42, 1)
        else:
            color = Color(1, 1, 1, 1)
        assembly.add(workplane, name=panel_name, color=color)
    
    return assembly


# ======================================================================
# ======================================================================
# ======================================================================
# TO DO: Put utility functions in separate modules?

def basic_rect(width: float, height: float, thickness: float) -> Workplane:
    return (
        Workplane("XY")
        .box(width, height, thickness)
        .translate((0, 0, 0.5 * thickness))
    )


def basic_rect_with_hole(
    width: float,
    height: float,
    thickness: float,
    hole_width: float,
    hole_height: float,
    hole_offset_x: float,
    hole_offset_y: float
) -> Workplane:
    panel = (
        Workplane("XY")
        .box(width, height, thickness)
        .translate((0, 0, 0.5 * thickness))
    )
    hole = (
        Workplane("XY")
        .box(hole_width, hole_height, 10)
        .translate((hole_offset_x, hole_offset_y, 0))
    )
    return panel - hole


def rect(
    width: float,
    height: float,
    thickness: float,
    tab_left: Optional[Tab],
    tab_right: Optional[Tab],
    tab_bottom: Optional[Tab],
    tab_top: Optional[Tab]
) -> Workplane:
    rect = (
        Workplane("XY")
        .box(width, height, thickness)
        .translate((0, 0, 0.5 * thickness))
    )
    rect_with_tabs = _add_tabs(
        panel_workplane=rect,
        tabs_dict={0: tab_left, 1: tab_right, 2: tab_bottom, 3: tab_top})

    return rect_with_tabs


def chamfered_hole(width: float, height: float, chamfer: float = 5) -> Workplane:
    return (
        chamfered_rect(
            width=width,
            height=height,
            thickness=100,
            chamfer=chamfer
        )
        .translate((0, 0, -50))
    )

def chamfered_rect(width: float, height: float, thickness: float, chamfer: float = 5) -> Workplane:
    return (
        Workplane("XY")
        .sketch()
        .rect(width, height)
        .vertices()
        .chamfer(chamfer)
        .finalize()
        .extrude(thickness)
    )


def semicircle_panel(radius: float, thickness: float) -> Workplane:
    return (
        Workplane("XY")
        .moveTo(radius, 0)
        .threePointArc((0, radius), (-radius, 0))
        .close()
        .extrude(thickness)
    )


def arch(width: float, height: float, thickness: float) -> Workplane:
    if height <= 0.5 * width:
        raise Exception("Arch height must be greater than half its width")

    arch_box_wp = (
        Workplane("XY")
        .box(width, height - 0.5 * width, thickness)
        .translate((0, -0.25 * width, 0.5 * thickness))
    )
    arch_semicircle_wp = (
        semicircle_panel(
            radius=0.5 * width,
            thickness=thickness
        )
        .translate((
            0,
            0.5 * (height - width),
            0
        ))
    )
    return arch_box_wp + arch_semicircle_wp


def gable_panel(
    width: float,
    height: float,
    gable_height: float,
    thickness: float,
    tab_left: Optional[Tab] = None,
    tab_bottom: Optional[Tab] = None,
    tab_right: Optional[Tab] = None,
    tab_top_right: Optional[Tab] = None,
    tab_top_left: Optional[Tab] = None
) -> Workplane:
    panel_wp = _gable_panel(
        width=width,
        height=height,
        gable_height=gable_height,
        thickness=thickness)

    panel_with_tabs = _add_tabs(
        panel_workplane=panel_wp,
        tabs_dict={
            0: tab_left, 1: tab_bottom, 2: tab_right, 3: tab_top_right,
            4: tab_top_left
        })

    return panel_with_tabs


def _gable_panel(
    width: float,
    height: float,
    gable_height: float,
    thickness: float
) -> Workplane:
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


def _add_tabs(
    panel_workplane: Workplane,
    tabs_dict: dict[int, Optional[Tab]]
) -> Workplane:
    face_index = -1

    def union_face_fn(face):
        nonlocal face_index
        face_index += 1
        normal = face.normalAt()
        a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
        tab = tabs_dict[face_index]
        if tab is None or tab.direction != TabDirection.OUT:
            return (
                Workplane("XY")
                .box(0.02, 0.02, 0.02)
                .translate((0, 0, 0.02))
                .val()
            )
        
        return (
            Workplane(face)
            .box(tab.width, 2 * tab.height, tab.thickness)
            .translate((
                tab.offset * math.cos(math.radians(a)),
                tab.offset * math.sin(math.radians(a)),
                0
            ))
            .rotateAboutCenter(
                (0, 0, 1), a)
            .val()
        )

    union_shapes = (
        panel_workplane
        .faces("#Z")
        .each(union_face_fn, combine=False)
    )

    face_index_2 = -1

    def cut_face_fn(face):
        nonlocal face_index_2
        face_index_2 += 1
        normal = face.normalAt()
        a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
        
        tab = tabs_dict[face_index_2]
        if tab is None or tab.direction != TabDirection.IN:
            return (
                Workplane("XY")
                .box(0.01, 0.01, 0.01)
                .translate((0, 0, 0.02))
                .val()
            )
        
        return (
            Workplane(face)
            .box(tab.width, 2 * tab.height, tab.thickness)
            .translate((
                tab.offset * math.cos(math.radians(a)),
                tab.offset * math.sin(math.radians(a)),
                0
            ))
            .rotateAboutCenter(
                (0, 0, 1), a)
            .val()
        )

    cut_shapes = (
        panel_workplane
        .faces("#Z")
        .each(cut_face_fn, combine=False)
    )

    result = panel_workplane - cut_shapes + union_shapes

    return result
