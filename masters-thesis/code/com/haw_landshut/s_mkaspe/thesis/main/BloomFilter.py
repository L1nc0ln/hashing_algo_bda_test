"""
@author: Michael Kaspera
"""

from bitarray import bitarray
from math import log

class BloomFilter:
    
    def __init__(self, capacity):
        """
        @param capacity: the number of cells in the underlying bit array
        """
        self.b_filter = bitarray(capacity)
        self.b_filter.setall(0)
        self.capacity = capacity
    
    def putHashedValues(self, values):
        """
        @param values: list of lists with the hashed values for which to set the cells to 1
        inputs the provided values to the Bloom Filter
        """
        for value_list in values:
            for value in value_list:
                self.b_filter[value%self.capacity] = 1
    
    def checkFalsePositive(self, hashed_values):
        """
        @param hashed_values: list of hashed values for which to check if the cells are set
        @return: are all hit cells set to 1?
        """
        for hashed_value in hashed_values:
            if self.b_filter[hashed_value%self.capacity] == 0:
                return False
        return True
    
    def getHashedValues(self, values):
        """
        @param values: list of lists with hash values, inner lists have length len(number of hash functions)
        @return: list of booleans that show if the value is deemed in the Bloom Filter or not
        checks for each list of hashes if the value is deemed in the Bloom Filter and returns the results
        as a list of booleans
        """
        __result_list__ = []
        for value_list in values:
            is_in = self.checkFalsePositive(value_list)
            __result_list__.append(is_in)
        return __result_list__
    
    def __num_set_elems__(self):
        """
        @return: the number of set cells in the Bloom Filter
        """
        sum_set = 0
        for value in self.b_filter:
            if value == 1:
                sum_set += 1
        return sum_set
    
    def fillFactor(self):
        """
        @return: the amount of set cells in the Bloom Filter divided by its capacity
        """
        return self.__num_set_elems__()/self.capacity
    
    def guessNumElements(self):
        """
        @return: estimated amount of contained entries in the Bloom Filter
        """
        guessed_num = -(self.capacity//len(self.b_filter))*log(1-(self.__num_set_elems__()/self.capacity))
        return guessed_num

