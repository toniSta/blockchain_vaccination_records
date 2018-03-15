## Consensus
The goal of this section is to give a brief overview of the implemented consensus protocol.
Please refer to the source code of [Chain](blockchain/chain.py) and [FullClient](blockchain/full_client.py) for all details.

To reach consensus between all participants in the network, we introduce the concept of judgements.
This means we make a decision on a democratic basis. 
As long as a block holds positive votes from at least half of the entitled voters it is accepted as part of the chain.
Otherwise it is rejected.
See [Judgements](#judgements) for more details on the judgement process.
It will occur that at some point in time one node has more than one block with the same index that fulfills the consensus requirement.
This means we (temporarily) have multiple possible branches and need to store the chain as a tree structure.
Once a branch is denied by more than the half of admission nodes it is removed from the chain (and disk).
Instead we will save the root block of the deleted branch as a `dead branch`.
More precisely we will store the judgements of this block since this is the actual proof.
This enables us to reject this block directly if we receive it at a later point in time (e.g. due to network latency).

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
 2. Is the block created by the expected creator? (refer to [Creator Election](#creator-election))
 3. Is the block creation time older than every alternative block with the same index?
 
If all 3 questions can be answered with yes (again based on the current state), the admission will create an `accept` judgement.
At the same time every alternative branch (every sub-tree with the same index as root) will be updated to a `deny` judgement for every block in the branch.
If one of the questions is answered with no the block will get a `deny` judgement.

As you can see every admission has only one active branch at every point in time.
Since blocks and judgements are broadcast in the network every admission will base its decision on the same information over time.
This means the chain is going to converge to one branch.

### Creator Election
We use some sort of proof of stake during the election of the next block creator.
Every admission has a counter since it created its last block (or was registered as a new admission).
The counter increases continuously.
Whenever an admission node creates a block its counter is reset.
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
> While the election is robust to abandoned admissions it would be more efficient if they would be unregistered and therefore removed from the creator election.

### Synchronization
A new client or a client that was temporarily shut down needs to get the latest state of the blockchain.
Therefore it will ask a direct neighbor to send the latest state.
Since we may already have a part of the chain, we don't need to resend the whole chain.

The started client will send a sync request to any neighbor until one commits to do the synchronization.
Such a sync request contains the requester and the last unique block of the chain. 
This means the client will search for the block with the lowest index that has 2 or more descendant blocks.

The responding node will do the following steps to determine which part of the chain has to be sent:
1. Is the requested block somehow part of the current chain? If not: resend from genesis block.  
*We can't determine if the requested block didn't reach the node yet or was already deleted by deny judgements.*
2. Search if there exists a block with a lower index that has more than 1 descendant. 
Resend from this block instead of the requested block.  
*There exist some new branches that the requesting node isn't aware of.*

After these steps are completed, the responder will resend all blocks and judgements since (and including) the 
determined block.
Additionally it will send all judgments of dead branches. 
This is necessary to enable the requester to delete outdated branches.
