"""
@author: Michael Kaspera
"""

import os

__result_list__ = ['test_type', 'hash_algorithms', 'num_operations', 'random_type', 'seed', 'num_elements', 'distribution_param_1',
               'distribution_param_2', 'time_taken', 'collisions', 'chi_square', 'left_rim', 'left_value',
               'right_rim', 'right_value', 'streak_1', 'streak_2', 'streak_3', 'streak_4', 'streak_5', 'streak_6', 'streak_7',
               'streak_8', 'streak_9', 'streak_10+', 'max_streak', 'est_dist_elems', 'dist_elems', 'avg_real_count', 'avg_est_count', 'avg_error',
               'max_error', 'bloom_capacity', 'num_bloom_tests', 'false_pos', 'fill_factor']
__csv_header__ = ['test type', 'hash algorithm 1', 'seed 1', 'hash algorithm 2', 'seed 2', 'hash algorithm 3', 'seed 3', 
                  'hash algorithm 4', 'seed 4', 'hash algorithm 5', 'seed 5', 'hash algorithm 6', 'seed 6', 'hash algorithm 7',
                  'seed 7', 'num operations', 'type of random', 'seed', 'number of elements', 'first distribution parameter',
                  'second distribution parameter',
                  'time taken hashing', 'collisions', 'chi square', 'chi sq left rim', 'left rim val', 'chi sq right rim',
                  'right rim val', 'streak 1', 'streak 2', 'streak 3', 'streak 4', 'streak 5', 'streak 6', 'streak 7', 'streak 8',
                  'streak 9', 'streak 10+', 'max streak', 'estimated distinct elements', 'distinct elements', 'average real count',
                  'average est count', 'average error', 'max error', 'bloom filter capacity', 'number of bloom filter tests',
                  'false positives', 'fill factor']
__delimiter__ = ';'

    
def writeResultCSV(file_name, append, test_results):
    """
    @param file_name: the name of the file to write to. NOTE: file will be placed in the results folder
    @param append: if the file is not empty append or overwrite?
    @param test_results: the dict containing the information to be written to a file
    writes the contents of the test_results to file, each information seperated by a ','
    so it can be imported to excel/google spreadsheets and such
    """
    is_new_file = False
    if append:
        if not os.path.isfile(file_name) or os.path.getsize(file_name) <= 4:
            is_new_file = True
        with open(file_name, 'a') as file:
            if is_new_file:
                file.write(__createFuckingCSVHeader__())
            result_string = __create_result_string__(test_results)
            __write_line__(file, result_string)
    else:
        with open(file_name, 'w') as file:
            result_string = __create_result_string__(test_results)
            __write_line__(file, result_string)

def __write_line__(file, to_write):
    file.write(str(to_write))
    
def __create_result_string__(test_results):
    """
    @param test_results: dict containing the test results to be converted to a string
    """
    result_string = ''
    for key in __result_list__:
        print(key)
        if key in test_results:
            if key != 'hash_algorithms' and key != 'seeds':
                if key == 'count_bit_flip_dist':
                    if len(test_results[key]) == 32:
                        '''append 32 commata to bring it inline with the header'''
                        result_string += __listToCsv__(test_results[key]) + __delimiterTimesX__(31)
                    else:
                        result_string += __listToCsv__(test_results[key])
                elif key == 'bit_flip_dist':
                    if len(test_results[key]) == 32:
                        result_string += __delimiterTimesX__(31) + __listToCsv__(test_results[key])
                    else:
                        result_string += __listToCsv__(test_results[key])
                else:   
                    result_string += str(test_results[key])
            elif key == 'hash_algorithms':
                result_string += __resolveHashAlgorithmColumns__(test_results[key], test_results['seeds']) if 'seeds' in \
                                        test_results else __resolveHashAlgorithmColumns__(test_results[key], None)  
        result_string += __delimiter__
    result_string += '\n'
    return result_string

def __listToCsv__(items):
    result_string = ''
    for item in items:
        result_string += str(item) + __delimiter__
    return result_string
        
def __resolveHashAlgorithmColumns__(hash_algorithms, seeds):
    """
    @param hash_algorithms: a list of file names that contain the hash algorithms
    @param seeds: a list of numbers, blanks or just None
    create a string from the hash algorithms that always fills 7 columns in a csv,
    empty colums at the end if too little hash algorithms
    """
    hash_algorithms_list = hash_algorithms
    if seeds == None:
        seeds = ['', '', '', '', '', '', '']
    return_string = ''
    for index in range(len(hash_algorithms_list)):
        hash_algo = hash_algorithms_list[index][hash_algorithms_list[index].rfind('/'):]
        try:
            return_string += hash_algo + __delimiter__ + seeds[index] + __delimiter__
        except IndexError:
            return_string += hash_algo + __delimiter__ + __delimiter__
    for _ in range(6 - len(hash_algorithms)):
        return_string += __delimiter__ + ' ' + __delimiter__
    '''add final comma to seperate from next field'''
    return_string += __delimiter__
    return return_string

def __delimiterTimesX__(x):
    return_string = ''
    for _ in range(x):
        return_string += __delimiter__
    return return_string

def __createFuckingCSVHeader__():
    """
    @return: the csv header put together into one string
    puts together all the pieces of the csv header since you
    can't have a properly formatted multiline string otherwise
    """
    complete_header = ''
    for part_string in __csv_header__:
        complete_header += part_string
    complete_header += __delimiter__
    complete_header += '\n'
    return complete_header
            
            