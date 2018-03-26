#include "stdio.h"
#include "djb2.h"

unsigned long djb2Hash(unsigned char *str){
	unsigned long hash = 5381;
        int c;

        while (c = *str++)
        	hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

        return hash;
}

void djb2HashNumbers(int size, unsigned char **array, int* char_len, unsigned long *return_array){
	int counter = 0;
	/*
	 * printf("c-code: size: %d\n", size);
	 * printf("c-code: arrayAccess: %s\n", array[1]);
	 * printf("c-code: returnArray access: %lu\n", returnArray[size-1]);
	 */
	for(counter = 0; counter < size; counter++){
		return_array[counter] = hash(array[counter]);
	}
}
