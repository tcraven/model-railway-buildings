import cadquery as cq
import math

counter = 0

def face_fn(face):
    global counter
    counter += 1
    normal = face.normalAt()
    a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
    return (
        cq.Workplane(face)
        .box(2, 1 + counter, 1)
        .rotateAboutCenter(
            (0, 0, 1), a)
        .val()
    )


result = (
    cq.Workplane("XY")
    .polygon(5, 10)
    .extrude(1)
    #.box(10, 10, 10)
    .faces("#Z")
    .each(face_fn)
)


import cadquery as cq
import math

length=60
width=40
roof_width=20

face_index = -1

def face_fn(face):
    global face_index
    face_index += 1
    normal = face.normalAt()
    a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
    return (
        cq.Workplane(face)
        .box(20, 4, 2)
        .rotateAboutCenter(
            (0, 0, 1), a)
        .val()
    )


result = (
    cq.Workplane("XY")
    .sketch()
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
    .finalize()
    .extrude(2)
    #.box(10, 10, 10)
    .faces("#Z")
    .each(face_fn)
)

# House wall with inner tabs

import cadquery as cq
import math

length=60
width=40
roof_width=20

roof_a = math.atan2(roof_width, 0.5 * length) * 180 / math.pi

face_index = -1

def face_loc_fn(loc):
    global face_index
    face_index += 1
    
    if face_index == 0:
        a = roof_a
    if face_index == 1:
        a = -roof_a
    if face_index == 2:
        a = 90
    if face_index == 3:
        a = 0
    if face_index == 4:
        a = 90

    return (
        cq.Workplane(loc)
        .box(20, 4, 2)
        .rotateAboutCenter((0, 0, 1), a)
        .val()
    )


result = (
    cq.Workplane("XY")
    .sketch()
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
    .finalize()
    .extrude(2)
    #.box(10, 10, 10)
    .faces("#Z")
    .cutEach(face_loc_fn)
)




import cadquery as cq
import math

length=60
width=40
roof_width=20

roof_a = math.atan2(roof_width, 0.5 * length) * 180 / math.pi

face_index = -1

def face_loc_fn(loc):
    global face_index
    face_index += 1
    
    if face_index == 0:
        a = roof_a
    if face_index == 1:
        a = -roof_a
    if face_index == 2:
        a = 90
    if face_index == 3:
        # Return shape with no overlap - no cut
        return (
            cq.Workplane(loc)
            .box(1, 1, 1)
            .translate((0, -5, 0))
            .val()
        )
    if face_index == 4:
        a = 90

    return (
        cq.Workplane(loc)
        .box(20, 4, 2)
        .rotateAboutCenter((0, 0, 1), a)
        .val()
    )


result = (
    cq.Workplane("XY")
    .sketch()
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
    .finalize()
    .extrude(2)
    .faces("#Z")
    .cutEach(face_loc_fn)

    .faces(">Z")
    .center(10, -10)
    .rect(16, 20)
    .cutThruAll()

    .faces(">Z")
    .center(0, 10)
    .circle(8)
    .cutThruAll()

    # try .item(0) on faces?
)



# =====================




import math
from cadquery import Workplane

a = (
    Workplane("XY")
    .box(5, 5, 1)
)
b = (
    Workplane("XY")
    .move(2, 3)
    .box(5, 5, 1)
)
c = a.union(b)

width = 40
height = 30
roof_height = 15

d2 = Workplane("XY").sketch().rect(50, 50).finalize().extrude(1)
d3 = Workplane("XY").sketch().regularPolygon(50, 5).finalize().extrude(1)

d = (
    Workplane("XY")
    .sketch()
    .polygon(
        [
            (-0.5 * width, 0.5 * height),
            (-0.5 * width, -0.5 * height),
            (0.5 * width, -0.5 * height),
            (0.5 * width, 0.5 * height),
            (0, 0.5 * height + roof_height)
        ],
        mode="a"
    )
    .finalize()
    .extrude(1)
)

e0 = c.union(d)
e1 = c.intersect(d)
e2 = c.cut(d)

# Objects are not modified - new ones are created
# operations - union, intersect, cut

# The edge order for a rect is: left, bottom, right, top
# => Use same convention for my other shapes
# gable: left, bottom, right, top-right, top-left

tab_defs_dict = {
    0: {
        "type": "none",
        "width": 15,
        "height": 1,
        "offset": 3
    },
    1: {
        "type": "in",
        "width": 15,
        "height": 1,
        "offset": 3
    },
    2: {
        "type": "out",
        "width": 15,
        "height": 1,
        "offset": 3
    },
    3: {
        "type": "in",
        "width": 15,
        "height": 1,
        "offset": 0
    },
    4: {
        "type": "out",
        "width": 15,
        "height": 1,
        "offset": 3
    }
}

face_index = -1

def union_face_fn(face):
    global face_index
    face_index += 1
    normal = face.normalAt()
    a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
    
    tab_def = tab_defs_dict[face_index]
    if tab_def["type"] != "out":
        return (
            cq.Workplane("XY")
            .box(0.2, 0.2, 0.2)
            .translate((0, 0, 0.5))
            .val()
        )
    
    return (
        cq.Workplane(face)
        .box(tab_def["width"], 2 * tab_def["height"], 1)
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
     d
     .faces("#Z")
     .each(union_face_fn, combine=False)
)



face_index_2 = -1

def cut_face_fn(face):
    global face_index_2
    face_index_2 += 1
    normal = face.normalAt()
    a = 90 + math.atan2(normal.y, normal.x) * 180 / math.pi
    
    tab_def = tab_defs_dict[face_index_2]
    if tab_def["type"] != "in":
        return (
            cq.Workplane("XY")
            .box(0.1, 0.1, 0.1)
            .translate((0, 0, 0.5))
            .val()
        )
    
    return (
        cq.Workplane(face)
        .box(tab_def["width"], 2 * tab_def["height"], 1)
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
     d
     .faces("#Z")
     .each(cut_face_fn, combine=False)
)

result = d - cut_shapes + union_shapes


show_object(result)









import math
from cadquery import Workplane

gable_width = 70
gable_height = 30
overhang_width = 10
end_height = 3
end_width = 3
thickness = 2

roof_a = math.atan2(gable_height, 0.5 * gable_width) * 180 / math.pi
tan_a = math.tan(math.radians(roof_a))
t_width = 0.5 * (gable_width + overhang_width)
t_height = t_width * tan_a
overhang_height = end_width * tan_a + end_height

result = (
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


show_object(result)

