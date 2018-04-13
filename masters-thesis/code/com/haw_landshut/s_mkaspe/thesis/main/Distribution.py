"""
@author: Michael Kaspera
"""

import ctypes
import random
import numpy as np
from com.haw_landshut.s_mkaspe.thesis.main import Mappings

class Distribution:
    '''
    classdocs
    '''

    def __init__(self, random_type, seed, min_roll, max_roll, keep_record):
        """
        @param seed: the seed to use to create random data
        @param keep_record: store the last read chunk for retrieval
        """
        self.random_type = random_type
        '''only for non-random distribution'''
        self.current_index = int(min_roll)
        random.seed(seed)
        self.min_roll = int(min_roll)
        self.max_roll = int(max_roll)
        self.keep_record = keep_record
        self.last_chunk = []

    
    def generateChunk(self, chunk_size, data_type):
        """
        @param chunk_size: the amount of values to generate
        @param data_type: the data type to which the generated information should be converted
        @return: a list containing the generated values, converted to the type 'data_type'
        """
        if data_type != ctypes.c_char_p:
            chunk = (data_type * chunk_size)(*self.generateIntegers(chunk_size))
            return chunk
        else:
            strArrayType = ctypes.c_char_p * chunk_size
            strArray = strArrayType()
            if self.random_type == "random_uniform":
                for index in range(chunk_size):
                    strArray[index] = (str(random.randint(self.min_roll, self.max_roll))).encode('UTF8')
            elif self.random_type == "random_exponential":
                mid_val = (self.min_roll + self.max_roll) / 2
                strArray[index] = (str(random.expovariate(1/mid_val))).encode('UTF8')
            else:
                for index in range(chunk_size):
                    strArray[index] = (str(self.current_index + index)).encode('UTF8')
                self.current_index += chunk_size
            if self.keep_record:
                self.last_chunk = strArray
            return strArray
    
    def generateIntegers(self, chunk_size):
        chunk = []
        if self.random_type == "random_uniform":
            for _ in range(chunk_size):
                chunk.append(random.randint(self.min_roll, self.max_roll))
        elif self.random_type == "random_exponential":
            mid_val = (self.min_roll + self.max_roll) / 2
            for _ in range(chunk_size):
                chunk.append(random.expovariate(1/mid_val))
        else:
            for index in range(chunk_size):
                chunk.append(self.current_index + index)
            self.current_index += chunk_size
        if self.keep_record:
            self.last_chunk = chunk
        return chunk
        
    def getLastChunk(self):
        """
        @return: the last generated chunk of data
        """
        return self.last_chunk
    
def createHashingTable(seeds, data_type):
    hashing_tables_list = []
    for seed in seeds:
        random.seed(seed)
        number_of_bits = Mappings.pointer_num_bits_mapping[data_type]
        hashing_table = np.empty([4, 256], dtype=Mappings.pointer_type_mapping[data_type])
        for outer_index in range(4):
            for inner_index in range(256):
                hashing_table[outer_index][inner_index] = random.randint(0, pow(2, number_of_bits))
        hashing_tables_list.append(hashing_table)
    return hashing_tables_list

        