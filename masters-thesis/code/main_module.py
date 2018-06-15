"""
@author: Michael Kaspera
"""

import ctypes
import time
import com.haw_landshut.s_mkaspe.thesis.main.ConfigReader as ConfigReader
import com.haw_landshut.s_mkaspe.thesis.main.Distribution as Distribution
import com.haw_landshut.s_mkaspe.thesis.main.HyperLogLogTest as HyperloglogTest
import com.haw_landshut.s_mkaspe.thesis.main.CountMinSketchTest as CountMinSketchTest
import com.haw_landshut.s_mkaspe.thesis.main.BloomFilterTest as BloomFilterTest
import com.haw_landshut.s_mkaspe.thesis.main.DistributionTest as DistributionTest
import com.haw_landshut.s_mkaspe.thesis.main.Logs as logs
import numpy as np
from _operator import itemgetter
from com.haw_landshut.s_mkaspe.thesis.main import Mappings
from com.haw_landshut.s_mkaspe.thesis.old.mainmodule import num_operations
from math import sqrt


def getHashFunctionWrapping(unresolved_arguments, library_name, with_seed):
    """
    @param unresolved_arguments: the raw arguments types from the config
    @param library_name: the file name of the .so file that contains the hash function to be called
    @param with_seed: is a seed used? y/n
    @return: function handle to be called to hash a list of elements
    """
    argument_types = resolveArgumentTypes(unresolved_arguments)
    c_library = ctypes.CDLL(library_name)
    hash_function = Mappings.getFunctionName(library_name, c_library, with_seed)
    '''return values couldnt be read outside of the scope of the method calling it, so the return values are sent back
    via an empty array that gets filled with the results. That array is always the last passed parameter'''
    hash_function.restype = None
    hash_function.argtypes = (argument_types)
    return hash_function

def resolveArgumentTypes(unresolved_arguments):
    """
    @param unresolved_arguments: the raw arguments types from the config
    @return: list with the argument types translated to ctypes types
    """
    resolved_arguments = []
    for argument in unresolved_arguments:
        resolved_arguments.append(Mappings.type_mapping_c[argument])
    return resolved_arguments

def hashNextChunk(hash_function, seed, next_chunk_size, argument_types, unhashed_array, num_oversized_returns):
    """
    @param hash_function: the hash function to call for hashing the elements
    @param seed: seed for the hash function, a number or None if no seed
    @param next_chunk_size: how many elements are in the unhashed array
    @param argument_types: the types of the parameters passed to the hash function
    @param unhashed_array: list of elements to be hashed
    @return: touple with the amount of time the hash function took to run and a list with the hashed elements
    Given a list of elements to be hashed, a hash function and the necessary information to call that hash function
    hashes the elements of the list and returns the time it took to hash the list and a list with the hashed elements
    """
    '''argument_array has to be a list, even if the list with unhashed elements is the only thing in the list'''
    argument_array = [unhashed_array]
    '''if chars are passed to the hash function, the passed values are the third last 
       value (passed value, length of each value, return array)'''
    if argument_types[-3] == 'char**':
        length_infos = [0]*next_chunk_size
        length_infos = (Mappings.pointer_type_mapping[argument_types[-2]] * next_chunk_size)(*length_infos)
        for index in range(len(argument_array[0])):
            length_infos[index] = len(argument_array[0][index])
        argument_array.append(length_infos)
    if num_oversized_returns is not None:
        argument_array.insert(0, num_oversized_returns)
        return_array = np.empty([num_oversized_returns, next_chunk_size], dtype=Mappings.pointer_type_mapping[argument_types[-1]])
    else:
        return_array = [0]*next_chunk_size
        return_array = (Mappings.pointer_type_mapping[argument_types[-1]] * next_chunk_size)(*return_array)
    argument_array.append(return_array)
        
    
    #start time measurement and pass the argument_array to the c code
    #note: the array in which the results are saved in has to be the last argument
    if seed is None:
        start_time = time.process_time()
        hash_function(next_chunk_size, *argument_array)
        end_time = time.process_time()
    else:
        if not 'table_seed' in test_case:
            seed = int(seed)
        start_time = time.process_time()
        hash_function(next_chunk_size, seed, *argument_array)
        end_time = time.process_time()
        
    time_taken = 1000 * (end_time - start_time)
    return time_taken, argument_array[-1]

