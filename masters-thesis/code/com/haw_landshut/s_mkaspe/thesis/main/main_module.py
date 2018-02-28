"""
@author: Michael Kaspera
"""

import ctypes
import time
import com.haw_landshut.s_mkaspe.thesis.main.Statistics as statistics
import com.haw_landshut.s_mkaspe.thesis.main.ConfigReader as ConfigReader
import com.haw_landshut.s_mkaspe.thesis.main.Distribution as Distribution
import com.haw_landshut.s_mkaspe.thesis.main.HyperLogLogTest as HyperloglogTest
import com.haw_landshut.s_mkaspe.thesis.main.CountMinSketchTest as CountMinSketchTest
import com.haw_landshut.s_mkaspe.thesis.main.BloomFilterTest as BloomFilterTest
import com.haw_landshut.s_mkaspe.thesis.main.Logs as logs
from _operator import itemgetter

__header_print__ = '{0:30}{1:15}{2:23}{3:15}{4:20}{5:10}{6:20}{7:10}{8:20}'.format('hash_algorithm', 'operations',
                                                  'time taken',
                                                  'collisions', 'chi square', 'left rim', 'left value',
                                                  'right rim', 'right value')
__output_string_format__ = '{0:<30}{1:<15}{2:<20}{3:<3}{4:<15}{5:<20}{6:10}{7:20}{8:10}{9:20}'

__num_possible_hashes_map__ = {'uint32*' : pow(2,32), 'long*' : pow(2,64)}
__type_mapping_c__ = {'None' : None, 'int' : ctypes.c_int, 'uint32' : ctypes.c_uint32, 'uint32*' : ctypes.POINTER(ctypes.c_uint32),
                'char**' : ctypes.POINTER(ctypes.c_char_p), 'long*' : ctypes.POINTER(ctypes.c_ulong),
                'uint*' : ctypes.POINTER(ctypes.c_uint), 'int*' : ctypes.POINTER(ctypes.c_int)}
__pointer_type_mapping__ = {'uint32*' : ctypes.c_uint32, 'char**': ctypes.c_char_p,
                        'int*' : ctypes.c_int, 'long*' : ctypes.c_ulong}

def getHashFunctionWrapping(unresolved_arguments, hash_algorithm, with_seed):
    """
    @param unresolved_arguments: the raw arguments types from the config
    @param hash_algorithm: the file name of the .so file that contains the hash function to be called
    @param with_seed: is a seed used? y/n
    @return: function handle to be called to hash a list of elements
    """
    argument_types = resolveArgumentTypes(unresolved_arguments)
    c_code = ctypes.CDLL(hash_algorithm)
    hash_function = c_code.hashNumbersWSeed if with_seed else c_code.hashNumbers
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
        resolved_arguments.append(__type_mapping_c__[argument])
    return resolved_arguments

def checkForCollisions(result_dict, hashed_array):
    """
    @param result_dict: dict containing all hashed values so far
    @param hashed_array: list with new hashed values
    @return: the number of detected collisions
    """
    num_collisions = 0
    #check for collisions in returned array
    for hash_val in hashed_array:
        if hash_val in result_dict:
            num_collisions += 1
        else:
            result_dict[hash_val] = 1
    return num_collisions

def chiSquareBuckets(buckets, hashed_array, hashes_per_bucket):
    """
    @param buckets: number of buckets in total
    @param hashed_array: list storing the hashed values
    @param hashes_per_bucket: how big is the interval that a bucket spans
    Given a list of hashed values and buckets returns a list with the amount of values that belong to each bucket
    Note: if hashes_per_bucket is multiple of 2 bitshifting is done automatically by the compiler
    """
    for hash_val in hashed_array:
        bucket_number = (int)(hash_val/hashes_per_bucket)
        buckets[bucket_number] = buckets[bucket_number] + 1

