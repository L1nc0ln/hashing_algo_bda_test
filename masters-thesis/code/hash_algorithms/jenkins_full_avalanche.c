#include "stdint.h"
#include "stdio.h"
#include "time.h"


uint32_t hash( uint32_t a)
{
    a = (a+0x7ed55d16) + (a<<12);
    a = (a^0xc761c23c) ^ (a>>19);
    a = (a+0x165667b1) + (a<<5);
    a = (a+0xd3a2646c) ^ (a<<9);
    a = (a+0xfd7046c5) + (a<<3);
    a = (a^0xb55a4f09) ^ (a>>16);
    return a;
}


void hashNumbers(int array_length, uint32_t* array, uint32_t* return_array)
{
    int counter = 0;
    for(counter; counter < array_length; counter++){
	return_array[counter] = hash(array[counter]);
    }
}

int main(){
    int counter = 0;
    int runs = 16777216;
    clock_t start, end;
    double cpu_time_used;
    printf("doing %d runs", runs);
    start = clock();
    for(counter = 0; counter < runs; counter++){
	hash(counter);
    }
    end = clock();
    cpu_time_used = (((double) (end - start)) / CLOCKS_PER_SEC) * 1000;
    printf("it took %f ms to execute %d runs \n", cpu_time_used, runs);
}
