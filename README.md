# blockchain_vaccination_records

## Docker

Before you can use the demo compose file of this project, you need to build the base image containing all project dependency.
Run `docker build -f base.Dockerfile -t blockchain_base .` in the project root directory to build the base image.

After building the base image you can run `docker-compose up` to start the demo network.

## How to attach a controlable client

First you need to build the images in the project root dir (`blockchain_files` directory should only contain the genesis block):

```
docker build -t blockchain_base -f base.Dockerfile .
docker build -t full_client_image -f Full_Client.Dockerfile .
```

You can start a client with the following commands:

`docker run --name custom_client -p 9000 --network blockchainvaccinationrecords_default -e "SERVER_PORT=9000" full_client_image`

You may add one or more of the following options:
```
-e "NEIGHBORS_HOST_PORT=host:9000,host2:9000" # This option defines the direct neighbours of your client. You can use any service name of `docker-compose.yml` or any custom client (`--name` option)
-e "REGISTER_AS_ADMISSION=1" # Wheather the client should register itself as admission node after startup.
-e "RENDER_CHAIN_TREE=1" # Wheather the client should render the tree as a picture (best to combine with `-v`
-v /path/to/directory/containing/genesis_block:/app/blockchain/blockchain_files # Mount a directoryto store the blockchainfiles (and the rendered picture)
```

You can stop the client with `docker stop custom_client` and don't forget to clean up with `docker container prune -f && docker volume prune -f`

If you want to access you client, use `docker exec -it custom_client bash`


### Testing

- run tests with `pytest` in root directory of the repo
- in order to get the test coverage run: `py.test --cov blockchain tests --cov-report=html`
