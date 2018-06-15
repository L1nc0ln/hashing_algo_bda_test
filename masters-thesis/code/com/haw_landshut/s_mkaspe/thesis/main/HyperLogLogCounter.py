"""
@author: Michael Kaspera
"""
import numpy as np

class HyperLogLogCounter():
    '''
    classdocs
    '''
    __correction_constants__ = {16: 0.673, 32: 0.697, 64: 0.709}

    def __init__(self, p, hash_size):
        """
        @param p:
        @param __hash_size__: the number of bits in the hash
        """
        self.__hash_size__ = hash_size
        assert p >= 4 and p <= 16
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
        leftover_val = int(value & self.mask)
        '''to +1 here or not to +1'''
        rho = 1 + self.register_shifts - leftover_val.bit_length()
        self.registers[register_num] = max(self.registers[register_num], rho)
    
    def putHashedValues(self, values):
        """
        @param values: a list of hash values to put into the data structure
        inputs the values into the data structure
        """
        if isinstance(values[0], np.int64):
            print("isintance")
            tmp = []
            for value in values:
                tmp.append(np.asscalar(value))
            values = tmp
        for value in values:
            self.putHashedValue(value)
        
    def getEstDistElems(self):
        """
        @return: estimates the number of distinct elements in the data structure
        """
        harm_mean = 0
        for rho in self.registers:
            harm_mean += pow(2, -rho)
        harm_mean = 1.0 / harm_mean
        correction_const = self.__correction_constants__[self.number_registers] if self.number_registers \
                            in self.__correction_constants__ else __getCorrectionFunc__(self.number_registers)
        estimate = correction_const * self.number_registers * self.number_registers * harm_mean
        '''correcting for too large/small values'''
        if estimate < 2.5 * self.number_registers:
            print("low estimate")
            num_empty_bins = self.registers.count(0)
            estimate = self.number_registers * np.log(self.number_registers/num_empty_bins)
        elif estimate > 1/30 * pow(2, self.__hash_size__):
            print("high estimate")
            estimate = -pow(2, self.__hash_size__) * np.log(1 - estimate/pow(2, self.__hash_size__))
        return estimate

        
def __getCorrectionFunc__(number):
    """
    @param number: value for p for which the correction number should be determined
    """
    return 0.7213 / (1.0 + 1.079 / number)
        
        