def fillDataStructure(test_details, hash_function_list, put_function, time_taken_total, distribution):
    """
    @param test_details: contains information about specifics of the test, like the hash functions to test
    @param hash_function_list: a list of functions that do the hashing
    @param put_function: function (of the data structure) to call for storing the hashed values in the data structure 
    @param time_taken_total: variable used to store the amount of time it took to run the hashing function
    @return: the time_taken_total, including the running time of the hash function
    goes through the list of provided hash functions and gets the hashed values for each of the hash functions
    and then stores those values by calling the provided put_function
    """
    operations_left = num_operations
    
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        if test_details['argument_types'][-3] == 'char**':
            data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-3]]
        else:
            data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-2]]
        unhashed_array = distribution.generateChunk(next_chunk_size, data_type)
        hashed_values, time_taken = getHashedArrays(hash_function_list, next_chunk_size, test_details, unhashed_array)
        put_function(unhashed_array, hashed_values)
        operations_left = operations_left - chunk_size
        time_taken_total = time_taken_total + time_taken
    return time_taken_total

def getHashedArrays(hash_function_list, next_chunk_size, test_details, unhashed_array):
    """
    @param hash_function_list: a list of functions that do the hashing
    @param next_chunk_size: how many elements should be hashed in one function call
    @param argument_types: the types of the arguments passed to the hashing function in a list
    @param unhashed_array: list/array containing the items to be hashed
    @param seeds: None if no seeds are used, else a list of numbers
    @return: touple with a list of lists storing the hashed values and the time taken to run the hash functions
    goes through the list of provided hash functions and gets the hashed values for each of the hash functions.
    Also checks the amount of time the hash functions are running
    """
    if 'num_oversized_returns' in test_details:
        num_oversized_returns = int(test_details['num_oversized_returns'])
    else:
        num_oversized_returns = None
    hashed_values = []
    if test_details['seeds'] is None:
        for hash_function in hash_function_list:
            time_taken, hashed_array = hashNextChunk(hash_function, None, next_chunk_size, test_details['argument_types'],
                                                     unhashed_array, num_oversized_returns)
            hashed_values.append(hashed_array)
    else:
        for index, hash_function in enumerate(hash_function_list):
            time_taken, hashed_array = hashNextChunk(hash_function, test_details['seeds'][index], next_chunk_size,
                                                     test_details['argument_types'], unhashed_array, num_oversized_returns)
            hashed_values.append(hashed_array)
    if len(hashed_values) == 1 and isinstance(hashed_values[0], np.ndarray):
        hashed_values = hashed_values[0]
    return hashed_values, time_taken

def bloomFilterTest(test_details, test_results):
    """
    @param test_details: contains information about specifics of the test, like the hash functions to test
    @param test_results: dict used to store the results of the test
    @return: the test_results
    tests how well given hash functions (or one hash function with different seeds) does in the bloomFilter algorithm,
    specifics for the test are taken form the test_details. Hashing is done in chunks
    """
    time_taken_total    = 0
    bloom_filter_test   = BloomFilterTest.BloomFilterTest(int(test_details['capacity']))
    hash_function_list  = []
    distribution = Distribution.Distribution(test_results['random_type'], test_results['seed'], test_results['distribution_param_1'],
                                             test_results['distribution_param_2'], False)
    
    for index, hash_function in enumerate(test_details['hash_algorithm']):
        with_seed = False if test_details['seeds'] == None or test_details['seeds'][index] == '' else True
        hash_function_list.append(getHashFunctionWrapping(test_details['argument_types'], hash_function, with_seed))
    
    time_taken_total = fillDataStructure(test_details, hash_function_list, bloom_filter_test.putHashedValues, time_taken_total,
                                         distribution)
    
    test_results = getBloomFilterStats(bloom_filter_test, hash_function_list, test_details, test_results, distribution)
    test_results['time_taken'] = time_taken_total
    
    return test_results
    
