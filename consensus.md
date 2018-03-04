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

### Known Limitations

**TODO** (simple list)

## Recreating the genesis block

It may happen that you want to generate a new genesis block.
With the following command you can create a new keypair for the genesis admission and recreate the genesis block:

```bash
python recreate_genesis_block.py
```