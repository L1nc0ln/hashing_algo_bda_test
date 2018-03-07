"""
@author: Michael Kaspera
"""

import configparser

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
        test_case_options = ['input_type', 'return_type', 'distribution_file', 'distribution_details',
                             'test', 'num_buckets', 'rho', 'hash_size', 'row_size', 'test_distribution',
                             'num_tests', 'capacity']
        test_case_list_options = ['hash_algorithm', 'argument_types']
        test_list = []
        test_number = 1
        while True:
            try:
                currentSection = self.config['Test ' + str(test_number)]
            except KeyError:
                break
            test_case = {}
            for test_case_option in test_case_options:
                if test_case_option in currentSection:
                    test_case[test_case_option] = currentSection[test_case_option]
            for test_case_list_option in test_case_list_options:
                test_case[test_case_list_option] = splitArgumentTypes(currentSection[test_case_list_option])
            if 'seeds' in currentSection:
                test_case['seeds'] = splitArgumentTypes(self.config['Test ' + str(test_number)]['seeds'])
                '''make seeds have the same length as hash algorithms, even if the last algorithms have no seed'''
                if len(test_case['hash_algorithm']) > len(test_case['seeds']):
                    for _ in range(len(test_case['hash_algorithm']) - len(test_case['seeds'])):
                        test_case['seeds'].append('')
                if 'table_seed' in currentSection:
                    test_case['table_seed']     = True
            else:
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
