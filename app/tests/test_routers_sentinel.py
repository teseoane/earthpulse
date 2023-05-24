import os

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def test_attributes():
    with open('app/tests/images/test_image.tiff', 'rb') as img:
        response = client.post('/api/v1/attributes', files={'image': ('test_image.tiff', img, 'image/tiff')})

    assert response.status_code == 200
    assert response.json() == {
        'image_size': {
            'width': 2186,
            'height': 1384
        },
        'num_bands': 12,
        'crs': 'EPSG:4326',
        'bbox': [-0.00839, 38.747216, 0.2381, 38.878028]
    }


def test_thumbnail_endpoint():
    with open('app/tests/images/test_image.tiff', 'rb') as img:
        response = client.post(
            '/api/v1/thumbnail',
            files={'image': ('test_image.tiff', img, 'image/tiff')},
            data={'resolution': '300'},
        )

    assert response.status_code == 200
    assert response.json() == {'filename': 'test_image.tiff'}

    # Ensure the thumbnail was created correctly
    assert os.path.exists('thumbnail.png')

    # Load the created thumbnail
    img = Image.open('thumbnail.png')

    # Check the size of the thumbnail
    assert img.size[0] <= 300 and img.size[1] <= 300

    # Check the mode of the image
    assert img.mode == 'RGB'

    # Clean up
    os.remove('thumbnail.png')


def test_ndvi_endpoint():
    with open('app/tests/images/test_image.tiff', 'rb') as img:
        response = client.post(
            '/api/v1/ndvi',
            files={'image': ('test_image.tiff', img, 'image/tiff')},
            data={'palette': 'viridis'},
        )

    assert response.status_code == 200
    assert response.content
    assert response.headers['content-type'] == 'image/png'


@pytest.fixture(autouse=True)
def clean_up():
    yield
    if os.path.exists('thumbnail.png'):
        os.remove('thumbnail.png')
