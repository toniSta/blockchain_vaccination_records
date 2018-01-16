# Pull base image.

FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY blockchain blockchain
COPY requirements.txt .
COPY server.py .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

VOLUME ["/app/blockchain/blockchain_files"]

ENV SERVER_PORT 9000
ENV NEIGHBORS_HOST_PORT 127.0.0.1:9000

CMD python server.py
