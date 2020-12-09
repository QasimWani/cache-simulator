from cache import Cache
from load import LoadData

# for plotting
import matplotlib.pyplot as plt

CACHE_SIZE = [1024, 2048, 8192, 65536]
BLOCK_SIZE = [4, 8, 32, 256]
CACHE_PLACEMENT = ["DM", "2W", "4W", "FA"] #1,2,4,None
WRITE_POLICY = ["WB", "WT"]


def simulate(file, cache_size, block_size, placement_type, write_policy):
    cache = Cache(cache_size, block_size, placement_type, write_policy)
    for instruction in memory:
        policy, word = instruction
        if(policy == "load"):
            cache.read(word)
        elif (policy == "store"):
            cache.store(word)
    
    num_index = len(memory)
    hit_rate = cache.hit_count / num_index
    result = str(cache.cache_size) + "\t" + str(cache.block_size) + "\t" + str(placement_type) + "\t" + str(cache.num_blocks) + "\t" + str(cache.write_policy) + "\t" + str(num_index) + "\t" + str(round(hit_rate, 2)) + "\t\t" + str(cache.transfer_mem_cache) + "\t" + str(cache.transfer_cache_mem)
    file.write(result + "\n")
    
def run(file_to_write):
    for size in CACHE_SIZE:
        for block in BLOCK_SIZE:
            for placement in CACHE_PLACEMENT:
                for write in WRITE_POLICY:
                    simulate(file_to_write, size, block, placement, write)
                    
                    

if __name__ == "__main__":
    memory = LoadData("../data/simple5-4xWalk2020.trace").read() #const
    filename = "../data/test.result"
    f = open(filename, 'a') #set to append mode
    run(f)
    f.close()