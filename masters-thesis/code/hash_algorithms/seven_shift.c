#include "stdint.h"

uint32_t hash( uint32_t a)
{
    a -= (a<<6);
    a ^= (a>>17);
    a -= (a<<9);
    a ^= (a<<4);
    a -= (a<<3);
    a ^= (a<<10);
    a ^= (a>>15);
    return a;
}


void hashNumbers(int array_length, uint32_t* array, uint32_t* return_array)
{
    int counter = 0;
    for(counter; counter < array_length; counter++){
	    return_array[counter] = hash(array[counter]);
    }
}
