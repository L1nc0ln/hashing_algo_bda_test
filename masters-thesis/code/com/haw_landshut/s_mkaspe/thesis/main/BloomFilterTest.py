"""
@author: Michael Kaspera
"""
import com.haw_landshut.s_mkaspe.thesis.main.BloomFilter as BloomFilter

class BloomFilterTest():
    '''
    classdocs
    '''
    
    def __init__(self, capacity):
        """
        @param capacity: the number of cells in the underlying bit array
        """
        self.bloom_filter = BloomFilter.BloomFilter(capacity)
        self.entries = {}
        
    def putHashedValues(self, unhashed_list, hashed_values):
        """
        @param unhashed_list: list with the unhashed values to be put into the bloom filter
        @param hashed_values: list of lists with the hashed values for which to set the cells to 1
        inputs the provided values to the Bloom Filter and stores the unhashed values so they
        can be used to determine false positives later on
        """
        assert len(unhashed_list) == len(hashed_values[0])
        for unhashed_entry in unhashed_list:
            self.entries[unhashed_entry] = 1
        self.bloom_filter.putHashedValues(hashed_values)
    
    def checkFalsePositive(self, unhashed_value, hashed_values):
        """
        @param unhashed_value: the unhashed value belonging to the list of hashes
        @param hashed_values: list of hashed values for which to check if the cells are set
        @return: did the unhashed value occur in the data stream AND does the bloom filter say it was set
        """
        if not unhashed_value in self.entries:
            return 0
        elif (unhashed_value in self.entries) and (self.bloom_filter.checkFalsePositive(hashed_values)):
            return 1
        else:
            return 2
        
    def fillFactor(self):
        """
        @return: the amount of set cells in the Bloom Filter divided by its capacity
        """
        return self.bloom_filter.fillFactor()
    
    def guessNumElements(self):
        """
        @return: estimated amount of contained entries in the Bloom Filter
        """
        return self.bloom_filter.guessNumElements()
    
