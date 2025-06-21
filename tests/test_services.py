import base64
from io import BytesIO
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend.services.damage_detection import decode_image, detect_damage


def _encode_image(arr: np.ndarray) -> str:
    im = Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))
    buf = BytesIO()
    im.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def test_decode_image_roundtrip():
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    encoded = _encode_image(image)
    decoded = decode_image(encoded)
    assert decoded.shape == image.shape
    assert decoded.dtype == image.dtype


def test_detect_damage_square():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (40, 40), (255, 255, 255), -1)
    boxes = detect_damage(image)
    assert boxes, "no boxes returned"
    x, y, w, h = boxes[0]
    assert 15 <= x <= 25
    assert 15 <= y <= 25
    assert 20 <= w <= 30
    assert 20 <= h <= 30
