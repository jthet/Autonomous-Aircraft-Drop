FROM ubuntu:20.04 as base

LABEL maintainer="Jackson Thetford"

ENV DEBIAN_FRONTEND=noninteractive

# essentials
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    wget \
    cmake \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

# python 3.11
RUN apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

RUN python3.11 -m pip install --upgrade pip

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Set work directory in the container
WORKDIR /home/Autonomous-Aircraft-Drop

# Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy our code into the Docker image
COPY image-recognition ./image-recognition
COPY trajectory ./trajectory

# Commented out user creation and switch for now
# Security stuff we don't need yet ** We are running as root in the container **
# RUN useradd -m Autonomous-Aircraft-Drop
# USER Autonomous-Aircraft-Drop

# Build Command:

#  docker buildx build \
#  --push \
#  --platform linux/arm/v7,linux/arm64/v8,linux/amd64 \ --tag your-username/multiarch-example:buildx-latest .