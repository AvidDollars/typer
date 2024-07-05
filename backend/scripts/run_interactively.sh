#!/usr/bin/bash
image_name=typer-backend

docker build -t $image_name --file ../Dockerfile.prod .. && \

docker run \
        -it \
        --rm \
        --publish 8000:8000 \
    $image_name bash
