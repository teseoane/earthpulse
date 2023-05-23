from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_attributes():
    with open('test_image.tiff', 'rb') as img:
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
