#ifndef SHA_256_HEADER
#define SHA_256_HEADER

void calc_sha_256(uint8_t hash[32], const void *input, size_t len);

uint32_t uintSha256Hash(uint32_t toHash);

#endif
