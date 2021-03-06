#include "xxHash/xxhash.h"
#include "stdio.h"
#include "time.h"
#include "stdlib.h"
#include "string.h"
#include "xxhash.h"

void xxhashHashNumbers(int array_length, unsigned char** array, int* char_len, unsigned int* return_array){
	int counter = 0;
	for(counter; counter < array_length; counter++){
		return_array[counter] = XXH32(array[counter], char_len[counter], 0);
	}
}

void xxhashHashNumbersWSeed(int array_length, unsigned int seed, unsigned char** array, int* char_len, unsigned int* return_array){
    int counter = 0;
    for(counter; counter < array_length; counter++){
	return_array[counter] = XXH32(array[counter], char_len[counter], seed);
    }

}

unsigned int xxHash32(unsigned char* input, int input_len){
    return XXH32(input, input_len, 0);
}

unsigned int xxHashSeed32(unsigned char* input, int input_len, unsigned int seed){
    return XXH32(input, input_len, seed);
}

//int main(){
//    int counter = 0;
//    int runs = 16777216;
//    int len;
//    char buffer[8];
//    clock_t start, end;
//    double cpu_time_used;
//    printf("doing %d runs\n", runs);
//    fflush(stdout);
//    start = clock();
//    for(counter; counter < runs; counter++){
//	len = sprintf(buffer, "%d", counter);
//	XXH32(buffer, len, 0);	
//    }
//    end = clock();
//    cpu_time_used = (((double) (end - start)) / CLOCKS_PER_SEC) * 1000;
//    printf("it took %f ms to execute %d runs \n", cpu_time_used, runs);
//}
