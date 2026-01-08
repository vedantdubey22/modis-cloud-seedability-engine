import numpy as np

def create_color_map(shape, green, amber, gray):
    """
    Converts decision masks into colored output image
    """
    h, w = shape
    output = np.zeros((h, w, 3), dtype=np.uint8)

    output[green] = [0, 255, 0]       # Green
    output[amber] = [0, 165, 255]     # Amber (BGR)
    output[gray] = [128, 128, 128]    # Gray

    return output