def hashNextChunk(hash_function, seed, next_chunk_size, argument_types, unhashed_array):
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
    
    data_type_index = 1 if seed == None else 2
    if argument_types[data_type_index] == 'char**':
        length_infos = [0]*next_chunk_size
        length_infos = (__pointer_type_mapping__[argument_types[-2]] * next_chunk_size)(*length_infos)
        for index, string in enumerate(argument_array[0]):
            length_infos[index] = len(string)
        argument_array.append(length_infos)
    return_array = [0]*next_chunk_size
    return_array = (__pointer_type_mapping__[argument_types[-1]] * next_chunk_size)(*return_array)
    argument_array.append(return_array)
        
    
    #start time measurement and pass the argument_array to the c code
    #note: the array in which the results are saved in has to be the last argument
    if seed == None:
        start_time = time.process_time()
        hash_function(next_chunk_size, *argument_array)
        end_time = time.process_time()
    else:
        start_time = time.process_time()
        hash_function(next_chunk_size, int(seed), *argument_array)
        end_time = time.process_time()
        
    time_taken = 1000 * (end_time - start_time)
    return time_taken, argument_array[-1]

def fillDataStructure(test_details, hash_function_list, put_function, time_taken_total):
    """
    @param test_details: contains information about specifics of the test, like the hash functions to test
    @param hash_function_list: a list of functions that do the hashing
    @param put_function: function (of the data structure) to call for storing the hashed values in the data structure 
    @param time_taken_total: variable used to store the amount of time it took to run the hashing function
    @return: the time_taken_total, including the running time of the hash function
    goes through the list of provided hash functions and gets the hashed values for each of the hash functions
    and then stores those values by calling the provided put_function
    """
    distribution = Distribution.Distribution(test_details['distribution_file'], False)
    operations_left = num_operations
    
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        data_type_index = 1 if test_details['seeds'] == None else 2
        unhashed_array = distribution.readChunk(next_chunk_size, __pointer_type_mapping__[test_details['argument_types'][data_type_index]])
        hashed_values, time_taken = getHashedArrays(hash_function_list, next_chunk_size, test_details['argument_types'],
                                                    unhashed_array, test_details['seeds'])
        put_function(unhashed_array, hashed_values)
        operations_left = operations_left - chunk_size
        time_taken_total = time_taken_total + time_taken
    distribution.closeReader()
    return time_taken_total

def getHashedArrays(hash_function_list, next_chunk_size, argument_types, unhashed_array, seeds):
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
    hashed_values = []
    if seeds == None:
        for hash_function in hash_function_list:
            time_taken, hashed_array = hashNextChunk(hash_function, None, next_chunk_size, argument_types,
                                                     unhashed_array)
            hashed_values.append(hashed_array)
    else:
        for index, hash_function in enumerate(hash_function_list):
            time_taken, hashed_array = hashNextChunk(hash_function, seeds[index], next_chunk_size,
                                                     argument_types, unhashed_array)
            hashed_values.append(hashed_array)
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
    
    for index, hash_function in enumerate(test_details['hash_algorithm']):
        with_seed = False if test_details['seeds'] == None or test_details['seeds'][index] == '' else True
        hash_function_list.append(getHashFunctionWrapping(test_details['argument_types'], hash_function, with_seed))
    
    time_taken_total = fillDataStructure(test_details, hash_function_list, bloom_filter_test.putHashedValues, time_taken_total)
    
    test_results = getBloomFilterStats(bloom_filter_test, hash_function_list, test_details, test_results)
    test_results['time_taken'] = time_taken_total
    
    return test_results
    