def getBloomFilterStats(bloom_filter_test, hash_function_list, test_details, test_results, distribution):
    """
    @param bloom_filter_test: the BloomFilterTest object containing the stored data for which to retrieve the stats
    @param hash_function_list: a list of functions that do the hashing
    @param test_details: dict that contains information about specifics of the test
    @param test_results: dict used to store the results of the test/the stats
    @return: the test_results
    determines how accurate the BloomFilter is using the amount of false positives generated. also stores the capacity of the filter,
    the fill factor and the number of false positive tests in the test_results.
    Retrieves the unhashed values from the provided distribution file and hashes them in chunks again to check for false
    positives
    """
    num_false_positives = 0
    num_true_positives = 0
    num_tests = test_details['num_tests']
    operations_left = int(num_tests)
    
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        if test_details['argument_types'][-3] == 'char**':
            data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-3]]
        else:
            data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-2]]
        unhashed_array = distribution.generateChunk(next_chunk_size, data_type)
        hashed_values, _ = getHashedArrays(hash_function_list, next_chunk_size, test_details, unhashed_array)
        for index, unhashed_val in enumerate(unhashed_array):
            fetch = itemgetter(index)
            status_flag = bloom_filter_test.containsValue(unhashed_val, list(map(fetch, hashed_values)))
            if status_flag == 1:
                num_true_positives += 1
            elif status_flag == 2:
                num_false_positives += 1
        operations_left = operations_left - chunk_size
    fill_factor = bloom_filter_test.fillFactor()
    
    test_results['num_bloom_tests'] = test_details['num_tests']
    test_results['num_stored']      = bloom_filter_test.countElements()
    test_results['false_pos']       = num_false_positives
    test_results['true_pos']        = num_true_positives
    test_results['fill_factor']     = fill_factor
    test_results['bloom_capacity']  = test_details['capacity']
    
    return test_results

def countMinTest(test_details, test_results):
    """
    @param test_details: contains information about specifics of the test, like the hash functions to test
    @param test_results: dict used to store the results of the test
    @return: the test_results
    tests how well given hash functions (or one hash function with different seeds) does in the countMin algorithm,
    specifics for the test are taken form the test_details. Hashing is done in chunks
    """
    time_taken_total = 0
    if 'num_oversized_returns' in test_details:
        num_rows = int(test_details['num_oversized_returns'])
    else:
        num_rows = len(test_details['hash_algorithm'])
    count_min_test   = CountMinSketchTest.CountMinSketchTest(test_details['row_size'], num_rows)
    distribution = Distribution.Distribution(test_results['random_type'], test_results['seed'], test_results['distribution_param_1'],
                                             test_results['distribution_param_2'], False)
    hash_function_list = []
    for index, hash_function in enumerate(test_details['hash_algorithm']):
        with_seed = False if test_details['seeds'] == None or test_details['seeds'][index] == '' else True
        hash_function_list.append(getHashFunctionWrapping(test_details['argument_types'], hash_function, with_seed))
    
    time_taken_total = fillDataStructure(test_details, hash_function_list, count_min_test.putMultHashed, time_taken_total,
                                         distribution)
    
    test_results = getCountMinStats(count_min_test, hash_function_list, test_details, test_results)
    test_results['time_taken'] = time_taken_total
    
    return test_results
   
def getCountMinStats(count_min_test, hash_function_list, test_details, test_results):
    """
    @param count_min_test: the CountMinSketchTest object containing the stored data for which to retrieve the stats
    @param hash_function_list: a list of functions that do the hashing
    @param test_details: dict that contains information about specifics of the test
    @param test_results: dict used to store the results of the test/the stats
    @return: the test_results
    determines how accurate the countMinSketch is using metrics like average and maximum errors. also stores average
    real and average estimated values in the test_results.
    Retrieves the original unhashed values from the countMinSketchTest data structure and hashes them in chunks again 
    since storing all hashed values doesnt seem feasible
    """
    contained_values    = count_min_test.getTop1000Keys()
    total_values        = 1000
    operations_left     = 1000
    average_error       = 0
    average_real_count  = 0
    average_est_count   = 0
    max_error           = 0
    
    next_chunk_size = operations_left
    contained_values_slice = contained_values
    if test_details['argument_types'][-3] == 'char**':
        data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-3]]
    else:
        data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-2]]
    contained_values_slice = (data_type * next_chunk_size)(*contained_values_slice)
    hashed_values, _ = getHashedArrays(hash_function_list, next_chunk_size, test_details, contained_values_slice)
    est_vals = count_min_test.getEstimates(hashed_values)
    real_vals = count_min_test.getRealValues(contained_values_slice)
    
    for index in range(len(contained_values_slice)):
        average_est_count = average_est_count + est_vals[index]
        average_real_count = average_real_count + real_vals[index]
        average_error = average_error + sqrt((real_vals[index] - est_vals[index]) * (real_vals[index] - est_vals[index]))
        if abs(real_vals[index] - est_vals[index]) > max_error:
            max_error = abs(real_vals[index] - est_vals[index])
        
    test_results['row_size']        = test_details['row_size']
    test_results['avg_real_count']  = average_real_count/total_values
    test_results['avg_est_count']   = average_est_count/total_values
    test_results['avg_error']       = average_error/total_values
    test_results['max_error']       = max_error
    
    return test_results

