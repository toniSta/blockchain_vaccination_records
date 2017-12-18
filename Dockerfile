# Pull base image.

FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD bash
