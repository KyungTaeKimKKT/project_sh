# Use an official Python runtime as a parent image
FROM python:3.10-slim
LABEL maintainer="kkt"

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /background

# Install any needed dependencies specified in requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y fcitx fcitx-hangul fonts-noto-cjk dbus-x11 fcitx-frontend-qt6
RUN apt install tzdata
RUN apt-get install  ffmpeg libsm6 libxext6 -y
RUN apt-get install -y graphviz
RUN python -m venv /py-bg && \
    /py-bg/bin/pip install --upgrade pip 

COPY ./requirements-bg.txt /tmp/requirements-bg.txt
RUN pip install --no-cache-dir -r /tmp/requirements-bg.txt 
RUN rm -rf /tmp

# Copy the current directory contents into the container at /app
COPY . /background

# Make port 8080 available to the world outside this container
EXPOSE 9990

# Define environment variable
# ENV NAME World

USER root

# WORKDIR /background
# # Run  when the container launches
# RUN chmod +x ./run.sh
# CMD ["sh", "run.sh"]

