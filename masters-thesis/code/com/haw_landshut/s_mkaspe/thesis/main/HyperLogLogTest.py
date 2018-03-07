"""
@author: Michael Kaspera
"""
import com.haw_landshut.s_mkaspe.thesis.main.HyperLogLogCounter as HyperLogLogCounter

class HyperLogLogTest():
    '''
    classdocs
    '''


    def __init__(self, p, hash_size):
        """
        @param p:
        @param hash_size: the number of bits in the hash
        """
        self.hyperloglog_counter = HyperLogLogCounter.HyperLogLogCounter(p, hash_size)
        self.dict = {}
        
    def putHashedValues(self, unhashed_list, hashed_values):
        """
        @param unhashed_list: the unhashed values to store for comparison later on
        @param hashed_values: a list of lists with the hashed values corresponding to the unhashed values
        """
        for value in unhashed_list:
            if value in self.dict:
                self.dict[value] += 1
            else:
                self.dict[value] = 1
        self.hyperloglog_counter.putHashedValues(hashed_values)
    
    def getEstDistElems(self):
        """
        @return: the estimated amount of distinct elements that were stored in the data structure
        """
        return self.hyperloglog_counter.getEstDistElems()
    
    def getDistElems(self):
        """
        @return: the (real) amount of distinct elements that were put into the data structure
        """
        return len(self.dict)
    
    