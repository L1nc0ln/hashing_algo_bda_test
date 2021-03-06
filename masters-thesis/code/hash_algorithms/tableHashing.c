#include "stdint.h"
#include "tableHashing.h"

uint32_t tableHashingHash(uint32_t x, uint32_t hash_table[4][256]){
    uint32_t index;
    uint32_t h = 0;
    uint8_t c;
    for(index = 0; index < 4; index++){
        c = x;
        h ^= hash_table[index][c];
        x = x >> 8;
    }
    return h;
}

void tableHashingHashNumbersWSeed(int array_length, uint32_t hash_table[4][256], uint32_t* array,
        uint32_t* return_array){
    int counter = 0;
    for(counter; counter < array_length; counter++){
        return_array[counter] = tableHashingHash(array[counter], hash_table);
    }
}

