import base64
from io import BytesIO
from typing import List, Tuple

import cv2
import numpy as np
from PIL import Image


def decode_image(base64_str: str) -> np.ndarray:
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data)).convert('RGB')
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def detect_damage(image: np.ndarray) -> List[Tuple[int, int, int, int]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 500:  # simple area threshold
            boxes.append((int(x), int(y), int(w), int(h)))
    return boxes



