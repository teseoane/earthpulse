from typing import Optional

import numpy as np
import rasterio
from fastapi import UploadFile
from PIL import Image
from rasterio.plot import reshape_as_image


def task_create_thumbnail(image: UploadFile, resolution: Optional[int] = None):
    import time
    time.sleep(10)
    with rasterio.open(image.file) as dataset:
        img = dataset.read([1, 2, 3])

    img_array = np.array(img)
    img_array = reshape_as_image(img_array)

    img_norm = (img_array - img_array.min()) / (img_array.max() - img_array.min())

    img_pil = Image.fromarray(np.uint8(img_norm * 255))

    if resolution:
        img_pil.thumbnail((resolution, resolution))

    img_pil.save('thumbnail.png')
