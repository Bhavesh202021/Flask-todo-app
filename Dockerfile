# syntax=docker/dockerfile:1

#base image
FROM python:3.8-slim-buster

#create a working directory
WORKDIR /app

#The first parameter tells Docker what file(s) you would like to copy into the image. 
#The second parameter tells Docker where you want that file(s) to be copied to
COPY requirements.txt requirements.txt

# the RUN command to execute the command pip3 install. 
RUN pip install -r requirements.txt

#we have installed our dependencies. The next step is to add our source code into the image.
COPY . .

EXPOSE 8000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]