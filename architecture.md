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

### Synchronization

**TODO** 

> **Known Limitations:**
> - If the requested block is not part of the chain of the asked neighbor the complete chain needs to be resend.
> To sove this you would need to remeber which blocks were part of a dead branch.    