def getBloomFilterStats(bloom_filter_test, hash_function_list, test_details, test_results):
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
    distribution = Distribution.Distribution(test_details['test_distribution'], False)
    num_tests = test_details['num_tests']
    operations_left = int(num_tests)
    
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        data_type_index = 1 if test_details['seeds'] == None else 2
        unhashed_array = distribution.readChunk(next_chunk_size, __pointer_type_mapping__[test_details['argument_types'][data_type_index]])
        hashed_values, _ = getHashedArrays(hash_function_list, next_chunk_size, test_details['argument_types'],
                                                    unhashed_array, test_details['seeds'])
        for index, unhashed_val in enumerate(unhashed_array):
            fetch = itemgetter(index)
            is_false_positive = bloom_filter_test.checkFalsePositive(unhashed_val, list(map(fetch, hashed_values)))
            if is_false_positive:
                num_false_positives += 1
        operations_left = operations_left - chunk_size
    distribution.closeReader()
    fill_factor = bloom_filter_test.fillFactor()
    
    test_results['num_bloom_tests'] = test_details['num_tests']
    test_results['false_pos']       = num_false_positives
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
    count_min_test   = CountMinSketchTest.CountMinSketchTest(test_details['row_size'], len(test_details['hash_algorithm']))
    
    hash_function_list = []
    for index, hash_function in enumerate(test_details['hash_algorithm']):
        with_seed = False if test_details['seeds'] == None or test_details['seeds'][index] == '' else True
        hash_function_list.append(getHashFunctionWrapping(test_details['argument_types'], hash_function, with_seed))
    
    time_taken_total = fillDataStructure(test_details, hash_function_list, count_min_test.putMultHashed, time_taken_total)
    
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
    contained_values    = count_min_test.getContainedKeys()
    total_values        = len(contained_values)
    operations_left     = total_values
    current_index       = 0
    average_error       = 0
    average_real_count  = 0
    average_est_count   = 0
    max_error           = 0
    
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        end_index = current_index + next_chunk_size
        contained_values_slice = contained_values[current_index:end_index]
        contained_values_slice = (__pointer_type_mapping__[test_details['argument_types'][1]] * next_chunk_size)(*contained_values_slice)
        hashed_values, _ = getHashedArrays(hash_function_list, next_chunk_size, test_details['argument_types'],
                                                    contained_values_slice, test_details['seeds'])
        for index, unhashed_val in enumerate(contained_values_slice):
            fetch = itemgetter(index)
            est_val = count_min_test.getEstimate(list(map(fetch, hashed_values)))
            real_val = count_min_test.getRealValue(unhashed_val)
            average_est_count = average_est_count + est_val
            average_real_count = average_real_count + real_val
            average_error = average_error + (real_val - est_val) * (real_val - est_val)
            if abs(real_val - est_val) > max_error:
                max_error = abs(real_val - est_val)
        operations_left = operations_left - chunk_size
        
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
    distribution = Distribution.Distribution(test_details['distribution_file'], True)
    with_seed = False if test_details['seeds'] == None else True
    hash_function = getHashFunctionWrapping(test_details['argument_types'], test_details['hash_algorithm'][0], with_seed)
    operations_left = num_operations
    
    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        data_type_index = 1 if test_details['seeds'] == None else 2
        unhashed_array = distribution.readChunk(next_chunk_size, __pointer_type_mapping__[test_details['argument_types'][data_type_index]])
        hashed_array, time_taken = getHashedArrays([hash_function], next_chunk_size, test_details['argument_types'],
                                                    unhashed_array, test_details['seeds'])
        hyperloglog_test.putHashedValues(distribution.getLastChunk(), hashed_array[0])
        operations_left = operations_left - chunk_size
        time_taken_total = time_taken_total + time_taken
    distribution.closeReader()
    est_distinct_elems = hyperloglog_test.getEstDistElems()
    distinct_elems = hyperloglog_test.getDistElems()
    
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
    num_buckets = int(test_details['num_buckets'])
    assert num_buckets * 5 < num_operations
    distribution = Distribution.Distribution(test_details['distribution_file'], False)
    with_seed = False if test_details['seeds'] == None else True
    hash_function = getHashFunctionWrapping(test_details['argument_types'], test_details['hash_algorithm'][0], with_seed)
                
