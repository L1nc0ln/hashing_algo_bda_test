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
#include "xxhash.h"
#include "knuth_hash.h"

static const char JENKINS_STRING[] = "jenkins_full_avalanche.so";
//static const char DJB2_STRING[] = "djb2.so";
static const char SEVEN_SHIFT_STRING[] = "seven_shift.so";
static const char KNUTH_HASH_STRING[] = "knuth_hash.so";
static const char TABLE_HASHING_STRING[] = "tableHashing.so";
static const char TWISTED_TABLE_HASHING_STRING[] = "twistedTableHashing.so";
static const char THOMAS_WANG_STRING[] = "thomas_wang_hash.so";
static const char XXHASH_STRING[] = "xxhash.so";
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

void printUIntArray(long array[], int length){
    int counter = 0;
    printf("[");
    for(counter; counter < length - 1; counter++){
        printf("%ld%c", array[counter], delimiter);
    }
    printf("%ld]\n", array[length - 1]);
}

void writeUIntArray(char* prefix, long array[], int length,
                    FILE *file_ptr){
    int counter = 0;
    fprintf(file_ptr, "%s", prefix);
    fprintf(file_ptr, "%c", delimiter);
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
    printUIntArray(amountOfFlippedBits, 33);
    printf("bit flipped how often:\n");
    printUIntArray(timesBitFlipped, 32);
}

void checkFlippedBits(uint32_t flippedBits){
    int numFlippedBits = 0;
    int counter = 0;
    for(counter; counter <= 32; counter++){
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

void avalancheTestTableHashing(uint32_t (*f_ptr)(uint32_t x, uint32_t hash_table[4][256]), uint32_t seed){
    uint32_t hashing_table [4][256];
    srand(seed);
    for(int outerCounter = 0; outerCounter < 4; outerCounter++){
        for(int innerCounter = 0; innerCounter < 256; innerCounter++){
            hashing_table[outerCounter][innerCounter] = rand();
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
            hashing_table[outerCounter][innerCounter] = rand();
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

void avalancheTestString(uint32_t (*f_ptr)(unsigned char*, int)){
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    unsigned char original_string[NUMBER_STRING_SIZE];
    unsigned char changed_string[NUMBER_STRING_SIZE];
    for(counter = 0; counter < numberOfLoops; counter++){
        sprintf(original_string, "%d", counter);
        uint32_t original_val = (*f_ptr)(original_string, NUMBER_STRING_SIZE);
        for(int char_index = 0; char_index < NUMBER_STRING_SIZE; char_index++){
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
        sprintf(original_string, "%d", counter);
        uint32_t original_val = (*f_ptr)(original_string, NUMBER_STRING_SIZE, seed);
        for(int char_index = 0; char_index < NUMBER_STRING_SIZE; char_index++){
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

void avalancheTest(char* hash_function){
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
    }
    writeResults(hash_function, 0);
    printResults(hash_function);
}

void avalancheTestWSeed(char* hash_function, uint32_t seed){
    if(strcmp(hash_function, XXHASH_STRING) == 0){
        avalancheTestStringWSeed(xxHashSeed32,seed); 
    } else if(strcmp(hash_function, TABLE_HASHING_STRING) == 0){
        avalancheTestTableHashing(tableHashingHash, seed);
    } else if(strcmp(hash_function, TWISTED_TABLE_HASHING_STRING) == 0){
        avalancheTestTwistedTableHashing(twistedTableHashingHash, seed);
    } else if(strcmp(hash_function, KNUTH_HASH_STRING) == 0){
        avalancheTestUintWSeed(knuth_hashHashWSeed, seed);
    }
    writeResults(hash_function, seed);
    printResults(hash_function);
}

int main(){
    printf("number of loops: %d\n", numberOfLoops);
    avalancheTest("jenkins_full_avalanche.so"); 
    avalancheTest("seven_shift.so");
}

