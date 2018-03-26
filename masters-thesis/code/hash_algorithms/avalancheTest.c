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

static const char JENKINS_STRING[] = "jenkins_full_avalanche.so";
//static const char DJB2_STRING[] = "djb2.so";
static const char SEVEN_SHIFT_STRING[] = "seven_shift.so";
static const char TABLE_HASHING_STRING[] = "tableHashing.so";
static const char TWISTED_TABLE_HASHING_STRING[] = "twistedTableHashing.so";
static const char THOMAS_WANG_STRING[] = "thomas_wang_hash.so";
static const char XXHASH_STRING[] = "xxhash.so";
static const int NUMBER_STRING_SIZE = 12;
const int NUMBER_OF_LOOPS = 1 << 20;
const uint32_t masks[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768,
                          65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216,
                          33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648};
const int byteMask[] = {1, 2, 4, 8, 16, 32, 64, 128};
const int BITS_IN_BYTE = 8;
const int MASK_LEN = 32;
uint32_t amountOfFlippedBits[33] = {0};
uint32_t timesBitFlipped[32] = {0};

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

void printUIntArray(uint32_t array[], int length){
    int counter = 0;
    printf("[");
    for(counter; counter < length - 1; counter++){
        printf("%d,", array[counter]);
    }
    printf("%d]\n", array[length - 1]);
}

void writeUIntArray(char* prefix, uint32_t array[], int length,
                    char* filename){
    FILE *file_ptr;
    file_ptr = fopen(filename, "a");
    int counter = 0;
    fprintf(file_ptr, "%s", prefix);
    fprintf(file_ptr, ",");
    for(counter; counter < length; counter++){
        fprintf(file_ptr, "%d,", array[counter]);
    }
    fprintf(file_ptr, "\n");
}

void printResults(char* hashing_algorithm){
    writeUIntArray(hashing_algorithm, amountOfFlippedBits, 33, "avalancheResults.csv");
    writeUIntArray(hashing_algorithm, timesBitFlipped, 32, "avalancheResults.csv"); 
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
    for(counter = 0; counter < NUMBER_OF_LOOPS; counter++){
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
    for(counter = 0; counter < NUMBER_OF_LOOPS; counter++){
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
    for(counter = 0; counter < NUMBER_OF_LOOPS; counter++){
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
    for(counter = 0; counter < NUMBER_OF_LOOPS; counter++){
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
    for(counter = 0; counter < NUMBER_OF_LOOPS; counter++){
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
    }
    printResults(hash_function);
}

void avalancheTestWSeed(char* hash_function, uint32_t seed){
    if(strcmp(hash_function, XXHASH_STRING) == 0){
        avalancheTestStringWSeed(xxHashSeed32,seed); 
    } else if(strcmp(hash_function, TABLE_HASHING_STRING) == 0){
        avalancheTestTableHashing(tableHashingHash, seed);
    } else if(strcmp(hash_function, TWISTED_TABLE_HASHING_STRING) == 0){
        avalancheTestTwistedTableHashing(twistedTableHashingHash, seed);
    }
    printResults(hash_function);
}

int main(){
    printf("number of loops: %d\n", NUMBER_OF_LOOPS);
    avalancheTest("xxhash.so"); 
}

