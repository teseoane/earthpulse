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

## API Documentation

### POST /attributes
This endpoint is responsible for extracting and returning the attributes of an uploaded raster image.

#### Parameters:
- `image`: The raster image file to be processed. This should be included in the body of the request as form data.

#### Response:
Returns a JSON object containing the attributes of the image:
- `image_size`: A dictionary with 'width' and 'height' of the image.
- `num_bands`: The number of bands in the image.
- `crs`: The Coordinate Reference System (CRS) of the image.
- `bbox`: The bounding box of the image.

Example usage:
```bash
curl -X POST -F "image=@path_to_your_image.tiff" http://localhost:8888/api/v1/attributes
```

### POST /thumbnail
This endpoint creates a thumbnail of an uploaded raster image and saves it as 'thumbnail.png'.

#### Parameters:
- `image`: The raster image file to be processed. This should be included in the body of the request as form data.
- `resolution` (optional): The resolution for the thumbnail.

#### Response:
Returns a JSON object containing the filename of the image.

Example usage:
```bash
curl -X POST -F "image=@path_to_your_image.tiff" -F "resolution=200" http://localhost:8888/api/v1/thumbnail
```

### POST /ndvi
This endpoint calculates the Normalized Difference Vegetation Index (NDVI) of an uploaded raster image.

#### Parameters:
- `image`: The raster image file to be processed. This should be included in the body of the request as form data.
- `palette` (optional): The color palette to be used for the resulting NDVI image. The default palette is 'viridis'.

#### Response:
Returns the resulting NDVI image as a PNG file.

Example usage:
```bash
curl -X POST -F "image=@path_to_your_image.tiff" -F "palette=magma" http://localhost:8888/api/v1/ndvi
```

## Notes:

I chose to let the hole code in the router to be easyer to check the amount of lines but I prefer to add a service layer and let the router only performs validation checks.

TODO:
- Move the core processing logic to a separate service layer to encapsulate the business logic and keep the router clean. The service layer can contain functions responsible for image processing and interacting with the rasterio library.
- Add edge cases tests and all the requiered error handling validations
- Add logs to provide a better track.
- The create_thumbnail function can be executed in the background or sent to a queue and consumed by a broker to improve responsiveness of the API. So we can scalate it as needed.
- Implement validations for valid palettes to ensure that only valid palette names are accepted.
- Implement file validations to check if the uploaded file is in the correct format and can be read by rasterio. For example, you can check if the file is an image and raise an exception if it's not. Here's an example validation function that checks if the file is an image:
```python
# Example:
async def validate_file(file: UploadFile):
    if "image" not in file.content_type:
        raise HTTPException(status_code=400, detail="File is not an image.")
    return file
```
