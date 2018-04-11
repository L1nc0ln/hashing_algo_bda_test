#include "stdint.h"
#include "knuth_hash.h"
#include "assert.h"

const uint32_t knuth_rec_var = 2654435769;

uint32_t knuth_hashHashWSeed(uint32_t input, uint32_t seed){
    return input * seed;
}

uint32_t knuth_hashHash(uint32_t input){
    return knuth_hashHashWSeed(input, knuth_rec_var);
}

uint32_t knuth_hashHashInterval(uint32_t input, int factor_of_two) {
    assert(factor_of_two >= 0 && factor_of_two <= 32);

    const uint32_t tmp = input;
    return (tmp * knuth_rec_var) >> (32 - factor_of_two);
}

uint32_t knuth_hashHashNumbers(int array_length, uint32_t* array, uint32_t* return_array) {
    int counter = 0;
    for(counter; counter < array_length; counter++){
        return_array[counter] = knuth_hashHash(array[counter]);
    }
}

uint32_t knuth_hashHashNumbersWSeed(int array_length, uint32_t seed, uint32_t* array,
                                    uint32_t* return_array) {
    int counter = 0;
    for(counter; counter < array_length; counter++){
        return_array[counter] = knuth_hashHashWSeed(array[counter], seed);
    }
}