def hyperLogLogTest(test_details, test_results):
    """
    @param test_details: contains information about specifics of the test, like the hash functions to test
    @param test_results: dict used to store the results of the test
    @return: the test_results
    tests how well a given hash function does in the hyperloglog algorithm, specifics for the test are 
    taken form the test_details. Hashing is done in chunks
    """
    time_taken_total = 0
    hyperloglog_test = HyperloglogTest.HyperLogLogTest(int(test_details['rho']), int(test_details['hash_size']))
    distribution = Distribution.Distribution(test_results['random_type'], test_results['seed'], test_results['distribution_param_1'],
                                             test_results['distribution_param_2'], True)
    with_seed = False if test_details['seeds'] == None else True
    hash_function = getHashFunctionWrapping(test_details['argument_types'], test_details['hash_algorithm'][0], with_seed)
    operations_left = num_operations
    
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        if test_details['argument_types'][-3] == 'char**':
            data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-3]]
        else:
            data_type = Mappings.pointer_type_mapping[test_details['argument_types'][-2]]
        unhashed_array = distribution.generateChunk(next_chunk_size, data_type)
        hashed_array, time_taken = getHashedArrays([hash_function], next_chunk_size, test_details,  unhashed_array)
        hyperloglog_test.putHashedValues(distribution.getLastChunk(), hashed_array[0])
        operations_left = operations_left - chunk_size
        time_taken_total = time_taken_total + time_taken
    est_distinct_elems = hyperloglog_test.getEstDistElems()
    distinct_elems = hyperloglog_test.getDistElems()
    
    test_results['rho']             = test_details['rho']
    test_results['est_dist_elems']  = est_distinct_elems
    test_results['dist_elems']      = distinct_elems
    test_results['time_taken']      = time_taken_total
    
    return test_results

def distributionTest(test_details, test_results):
    """
    @param test_details: contains information about specifics of the test, like the hash functions to test
    @param test_results: dict used to store the results of the test
    tests the distribution of hash values for a hash function using the chi_square value, specifics for the test are 
    taken form the test_details. Hashing is done in chunks
    @return: the test_results
    """
    #    set up counters, result arrays and the like
    num_buckets         = int(test_details['num_buckets'])
    assert num_buckets * 5 < num_operations
    time_taken_total    = 0
    num_possible_hashes = Mappings.num_possible_hashes_map[test_details['return_type']]
    operations_left     = num_operations
    argument_types      = test_details['argument_types']
    distribution_test   = DistributionTest.DistributionTest(num_buckets, num_possible_hashes)
    distribution = Distribution.Distribution(test_results['random_type'], test_results['seed'], test_results['distribution_param_1'],
                                             test_results['distribution_param_2'], False)
    with_seed = False if test_details['seeds'] == None else True
    hash_function = getHashFunctionWrapping(test_details['argument_types'], test_details['hash_algorithm'][0], with_seed)
                
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        
        if argument_types[-3] == 'char**':
            data_type = Mappings.pointer_type_mapping[argument_types[-3]]
        else:
            data_type = Mappings.pointer_type_mapping[argument_types[-2]]
        unhashed_array = distribution.generateChunk(next_chunk_size, data_type)
        hashed_array, time_taken = getHashedArrays([hash_function], next_chunk_size, test_details, unhashed_array)
        time_taken_total = time_taken_total + time_taken
        
        distribution_test.checkForCollisions(hashed_array[0])
        distribution_test.streakTest(hashed_array[0])
        distribution_test.chiSquareBuckets(hashed_array[0])
        
        operations_left = operations_left - chunk_size
        
    distribution_test.getStreakResults(test_results)
    chi_square                      = distribution_test.getChiSquareStats()
    test_results['num_collisions']  = distribution_test.getNumCollisions()
    test_results['time_taken']      = time_taken_total
    test_results['chi_square']      = chi_square[0]
    test_results['left_rim']        = chi_square[1][0]
    test_results['left_value']      = chi_square[1][1]
    test_results['right_rim']       = chi_square[1][2]
    test_results['right_value']     = chi_square[1][3]
    
    return test_results

