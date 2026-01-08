import cv2
import numpy as np
from PIL import Image

def read_gif_first_frame(path, size=(512, 512)):
    """
    Reads first frame of a GIF using PIL (reliable for satellite GIFs)
    """
    gif = Image.open(path)
    gif.seek(0)  # first frame

    frame = np.array(gif)

    # conver grayscale to BGR
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    frame = cv2.resize(frame, size)
    return frame
