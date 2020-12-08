class LoadData():
    """
    Loads data from a trace input file into an array of shape (N, 2), where N represents the Total Memory Requests and 2 represents cache input.
    """
    def __init__(self, filename):
        #assuming N x 2.
        self.filename = filename
    
    def to_bin(address):
        """ Convert hex string to 32 bit binary """
        return bin(int(address, 16))[2:].zfill(32)[::-1]

    def read(self):
        """ Read data from a file delimiterized by \n """
        f = open(self.filename,'r')
        content = f.readlines()
        memory = []
        for data in content:
            function, address = data.strip().split("\t")
            memory.append([function, self.to_bin(address)]) #simulate main memory
        return memory