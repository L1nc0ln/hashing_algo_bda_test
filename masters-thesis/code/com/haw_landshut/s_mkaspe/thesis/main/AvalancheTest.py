'''
@author: Michael Kaspera
'''

class AvalancheTest():
    '''
    classdocs
    '''

    def __init__(self, hash_size):
        """
        @param hash_size: number of bits in the hashed value (typically 32 or 64)
        """
        self.__hash_size__ = hash_size
        self.__flipped_bits_distribution__ = []
        self.__bit_flipped_count__ = []
        self.masks = []
        for index in range(hash_size):
            self.__flipped_bits_distribution__.append(0)
            self.__bit_flipped_count__.append(0)
            self.masks.append(pow(2, index))
    
    def checkFlippedBits(self, original, changed_values):
        """
        @param original: the value (integer) to compare the other values to
        @param changed_values: list of values that should be compared to the original value
        checks how many bits were flipped for each value in the list by masking and xor-ing
        also keeps track of how many bits were flipped each time and how often each bit was flipped
        """
        for changed_value in changed_values:
            self.__extractBitInfo__(original ^ changed_value)
            
    def checkFlippedBitsList(self, hashed_list, num_originals):
        index = 0
        for _ in range(num_originals):
            current_original = hashed_list[index]
            index += 1
            for _ in range(self.__hash_size__):
                self.__extractBitInfo__(current_original ^ hashed_list[index])
                index += 1
    
    def __extractBitInfo__(self, flipped_bits):
        """
        @param: integer for which to discern which bits are set
        stores how many bits were set in the the flipped_bits_distribution
        if a bit was set increases the counter for that bit in the bit_flipped_count
        """
        num_changed_bits = 0
        bit_index  = self.__hash_size__ - 1
        for mask in self.masks:
            if mask & flipped_bits != 0:
                num_changed_bits += 1
                self.__bit_flipped_count__[bit_index] += 1
            bit_index -= 1
        self.__flipped_bits_distribution__[num_changed_bits] += 1
    
    def getFlippedBitDistribution(self):
        """
        @return: a list with the index indicating how many bits were flipped and the value at that index telling how often \
        that many bits were flipped
        i.e. if the 5th element contains the value 10000 then 5 bits were flipped in the modified values 10000 times
        """
        return self.__flipped_bits_distribution__
    
    def getBitFlippedCount(self):
        """
        @return: a list where the value indicates how many times the bit at that index was flipped
        """
        return self.__bit_flipped_count__
    
