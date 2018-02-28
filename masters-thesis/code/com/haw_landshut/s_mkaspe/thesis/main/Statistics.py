"""
@author: Michael Kaspera
"""

from math import sqrt

__chi_square_x_p_values__ = [-2.33, -1.64, -0.674, 0, 0.674, 1.64, 2.33]
__chi_square_percentage_table__ = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]

'''note: dof = buckets - 1'''
def calculate_percentage(chi_square_val, dof):
    """
    @param chi_square_val: the value for chi_square
    @param dof: degrees of freedom for which the interval that the chi_square value lies in should be calulated
    calculates in which interval of probability the given chi_square value is given a degree of freedom
    output is [left probability edge, left probability value, right probability edge, right probability value]
    """
    percentage_values = []
    for x_p in __chi_square_x_p_values__:
        percentage_values.append(dof + sqrt(2*dof)*x_p + (2/3*x_p*x_p) - 2/3)
    if chi_square_val > percentage_values[-1]:
        return [0.99, percentage_values[-1], 1, float('inf')]
    elif chi_square_val < percentage_values[0]:
        return [0, -float('inf'), 0.01, percentage_values[0]]
    else:
        for index in range(len(percentage_values)):
            if percentage_values[index] > chi_square_val:
                return [__chi_square_percentage_table__[index -1], percentage_values[index - 1],
                        __chi_square_percentage_table__[index], percentage_values[index]]
    

def createEvenExpectedDistribution(num_buckets, num_hashes):
    """
    @param num_buckets: number of buckets to fill
    @param num_hashes: number of hashes to be distributed over the buckets
    creates a Distribution where all buckets have the same amount of items in it
    """
    even_expected_distribution = []
    for _ in range(num_buckets):
        even_expected_distribution.append(num_hashes/num_buckets)
    return even_expected_distribution

def createRealDistribution(array):
    """
    @param array: 
    """
    realDistribution = []
    for listing in array:
        realDistribution.append(len(listing))
    return realDistribution

def chiSquare(expected_distribution, real_distribution):
    if len(expected_distribution) != len(real_distribution):
        return 0
    arraySize = len(expected_distribution)
    chi_square_val = 0
    for index in range(arraySize):
        chi_square_val += pow((real_distribution[index] - expected_distribution[index]), 2)/expected_distribution[index]
    return [chi_square_val, calculate_percentage(chi_square_val, len(expected_distribution) - 1)]

def chiSquareAdv(expected_distribution, real_distribution):
    if len(expected_distribution) != len(real_distribution):
        return 0
    array_size = len(expected_distribution)
    chi_square_val = 0
    n = sum(real_distribution, 0)
    total_distribution = sum(expected_distribution, 0)
    for index in range(array_size):
        chi_square_val += pow(real_distribution[index], 2)/(expected_distribution[index]/total_distribution)
    chi_square_val = chi_square_val/n - n
    return [chi_square_val, calculate_percentage(chi_square_val, len(expected_distribution) - 1)]
