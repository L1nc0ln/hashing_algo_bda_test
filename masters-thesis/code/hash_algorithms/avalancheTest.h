#ifndef AVALANCHE_TEST_HEADER
#define AVALANCHE_TEST_HEADER
#include "stdint.h"

void avalancheTest(char* hash_function, int num_loops);

void avalancheTestWSeed(char* hash_function, uint32_t seed, int num_loops);

#endif
