from buildings import panels

# length 100

thickness = 1.69

panel = panels.rafter_extension(
    gable_width=70,
    gable_height=30,
    length=10,
    thickness=0.56 * 4)

rp = panels.roof_panel(
    width=100,
    gable_width=70,
    gable_height=30,
    rafter_length=10,
    overhang_length=5,
    thickness=1.69)

g = (
    panel
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .rotate((0, 0, 0), (0, 0, 1), -90)
    .translate((0.5 * thickness, -15.54, 5))
)

result = rp + g

show_object(result)
