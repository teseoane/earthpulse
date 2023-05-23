from io import BytesIO

import rasterio
from fastapi import APIRouter, UploadFile

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
