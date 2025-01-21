FROM python:3.10

# Installing all python dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/