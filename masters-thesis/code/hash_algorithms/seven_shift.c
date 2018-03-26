#include "stdint.h"
#include "seven_shift.h"

uint32_t seven_shiftHash( uint32_t a)
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

uint32_t sevenShiftHash(uint32_t a){
    a -= (a<<6);
    a ^= (a>>17);
    a -= (a<<9);
    a ^= (a<<4);
    a -= (a<<3);
    a ^= (a<<10);
    a ^= (a>>15);
    return a;
}

void seven_shiftHashNumbers(int array_length, uint32_t* array, uint32_t* return_array)
{
    int counter = 0;
    for(counter; counter < array_length; counter++){
	    return_array[counter] = sevenShiftHash(array[counter]);
    }
}
