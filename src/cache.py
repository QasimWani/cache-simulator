from load import LoadData
import LinkedList
from math import log2


class Cache():
    """
    Construct an LRU Cache for specific set of parameters
    """
    def __init__(self, cache_size, block_size, placement_type, write_policy, address_size=32):
        """ Initialize cache block with user defined policy """
        
        self.cache_size = cache_size
        self.block_size = block_size
        
        if(placement_type == "DM"):
            placement_type = 1
        elif placement_type == "2W":
            placement_type = 2
        elif placement_type == "4W":
            placement_type = 4
        else:
            placement_type = None
                        
        self.placement_type = placement_type # note: DM - 1; 2W - 2; 4W - 4; FA - None
        self.write_policy = write_policy
        self.address_size = address_size / 8 #32-bit to bytes
        # compute offset
        self.offset = int(log2(block_size))
        # compute number of blocks per set
        self.num_blocks = placement_type if placement_type is not None else cache_size // block_size
        # compute number of sets
        self.num_set    = int ((cache_size / block_size) // self.num_blocks)
        # compute index
        self.index = 0 if self.placement_type is None else int(log2( self.num_set ))
        # compute tag
        self.tag = address_size - self.index - self.offset

        ### Counters
        self.hit_count = 0
        self.miss_count = 0
        self.transfer_mem_cache = 0 # total bytes transfered from memory to the cache
        self.transfer_cache_mem = 0 # total bytes transfered from cache to the memory

        ##### CREATE CACHE #####
        self.CACHE = [None] * self.num_set

    def read(self, address):
        """
        Reads a block of memory from cache
        """
        offset, index, tag = self.getBits(address) #split address into offset, index (if placement_type != FA), tag
        # in order to read from cache, check for cache hit first
        # check for cache size in cache-miss first and if possible, append. otherwise remove LRU block
        if(self.CACHE[index] is None): #miss, guaranteed to have some memory left.
            self.load_new_block(tag, index)
        
        elif (node := self.CACHE[index].containsNodeWithValue(tag)) is not None: #hit
            self.hit_count += 1
            self.CACHE[index].LRU(node, True)
        
        else: #append to set
            # check for memory size first, and only create new node if current_size < total_size
            self.miss_count += 1
            self.transfer_mem_cache += self.block_size
            
            current_size = self.address_size * (self.miss_count + self.hit_count)
            node = LinkedList.Node(0, tag)

            if(current_size >= self.cache_size or self.CACHE[index].getSize() >= self.num_blocks):
                #remove LRU cache block.
                self.CACHE[index].remove(self.CACHE[index].tail)
                
            self.CACHE[index].LRU(node)
            
    def load_new_block(self, tag, index):
        """ Loads a new block to cache on miss """
        self.miss_count += 1
        self.transfer_mem_cache += self.block_size #transfer entire block to memory
        node = LinkedList.Node(0, tag) #create node with dirty and tag bits
        dll  = LinkedList.DoublyLinkedList()
        dll.LRU(node)
        self.CACHE[index] = dll
        
    def store(self, address):
        """ 
        Stores a block of memory into cache
        """
        if self.write_policy == "WB":
            self.writeBack(address)
        else:
            self.writeThrough(address)
            
    def writeBack(self, address):
        """
        Helper method for performing writeback
        """
        offset, index, tag = self.getBits(address) #split address into offset, index (if placement_type != FA), tag
        # in order to write to cache, we need to check for cache hit first.
        # but we also have to make sure that there's enough memory in cache to write to and the valid index has enough free blocks.
        if(self.CACHE[index] is None): #direct miss
            self.load_new_block(tag, index)
            self.transfer_cache_mem += self.address_size
        elif (node := self.CACHE[index].containsNodeWithValue(tag)) is not None: #hit, check for dirty status
            node.dirty = True
            self.hit_count += 1
            self.CACHE[index].LRU(node, True)
        else: #check for valid bit
            self.miss_count += 1
            self.transfer_mem_cache += self.block_size
            
            current_size = self.address_size * (self.miss_count + self.hit_count)
            node = LinkedList.Node(0, tag)

            if(current_size >= self.cache_size or self.CACHE[index].getSize() >= self.num_blocks):
                #remove LRU cache block.
                self.CACHE[index].remove(self.CACHE[index].tail)
                
            self.CACHE[index].LRU(node)
            
            
    def writeThrough(self, address):
        """
        Helper method for performing writethrough
        """
        offset, index, tag = self.getBits(address) #split address into offset, index (if placement_type != FA), tag
        # in order to write to cache, we need to check for cache hit first.
        # but we also have to make sure that there's enough memory in cache to write to and the valid index has enough free blocks.
        if(self.CACHE[index] is None): #miss, guaranteed to have some memory left.
            self.load_new_block(tag, index, self.address_size)
            self.transfer_cache_mem += self.address_size
            
        elif (node := self.CACHE[index].containsNodeWithValue(tag)) is not None: #hit
            self.transfer_cache_mem += self.address_size
            self.CACHE[index].LRU(node, True)
            
        else:
            # check for memory size first, and only create new node if current_size < total_size
            self.miss_count += 1
            self.transfer_mem_cache += self.block_size
            self.transfer_cache_mem += self.address_size
            
            current_size = self.address_size * (self.miss_count + self.hit_count)
            node = LinkedList.Node(0, tag)

            if(current_size >= self.cache_size or self.CACHE[index].getSize() >= self.num_blocks):
                #remove LRU cache block.
                self.CACHE[index].remove(self.CACHE[index].tail)
                
            self.CACHE[index].LRU(node)
    
    def getBits(self, address):
        """ 
        Generates offset, index, and tag bits 
        """
        offset_bits = address[0 : self.offset][::-1]
        index_bits  = self.index if (self.placement_type is None or self.offset <= self.offset + self.index) else int(address[self.offset : self.offset + self.index][::-1], 2)
        tag_bits    = address[-self.tag :][::-1]
        
        return offset_bits, index_bits, tag_bits