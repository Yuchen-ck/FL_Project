FROM ubuntu:22.04

MAINTAINER xavier

ENV DEBIAN_FRONTEND=noninteractive

ENV LIBGL_ALWAYS_INDIRECT=1

# Install Python 3, PyQt5,
RUN apt-get update -y && apt-get install -y software-properties-common 
RUN add-apt-repository --yes ppa:deadsnakes/ppa
RUN apt-get update -y && apt install -y python3.7 \
	python3.7-distutils \
	python3-pip \
	ttf-wqy-microhei \
	language-pack-zh*  
RUN apt-get install -y python3-pyqt5 python3.7-dev

# Install Python required package
RUN python3.7 -m pip install pip
RUN python3.7 -m pip install SIP pyQt5
RUN python3.7 -m pip install --upgrade PyQt5
COPY *.txt /home/qtuser/client-system/
RUN python3.7 -m pip install -r /home/qtuser/client-system/requirements.txt

# Add user for user Pyqt5
RUN adduser --quiet --disabled-password qtuser

# Copy python code
COPY * /home/qtuser/client-system/
RUN chmod -R 777 /home/qtuser
# Change work directory
WORKDIR "/home/qtuser/client-system"
