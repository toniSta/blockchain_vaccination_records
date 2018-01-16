# Pull base image.

FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY blockchain blockchain
COPY requirements.txt .
COPY server.py .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD python server.py
