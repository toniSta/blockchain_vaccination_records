# Pull base image.

FROM blockchain_base

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

VOLUME ["/app/blockchain/blockchain_files"]

ENV NEIGHBORS_HOST_PORT 127.0.0.1:9000

CMD python main.py
