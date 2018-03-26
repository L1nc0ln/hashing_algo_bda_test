#include "stdint.h"
#include "thomas_wang_hash.h"

uint32_t thomas_wang_hashHash( uint32_t a)
{
    a += ~(a<<15);
    a ^=  (a>>10);
    a +=  (a<<3);
    a ^=  (a>>6);
    a += ~(a<<11);
    a ^=  (a>>16);
}

uint32_t thomasWangHash( uint32_t a)
{
    a += ~(a<<15);
    a ^=  (a>>10);
    a +=  (a<<3);
    a ^=  (a>>6);
    a += ~(a<<11);
    a ^=  (a>>16);
}

uint32_t* thomas_wang_hashHashNumbers(int array_length, uint32_t* array, uint32_t* return_array)
{
    int counter = 0;
    for(counter; counter < array_length; counter++){
	return_array[counter] = thomasWangHash(array[counter]);
    }
    return return_array;
}

