'''
@author: Michael Kaspera
'''

import com.haw_landshut.s_mkaspe.thesis.main.Statistics as statistics

class DistributionTest():
    '''
    classdocs
    '''


    def __init__(self, num_buckets, num_possible_hashes):
        """
        @param num_buckets: the number of buckets used for the chi-square test
        @param num_possible_hashes: the number of possible different hash values (usually 2^32 or 2^64)
        """
        self.buckets             = []
        self.num_buckets         = num_buckets
        self.num_possible_hashes = num_possible_hashes
        self.hashes_per_bucket   = num_possible_hashes/num_buckets
        self.result_dict         = {}
        self.num_collisions      = 0
        self.previous_element    = 0
        self.current_streak      = 0
        self.streak_details      = {}
        self.skip_flag           = False
        self.streak_test_start   = True
        
        for _ in range(num_buckets):
            self.buckets.append(0)
    
    def streakTest(self, elements):
        """
        @param elements: list of hash values generated
        checks how often a bigger elements follows the current element and builds a set of
        how often which kind of streak happens
        """
        if self.streak_test_start:
            self.streak_test_start = False
            self.previous_element = elements[0]
            for element in elements[1:]:
                if self.skip_flag:
                    self.skip_flag = False
                else:
                    if element > self.previous_element:
                        self.current_streak += 1
                    else:
                        if self.current_streak in self.streak_details:
                            self.streak_details[self.current_streak] += 1
                        else:
                            self.streak_details[self.current_streak] = 1
                        self.current_streak = 0
                        self.skip_flag = True
                self.previous_element = element
        else:
            for element in elements:
                if self.skip_flag:
                    self.skip_flag = False
                else:
                    if element > self.previous_element:
                        self.current_streak += 1
                    else:
                        if self.current_streak in self.streak_details:
                            self.streak_details[self.current_streak] += 1
                        else:
                            self.streak_details[self.current_streak] = 1
                        self.current_streak = 0
                        self.skip_flag = True
                self.previous_element = element
    
    def getStreakResults(self, test_results):
        """
        @param test_results: dict to store the results of the streak test in
        test results are: streaks from 0 - 9, number of streaks of all > 9 combined, maximum streak
        """
        '''insert current streak into results, since this the last one is never inserted by the streak test since
        there could be another chunk coming'''
        if self.current_streak in self.streak_details:
            self.streak_details[self.current_streak] += 1
        else:
            self.streak_details[self.current_streak] = 1
        for index in range(0, 10):
            test_results['streak_' + str(index)] = self.streak_details[index] if index in self.streak_details else 0
            print(self.streak_details[index] if index in self.streak_details else 0)
        num_big_streaks = 0
        for key in self.streak_details.keys():
            if key > 9:
                num_big_streaks += self.streak_details[key]
        test_results['streak_10+'] = num_big_streaks
        test_results['max_streak'] = max(self.streak_details.keys())
    
    def checkForCollisions(self, hashed_array):
        """
        @param hashed_array: list with new hashed values
        """
        #check for collisions in returned array
        for hash_val in hashed_array:
            if hash_val in self.result_dict:
                self.num_collisions += 1
            else:
                self.result_dict[hash_val] = 1
    
    def chiSquareBuckets(self, hashed_array):
        """
        @param hashed_array: list storing the hashed values
        @param hashes_per_bucket: how big is the interval that a bucket spans
        Given a list of hashed values and buckets returns a list with the amount of values that belong to each bucket
        Note: if hashes_per_bucket is multiple of 2 bitshifting is done automatically by the compiler
        """
        for hash_val in hashed_array:
            bucket_number = (int)(hash_val/self.hashes_per_bucket)
            self.buckets[bucket_number] = self.buckets[bucket_number] + 1
            
    def getNumCollisions(self):
        """
        @return: the number of collisions that occurred so far, checked in the data passed to the checkForCollisions method
        """
        return self.num_collisions
            
    def getChiSquareStats(self):
        """
        @return calculate the chi-square value, and the left and right rim percentages and values for the values \
        inserted by the chiSquareBuckets method so far
        """
        return statistics.chiSquareAdv(statistics.createEvenExpectedDistribution(self.num_buckets, self.num_possible_hashes),
                                       self.buckets)
        