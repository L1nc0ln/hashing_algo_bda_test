"""
@author: Michael Kaspera
"""

import ctypes
import random

class Distribution:
    '''
    classdocs
    '''

    def __init__(self, is_random, seed, min_roll, max_roll, keep_record):
        """
        @param seed: the seed to use to create random data
        @param keep_record: store the last read chunk for retrieval
        """
        self.is_random = is_random
        '''only for non-random distribution'''
        self.current_index = int(min_roll)
        random.seed(seed)
        self.min_roll = int(min_roll)
        self.max_roll = int(max_roll)
        self.keep_record = keep_record
        if self.keep_record:
            self.last_chunk = []

    
    def generateChunk(self, chunk_size, data_type):
        """
        @param chunk_size: the amount of values to generate
        @param data_type: the data type to which the generated information should be converted
        @return: a list containing the generated values, converted to the type 'data_type'
        """
        if data_type != ctypes.c_char_p:
            chunk = []
            if self.is_random:
                for _ in range(chunk_size):
                    chunk.append(random.randint(self.min_roll, self.max_roll))
            else:
                for index in range(chunk_size):
                    chunk.append(self.current_index + index)
                self.current_index += chunk_size
            chunk = (data_type * chunk_size)(*chunk)
            if self.keep_record:
                self.last_chunk = chunk
            return chunk
        else:
            strArrayType = ctypes.c_char_p * chunk_size
            strArray = strArrayType()
            if self.is_random:
                for index in range(chunk_size):
                    strArray[index] = (str(random.randint(self.min_roll, self.max_roll))).encode('UTF8')
            else:
                for index in range(chunk_size):
                    strArray[index] = (str(self.current_index + index)).encode('UTF8')
                self.current_index += chunk_size
            if self.keep_record:
                self.last_chunk = strArray
            return strArray
    
    def getLastChunk(self):
        """
        @return: the last generated chunk of data
        """
        return self.last_chunk

def createHashingTable(seed, number_of_bits):
    random.seed(seed)
    hashing_table = [[random.randint(0, pow(2, number_of_bits)) for _ in range(256)] for _ in range(4)]
    return hashing_table

        