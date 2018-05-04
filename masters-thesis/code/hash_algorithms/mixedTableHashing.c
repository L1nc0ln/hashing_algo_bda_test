#include "stdint.h"
#include "mixedTableHashing.h"

uint32_t mixedTableHashingHash(uint32_t x, uint64_t hash_table_1[4][256],
                                uint32_t hash_table_2[4][256]){
    uint64_t hash = 0;
    for(int index = 0; index < 4; ++index, x >>= 8)
        hash ^= hash_table_1[index][(uint8_t)x];
    uint32_t derived = hash >> 32;
    for(int index = 0; index < 4; ++index, derived >>= 8)
        hash ^= hash_table_2[index][(uint8_t)derived];
    return (uint32_t)hash;
}

uint32_t mixedTableHashingHashNumbersWSeed(int array_length, uint64_t hash_table_1[4][256],
                                           uint32_t hash_table_2[4][256], uint32_t* array, 
                                           uint32_t* return_array){
    for(int counter = 0; counter < array_length; counter++){
        return_array[counter] = mixedTableHashingHash(array[counter], hash_table_1, hash_table_2);
    }
}
