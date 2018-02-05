# blockchain_vaccination_records

## Docker

Before you can use the demo compose file of this project, you need to build the base image containing all project dependency.
Run `docker build -f base.Dockerfile -t blockchain_base .` in the project root directory to build the base image.

After building the base image you can run `docker-compose up` to start the demo network.

## How to attach a controlable client

First you need to build the images in the project root dir:

```
docker build -t blockchain_base -f base.Dockerfile .
docker build -t full_client_image -f Full_Client.Dockerfile .
```

You can clean up after starting the client with: `docker container prune -f && docker volume prune -f` (after stopping the container)

remember: run `docker build` with clean `blockchain_files` directory

for no use: `docker run --name custom_client -p 9000 --network blockchainvaccinationrecords_default -e "SERVER_PORT=9000" -e "NEIGHBORS_HOST_PORT=admission:9000" full_client_image`
to start a client.

You can delete old files with 


# work in progress:

docker run --name custom_client -p 9000 --network blockchainvaccinationrecords_default -e "SERVER_PORT=9000" full_client_image
-e "NEIGHBORS_HOST_PORT=host:9000,host2:9000"
-e "REGISTER_AS_ADMISSION=1"
-e "RENDER_CHAIN_TREE=1"
-v /path/to/directory/containing/genesis_block:/app/blockchain/blockchain_files

 docker container prune -f && docker volume prune -f

### Testing

- run tests with `pytest` in root directory of the repo
- in order to get the test coverage run: `py.test --cov blockchain tests --cov-report=html`
