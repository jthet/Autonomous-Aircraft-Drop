FROM python:3.11-slim as base

LABEL maintainer="Jackson Thetford"

# # # Security stuff we don't need yet ** We are running as root in the container **
# RUN useradd -m Autonomous-Aircraft-Drop
# USER Autonomous-Aircraft-Drop
# # # 

WORKDIR /home/Autonomous-Aircraft-Drop

# install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy our code
COPY image-recognition ./image-recognition
COPY trajectory ./trajectory

