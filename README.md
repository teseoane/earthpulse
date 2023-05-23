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
