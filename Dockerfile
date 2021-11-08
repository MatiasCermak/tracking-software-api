FROM python:3.8.10

# ENV PYTHONUNBUFFERED 1

RUN mkdir /TSA

# Set the working directory to /music_service
WORKDIR /TSA

# Copy the current directory contents into the container at /music_service
ADD /TSA/ /TSA/

ADD requirements.txt /TSA/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt