"""
@author: Michael Kaspera
"""
from math import inf

class CountMinSketch():
    '''
    classdocs
    '''


    def __init__(self, row_size, num_hash_functions):
        """
        @param row_size: how many rows the CountMin Sketch data structure should have
        @param num_hash_functions: the number of different hash functions the CountMin Sketch data structure uses
        """
        self.row_size = int(row_size)
        self.table = [[0 for _ in range(self.row_size)] for _ in range(num_hash_functions)]

    
    def putHashed(self, hash_values):
        """
        @param hash_values: list of hash values belonging to a value that should be put into the data structure
        """
        for counter, hash_value in enumerate(hash_values):
            self.table[counter][hash_value%self.row_size] += 1
    
    def putMultHashed(self, hashed_values):
        """
        @param hashed_values: list of lists with the hashed values to put into the data structure
        """
        for index in range(len(hashed_values)):
            self.putHashed(element[index] for element in hashed_values)
    
    def getEstimate(self, hashed_values):
        """
        @param hashed_values: the hashed values of an item for which to look for
        @return: the estimated amount of times the value belonging to the hashed_values occurred in the data stream
        """
        min_val = inf
        for counter, hash_val in enumerate(hashed_values):
            if self.table[counter][hash_val%self.row_size] < min_val:
                min_val = self.table[counter][hash_val%self.row_size]
        return min_val
    