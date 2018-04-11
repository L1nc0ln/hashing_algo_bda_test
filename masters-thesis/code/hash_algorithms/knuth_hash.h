#ifndef KNUTH_HASH_HEADER
#define KNUTH_HASH_HEADER

uint32_t knuth_hashHash(uint32_t input);

uint32_t knuth_hashHashWSeed(uint32_t input, uint32_t seed);

uint32_t knuth_hashHashInterval(uint32_t input, int factor_of_two);

uint32_t knuth_hashHashNumbers(int array_length, uint32_t* array, uint32_t* return_array);

uint32_t knuth_hashHashNumbersWSeed(int array_length, uint32_t seed, uint32_t* array,
        uint32_t* return_array);

#endif
