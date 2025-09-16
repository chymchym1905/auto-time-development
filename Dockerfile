FROM python:3.10.14-slim-bullseye

WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install ultralytics easyocr pytube yt-dlp ipykernel
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Make port 80 available to the world outside this container
EXPOSE 80