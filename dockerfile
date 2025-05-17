FROM python:3.10

RUN apt update && apt dist-upgrade -y
RUN apt install tzdata -y
RUN apt install ffmpeg libsm6 libxext6  -y
RUN apt install nano -y
ENV TZ="Europe/Berlin"

WORKDIR /njoy-video-service

COPY ["requirements.txt", "./"]
EXPOSE 8631

RUN python3 -m pip install -r requirements.txt
COPY . .

CMD ["python3", "run.py"]