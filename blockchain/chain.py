"""This module implements the chain functionality."""
import logging
import os
from collections import deque
from subprocess import CalledProcessError
from threading import RLock, current_thread
from .block import Block
from .config import CONFIG
from blockchain.transaction import *
from anytree import Node, RenderTree
from anytree.search import find, findall
from anytree.exporter import DotExporter

logger = logging.getLogger("blockchain")


class Chain(object):
    """Basic chain class."""
    class __Chain:
        def __init__(self, load_persisted=True):
            """Create initial chain and tries to load saved state from disk."""
            self.genesis_block = None
            self.chain_tree = None
            self.dangling_blocks = set()
            self._lock = RLock()
            if load_persisted and self._can_be_loaded_from_disk():
                self._load_from_disk()

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
            for pre, fill, node in RenderTree(self.chain_tree):
                node_representation = "{}index: {}, hash: {}\n".format(pre,
                                                                       node.index,
                                                                       node.name)
                tree_representation += node_representation
            return tree_representation

        def _can_be_loaded_from_disk(self):
            """Return if the blockchain can be loaded from disk.

            True if the blockchain persistance folder
            and the genesis block file are present.
            """
            return os.path.isdir(CONFIG["persistance_folder"]) and \
                   len([f for f in os.listdir(CONFIG["persistance_folder"])
                        if f.startswith("0_")]) == 1  # there should only be one genesis file starting with '0_..._...'

        def _load_from_disk(self):
            current_block_level = 0
            block_files = os.listdir(CONFIG["persistance_folder"])
            level_prefix = str(current_block_level) + "_"
            blocks_at_current_level = [f for f in block_files if f.startswith(level_prefix)]
            while len(blocks_at_current_level) > 0:
                for block_name in blocks_at_current_level:
                    block_path = os.path.join(CONFIG["persistance_folder"], block_name)
                    with open(block_path, "r") as block_file:
                        logger.info("Loading block {} from disk".format(block_path))
                        recreated_block = Block(block_file.read())
                        self.add_block(recreated_block)
                current_block_level += 1
                level_prefix = str(current_block_level) + "_"
                blocks_at_current_level = [f for f in block_files if f.startswith(level_prefix)]
            logger.info("Finished loading chain from disk")

        def add_block(self, block):
            """Add a block to the blockchain tree.

            TODO: It might happen that a block does not fit into the chain, because the
            previous block was not received until that point. Thus, we have to add
            to the set of dangling block. This methods returns True, if the new
            block was added to the chain, otherwise False.
            """
            with self._lock:
                # Check if block is genesis and no genesis is present
                if not self.chain_tree and block.index == 0:
                    block_creation_cache = deque()
                    doctors_cache = set()
                    vaccine_cache = set()
                    self._update_caches(block, block_creation_cache, doctors_cache, vaccine_cache)

                    self.chain_tree = self._generate_tree_node(block,
                                                               block_creation_cache,
                                                               doctors_cache,
                                                               vaccine_cache)
                    self.genesis_block = block
                    logger.debug("Added genesis to chain.")
                else:
                    # No genesis, just regular block
                    # Full client ensures, that previous block is present
                    parent_node = find(self.chain_tree,
                                       lambda node: node.name == block.previous_block)
                    block_creation_cache = parent_node.block_creation_cache.copy()
                    doctors_cache = set().union(parent_node.doctors_cache)
                    vaccine_cache = set().union(parent_node.vaccine_cache)
                    self._update_caches(block, block_creation_cache, doctors_cache, vaccine_cache)
                    self._generate_tree_node(block, block_creation_cache, doctors_cache, vaccine_cache, parent_node)

                logger.debug("Added block {} to chain.".format(block.index))

                if os.getenv("RENDER_CHAIN_TREE") == '1':
                    # graphviz needs to be installed for the next line!
                    try:
                        DotExporter(self.chain_tree,
                                    nodenamefunc=nodenamefunc,
                                    nodeattrfunc=nodeattrfunc
                                    ).to_picture(os.path.join(CONFIG["persistance_folder"], 'current_state.png'))
                    except CalledProcessError as e:
                        logger.debug("Couldn't print chain tree: {}".format(e.stdout))
                return True

        def _generate_tree_node(self, block, block_creation_cache, doctors_cache, vaccine_cache, parent_node=None):
            return Node(block.hash,
                        index=block.index,
                        parent=parent_node,
                        block=block,
                        block_creation_cache=block_creation_cache,
                        doctors_cache=doctors_cache,
                        vaccine_cache=vaccine_cache)

        def _update_caches(self, block, block_creation_cache, doctors_cache, vaccine_cache):
            """Update the block creation cache and refresh the registered doctors and vaccines."""
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

        def find_blocks_by_index(self, index):
            """Find blocks by its index. Return None at invalid index."""
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
            return findall(self.chain_tree, lambda node: node.index == index)

        def find_block_by_hash(self, hash):
            """Find a block by its hash. Return None if hash not found."""
            block_node = self._find_tree_node_by_hash(hash)
            if block_node:
                return block_node.block
            return

        def _find_tree_node_by_hash(self, hash):
            return find(self.chain_tree, lambda node: node.name == hash)

        def get_leaves(self):
            """Return all possible leaf blocks of the chain."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                return [leaf.block for leaf in leaves]

        def remove_tree_at_hash(self, node_hash):
            """Delete a side chain by removing a branch.

            Remove a whole branch by detaching its root node.
            """
            with self._lock:
                node_to_delete = find(self.chain_tree, lambda node: node.hash == node_hash)
                if node_to_delete:
                    node_to_delete.parent = None
                    #TODO delete block file from disk
                else:
                    logger.info("Block with hash {} not found".format(node_hash))

        def get_tree_list_at_hash(self, hash):
            """Collect all descendants from the specified node."""
            selected_node = find(self.chain_tree, lambda node: node.hash == hash)
            if selected_node:
                return [node.block for node in selected_node.descendants]
            else:
                return []

        def get_block_creation_history_by_hash(self, n, hash):
            """Return list [public keys of the oldest n blockcreating admission nodes].
            Return None if n is out of bounds for the given leaf."""
            with self._lock:
                node = self._find_tree_node_by_hash(hash)
                if n > len(node.block_creation_cache) or n < 0:
                    return
                block_creation_history = []
                for i in range(n):
                    block_creation_history.append(node.block_creation_cache[i])
                return block_creation_history

        def get_admissions(self):
            """Return list of tuples (hash, set  of currently registered admissions) of every leaf in the chain tree."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                result = []
                for leave in leaves:
                    # in case of changing this method do not return a reference to the original leave.block_creation_cache!
                    result.append((leave.name, set(leave.block_creation_cache)))

                return result

        def _get_all_leaf_nodes(self):
            return findall(self.chain_tree, lambda node: node.is_leaf is True)

        def get_doctors(self):
            """Return list of tuples (hash, set of currently registered doctors)."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                result = []
                for leaf in leaves:
                    result.append((leaf.name, set(leaf.doctors_cache)))
                return result

        def get_vaccines(self):
            """Return a list of tuples (hash, set of currently registered vaccines)."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                result = []
                for leaf in leaves:
                    result.append((leaf.name, set(leaf.vaccine_cache)))
                return result

        def get_registration_caches(self):
            """Return a list of tuples (hash, set(admissions), set(doctors), set(vaccines))."""
            with self._lock:
                leaves = self._get_all_leaf_nodes()
                result = []
                for leaf in leaves:
                    result.append((leaf.name,
                                   set(leaf.block_creation_cache),
                                   set(leaf.doctors_cache),
                                   set(leaf.vaccine_cache)))
                return result

        def get_registration_caches_by_blockhash(self, hash):
            """Return a tuple of sets containing the registered admissions, doctors,
            and vaccines at the blockheight of the given hash."""
            with self._lock:
                tree_node = self._find_tree_node_by_hash(hash)
                return set(tree_node.block_creation_cache), set(tree_node.doctors_cache), set(tree_node.vaccine_cache)

        def get_registration_caches_by_blockindex(self, index):
            """Return a list of tuples of hash and sets containing the registered admissions, doctors,
            and vaccines of blocks with the given blockindex."""
            with self._lock:
                tree_nodes = self._find_tree_nodes_by_index(index)
                result = []
                for node in tree_nodes:
                    result.append((node.name,
                                   set(node.block_creation_cache),
                                   set(node.doctors_cache),
                                   set(node.vaccine_cache)
                                   ))
                return result

        def get_parent_block_by_hash(self, hash):
            node = self._find_tree_node_by_hash(hash)
            parent_node = node.parent
            return parent_node.block

        def lock_state(self):
            return self._lock._is_owned()

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
    return "Index: {}\n" \
           "Hash: {}".format(node.index, node.name)


def nodeattrfunc(node):
    if node.index == 0:
        return "style = filled,fillcolor = red, shape = rectangle"
    else:
        return "shape = rectangle"
