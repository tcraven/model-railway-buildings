# 2mm corrugated card sheets are width="269.4mm" height="205.9mm"

MEDIA_INFO_BY_NAME = {
    "1.69mm": {
        "description": "1.69mm corrugated card",
        "thickness": 1.69,
        "width": 265,
        "height": 165
    },
    "2x1.69mm": {
        "description": "Two layers of 1.69mm corrugated card",
        "layer_media_name": "1.69mm",
        "layer_count": 2
    },
    "0.56mm": {
        "description": "0.56mm white card",
        "thickness": 0.56,
        "width": 265,
        "height": 165
    },
    "2x0.56mm": {
        "description": "Two layers of 0.56mm white card",
        "layer_media_name": "0.56mm",
        "layer_count": 2
    }
}

def get_media_info(media_name):
    return MEDIA_INFO_BY_NAME[media_name]


def get_media_thickness(media_name):
    media_info = get_media_info(media_name=media_name)
    # If the media has thickness, return it
    if "thickness" in media_info:
        return media_info["thickness"]
    
    # Otherwise the media is made up of layers of another media, so
    # calculate the thickness from the other media
    layer_media_info = get_media_info(media_info["layer_media_name"])
    return layer_media_info["thickness"] * media_info["layer_count"]


def get_media_dimensions(media_name):
    media_info = get_media_info(media_name=media_name)
    # If the media has width, return width and height
    if "width" in media_info:
        return {
            "width": media_info["width"],
            "height": media_info["height"]
        }
    
    # Otherwise the media is made up of layers of another media, so
    # get the width and height from the other media
    layer_media_info = get_media_info(media_info["layer_media_name"])
    return {
        "width": layer_media_info["width"],
        "height": layer_media_info["height"]
    }


def get_layer_count(media_name):
    media_info = get_media_info(media_name=media_name)
    if "layer_count" not in media_info:
        return 1
    
    return media_info["layer_count"]


def get_layer_media_name(media_name):
    media_info = get_media_info(media_name=media_name)
    if "layer_media_name" in media_info:
        return media_info["layer_media_name"]
    
    return media_name
