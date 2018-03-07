"""This module implements the chain functionality."""
import logging
import os
import threading
from collections import deque
from subprocess import CalledProcessError
from threading import RLock, current_thread
from Crypto.PublicKey import RSA

from blockchain.network.network import Network
from .block import Block
from .config import CONFIG
from blockchain.transaction import *
from anytree import Node, RenderTree
from anytree.search import find, findall
from anytree.exporter import DotExporter
# noinspection PyUnresolvedReferences
from blockchain.judgement import Judgement

logger = logging.getLogger("blockchain")


class Chain(object):
    """Chain Singleton

    Provide methods to load or store blocks, judgements and dead branches.
    Furthermore handle every interaction with the blockchain itself (e.g. add blocks/judgements, search for blocks).
    """
    class __Chain:
        def __init__(self, load_persisted=True):
            """Create initial chain and tries to load saved state from disk."""
            self.genesis_block = None
            self.chain_tree = None
            self.dangling_nodes = set()
            self._lock = RLock()
            if load_persisted and self._can_be_loaded_from_disk():
                self._load_from_disk()

        def _can_be_loaded_from_disk(self):
            """Return if the blockchain can be loaded from disk.

            True if the blockchain persistance folder and the genesis block file are present.
            """
            return os.path.isdir(CONFIG.persistance_folder) and \
                   len([f for f in os.listdir(CONFIG.persistance_folder)
                        if f.startswith("0_")]) == 1  # there should only be one genesis file starting with '0_..._...'

        def _load_from_disk(self):
            """Recreate blockchain tree from disk

            Read every block from disk, search its judgements and create tree node.
            """
            current_block_level = 0
            block_files = os.listdir(CONFIG.persistance_folder)
            level_prefix = str(current_block_level) + "_"
            blocks_at_current_level = [f for f in block_files if f.startswith(level_prefix)]
            while len(blocks_at_current_level) > 0:
                for block_name in blocks_at_current_level:
                    block_path = os.path.join(CONFIG.persistance_folder, block_name)
                    with open(block_path, "r") as block_file:
                        logger.info("Loading block {} from disk".format(block_path))
                        recreated_block = Block(block_file.read())
                        judgements = self._load_judgements_from_disk(self._get_judgement_path(block_name))
                        self.add_block(recreated_block, judgements=judgements)
                current_block_level += 1
                level_prefix = str(current_block_level) + "_"
                blocks_at_current_level = [f for f in block_files if f.startswith(level_prefix)]
            logger.info("Finished loading chain from disk")

        def _load_judgements_from_disk(self, file_path):
            """Load judgements from a file.

            :param file_path: Filename of the file containing judgements. 1 per line
            :return: dict of judgements <sender of judgement>: <judgement>
            """
            judgements = {}
            try:
                with open(file_path, "r") as file:
                    for line in file:
                        judgement = eval(line)
                        judgements[judgement.sender_pubkey] = judgement
            except FileNotFoundError:
                pass
            return judgements

        def add_block(self, block, judgements=None):
            """Add a block to the blockchain tree.

            This method adds a block to the chain tree and returns a set of blocks, that needs
            to be denied due to the new block.
            Remove block from set of dangling blocks if present.

            :param block: Block object that should be added.
            :param judgements: Optional dict of judgements <sender of judgement>: <judgement>
            :return: Set of blocks that needs to be invalidated.
            """
            if not judgements:
                judgements = {}
            with self._lock:
                # Check if block is genesis and no genesis is present
                invalidated_blocks = set()

                if not self.chain_tree and block.index == 0:
                    block_creation_cache = deque()
                    doctors_cache = set()
                    vaccine_cache = set()
                    self._update_caches(block, block_creation_cache, doctors_cache, vaccine_cache)

                    self.chain_tree = self._generate_tree_node(block,
                                                               block_creation_cache,
                                                               doctors_cache,
                                                               vaccine_cache,
                                                               judgements=judgements)
                    self.genesis_block = block
                    logger.debug("Added genesis to chain.")
                else:
                    # No genesis, just regular block
                    # Full client ensures, that previous block is present
                    if self.find_block_by_hash(block.hash):
                        # block is already part of the chain
                        return invalidated_blocks
                    parent_node = find(self.chain_tree,
                                       lambda node: node.name == block.previous_block)
                    block_creation_cache = parent_node.block_creation_cache.copy()
                    doctors_cache = set().union(parent_node.doctors_cache)
                    vaccine_cache = set().union(parent_node.vaccine_cache)
                    self._update_caches(block, block_creation_cache, doctors_cache, vaccine_cache)
                    if self.is_block_dangling(block):
                        dangling_node = self._remove_block_from_dangling_list(block)
                        judgements = dangling_node.judgements
                    new_node = self._generate_tree_node(block, block_creation_cache, doctors_cache, vaccine_cache,
                                             parent_node=parent_node, judgements=judgements)

                    self._persist_judgements_for_node(new_node)

                    for node in new_node.siblings:
                        if new_node.block.timestamp > node.block.timestamp:
                            invalidated_blocks.add(new_node.block)
                            break

                    if len(invalidated_blocks) == 0:
                        # WONTFIX: only return list of blocks of nodes in the branch that needs to be invalidated.
                        # This will need some architectural changes
                        for node in new_node.siblings:
                            invalidated_blocks.add(node.block)
                            for node2 in node.descendants:
                                invalidated_blocks.add(node2.block)

                logger.debug("Added block {} to chain.".format(block.index))

                return invalidated_blocks

        def _update_caches(self, block, block_creation_cache, doctors_cache, vaccine_cache):
            """Update the block creation, doctor and vaccine cache.

            :param block: Block object of the new block whose contents should be added to the caches.
            :param block_creation_cache: A `deque` object representing the queue of admission sorted by age.
            :param doctors_cache: Set of doctors.
            :param vaccine_cache: Set of vaccines.
            """
            with self._lock:
                self._update_block_creation_cache(block, block_creation_cache)
                for transaction in block.transactions:
                    if type(transaction).__name__ == "PermissionTransaction":
                        if transaction.requested_permission is Permission.doctor:
                            doctors_cache.add(transaction.sender_pubkey)
                    elif type(transaction).__name__ == "VaccineTransaction":
                        vaccine_cache.add(transaction.vaccine)

        def _update_block_creation_cache(self, block, block_creation_cache):
            """Refresh the block creation cache.

            Moves the current block creator to the right side of the queue,
            adds any new admission nodes to the left side of the queue in the order
            they appear in the block.
            """
            with self._lock:
                block_creator = block.public_key
                if block_creator in block_creation_cache:
                    block_creation_cache.remove(block_creator)
                block_creation_cache.append(block_creator)
                for transaction in block.transactions:
                    if type(transaction).__name__ == "PermissionTransaction":
                        if transaction.requested_permission is Permission.admission:
                            block_creation_cache.appendleft(transaction.sender_pubkey)

        def _generate_tree_node(self, block, block_creation_cache=None, doctors_cache=None, vaccine_cache=None,
                                parent_node=None, judgements=None):
            """Create tree node

            The params `block_creation_cache`, `doctors_cache`, `vaccine_cache` should already
            contain the contents of the block.

            :param block: Block of the node
            :param block_creation_cache: Queue of block creators.
            :param doctors_cache: Set of doctors.
            :param vaccine_cache: Set of vaccines
            :param parent_node: Parent Node object. If `None` it creates a root Node.
            :param judgements: Dict of judgements
            :return: Node object that is already part of the tree.
            """
            if not judgements:
                judgements = {}
            return Node(block.hash,
                        index=block.index,
                        parent=parent_node,
                        block=block,
                        block_creation_cache=block_creation_cache,
                        doctors_cache=doctors_cache,
                        vaccine_cache=vaccine_cache,
                        judgements=judgements)

        def _remove_block_from_dangling_list(self, block):
            """Remove block from the set of dangling tree nodes.

            :return: tree node containing block. None if block is not dangling.
            """
            for node in self.dangling_nodes:
                if node.block == block:
                    self.dangling_nodes.discard(node)
                    return node
            return None

        def update_judgements(self, judgement):
            """Attach  judgement to node with the corresponding block.

            :return: True if the judgement was new, False if it was already there
            """
            changed_judgments= False
            with self._lock:
                node = self._find_tree_node_by_hash(judgement.hash_of_judged_block)
                if node:
                    if judgement.sender_pubkey in node.judgements:  # already received a judgement from that node
                        if node.judgements[judgement.sender_pubkey].accept_block and not judgement.accept_block:  # judgement was revoked
                            node.judgements[judgement.sender_pubkey] = judgement  # replace old judgement with the new one
                            changed_judgments = True
                    else:
                        node.judgements[judgement.sender_pubkey] = judgement
                        changed_judgments = True

                    self._persist_judgements_for_node(node)
                    self._check_branch_for_deletion(node)

                else:
                    node = self._get_dangling_node_by_hash(judgement.hash_of_judged_block)
                    if not node:
                        # since blocks are send before judgements by every node, this shouldn't happen.
                        logger.debug("Could not add judgement, block with hash {} not found in tree or dangling blocks"
                                     .format(judgement.hash_of_judged_block))
                        return changed_judgments

                    if judgement.sender_pubkey in node.judgements:  # already received a judgement from that node
                        if node.judgements[judgement.sender_pubkey].accept_block and not judgement.accept_block:  # judgement was revoked
                            node.judgements[judgement.sender_pubkey] = judgement  # replace old judgement with the new one
                            changed_judgments = True
                    else:
                        node.judgements[judgement.sender_pubkey] = judgement
                        changed_judgments = True
                return changed_judgments

        def _persist_judgements_for_node(self, node):
            """Save judgements of contained in node onto disk."""
            file_name = self._get_file_name(node=node)
            judgement_path = os.path.join(CONFIG.persistance_folder, 'judgements', file_name)
            if not os.path.exists(os.path.dirname(judgement_path)):
                os.makedirs(os.path.dirname(judgement_path))
            with open(judgement_path, 'w') as file:
                for judgement in node.judgements:
                    file.write(repr(node.judgements[judgement]) + '\n')

        def _get_dangling_node_by_hash(self, hash_of_judged_block):
            """Return tree node with corresponding hash_of_judged_block"""
            for node in self.dangling_nodes:
                if node.block.hash == hash_of_judged_block:
                    return node

        def _check_branch_for_deletion(self, node):
            """Check if a branchs needs to be deleted and delete if necessary"""
            number_of_denies = 0
            for judgement in node.judgements:
                if not node.judgements[judgement].accept_block:
                    number_of_denies += 1

            # The admission that created the block doesn't judge. Therefore '-1'
            number_of_admissions = len(self.get_registration_caches_by_blockhash(node.block.previous_block)) - 1
            if number_of_denies > number_of_admissions / 2:
                logger.debug("Going to remove sub tree starting with block: {}".format(node.block))
                self._remove_tree_at_node(node)

        def _remove_tree_at_node(self, node):
            """Delete a branch by removing a subtree.

            Remove a whole branch by detaching its root node and deleting all files associated with any node of
            the subtree.
            Resend a list of transactions that was unique in this subtree concurrently.
            """
            unique_transactions = []
            with self._lock:
                parent_node = node.parent
                node.parent = None
                nodes_to_delete = node.descendants
                for tx in node.block.transactions:
                    if not self._is_transaction_in_subtree(tx, parent_node):
                        unique_transactions.append(tx)
                self._remove_block_file(node)
                self._save_dead_branch(node)
                for node in nodes_to_delete:
                    for tx in node.block.transactions:
                        if not self._is_transaction_in_subtree(tx, parent_node):
                            unique_transactions.append(tx)
                    self._remove_block_file(node)
                    self._remove_judgement_file(node)
                t = threading.Thread(target=self._resend_transactions,
                                     args=(unique_transactions,),
                                     name="resend transactions",
                                     daemon=True)
                t.start()

        def _is_transaction_in_subtree(self, tx, root_node):
            """Check if a transaction tx is contained in a subtree underneath root_node."""
            for node in root_node.descendants:
                if tx in node.block.transactions:
                    return True
            return False

        def _remove_block_file(self, node):
            """Remove block in node from disk"""
            file_name = self._get_file_name(node=node)
            persistence_folder = CONFIG.persistance_folder
            file_path = os.path.join(persistence_folder, file_name)
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass

        def _remove_judgement_file(self, node):
            """
            Remove judgement files associated with this node.

            The method removes the current judgement file of the node and checks if there are any dead branch files of
            former childs. Those files are removed as well.
            """
            file_name = self._get_file_name(node=node)
            judgement_path = self._get_judgement_path(file_name)
            try:
                os.remove(judgement_path)
            except FileNotFoundError:
                pass

            dead_branch_path = self._get_dead_branch_path()
            try:
                dead_branch_files = os.listdir(dead_branch_path)
            except FileNotFoundError:
                dead_branch_files = []
            level_prefix = str(node.block.index + 1) + "_" + str(node.block.hash)
            old_dead_branches = [f for f in dead_branch_files if f.startswith(level_prefix)]

            for dead_branch in old_dead_branches:
                try:
                    os.remove(dead_branch)
                except FileNotFoundError:
                    pass  #file already removed by another thread

        def _resend_transactions(self, transactions):
            """Send transactions to myself.

            :param transactions: Iterable of transactions.
            """
            for tx in transactions:
                Network.send_transaction('http://localhost:9000', repr(tx))

        def _save_dead_branch(self, node):
            """Save dead branch to disk.

            Save node as dead branch to disk and remove the judgements file.
            """
            file_name = self._get_file_name(node=node)
            judgement_path = self._get_judgement_path(file_name)
            dead_branch_path = self._get_dead_branch_path(file_name)
            if not os.path.exists(os.path.dirname(dead_branch_path)):
                os.makedirs(os.path.dirname(dead_branch_path))
            try:
                os.rename(judgement_path, dead_branch_path)
            except FileNotFoundError:
                pass  # For safety. Shouldn't occur.

        def add_dangling_block(self, block):
            """Transform node into tree node and add it to the set of dangling nodes."""
            with self._lock:
                node = self._generate_tree_node(block)
                if not self.is_block_dangling(block):
                    self.dangling_nodes.add(node)

        def get_leaves(self):
            """Return list of all leaf blocks of the chain."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                return [leaf.block for leaf in leaves]

        def _get_all_leaf_nodes(self):
            """Return list of all leaf nodes of the chain tree."""
            return findall(self.chain_tree, lambda node: node.is_leaf is True)

        def get_admissions(self):
            """Return list of tuples (hash, set  of currently registered admissions) of every leaf in the chain tree."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                result = []
                for leave in leaves:
                    # in case of changing this method do not return a reference to the original leave.block_creation_cache!
                    result.append((leave.name, set(leave.block_creation_cache)))

                return result

        def get_registration_caches(self):
            """Return a list of tuples (hash, set(admissions), set(doctors), set(vaccines)) of every leaf in the
            chain tree."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                result = []
                for leaf in leaves:
                    result.append((leaf.name,
                                   set(leaf.block_creation_cache),
                                   set(leaf.doctors_cache),
                                   set(leaf.vaccine_cache)))
                return result

        def get_tree_list_at_hash(self, hash):
            """Return all blocks after the given hash.

            :param hash: Hash of the block whose decedents should be returned.
            :return: [] if hash is not part of the chain.
            """
            selected_node = find(self.chain_tree, lambda node: node.block.hash == hash)
            if selected_node:
                return [node.block for node in selected_node.descendants]
            else:
                return []

        def find_blocks_by_index(self, index):
            """Find all blocks with index.
            Return None if index is not part of the chain."""
            with self._lock:
                nodes = self._find_tree_nodes_by_index(index)
                if nodes:
                    result = []
                    for node in nodes:
                        result.append(node.block)
                    return result
                else:
                    return

        def _find_tree_nodes_by_index(self, index):
            """Find all nodes with index"""
            return findall(self.chain_tree, lambda node: node.index == index)

        def find_block_by_hash(self, hash):
            """Find a block by its hash.
            Return None if hash not in tree. Dangling Nodes are ignored."""
            block_node = self._find_tree_node_by_hash(hash)
            if block_node:
                return block_node.block
            return

        def _find_tree_node_by_hash(self, hash):
            """Find tree node with hash."""
            return find(self.chain_tree, lambda node: node.name == hash)

        def get_block_creation_history_by_hash(self, n, hash):
            """Return list [public keys of the oldest n blockcreating admission nodes].
            Return None if n is out of bounds for the cache of the given hash."""
            with self._lock:
                node = self._find_tree_node_by_hash(hash)
                if n > len(node.block_creation_cache) or n < 0:
                    return
                block_creation_history = []
                for i in range(n):
                    block_creation_history.append(node.block_creation_cache[i])
                return block_creation_history

        def get_registration_caches_by_blockhash(self, hash):
            """Return a tuple of sets containing the registered admissions, doctors,
            and vaccines at hash."""

            with self._lock:
                tree_node = self._find_tree_node_by_hash(hash)
                return set(tree_node.block_creation_cache), set(tree_node.doctors_cache), set(tree_node.vaccine_cache)

        def get_parent_block_by_hash(self, hash):
            """Return parent block of hash.

            This method doesn't check if hash is part of the tree. Use `find_block_by_hash` to check if the
            block is part of the chain.
            """
            node = self._find_tree_node_by_hash(hash)
            parent_node = node.parent
            return parent_node.block

        def is_dead_branch_root(self, block):
            """Check if block is the root of a dead_branch"""
            file_name = self._get_file_name(block=block)
            dead_branch_path = self._get_dead_branch_path(file_name)
            return os.path.exists(dead_branch_path)

        def is_block_dangling(self, block):
            """Check if block is a dangling block"""
            with self._lock:
                for node in self.dangling_nodes:
                    if node.block == block:
                        return True
                return False

        def get_list_of_dangling_blocks(self):
            """Return list of currently dangling blocks."""
            blocks = []
            with self._lock:
                for node in self.dangling_nodes:
                    blocks.append(node.block)
                return blocks

        def get_first_branching_block(self):
            """Return the first block which has more than one following block."""
            with self._lock:
                current_node = self.chain_tree
                while current_node.children:
                    if len(current_node.children) != 1:
                        # The current node has no children == end of chain or we have more than one branch
                        return current_node.block
                    current_node = current_node.children[0]
                return current_node.block

        def get_judgements_for_blockhash(self, blockhash):
            """Return list of judgements of blockhash."""
            judgement_dict = self._find_tree_node_by_hash(blockhash).judgements
            judgements = []
            for judge in judgement_dict:
                judgements.append(judgement_dict[judge])

            return judgements

        def get_dead_branches_since_blockhash(self, blockhash):
            """Return a list of judgements of all dead branches after blockhash."""
            path = self._get_dead_branch_path()
            try:
                content = os.listdir(path)
            except FileNotFoundError:
                content = []
            min_index = self._find_tree_node_by_hash(blockhash).block.index
            if not content:
                return []
            max_index = int(max(content).split('_')[0])
            judgements = []
            for index in range(min_index, max_index+1):
                files = [s for s in content if s.startswith(str(index)+'_')]
                for file in files:
                    judgement_dict = self._load_judgements_from_disk(self._get_dead_branch_path(file))
                    for judge in judgement_dict:
                        judgements.append(judgement_dict[judge])
            return judgements

        def lock_state(self):
            """Return if Chain is locked by another thread."""
            return self._lock._is_owned()

        def _get_judgement_path(self, file_name):
            return os.path.join(CONFIG.persistance_folder, 'judgements', file_name)

        def _get_dead_branch_path(self, file_name=None):
            if file_name:
                return os.path.join(CONFIG.persistance_folder, 'dead_branches', file_name)
            return os.path.join(CONFIG.persistance_folder, 'dead_branches')

        def _get_file_name(self, node=None, block=None):
            if node:
                return "_".join([str(node.block.index), node.block.previous_block, node.block.hash])
            if block:
                return "_".join([str(block.index), block.previous_block, block.hash])

        def render_current_tree(self):
            """Render tree for demo.

            Render tree as png graphic and save in configured persistance folder.
            """
            if os.getenv("RENDER_CHAIN_TREE") == '1':
                # graphviz needs to be installed for the next line!
                try:
                    DotExporter(self.chain_tree,
                                nodenamefunc=nodenamefunc,
                                nodeattrfunc=nodeattrfunc
                                ).to_picture(os.path.join(CONFIG.persistance_folder, 'current_state.png'))
                except CalledProcessError as e:
                    logger.debug("Couldn't print chain tree: {}".format(e.stdout))

        def __enter__(self):
            self._lock.acquire()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._lock.release()
            if exc_type or exc_val or exc_tb:
                logger.exception("Thread '{}' got an exception within a with \
                                 statement. Type: {}; Value: {}; Traceback:"
                                 .format(current_thread(),
                                         exc_type,
                                         exc_val))

        def __str__(self):
            tree_representation = ""
            if not self.chain_tree:
                return tree_representation
            for pre, fill, node in RenderTree(self.chain_tree):
                node_representation = "{}index: {}, hash: {}\n".format(pre,
                                                                       node.index,
                                                                       node.name)
                tree_representation += node_representation
            return tree_representation

    __instance = None

    def __new__(cls, load_persisted=True):
        """Create a singleton instance of the chain."""
        if cls.__instance is None:
            cls.__instance = Chain.__Chain(load_persisted=load_persisted)
        return cls.__instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)


def nodenamefunc(node):
    """Render graphic content of node.
    One Node is represented by its index, Hash, no. of transactions, accepts and denies.
    """
    denies = 0
    accepts = 0
    for judgement in node.judgements:
        if node.judgements[judgement].accept_block:
            accepts += 1
        else:
            denies += 1
    return "Index: {}\n" \
           "Hash: {}\n" \
           "Transactions: {} | Accepts: {} | Denies: {}".format(
                                        node.index,
                                        node.name,
                                        len(node.block.transactions),
                                        accepts,
                                        denies)


def nodeattrfunc(node):
    """Render appearance of node in graphic.
    Blocks generated by the client itself are darker green.
    Path that is currently accepted by the client is lighter green.
    Every other path is red.
    """
    key_folder = CONFIG.key_folder
    path = os.path.join(key_folder, CONFIG.key_file_names[0])
    with open(path, "rb") as key_file:
        public_key = RSA.import_key(key_file.read()).exportKey("DER")

    if public_key == node.block.public_key:
        return "style = filled,fillcolor = green4, shape = rectangle"
    elif public_key in node.judgements:
        if node.judgements[public_key].accept_block:
            return "style = filled,fillcolor = green3, shape = rectangle"
        else:
            return "style = filled,fillcolor = red3, shape = rectangle"
    else:
        return "shape = rectangle"
