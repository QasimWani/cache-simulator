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
        self.placement_type = placement_type # note: DM - 1; 2W - 2; 4W - 4; FA - None
        self.write_policy = write_policy
        self.address_size = address_size

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
        print(self.CACHE)
        
        # in order to read from cache, check for cache hit first
        # check for cache size in cache-miss first and if possible, append. otherwise remove LRU block
        if(self.CACHE[index] is None): #miss, guaranteed to have some memory left.
            self.miss_count += 1
            self.transfer_mem_cache += self.address_size #transfer 32 bytes to memory
            node = LinkedList.Node(0, tag) #create node with dirty and tag bits
            dll  = LinkedList.DoublyLinkedList()
            dll.LRU(node)
            self.CACHE[index] = dll
        
        elif (node := self.CACHE[index].containsNodeWithValue(tag)) is not None: #hit
            self.hit_count += 1
            self.CACHE[index].LRU(node, True)
        
        else: #append to set
            # check for memory size first, and only create new node if current_size < total_size
            self.miss_count += 1
            self.transfer_mem_cache += self.address_size
            
            current_size = self.address_size * (self.miss_count + self.hit_count)
            node = LinkedList.Node(0, tag)

            if(current_size >= self.cache_size or self.CACHE[index].getSize() >= self.num_blocks):
                #remove LRU cache block.
                self.CACHE[index].remove(self.CACHE[index].tail)
                
            self.CACHE[index].LRU(node)
            


    def store(self, address):
        """ 
        Stores a block of memory into cache
        """
        pass

    def getBits(self, address):
        """ 
        Generates offset, index, and tag bits 
        """
        offset_bits = address[0 : self.offset][::-1]
        index_bits  = self.index if (self.placement_type is None) else int(address[self.offset : self.offset + self.index][::-1], 2)
        tag_bits    = address[-self.tag :][::-1]
        
        return offset_bits, index_bits, tag_bits

def to_bin(address):
    return bin(int(address, 16))[2:].zfill(32)[::-1]

if __name__ == "__main__":
    temp = Cache(1024, 4, None, "WB")
    print("Num set", temp.num_set)
    print("Num block", temp.num_blocks)
    
    temp.read(to_bin("0x00000010"))
    temp.read(to_bin("0x00000018"))
    temp.read(to_bin("0x00000020"))
    temp.read(to_bin("0x00000028"))
    temp.read(to_bin("0x00000050"))
    
    # print(temp.miss_count, temp.hit_count)
    # print(temp.transfer_mem_cache)