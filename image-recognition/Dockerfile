FROM nvidia/cuda:11.8.0-base-ubuntu20.04

LABEL maintainer="Jackson Thetford"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    git \
    gcc \
    libglib2.0-0 \
    libgl1-mesa-glx \
    vim \
    python3-pip \
    && apt-get clean \
    build-essential \
    cmake \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    g++ \
    make \
    ninja-build \ 
    && rm -rf /var/lib/apt/lists/*


# python 3
RUN add-apt-repository ppa:deadsnakes/ppa

# Install Python 3.11
RUN apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# bootstrap method for pip bc i was having issues with it 
RUN apt-get remove -y python3-pip && apt-get autoremove -y
RUN wget --no-check-certificate -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py' && \
    python3.11 get-pip.py

# python3.11 as default 
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install Python packages
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install gdown

WORKDIR /home
RUN git clone https://github.com/jthet/Autonomous-Aircraft-Drop /home/Autonomous-Aircraft-Drop

RUN git clone https://github.com/ultralytics/yolov5 /home/yolov5
WORKDIR /home/yolov5

# need this for OpenCV
RUN apt-get update && apt-get install -y \ 
    libopencv-dev

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN pip3 install --no-cache-dir ultralytics opencv-python pillow 

# idk if we need this ... is this just install torch and torchvision???? is it not installed on line 55?
RUN gdown https://drive.google.com/uc?id=1hs9HM0XJ2LPFghcn7ZMOs5qu5HexPXwM \
    && gdown https://drive.google.com/uc?id=1m0d8ruUY8RvCP9eVjZw4Nc8LAwM8yuGV

RUN apt-get install libcap-dev 
RUN pip3 install picamera2
RUN apt-get install libcamera*
# putting this down here bc wanna keep cache.


# docker buildx build --platform linux/arm64/v8 --tag jthet/autonomous-aircraft-drop:ml-dev .