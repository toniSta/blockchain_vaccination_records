# A Blockchain for vaccinations

This project is about the idea to store vaccination records anonymously and publicly available as a blockchain.
It provides a prototype to demonstrate the principal functionality.
It solves the problem of an effective, scalable consensus protocol by exploiting general assumptions within the domain of vaccinations.

**TODO**: extend this paragraph

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and demonstration 
purposes.

### Prerequisites

The prototype is implemented with Python 3.x. We recommend a version >= 3.6.
We use Docker to deploy our demonstration. 
You will need to install `docker` (>= 17.10) and `docker-compose` (>=1.16).
We visualize the current chain state as png image. 
You may want to install an image viewer which is able to refresh the opened image. 
On windows, we recommend [JPEGView](https://sourceforge.net/projects/jpegview/).

### Installing

First of all you'll need to get a copy of the project:

```bash
git clone https://github.com/toniSta/blockchain_vaccination_records.git
cd blockchain_vaccination_records
```

Continue by installing the projects python requirements:

```bash
pip install -r requirements.txt
```

Now you are prepared to run the [tests](#running-the-tests) or to [deploy](#deployment) the demo.

## Running the tests

You can run the tests with `pytest` within the root directory of the repository.

To get a report about the test coverage, run:
```bash
pytest --cov blockchain tests --cov-report=html
```
You'll find the report within the subdirectory `htmlcov`.

## Deployment

docker built.....

## Documentation

how to build? (Sphinx)
http://www.sphinx-doc.org/en/master/tutorial.html
http://docs.python-guide.org/en/latest/writing/documentation/

python -m pydoc blockchain

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the 
[tags on this repository](https://github.com/toniSta/blockchain_vaccination_records/tags). 

## Authors (alphabetical)

|Name   	        | Work   	        | Profile   	                                |
|---	            |---	            |---	                                        |
|Benedikt Bock   	|Initial work   	|[Benedikt1992](https://github.com/Benedikt1992)|
|Alexander Preuß   	|Initial work   	|[alpreu](https://github.com/alpreu)            |
|Toni Stachewicz   	|Initial work   	|[toniSta](https://github.com/toniSta)          |

## License

**TODO** which License do we want to use?

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

**TODO** Any?





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

a4:
docker run --name a4 -it -p 9000 --network blockchainvaccinationrecords_default -e "REGISTER_AS_ADMISSION=1"  -e "START_CLI=1" -e "NEIGHBORS_HOST_PORT=a3:9000,genesis_admission:9000" full_client_image
a5:
docker run --name a5 -it -p 9000 --network blockchainvaccinationrecords_default -e "REGISTER_AS_ADMISSION=1"  -e "CONFIRM_BLOCKSENDING=1" -e "NEIGHBORS_HOST_PORT=genesis_admission:9000,d1:9000" full_client_image
d3:
docker run --name d3 -it -p 9000 --network blockchainvaccinationrecords_default -e "START_CLI=1" -e "NEIGHBORS_HOST_PORT=d1:9000,a2:9000,d2:9000" full_client_image


### Demo Interactions
- ENV Variable START_CLI -> starts CLI for doctor (transaction creation) or admission (block creation)
- ENV Variable REGISTER_AS_ADMISSION -> necessary to enable start_cli to find out if doctor or admission
- ENV Variable CONFIRM_BLOCKSENDING -> if set the node participates in creator election and if it becomes the blockcreator it creates the blocks and waits for confirmation before sending
