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

I chose to let the hole code in the router to be easyer to check the amount of lines but I prefer to add a service layer and let the router only performs validation checks.

TODO:
- Move the core processing logic to a separate service layer to encapsulate the business logic and keep the router clean. The service layer can contain functions responsible for image processing and interacting with the rasterio library.
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
