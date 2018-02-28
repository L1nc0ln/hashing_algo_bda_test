"""
@author: Michael Kaspera
"""

import ctypes

class Distribution:
    '''
    classdocs
    '''

    def __init__(self, file_name, keep_record):
        """
        @param file_name: the file to read from. NOTE: the file is assumed to be in the distributions folder
        @param keep_record: store the last read chunk for retrieval
        IMPORTANT: close the reader by calling closeReader after you're done reading from the file
        """
        self.reader = open('../distributions/' + file_name, 'r')
        self.keep_record = keep_record
        if self.keep_record:
            self.last_chunk = []

    
    def readChunk(self, chunk_size, data_type):
        """
        @param chunk_size: the amount of lines to read
        @param data_type: the data type to which the read information should be converted
        @return: a list containing the read lines, converted to the type 'data_type'
        """
        if data_type != ctypes.c_char_p:
            chunk = []
            for _ in range(chunk_size):
                chunk.append(int(self.reader.readline()))
            chunk = (data_type * chunk_size)(*chunk)
            if self.keep_record:
                self.last_chunk = chunk
            return chunk
        else:
            strArrayType = ctypes.c_char_p * chunk_size
            strArray = strArrayType()
            for index in range(chunk_size):
                strArray[index] = (self.reader.readline()).encode('UTF8')
            if self.keep_record:
                self.last_chunk = strArray
            return strArray
    
    def getLastChunk(self):
        """
        @return: the last read chunk of data
        """
        return self.last_chunk
    
    def closeReader(self):
        """
        closes the utilised reader. Call this when you are done reading from the file
        """
        self.reader.close()
        