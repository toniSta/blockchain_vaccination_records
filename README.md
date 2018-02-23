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

[![Build Status](https://travis-ci.org/toniSta/blockchain_vaccination_records.svg?branch=master)](https://travis-ci.org/toniSta/blockchain_vaccination_records)
[![Coverage Status](https://coveralls.io/repos/github/toniSta/blockchain_vaccination_records/badge.svg?branch=master)](https://coveralls.io/github/toniSta/blockchain_vaccination_records?branch=master)

You can run the tests with `pytest` within the root directory of the repository.

To get a report about the test coverage, run:
```bash
pytest --cov blockchain tests --cov-report=html
```
You'll find the report within the subdirectory `htmlcov`.

## Deployment of the demonstration

We use `docker` and `docker-compose` to deploy the demo of this application.
Before running the demonstration, you have to build the images used by the demo (both in the root directory):

```bash
docker build -t blockchain_base -f base.Dockerfile .
docker build -t full_client_image -f Full_Client.Dockerfile .
```

After building the base image you can run `docker-compose up` to start the demo network.
This will start and connect the following network (nodes GA, A1-3, D1-2; see [Network Participants](#network-participants))

![demo network layout](img/network.png "demo network layout")

The nodes `A4-6` and `D3` can be controlled by you (see [How to interact within the demonstration](#how-to-interact-within-the-demonstration)). 
You can start them with the following commands (one per window):
```bash
./start_a4.sh
./start_a5.sh
./start_a6.sh
./start_d3.sh
```

To stop the demonstration you can stop the compose network by hitting `Ctrl+C`. After the container were stopped sucessfully
you can run `./stop_and_clean.sh` to stop the additional clients and cleaning up the docker environment.
Most certainly you also want to delete the contents of the directory `blockchain/blockchain_files`. 
However, don't delete the file starting with `0_` (You can restore the file with `git checkout blockchain/blockchain_files/`).

### How to interact within the demonstration
**Current state of the blockchain**

First of all you can have a look on the state of the blockchain as seen by the `GA` node. 
It will store its files in the directory `blockchain/blockchain_files`.
It will also contain an image `current_state.png`. 
This is a rendered image of the current chain. 
It will be renewed whenever the `GA` node adds a block to its chain.
You may want to use an image viewer with an auto-refresh feature (see [Prerequisites](#prerequisites)).

**Interactive clients**

Furthermore, there are 3 types of clients that can be controlled by you.
We use environment variables inside the docker container  to specify which client should be started.

- Create Block at any time (`A4`)  
This client will you allow to create blocks independently from the normal creator election.
This client will start with the following environment variables `REGISTER_AS_ADMISSION=1` and `START_CLI=1`.
- Confirm to broadcast a created block (`A5` + `A6`)  
This kind of client will register itself as admission node (see [Network Participants](#network-participants)).
It will generate block if it is its turn.
It won't broadcast this block immediately.
It will ask you for confirmation before broadcasting the block.
You can start it with the environment variables `REGISTER_AS_ADMISSION=1` and `CONFIRM_BLOCKSENDING=1`.
- Create and submit transactions (`D3`)  
This node lets you create any kind of transaction, see **TODO**. 
The node `D3` has a uni-directional connection to the nodes `A1-3` and `GA`. 
This means it will send new transactions to all admission nodes (see [Network Participants](#network-participants)) of the base network.
You can start this kind of client by setting the environment variable `START_CLI=1`.

There are some more environment variables to setup the nodes:

- `NEIGHBORS_HOST_PORT`  
This is a `,`-separated list of the nodes neighbors. 
One entry contains the (resolvable) hostname/ip and the port the neighbor listens to (default is `9000`).
A list may look like this: `a2:9000,d2:9000`.
If you want to extend the demo network, keep in mind that you need at least 1 bi-directional connection with the existing network.
- `SERVER_PORT`  
This is the port the client listens on (defaults to `9000`).
- `RENDER_CHAIN_TREE`  
If set to `1` the client will render the chain as image.

You can also add host volumes to the client. 
These are the directories inside the container that can be replaced with a hostmount:

- `/app/blockchain/blockchain_files`  
This is the directory where the container will store its blockchain. 
Keep in mind that the hostmount directory must contain the genesis block before starting the container.
Don't use `blockchain/blockchain_files`.
This directory is reserved  for the `GA` node.
Example: `/path/to/directory/containing/genesis_block:/app/blockchain/blockchain_files`
- `/app/blockchain/keys`  
This directory contains the keys used by the client. 
In most cases you don't need to replace the directory by a hostmount.
The directory `blockchain/keys` is reserved by the `GA` node.

**Start own nodes**

You can start your own clients. 
You have to connect them to the existing network manually by extending the `NEIGHBORS_HOST_PORT` variable of the nodes you want to connect to.
This is the base command that starts a client:
```bash
docker run --name custom_client -it -p 9000 --network blockchainvaccinationrecords_default full_client_image
```
Replace `custom_client` with the name of the client. 
This name will also be resolvable by other clients.
If you changed the default directory name of the repository, you also need to change `blockchainvaccinationrecords_default`.
You can run `docker network ls` to get a list of the created networks after starting `docker-compose`.
With `-e` you can add environment variables (e.g. `-e "START_CLI=1"`).
`-v` will add hostmounts (e.g. `-v /absolute/path:/app/blockchain/blockchain_files`).
Both flags can be repeated to add multiple environment variables or mounts.

**Get bash access for the clients `A4-6` and `D3`**

You can use one of the following commands to get a bash terminal inside the container:

```bash
docker exec -it a4 bash
docker exec -it a5 bash
docker exec -it a6 bash
docker exec -it d3 bash
```

You will find the debug logs in `/var/log/blockchain/server.log`.
The blockchain files are located in the former mentioned directories.


**Stopping network nodes**

You can stop nodes of the base network and restart them at later time.

Commands to stop nodes:
```bash
docker-compose stop genesis_admission
docker-compose stop a1
docker-compose stop a2
docker-compose stop a3
docker-compose stop d1
docker-compose stop d2
```

Use `docker-compose start <name>` to start the node again.

**TODO below this line**
---

## Architecture

### Network Participants

This means genesis admission, admissions, doctors, patients

## Code Documentation

**TODO** get Sphinx running. It possible to auto-build docs with sphinx on readthe docs:
- https://github.com/rtfd/readthedocs.org
- http://www.sphinx-doc.org/en/master/tutorial.html
- http://docs.python-guide.org/en/latest/writing/documentation/

We use python doc strings inside the source files. Each method has it's own documentation.

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
