#include "stdint.h"

uint32_t hash32(uint32_t x, uint64_t hash_table[4][256]){
    uint32_t index;
    uint64_t h = 0;
    uint8_t c;
    for(index = 0; index < 3; index++){
        c = x;
        h ^= hash_table[index][c];
        x = x >> 8;
    }
    c = x ^ h;
    h ^= hash_table[index][c];
    h >> 32;
    return ((uint32_t) h);
}

void hashNumbersWSeed(int array_length, uint64_t hash_table[4][256],
        uint32_t* array, uint32_t* return_array){
    int counter = 0;
    for(counter; counter < array_length; counter++){
        return_array[counter] = hash32(array[counter], hash_table);
    }
}

