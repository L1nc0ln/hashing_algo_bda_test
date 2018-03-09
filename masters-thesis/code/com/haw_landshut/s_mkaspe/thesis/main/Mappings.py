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