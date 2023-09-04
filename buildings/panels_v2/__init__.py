import copy
from dataclasses import dataclass, field
from typing import Union
from cadquery import Assembly, Workplane
from buildings import transforms_v2
from buildings.media_v2 import Media
from buildings.transforms_v2 import Transform

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
            wp = cutout.workplane
            wp = transforms_v2.apply_transform(
                workplane=wp,
                transform=cutout.transform
            )
            wp = transforms_v2.apply_transform(
                workplane=wp,
                transform=child_pg.transform
            )
            for panel_name in cutout.subtract_from:
                panel = panels_by_name[panel_name]
                panel.workplane = panel.workplane - wp

    return None


def add_child_panel_group(parent: PanelGroup, child: PanelGroup) -> None:
    """
    When a child is added, cutouts are applied to the parent panel workplanes
    as necessary.
    """
    parent.children.append(child)
    apply_cutouts_from_children(panel_group=parent)


def get_assembly(panel_group: PanelGroup) -> Assembly:
    workplanes = get_all_transformed_workplanes(panel_group=panel_group)
    panels = get_all_panels(panel_group=panel_group)
    panel_names = [p.name for p in panels]
    # This works because the panels are processed in the same order by both
    # functions
    named_workplanes = zip(panel_names, workplanes)

    assembly = Assembly(name=panel_group.name)
    for panel_name, workplane in named_workplanes:
        assembly.add(workplane, name=panel_name)
    
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
