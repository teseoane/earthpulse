from io import BytesIO
from typing import Optional

import numpy as np
import rasterio
from fastapi import APIRouter, Form, UploadFile
from PIL import Image
from rasterio.plot import reshape_as_image

router = APIRouter()


@router.post('/attributes')
async def attributes(image: UploadFile):
    with rasterio.open(BytesIO(await image.read())) as dataset:
        attributes = {
            'image_size': {'width': dataset.width, 'height': dataset.height},
            'num_bands': dataset.count,
            'crs': dataset.crs.to_string(),
            'bbox': dataset.bounds
        }
    return attributes


@router.post('/thumbnail')
async def create_thumbnail(image: UploadFile, resolution: Optional[int] = Form(None)):
    with rasterio.open(image.file) as dataset:
        img = dataset.read([1, 2, 3])

    img_array = np.array(img)
    img_array = reshape_as_image(img_array)

    img_norm = (img_array - img_array.min()) / (img_array.max() - img_array.min())

    img_pil = Image.fromarray(np.uint8(img_norm * 255))

    if resolution:
        img_pil.thumbnail((resolution, resolution))

    img_pil.save('thumbnail.png')
    return {'filename': str(image.filename)}
