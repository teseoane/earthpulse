FROM python:3.11.3-slim-bullseye

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libgdal-dev

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
