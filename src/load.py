class LoadData():
    """
    Loads data from a trace input file into an array of shape (N, 2), where N represents the Total Memory Requests and 2 represents cache input.
    """
    def __init__(self, filename):
        #assuming N x 2.
        self.filename = filename
        self.memory = []
    def to_bin(self, address):
        """ Convert hex string to 32 bit binary """
        return bin(int(address, 16))[2:].zfill(32)[::-1]

    def read(self):
        """ Read data from a file delimiterized by \n """
        f = open(self.filename,'r')
        content = f.readlines()
        for data in content:
            function, address = data.strip().split("\t")
            self.memory.append([function, self.to_bin(address)]) #simulate main memory
        return self.memory
    
    def __len__(self):
        """ Override the length property to return number of elements """
        return len(self.memory)