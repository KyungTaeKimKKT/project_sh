FROM python:3.10
LABEL maintainer="kkt"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y fcitx fcitx-hangul fonts-noto-cjk dbus-x11 fcitx-frontend-qt6
RUN apt install tzdata
RUN apt-get install  ffmpeg libsm6 libxext6 -y
RUN apt install -y portaudio19-dev
RUN apt install -y python3-pyqt6 
RUN apt-get install -y zbar-tools 
RUN apt -y install libxcb-*
RUN apt-get install -y alsa-utils
    # apk add sdl2-dev \
    #         qtcore-qt5-dev \
    #         cmake \
    #         gcc \
    #         make \
    #         zlib-dev \
    #         libffi-dev &&\
RUN python -m  venv /py
RUN /py/bin/pip install --upgrade pip 
COPY ./requirements_pyqt6.txt /tmp/requirements_pyqt6.txt
RUN /py/bin/pip install -r /tmp/requirements_pyqt6.txt
RUN rm -rf /tmp

# RUN adduser \
#     --disabled-password \
#     --no-create-home \
#     root


COPY . /monitor
WORKDIR /monitor
# EXPOSE 44444

# COPY ./config_alsa/asound.conf /etc/asound.conf

ENV PATH="/py/bin:$PATH"

USER root

# CMD [ "python3", "/rpi/main.py" ]