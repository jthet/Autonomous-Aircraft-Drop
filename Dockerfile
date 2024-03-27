FROM python:3.11 as base

LABEL maintainer="Jackson Thetford"

# # # Security stuff we don't need yet ** We are running as root in the container **
# RUN useradd -m Autonomous-Aircraft-Drop
# USER Autonomous-Aircraft-Drop
# # # 

WORKDIR /home/Autonomous-Aircraft-Drop

RUN apt-get update && apt-get install -y cmake patchelf

# install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy our code
COPY image-recognition ./image-recognition
COPY trajectory ./trajectory

# Build Command:

#  docker buildx build \
#  --push \
#  --platform linux/arm/v7,linux/arm64/v8,linux/amd64 \ --tag your-username/multiarch-example:buildx-latest .