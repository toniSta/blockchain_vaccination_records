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

`docker run --name custom_client -it -p 9000 --network blockchainvaccinationrecords_default full_client_image`

You may add one or more of the following options:
```
-e "NEIGHBORS_HOST_PORT=host:9000,host2:9000" # This option defines the direct neighbours of your client. You can use any service name of `docker-compose.yml` or any custom client (`--name` option)
-e "REGISTER_AS_ADMISSION=1" # Wheather the client should register itself as admission node after startup.
-e "RENDER_CHAIN_TREE=1" # Wheather the client should render the tree as a picture (best to combine with `-v`
-e "START_CLI=1"  # This will start a cli dependend on REGISTER_AS_ADMISSION you will get a doctor cli oder a admission cli
-v /path/to/directory/containing/genesis_block:/app/blockchain/blockchain_files # Mount a directoryto store the blockchainfiles (and the rendered picture)
```

You can stop the client with `docker stop custom_client` and don't forget to clean up with `docker container prune -f && docker volume prune -f`

If you want to access you client, use `docker exec -it custom_client bash`


### Testing

- run tests with `pytest` in root directory of the repo
- in order to get the test coverage run: `py.test --cov blockchain tests --cov-report=html`


### Demo Interactions
- ENV Variable START_CLI -> starts CLI for doctor (transaction creation) or admission (block creation)
- ENV Variable REGISTER_AS_ADMISSION -> necessary to enable start_cli to find out if doctor or admission
- ENV Variable CONFIRM_BLOCKSENDING -> if set the node participates in creator election and if it becomes the blockcreator it creates the blocks and waits for confirmation before sending
