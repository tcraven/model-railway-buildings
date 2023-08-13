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



