#include "stdint.h"
#include "stdlib.h"
#include "stdio.h"
#include "time.h"
#include "string.h"
#include "jenkins_full_avalanche.h"
//#include "djb2.h"
#include "seven_shift.h"
#include "tableHashing.h"
#include "thomas_wang_hash.h"
#include "twistedTableHashing.h"
#include "mixedTableHashing.h"
#include "xxhash.h"
#include "knuth_hash.h"
#include "sha256.h"

static const char JENKINS_STRING[] = "jenkins_full_avalanche.so";
//static const char DJB2_STRING[] = "djb2.so";
static const char SEVEN_SHIFT_STRING[] = "seven_shift.so";
static const char KNUTH_HASH_STRING[] = "knuth_hash.so";
static const char TABLE_HASHING_STRING[] = "tableHashing.so";
static const char TWISTED_TABLE_HASHING_STRING[] = "twistedTableHashing.so";
static const char MIXED_TABLE_HASHING_STRING[] = "mixedTableHashing.so";
static const char THOMAS_WANG_STRING[] = "thomas_wang_hash.so";
static const char XXHASH_STRING[] = "xxhash.so";
static const char SHA256_HASH_STRING[] = "sha256.so";
static const int NUMBER_STRING_SIZE = 12;
static const char delimiter = ';';
const uint32_t masks[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768,
                          65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216,
                          33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648};
const int byteMask[] = {1, 2, 4, 8, 16, 32, 64, 128};
const int BITS_IN_BYTE = 8;
const int MASK_LEN = 32;
long amountOfFlippedBits[33] = {0};
long timesBitFlipped[32] = {0};
int numberOfLoops = 1 << 30;

void printBinary(uint32_t input){
    while (input) {
        if (input & 1)
            printf("1");
        else
            printf("0");
        input >>= 1;
    }
    printf("\n");
}

void printLongArray(long array[], int length){
    int counter = 0;
    printf("[");
    for(counter; counter < length - 1; counter++){
        printf("%ld%c", array[counter], delimiter);
    }
    printf("%ld]\n", array[length - 1]);
}

void printUIntArray(uint32_t array[], int length){
    int counter = 0;
    printf("[");
    for(counter; counter < length - 1; counter++){
        printf("%d%c", array[counter], delimiter);
    }
    printf("%d]\n", array[length - 1]);
}

void writeUIntArray(char* prefix, long array[], int length,
                    FILE *file_ptr){
    int counter = 0;
    fprintf(file_ptr, "%s%c", prefix, delimiter);
    for(counter; counter < length; counter++){
        fprintf(file_ptr, "%ld%c", array[counter], delimiter);
    }
}

void writeResults(char* hash_algorithm, uint32_t seed){
    FILE *file_ptr;
    file_ptr = fopen("avalancheResults.csv", "a");
    char numOperationsString[12];
    sprintf(numOperationsString, "%d", numberOfLoops);
    writeUIntArray(hash_algorithm, amountOfFlippedBits, 33, file_ptr);
    writeUIntArray(numOperationsString, timesBitFlipped, 32, file_ptr);
    fprintf(file_ptr, "%d\n", seed);
}

void printResults(char* hashing_algorithm){
    printf("amount of flipped bits:\n");
    printLongArray(amountOfFlippedBits, 33);
    printf("bit flipped how often:\n");
    printLongArray(timesBitFlipped, 32);
}

void checkFlippedBits(uint32_t flippedBits){
    int numFlippedBits = 0;
    int counter = 0;
    for(counter; counter <= 31; counter++){
        if((masks[counter] & flippedBits) != 0){
            timesBitFlipped[31 - counter] += 1;
            numFlippedBits += 1;
        }
    }
    amountOfFlippedBits[numFlippedBits] += 1;
}

