from buildings.panels_v2 import *

card_169 = SingleLayerMedia(
    name="card_1.69mm",
    description="1.69mm corrugated card",
    thickness=1.69,
    width=265,
    height=165
)
card_056 = SingleLayerMedia(
    name="card_0.56mm",
    description="0.56mm white card",
    thickness=0.56,
    width=265,
    height=165
)
wall_base_media = LayeredMedia(
    description="Two layers of 1.69mm corrugated card",
    media=card_169,
    layer_count=2,
    thickness=2 * 1.69
)
wall_front_media = LayeredMedia(
    description="Two layers of 0.56mm card",
    media=card_056,
    layer_count=2,
    thickness=2 * 0.56
)
wall_back_media = card_056
window_media = card_056

w = create_wall_with_windows(
    base_media=wall_base_media,
    front_media=wall_front_media,
    back_media=wall_back_media,
    window_media=window_media,
    transform=[]
)

a = get_assembly(panel_group=w)

show_object(a)
