'''
@author: Michael Kaspera
'''

import ctypes
import numpy as np

num_possible_hashes_map = {'uint32*' : pow(2,32), 'long*' : pow(2,64)}
type_mapping_c = {'None'     : None,
                  'int'      : ctypes.c_int,
                  'uint32'   : ctypes.c_uint32,
                  'uint32*'  : ctypes.POINTER(ctypes.c_uint32),
                  'char*'    : ctypes.c_char,
                  'char**'   : ctypes.POINTER(ctypes.c_char_p),
                  'long*'    : ctypes.POINTER(ctypes.c_ulong),
                  'uint*'    : ctypes.POINTER(ctypes.c_uint),
                  'int*'     : ctypes.POINTER(ctypes.c_int),
                  'uint32**' : np.ctypeslib.ndpointer(dtype=np.uint32, ndim=2),
                  'uint64**' : np.ctypeslib.ndpointer(dtype=np.uint64, ndim=2)}
pointer_type_mapping = {'uint32*'   : ctypes.c_uint32,
                        'char**'    : ctypes.c_char_p,
                        'int*'      : ctypes.c_int,
                        'long*'     : ctypes.c_ulong,
                        'uint32**'  : np.uint32,
                        'uint64**'  : np.uint64}
pointer_num_bits_mapping = {'uint32**'  : 32,
                            'uint64**'  : 64,
                            'long*'     : 64}

def getFunctionName(library_name, library, with_seed):
    if with_seed:
        if library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/jenkins_full_avalanche.so':
            return library.jenkins_full_avalancheHashNumbersWSeed
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/seven_shift.so':
            return library.seven_shiftHashNumbersWSeed
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/tableHashing.so':
            return library.tableHashingHashNumbersWSeed
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/twistedTableHashing.so':
            return library.twistedTableHashingHashNumbersWSeed
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/thomas_wang_hash.so':
            return library.thomas_wang_hashHashNumbersWSeed
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/xxhash.so':
            return library.xxhashHashNumbersWSeed
    else:
        if library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/jenkins_full_avalanche.so':
            return library.jenkins_full_avalancheHashNumbers
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/seven_shift.so':
            return library.seven_shiftHashNumbers
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/tableHashing.so':
            return library.tableHashingHashNumbersWSeed
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/twistedTableHashing.so':
            return library.twistedTableHashingHashNumbersWSeed
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/thomas_wang_hash.so':
            return library.thomas_wang_hashHashNumbers
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/xxhash.so':
            return library.xxhashHashNumbers
        elif library_name == '/home/linc/workspace/masters-thesis/code/hash_algorithms/djb2.so':
            return library.djb2HashNumbers
    