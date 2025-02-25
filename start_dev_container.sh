#!/bin/bash
set -e

echo "Building docker container image baby_tracker_image_evidence"
docker buildx build -t baby_tracker_image_evidence -f Dockerfile .

echo "Starting Evidence.dev development docker container"
docker run -d \
--mount type=bind,source=/$(pwd)/evidence,target=/evidence \
--publish 3000:3000 \
-it \
--rm \
--name baby_tracker_container \
baby_tracker_image_evidence

echo "Evidence.dev available at localhost:3000 once docker container setup is complete"