"""
@author: Michael Kaspera
"""


class HyperLogLogCounter():
    '''
    classdocs
    '''
    __correction_constants__ = {16: 0.673, 32: 0.697, 64: 0.709}

    def __init__(self, p, hash_size):
        """
        @param p:
        @param hash_size: the number of bits in the hash
        """
        self.hash_size = hash_size
        assert p >= 4 & p <= 16
        self.register_shifts = hash_size - p
        '''mask to cover up the first p bits'''
        self.mask = pow(2, self.register_shifts) - 1
        self.p = p
        self.number_registers = pow(2, self.p)
        self.registers = [0] * self.number_registers
    
    def putHashedValue(self, value):
        """
        @param value: the (hashed) value to insert into the data structure
        """
        register_num = value >> self.register_shifts
        leftover_val = value & self.mask
        rho = self.register_shifts - leftover_val.bit_length()
        if self.registers[register_num] < rho:
            self.registers[register_num] = rho
    
    def putHashedValues(self, values):
        """
        @param values: a list of hash values to put into the data structure
        inputs the values into the data structure
        """
        for value in values:
            self.putHashedValue(value)
        
    def getEstDistElems(self):
        """
        @return: estimates the number of distinct elements in the data structure
        """
        harm_mean = 0
        for rho in self.registers:
            harm_mean += pow(2, -self.registers[rho])
        harm_mean = (1.0 / harm_mean) * self.number_registers
        correction_const = self.__correction_constants__[self.number_registers] if self.number_registers \
                            in self.__correction_constants__ else __getCorrectionFunc__(self.number_registers)
        return correction_const * self.number_registers * harm_mean

        
def __getCorrectionFunc__(number):
    """
    @param number: value for rho for which the correction number should be determined
    """
    return 0.7213 / (1.0 + 1.079 / number)
        
        
