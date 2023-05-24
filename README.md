# EarthPulse Test

## Running local environment

### Build the image
```bash
docker-compose build
```

### Run the container
```bash
docker-compose up
```

### Running the tests
```bash
docker compose  run --rm web python -m pytest

## Notes:
TODO list:

- create_thumbnail can be done asyncronous in a task but need to add a queue and a broker
- validations for valid palettes
- validation for the files like and also check if the file is a raster dataset that can be read by rasterio.

```python
# Example:
async def validate_file(file: UploadFile):
    if "image" not in file.content_type:
        raise HTTPException(status_code=400, detail="File is not an image.")
    return file
```
