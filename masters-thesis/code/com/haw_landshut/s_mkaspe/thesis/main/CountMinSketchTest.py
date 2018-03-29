"""
@author: Michael Kaspera
"""
import com.haw_landshut.s_mkaspe.thesis.main.CountMinSketch as CountMinSketch
import heapq

class CountMinSketchTest():
    """
    classdocs
    """

    def __init__(self, row_size, num_hash_functions):
        """
        @param row_size: how many rows the CountMin Sketch data structure should have
        @param num_hash_functions: the number of different hash functions the CountMin Sketch data structure uses
        """
        self.row_size = row_size
        self.count_min_sketch = CountMinSketch.CountMinSketch(row_size, num_hash_functions)
        self.dict = {}
    
    def putMultHashed(self, unhashed_list, hashed_values):
        """
        @param unhashed_list: list of original values
        @param hashed_values: list of lists with the hashed values belonging to the unhashed_list
        """
        for value in unhashed_list:
            if value in self.dict:
                self.dict[value] += 1
            else:
                self.dict[value] = 1
        self.count_min_sketch.putMultHashed(hashed_values)
    
    
    def getEstimate(self, hashed_values):
        """
        @param hashed_values: the hashed values of an item for which to look for
        @return: the estimated amount of times the value belonging to the hashed_values occurred in the data stream
        """
        return self.count_min_sketch.getEstimate(hashed_values)
    
    def getEstimates(self, hashed_values):
        """
        @param hashed_values: a list of lists with the hashed values of the items for which to look for
        @return: list with the estimated amount of times the values belonging to the hashed_values occurred in the data stream
        """
        return self.count_min_sketch.getEstimates(hashed_values)
    
    def getRealValue(self, unhashed_value):
        """
        @param unhashed_value: value for which to look up the number of times it occurred
        @return: the amount of times the provided value occurred in the data stream so far
        """
        return self.dict[unhashed_value]
    
    def getRealValues(self, unhashed_values):
        """
        @param unhashed_values: values for which to look up the number of times they occurred
        @return: list with the amount of times the provided values occurred in the data stream so far
        """
        occurances = []
        for item in unhashed_values:
            occurances.append(self.dict[item])
        return occurances
    
    def getContainedKeys(self):
        """
        @return: a list containing all unhashed values that occurred in the data stream so far
        """
        return list(self.dict)
    
    def getTop1000Keys(self):
        """
        @return: list of the 1000 most called elements
        """
        return heapq.nlargest(1000, self.dict, key=self.dict.get)
    