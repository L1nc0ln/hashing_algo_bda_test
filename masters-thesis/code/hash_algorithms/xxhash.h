#ifndef XX_HASH_HEADER
#define XX_HASH_HEADER

unsigned int xxHash32(unsigned char* input, int input_len);

unsigned int xxHashSeed32(unsigned char* input, int input_len, unsigned int seed);

#endif
