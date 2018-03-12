#include "farmhash.h"

extern "C"
{
    void hashNumbers(int array_length, unsigned char** array, int* char_len, unsigned int* return_array){
        int counter = 0;
        for(counter; counter < array_length; counter++){
            return_array[counter] = hash32(array[counter], char_len[counter]);
        }
    }

    void hashNumbersWSeed(int array_length, unsigned int seed, unsigned char** array, int* char_len,
            unsigned int* return_array){
        int counter = 0;
        for(counter; counter < array_length, counter++){
            return_array[counter] = hash32WithSeed(array[counter], char_len[counter], seed);
        }
    }
}
