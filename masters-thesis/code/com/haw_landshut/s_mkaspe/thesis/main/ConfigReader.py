"""
@author: Michael Kaspera
"""

import configparser
import com.haw_landshut.s_mkaspe.thesis.main.Mappings as Mappings

class ConfigReader:
    """
    Wrapping class for the configparser to read from a custom config file and
    deliver the settings in the config file in a way that is usable for the main_module.
    For the output specifics see the get methods
    """
    
    def __init__(self, file_name):
        """
        @param file_name: the name of the config file to read
        reads in the config file, to get the contents call any of the get methods
        """
        self.config = configparser.ConfigParser(strict=False)
        self.config.read(file_name) 

    def getTestCases(self):
        """
        returns all test cases in the config as a list of dicts
        """
        test_case_options = ['distribution_details', 'test', 'num_buckets', 'rho', 'hash_size', 'row_size', 'num_tests', 'capacity',
                             'num_oversized_returns']
        test_list = []
        test_number = 1
        while True:
            try:
                currentSection = self.config['Test ' + str(test_number)]
            except KeyError:
                break
            test_case = {}
            hash_algo_list = splitArgumentTypes(currentSection['hash_algorithm'])
            test_case['hash_algorithm'] = []
            for hash_algo in hash_algo_list:
                test_case['hash_algorithm'].append(Mappings.hash_function_file_mapping[hash_algo])
            '''all hash algorithms have to have the same input/return/argument types so taking the one from the first algorithm is sufficient'''
            test_case['input_type'] = Mappings.input_type_to_hash_function[hash_algo_list[0]]
            test_case['return_type'] = Mappings.return_type_to_hash_function[hash_algo_list[0]]
            for test_case_option in test_case_options:
                if test_case_option in currentSection:
                    test_case[test_case_option] = currentSection[test_case_option]
            if 'seeds' in currentSection:
                test_case['argument_types'] = Mappings.argument_types_to_hash_function_seed[hash_algo_list[0]]
                test_case['seeds'] = splitArgumentTypes(self.config['Test ' + str(test_number)]['seeds'])
                '''make seeds have the same length as hash algorithms, even if the last algorithms have no seed'''
                if len(test_case['hash_algorithm']) > len(test_case['seeds']):
                    for _ in range(len(test_case['hash_algorithm']) - len(test_case['seeds'])):
                        test_case['seeds'].append('')
                if 'table_seed' in currentSection:
                    test_case['table_seed']     = True
            else:
                test_case['argument_types'] = Mappings.argument_types_to_hash_function[hash_algo_list[0]]
                test_case['seeds']              = None
            test_list.append(test_case)
            test_number += 1
        return test_list
    
    def getOptions(self):
        """
        returns all the items in the Options section of the config as dict
        """
        options_list = ['write_output', 'output_file', 'append', 'num_operations', 'chunk_size']
        options_dict = {}
        for option in options_list:
            options_dict[option] = self.config['Options'][option]
        return options_dict
    
def splitArgumentTypes(to_split):
    """
    @param to_split: string to be split along the commata
    short method to make a string with items seperated by commata into a list of those items
    """
    return to_split.replace(' ', '').split(',')
