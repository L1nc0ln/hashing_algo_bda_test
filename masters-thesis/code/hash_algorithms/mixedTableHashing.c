#include "stdint.h"
#include "stdlib.h"
#include "mixedTableHashing.h"

uint32_t mixedTableHashingHash(uint32_t x, uint64_t hash_table_1[4][256],
                                uint32_t hash_table_2[4][256]){
    uint64_t hash = 0;
    for(int index = 0; index < 4; index++, x >>= 8)
        hash ^= hash_table_1[index][(uint8_t)x];
    uint32_t derived = hash >> 32;
    for(int index = 0; index < 4; index++, derived >>= 8)
        hash ^= hash_table_2[index][(uint8_t)derived];
    return (uint32_t)hash;
}

/**
 * randoms a real Uint32 number, rand() only rolls up to 2^31-1
 * this function rolls a random number in the range [0, 2^32-1]
 */
uint32_t random32Bit(){
    uint32_t randomNumber = rand();
    uint32_t diceRoll = rand();
    if(diceRoll > 1073741823){
        randomNumber = randomNumber + 2147483648;
    }
    return randomNumber;
}

/**
 * since rand() only rolls a number up to 2^31-1 this method
 * first rolls a true 32 bit random number, shifts those 32 bits
 * 32 times to the left (thereby filling up the "higher" 32 bits)
 * and then adds a second, random 32 bit number to it (thereby
 * filling up the "lower" 32 bits)
 */
uint64_t random64Bit(){
    uint64_t firstPart = random32Bit();
    uint64_t secondPart = random32Bit();
    firstPart = firstPart << 32;
    return firstPart + secondPart;
}

void mixedTableHashingHashNumbersWSeed(int array_length, uint32_t seed, uint32_t* array,
                                                 uint32_t* return_array){
    uint64_t hashing_table [4][256];
    uint32_t hashing_table_2 [4][256];
    srand(seed);
    for(int outerCounter = 0; outerCounter < 4; outerCounter++){
        for(int innerCounter = 0; innerCounter < 256; innerCounter++){
            hashing_table[outerCounter][innerCounter] = random64Bit();
            hashing_table_2[outerCounter][innerCounter] = random32Bit();
        }
    }
    for(int counter = 0; counter < array_length; counter++){
        return_array[counter] = mixedTableHashingHash(array[counter], hashing_table, hashing_table_2);
    }
}