void avalancheTestUint(uint32_t (*f_ptr)(uint32_t)){
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    for(counter = 0; counter < numberOfLoops; counter++){
        uint32_t original_val = (*f_ptr)(counter);
        for(mask_counter = 0; mask_counter < MASK_LEN; mask_counter++){
            uint32_t changed_val = (*f_ptr)(counter ^ masks[mask_counter]);
            checkFlippedBits(original_val ^ changed_val);
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);
}

void avalancheTestUintWSeed(uint32_t (*f_ptr)(uint32_t, uint32_t), uint32_t seed){
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    for(counter = 0; counter < numberOfLoops; counter++){
        uint32_t original_val = (*f_ptr)(counter, seed);
        for(mask_counter = 0; mask_counter < MASK_LEN; mask_counter++){
            uint32_t changed_val = (*f_ptr)(counter ^ masks[mask_counter], seed);
            checkFlippedBits(original_val ^ changed_val);
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);
}

/**
 * randoms a real Uint32 number, rand() only rolls up to 2^31-1
 * this function rolls a random number in the range [0, 2^32-1]
 */
uint32_t uIntRandom(){
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
uint64_t uInt64Random(){
    uint64_t firstPart = uIntRandom();
    uint64_t secondPart = uIntRandom();
    firstPart = firstPart << 32;
    return firstPart + secondPart;
}

void avalancheTestTableHashing(uint32_t (*f_ptr)(uint32_t x, uint32_t hash_table[4][256]), uint32_t seed){
    uint32_t hashing_table [4][256];
    srand(seed);
    for(int outerCounter = 0; outerCounter < 4; outerCounter++){
        for(int innerCounter = 0; innerCounter < 256; innerCounter++){
            hashing_table[outerCounter][innerCounter] = uIntRandom();
        }
    }
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    for(counter = 0; counter < numberOfLoops; counter++){
        uint32_t original_val = (*f_ptr)(counter, hashing_table);
        for(mask_counter = 0; mask_counter < MASK_LEN; mask_counter++){
            uint32_t changed_val = (*f_ptr)(counter ^ masks[mask_counter], hashing_table);
            checkFlippedBits(original_val ^ changed_val);
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);
}

void avalancheTestTwistedTableHashing(uint32_t (*f_ptr)(uint32_t x, uint64_t hash_table[4][256]),
                                      uint32_t seed){
    uint64_t hashing_table [4][256];
    srand(seed);
    for(int outerCounter = 0; outerCounter < 4; outerCounter++){
        for(int innerCounter = 0; innerCounter < 256; innerCounter++){
            hashing_table[outerCounter][innerCounter] = uInt64Random();
        }
    }
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    for(counter = 0; counter < numberOfLoops; counter++){
        uint32_t original_val = (*f_ptr)(counter, hashing_table);
        for(mask_counter = 0; mask_counter < MASK_LEN; mask_counter++){
            uint32_t changed_val = (*f_ptr)(counter ^ masks[mask_counter], hashing_table);
            checkFlippedBits(original_val ^ changed_val);
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);
}

void avalancheTestMixedTableHashing(uint32_t (*f_ptr)(uint32_t x, uint64_t hash_table_1[4][256],
                                    uint32_t hash_table_2[4][256]), uint32_t seed){
    uint64_t hashing_table [4][256];
    uint32_t hashing_table_2 [4][256];
    srand(seed);
    for(int outerCounter = 0; outerCounter < 4; outerCounter++){
        for(int innerCounter = 0; innerCounter < 256; innerCounter++){
            hashing_table[outerCounter][innerCounter] = uInt64Random();
            hashing_table_2[outerCounter][innerCounter] = uIntRandom();
        }
    }
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    for(counter = 0; counter < numberOfLoops; counter++){
        uint32_t original_val = (*f_ptr)(counter, hashing_table, hashing_table_2);
        for(mask_counter = 0; mask_counter < MASK_LEN; mask_counter++){
            uint32_t changed_val = (*f_ptr)(counter ^ masks[mask_counter], hashing_table, hashing_table_2);
            checkFlippedBits(original_val ^ changed_val);
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);
}

void avalancheTestString(uint32_t (*f_ptr)(unsigned char*, int)){
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    unsigned char original_string[NUMBER_STRING_SIZE];
    unsigned char changed_string[NUMBER_STRING_SIZE];
    for(counter = 0; counter < numberOfLoops; counter++){
        uint32_t original_val = (*f_ptr)(original_string, NUMBER_STRING_SIZE);
        //go through all characters in the string
        for(int char_index = 0; char_index < NUMBER_STRING_SIZE; char_index++){
            //for each character change each bit
            for(int bit_index = 0; bit_index < 8; bit_index++){
                changed_string[char_index] = original_string[char_index] ^ byteMask[bit_index];
                uint32_t changed_val = (*f_ptr)(changed_string, NUMBER_STRING_SIZE);
                checkFlippedBits(original_val ^ changed_val);
            }
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);

}

void avalancheTestStringWSeed(unsigned int (*f_ptr)(unsigned char*, int, uint32_t), uint32_t seed){
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    unsigned char original_string[NUMBER_STRING_SIZE];
    unsigned char changed_string[NUMBER_STRING_SIZE];
    for(counter = 0; counter < numberOfLoops; counter++){
        uint32_t original_val = (*f_ptr)(original_string, NUMBER_STRING_SIZE, seed);
        //go through all characters in the string
        for(int char_index = 0; char_index < NUMBER_STRING_SIZE; char_index++){
            //for each character change each bit
            for(int bit_index = 0; bit_index < 8; bit_index++){
                changed_string[char_index] = original_string[char_index] ^ byteMask[bit_index];
                uint32_t changed_val = (*f_ptr)(changed_string, NUMBER_STRING_SIZE, seed);
                checkFlippedBits(original_val ^ changed_val);
            }
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);

}

void clearCounters(){
    for(int counter = 0; counter < 32; counter++){
        timesBitFlipped[counter] = 0;
    }
    for(int counter = 0; counter < 33; counter++){
        amountOfFlippedBits[counter] = 0;
    }
}

void avalancheTest(char* hash_function, int num_loops){
    numberOfLoops = num_loops;
    if(strcmp(hash_function, JENKINS_STRING) == 0){
        avalancheTestUint(jenkinsFullAvalancheHash);
    } else if(strcmp(hash_function, SEVEN_SHIFT_STRING) == 0){
        avalancheTestUint(sevenShiftHash);
    } else if(strcmp(hash_function, THOMAS_WANG_STRING) == 0){
        avalancheTestUint(thomasWangHash);
    } else if(strcmp(hash_function, XXHASH_STRING) == 0){
        avalancheTestString(xxHash32); 
    } else if(strcmp(hash_function, KNUTH_HASH_STRING) == 0){
        avalancheTestUint(knuth_hashHash);
    } else if(strcmp(hash_function, SHA256_HASH_STRING) == 0){
        avalancheTestUint(uintSha256Hash);
    }
    writeResults(hash_function, 0);
    printResults(hash_function);
    clearCounters();
}

void avalancheTestWSeed(char* hash_function, uint32_t seed, int num_loops){
    numberOfLoops = num_loops;
    if(strcmp(hash_function, XXHASH_STRING) == 0){
        avalancheTestStringWSeed(xxHashSeed32,seed); 
    } else if(strcmp(hash_function, TABLE_HASHING_STRING) == 0){
        avalancheTestTableHashing(tableHashingHash, seed);
    } else if(strcmp(hash_function, MIXED_TABLE_HASHING_STRING) == 0){
        avalancheTestMixedTableHashing(mixedTableHashingHash, seed);
    } else if(strcmp(hash_function, TWISTED_TABLE_HASHING_STRING) == 0){
        avalancheTestTwistedTableHashing(twistedTableHashingHash, seed);
    } else if(strcmp(hash_function, KNUTH_HASH_STRING) == 0){
        avalancheTestUintWSeed(knuth_hashHashWSeed, seed);
    }
    writeResults(hash_function, seed);
    printResults(hash_function);
    clearCounters();
}

