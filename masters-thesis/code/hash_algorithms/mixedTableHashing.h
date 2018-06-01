#ifndef MIXED_TABLE_HASHING_HEADER
#define MIXED_TABLE_HASHING_HEADER

uint32_t mixedTableHashingHash(uint32_t x, uint64_t hash_table_1[4][256],
                                uint32_t hash_table_2[4][256]);

void mixedTableHashingHashNumbersWSeed(int array_length, uint32_t seed, uint32_t* array,
                                           uint32_t* return_array);
#endif