def avalancheTest(test_details):
    """
    @param test_details: contains information about specifics of the test, like the hash functions to test
    Note: test results are not saved in python for the avalanche tests, they are written to the
    avalancheResults.csv file by the called c function
    """
    with_seed = False if test_details['seeds'] == None or test_details['seeds'] == '' else True
    c_library = ctypes.CDLL('hash_algorithms/avalancheTest.so')
    hash_function = c_library.avalancheTestWSeed if with_seed else c_library.avalancheTest
    '''return values couldnt be read outside of the scope of the method calling it, so the return values are sent back
    via an empty array that gets filled with the results. That array is always the last passed parameter'''
    hash_function.restype = None
    hash_function.argtypes = [ctypes.c_char_p, ctypes.c_uint32] if with_seed else [ctypes.c_char_p]
    hash_algo_name = ctypes.c_char_p(test_details['hash_algorithm'][0][test_details['hash_algorithm'][0].rfind('/') + 1:].encode('utf-8'))
    if with_seed:
        hash_function(hash_algo_name, int(num_operations), int(test_details['seeds'][0]))
    else:
        hash_function(hash_algo_name, int(num_operations))
    
    
def processDistributionDetails(distribution_details, test_results):
    """
    @param distribution_details: string seperated by _ including the distribution details
    @param test_results: the dict in which the test results are saved
    extracts details of the distribution and puts them into the test results.
    details are:
    is distribution random
    used seed for random distributions
    minimum value
    maximum value
    number of elements
    """
    distribution_details_list = distribution_details.split('_')
    if distribution_details_list[0] == 'ordered':
        test_results['random_type']             = 'ordered'
        test_results['num_elements']            = distribution_details_list[1]
        test_results['distribution_param_1']    = distribution_details_list[2]
        test_results['distribution_param_2']    = distribution_details_list[3]
        test_results['seed']                    = None
    else:
        if distribution_details_list[0] == 'random':
            test_results['random_type']         = 'random_uniform'
        elif distribution_details_list[0] == 'exp':
            test_results['random_type']         = 'random_exponential'
        elif distribution_details_list[0] == 'gauss':
            test_results['random_type']         = 'random_gauss'
        test_results['seed']                    = distribution_details_list[1]
        test_results['num_elements']            = distribution_details_list[2]
        test_results['distribution_param_1']    = distribution_details_list[3]
        test_results['distribution_param_2']    = distribution_details_list[4]


def runTestCase(test_details):
    """
    @param test_details: list of all test cases, each test case being a dict containing the specifics of the test
    loops through all test cases and calls the methods running the tests.
    Prints the results to the console and logs them as well
    """
    test_results                    = {}
    test_results['test_type']       = test_details['test']
    test_results['hash_algorithms'] = test_details['hash_algorithm']
    test_results['seeds']           = test_details['seeds']
    test_results['num_operations']  = num_operations
    if test_details['test'] == 'avalanche':
        test_results = avalancheTest(test_details)
    else:
        if 'table_seed' in test_details:
            test_details['seeds'] = Distribution.createHashingTable(test_details['seeds'],
                                                                   test_details['argument_types'][1])
        processDistributionDetails(test_details['distribution_details'], test_results)
        if test_details['test']   == 'distribution':
            test_results = distributionTest(test_details, test_results)
            for key in test_results.keys():
                print('key: ' , key, ', value:', test_results[key])
        elif test_details['test'] == 'hyperloglog':
            test_results = hyperLogLogTest(test_details, test_results)
            print('est: ', test_results['est_dist_elems'], 'real: ', test_results['dist_elems'])
        elif test_details['test'] == 'countMin':
            test_results = countMinTest(test_details, test_results)
            print('avg_real: ', test_results['avg_real_count'], ' avg est:', test_results['avg_est_count'], 'avg error:',
                  test_results['avg_error'], 'max error:', test_results['max_error'],'time taken hashing:', test_results['time_taken'])
        elif test_details['test'] == 'bloomFilter':
            test_results = bloomFilterTest(test_details, test_results)
            print('num_bloom_tests: ', test_results['num_bloom_tests'], 'stored in filter:', test_results['num_stored'],
                  'false_pos: ', test_results['false_pos'], 'true_pos: ', test_results['true_pos'],
                  'fill_factor: ', test_results['fill_factor'])
            
        if write_output:
                logs.writeResultCSV('results/results.csv', True, test_results)
        

if __name__ == '__main__':
    config          = ConfigReader.ConfigReader("configFile")
    test_cases      = config.getTestCases()
    options_list    = config.getOptions()
    write_output    = options_list['write_output']
    output_file     = options_list['output_file']
    append_output   = options_list['append']
    num_operations  = int(options_list['num_operations'])
    chunk_size      = int(options_list['chunk_size'])
    
    program_start_time = time.process_time()
    for test_number, test_case in enumerate(test_cases):
        print('test', test_number, ':', end='')
        runTestCase(test_case)
    program_end_time = time.process_time()
    program_time_taken = (program_end_time - program_start_time) * 1000
    print('program time in ms:', program_time_taken)
        