#    set up counters, result arrays and the like
    buckets             = []
    result_dict         = {}
    num_collisions      = 0
    time_taken_total    = 0
    num_possible_hashes = __num_possible_hashes_map__[test_details['return_type']]
    hashes_per_bucket   = num_possible_hashes/num_buckets
    operations_left     = num_operations
    argument_types      = test_details['argument_types']

    #    initialize bucket list
    for _ in range(num_buckets):
        buckets.append(0)

    while operations_left > 0:
        next_chunk_size = chunk_size if operations_left > chunk_size else operations_left
        
        data_type_index = 1 if test_details['seeds'] == None else 2
        unhashed_array = distribution.readChunk(next_chunk_size, __pointer_type_mapping__[argument_types[data_type_index]])
        hashed_array, time_taken = getHashedArrays([hash_function], next_chunk_size, test_details['argument_types'],
                                                    unhashed_array, test_details['seeds'])
        time_taken_total = time_taken_total + time_taken
        
        num_collisions += checkForCollisions(result_dict, hashed_array[0])
        chiSquareBuckets(buckets, hashed_array[0], hashes_per_bucket)
        
        operations_left = operations_left - chunk_size
        
    distribution.closeReader()
    chi_square = statistics.chiSquareAdv(statistics.createEvenExpectedDistribution(num_buckets, num_possible_hashes),
                                         buckets)
    test_results['num_collisions']  = num_collisions
    test_results['time_taken']      = time_taken_total
    test_results['chi_square']      = chi_square[0]
    test_results['left_rim']        = chi_square[1][0]
    test_results['left_value']      = chi_square[1][1]
    test_results['right_rim']       = chi_square[1][2]
    test_results['right_value']     = chi_square[1][3]
    
    return test_results

def printResult(test_details, test_results):
    """
    @param test_details:
    @param test_results:
    print the results of the distribution test to the console
    """
    print(__output_string_format__.format(test_details['hash_algorithm'][0][test_details['hash_algorithm'][0].rfind('/'):],
                                      test_results['num_operations'], test_results['time_taken'], 'ms', test_results['num_collisions'],
                                      test_results['chi_square'], test_results['left_rim'], test_results['left_value'],
                                      test_results['right_rim'], test_results['right_value']))
    
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
        test_results['is_random']       = 'false'
        test_results['num_elements']    = distribution_details_list[1]
        test_results['min_roll']        = distribution_details_list[2]
        test_results['max_roll']        = distribution_details_list[3]
    else:
        test_results['is_random']       = 'true'
        test_results['seed']            = distribution_details_list[1]
        test_results['num_elements']    = distribution_details_list[2]
        test_results['min_roll']        = distribution_details_list[3]
        test_results['max_roll']        = distribution_details_list[4]

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
    processDistributionDetails(test_details['distribution_details'], test_results)
    if test_details['test']   == 'collisions':
        test_results = distributionTest(test_details, test_results)
        printResult(test_details, test_results)
    elif test_details['test'] == 'hyperloglog':
        test_results = hyperLogLogTest(test_details, test_results)
        print('est: ', test_results['est_dist_elems'], 'real: ', test_results['dist_elems'])
    elif test_details['test'] == 'countMin':
        test_results = countMinTest(test_details, test_results)
        print('avg_real: ', test_results['avg_real_count'], ' avg est:', test_results['avg_est_count'], 'avg error:',
              test_results['avg_error'], 'max error:', test_results['max_error'],'time taken hashing:', test_results['time_taken'])
    elif test_details['test'] == 'bloomFilter':
        test_results = bloomFilterTest(test_details, test_results)
        print('num_bloom_tests: ', test_results['num_bloom_tests'], 'false_pos: ', test_results['false_pos'], 'fill_factor: ',
              test_results['fill_factor'])
        
    if write_output:
            logs.writeResultCSV('results.csv', True, test_results)
        

if __name__ == '__main__':
    config          = ConfigReader.ConfigReader("configFile")
    test_cases      = config.getTestCases()
    options_list    = config.getOptions()
    write_output    = options_list['write_output']
    output_file     = options_list['output_file']
    append_output   = options_list['append']
    num_operations  = int(options_list['num_operations'])
    chunk_size      = int(options_list['chunk_size'])
    
    print(__header_print__)
    for test_case in test_cases:
        runTestCase(test_case)
        