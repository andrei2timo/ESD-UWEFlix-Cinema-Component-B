# base image  
FROM python:3.10

# setup environment variable  
ENV DockerHOME=/app/UWEFlix_django

# set work directory
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file to DockerHOME
COPY requirements.txt $DockerHOME

# install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy whole project to DockerHOME
COPY . $DockerHOME

# copy Google API credentials file to DockerHOME
COPY credentials.json $DockerHOME

# set environment variable for Google API credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/UWEFlix_django/credentials.json

# port where the Django app runs
EXPOSE 8000

# start server
CMD python manage.py runserver 0.0.0.0:8000
