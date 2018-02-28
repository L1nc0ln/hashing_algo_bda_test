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
        test_list = []
        test_number = 1
        while True:
            try:
                currentSection = self.config['Test ' + str(test_number)]
            except KeyError:
                break
            test_case = {}
            test_case['hash_algorithm']         = splitArgumentTypes(currentSection["hash_algorithm"])
            test_case['input_type']             = currentSection['input_type']
            test_case['return_type']            = currentSection['return_type']
            test_case['argument_types']         = splitArgumentTypes(currentSection['argument_types'])
            test_case['distribution_file']      = currentSection["distribution_file"]
            test_case['distribution_details']   = currentSection["distribution_details"]
            test_case['test']                   = currentSection["test"]
            if 'seeds' in currentSection:
                test_case['seeds'] = splitArgumentTypes(self.config['Test ' + str(test_number)]['seeds'])
                '''make seeds have the same length as hash algorithms, even if the last algorithms have no seed'''
                if len(test_case['hash_algorithm']) > len(test_case['seeds']):
                    for _ in range(len(test_case['hash_algorithm']) - len(test_case['seeds'])):
                        test_case['seeds'].append('')
            else:
                test_case['seeds']              = None
            if test_case['test'] == 'collisions':
                test_case['num_buckets']        = currentSection['num_buckets']
            if test_case['test'] == 'hyperloglog':
                test_case['rho']                = currentSection['rho']
                test_case['hash_size']          = currentSection['hash_size']
            if test_case['test'] == 'countMin':
                test_case['row_size']           = currentSection['row_size']
            if test_case['test'] == 'bloomFilter':
                test_case['test_distribution']  = currentSection['test_distribution']
                test_case['num_tests']          = currentSection['num_tests']
                test_case['capacity']           = currentSection['capacity']
            test_list.append(test_case)
            test_number += 1
        return test_list
    
    def getOptions(self):
        """
        returns all the items in the Options section of the config as dict
        """
        options_dict = {}
        options_dict['write_output']    = self.config['Options']["write_output"]
        options_dict['output_file']     = self.config['Options']["output_file"]
        options_dict['append']          = self.config['Options']["append"]
        options_dict['num_operations']  = self.config['Options']["num_operations"]
        options_dict['chunk_size']      = self.config['Options']['chunk_size']
        return options_dict
    
def splitArgumentTypes(to_split):
    """
    @param to_split: string to be split along the commata
    short method to make a string with items seperated by commata into a list of those items
    """
    return to_split.replace(' ', '').split(',')
