#include "stdint.h"
#include "stdio.h"
#include "jenkins_full_avalanche.h"
#include "time.h"

const int NUMBER_OF_LOOPS = 1 << 30;
uint32_t amountOfFlippedBits[33] = {0};
uint32_t timesBitFlipped[32] = {0};
const uint32_t masks[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768,
                          65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216,
                          33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648};
const int MASK_LEN = 32;


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

int main(){
    clock_t start, end;
    start = clock();
    uint32_t counter = 0;
    int mask_counter = 0;
    for(counter = 0; counter < NUMBER_OF_LOOPS; counter++){
        uint32_t original_val = jenkinsFullAvalancheHash(counter);
        for(mask_counter = 0; mask_counter < MASK_LEN; mask_counter++){
            uint32_t changed_val = jenkinsFullAvalancheHash(counter ^ masks[mask_counter]);
            checkFlippedBits(original_val ^ changed_val);
        }
    }
    end = clock();
    double cpu_time_used = (((double)(end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute this code\n", cpu_time_used);
    printf("amount of flipped bits:\n");
    printUIntArray(amountOfFlippedBits, 33);
    printf("bit flipped how often:\n");
    printUIntArray(timesBitFlipped, 32);
}

