from io import BytesIO

import rasterio
from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post('/attributes')
async def attributes(image: UploadFile):
    with rasterio.open(BytesIO(await image.read())) as dataset:
        width, height = dataset.width, dataset.height
        num_bands = dataset.count
        crs = dataset.crs.to_string()
        bbox = dataset.bounds

    return {
        'image_size': {'width': width, 'height': height},
        'num_bands': num_bands,
        'crs': crs,
        'bbox': bbox
    }
