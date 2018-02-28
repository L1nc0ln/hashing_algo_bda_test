"""
@author: Michael Kaspera
"""

import random

def createRandomFile(seed, num_elements, min_roll, max_roll):
    """
    @param seed: the seed to be used
    @param num_elements: the number of elements in the file/the number of rolls
    @param min_roll: minimum that can be rolled
    @param max_roll: maximum that can be rolled
    creates a file of random numbers
    NOTE: file will be placed in the distributions folder
    """
    random.seed(seed)
    file_name = '../distributions/random_' + str(seed) + '_' + str(num_elements) + '_' + str(min_roll) + '_' + str(max_roll)
    with open(file_name, 'w') as file:
        for _ in range(num_elements):
            file.write(str(random.randint(min_roll, max_roll)) + '\n')
    
def createdOrderedFile(num_elements, min_num):
    """
    @param num_elements: number of elements in the file
    @param min_num: number to start with
    creates a file of numbers in ascending order
    NOTE: file will be placed in the distributions folder
    """
    file_name = '../distributions/ordered_'  + str(num_elements) + '_' + str(min_num) + '_' + str(min_num + num_elements)
    with open(file_name, 'w') as file:
        for num in range(min_num, min_num + num_elements):
            file.write(str(num) + '\n')

if __name__ == '__main__':
    num_elements = pow(2, 26)
    min_roll = pow(2, 10)
#     max_roll = pow(2, 24)
#     seed = 56135
#     createRandomFile(seed, num_elements, min_roll, max_roll)
    createdOrderedFile(num_elements, min_roll)
    