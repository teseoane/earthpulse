from io import BytesIO
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from fastapi import APIRouter, Form, HTTPException, Response, UploadFile
from PIL import Image
from rasterio.plot import reshape_as_image

router = APIRouter()


@router.post('/attributes')
async def attributes(image: UploadFile):
    with rasterio.open(image.file) as dataset:
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


@router.post('/ndvi')
async def calculate_ndvi(image: UploadFile, palette: str = 'viridis'):
    with rasterio.open(image.file) as src:
        band_red = src.read(4)  # B4
        band_nir = src.read(8)  # B8

    # calculate NDVI
    np.seterr(divide='ignore', invalid='ignore')
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

    # apply colormap
    try:
        ndvi_colored = plt.get_cmap(palette)(ndvi)
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid palette.')

    # convert to PNG
    im = Image.fromarray((ndvi_colored * 255).astype(np.uint8))
    byte_arr = BytesIO()
    im.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()

    return Response(content=byte_arr, media_type='image/png')
