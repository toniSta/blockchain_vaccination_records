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
This node lets you create any kind of transaction, see [Supported Transactions](#supported-transactions). 
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

## Architecture

### Network Participants

In our blockchain network exist 4 kinds of participants. Admissions and doctors should be distinct sets.
However, we don't check this in the prototype:
- **Admission**  
Admissions are the authorative part in the blockchain.
The job of an admission is to register new admissions, doctors and vaccines (see [Supported Transactions](#supported-transactions)).
It will receive transactions and create blocks containing the received transactions.
Admissions will be driven by public institutions.
Unlike other blockchain technologies we assume that the admission nodes are seen as trustworthy.
- **Genesis Admission**  
This admission is special as it generated the genesis block and obtains it right as admission within the genesis block.
- **Doctor**  
As the name suggests, doctors are doctors.
They have to register as doctor within the chain to obtain the right to create vaccination transactions.
We assume that a doctor won't DoS the network with transactions.
- **Patient**  
This participant will receive vaccinations and has no further rights.
We mock this type of participant in the prototype

### Supported Transactions
We support 3 kinds of transactions:

- **Permission**  
Each participant starts without any rights. 
This transactions allow to obtain further rights. 
There are 3 sub-types currently:
    - **Admission**  
    This kind will grant the status as admission.
    In general you would have to ask for approvals by other admissions beforehand.
    We don't check this in the prototype.
    - **Doctor**  
    As well this will grant you the doctor rights.
    In a real deployment an admission has to check if the doctor is a licensed doctor.
    - **Patient**  
    This will register your key as patient key
- **Vaccine**  
Register a new vaccine in the chain.
Only registered vaccines can be used in vaccination transactions.
- **Vaccination**  
This transactions depicts the process of a patient being vaccinated.

> __Currently unsupported__:
>
> - the removal of any registration process.

Transactions aren't stored on persistent storage until they are part of a block.
To make sure that a new transaction becomes part of the chain the sender needs to send it to multiple admissions.
We recommend at least to 6 admissions for a fault tolerance > 99,99%.
We assume a fault probability of 20% per admission node.


### Client Types

There are 2 types of clients.

- **Full Client**
This client supports all actions within the chain dependent on the rights of the participant's key.
It will contain a complete copy of the blockchain.
It is used by admissions to receive and validate transactions and to receive, validate and create new blocks.
Doctors use the client to generate new transactions and to send them to their neighbors.
- **Look-Up Client** `currently not implemented`  
Meant to offer a user interface to enable search operations like Which vaccinations has a specific patient?, What are my upcoming vaccinations?... .
This client can be used by any person and doesn't demand a valid key.
Used with a key, it enables push notifications about upcoming vaccinations.

## Consensus
The goal of this section is to give a brief overview of the implemented consensus protocol.
Please refer to the source code of [Chain](blockchain/chain.py) and [FullClient](blockchain/full_client.py) for all details.

To reach consensus between all participants in the network, we introduce the concept of judgements.
This means we make a decision on a democratic basis. 
As long as a block holds positive votes from at least the half of entitled voters it is accepted as part of the chain.
Otherwise it is rejected.
See [Judgements](#judgements) for more details on the judgement process.
It will occur that at some point in time one node has more than one block with the same index that fulfills the consensus requirement.
This means we have (temporarily) multiple possible branches and need to store the chain as a tree structure.

> __Notice__:
>
> We do not support to unregister any admissions. 
> This would be necessary in a real deployment together with an automatic unregister if the admission is inactive for a certain amount of time.

### Judgements
Entitled voters are all admission nodes without the admission node that created the block at hand.
Each admission node will cast a judgement based on its state of the chain.
An `accept` judgement can be changed into a `deny` judgements at a later point in time.
`Denies` are immutable in contrast.
Each admission will base its decision on the following rules:

 1. Is the block itself correct? (hash, index, transactions, size,...)
 2. Is the block created by the expected creator (refer to [Creator Election](#creator-election))?
 3. Is the block creation time older than every alternative block with the same index?
 
If all 3 questions can be answered with yes (again based on the current state), the admission will create an `accept` judgement.
At the same time every alternative branch (every sub-tree with the same index as root) will be updated to a `deny` judgement for every block in the branch.
If one of the questions is answered with `false` the block hat and will get a `deny` judgement.

As you can see every admission has only one active branch at every point in time.
Since blocks and judgements are broadcasted in the network every admission will base its decision on the same information over time.
This means the chain is going to converge to one branch.

### Creator Election
We use some sort of proof of stake during the election of the next block creator.
Every admission has an counter since it created its last block (or was added as admission).
The counter increases continiously.
Whenever an admission node created a block its counter is cleared.
The stake belongs to the admission with the highest counter.
This will result in a round robin like creator queue.
From our point of view this is the fairest distribution.

At this point the election would be vulnerable to admissions that do not send blocks anymore.
Therefore, we introduce a block creation timeout.
If the admission in charge doesn't create a block within the timeout the admission with the second highest counter has to create a block and so on.
If the admission with the lowest counter doesn't create a block we start over with the highest counter.
During the validation the difference between parent block creation time and block creation time has to be smaller than the timeout.

> __Notice__:
>
> While the election is robust to abandoned admissions it would be more efficient if they would be unregistered as admission.

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
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

## Acknowledgments

**TODO** Any? -> Thanks to C. Böhm
