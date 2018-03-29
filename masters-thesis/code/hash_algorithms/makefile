CC = gcc

SOURCES = avalancheTest.c seven_shift.c jenkins_full_avalanche.c xxhash.c \
	  tableHashing.c twistedTableHashing.c djb2.c thomas_wang_hash.c \
	  xxHash/xxhash.c

SHARED_LIB_SOURCES = seven_shift.c jenkins_full_avalanche.c tableHashing.c \
		     thomas_wang_hash.c twistedTableHashing.c djb2.c

SHARED_LIBS = seven_shift.so jenkins_full_avalanche.so tableHashing.so \
	      thomas_wang_hash.so twistedTableHashing.so djb2.so

EXECUTABLE = avalancheTest

$(EXECUTABLE) : $(SOURCES)
	$(CC) -o $(EXECUTABLE) $(SOURCES)

hash_shared_libs : $(SHARED_LIB_SOURCES)
	gcc -shared -o seven_shift.so -fPIC seven_shift.c
	gcc -shared -o jenkins_full_avalanche.so -fPIC jenkins_full_avalanche.c
	gcc -shared -o tableHashing.so -fPIC tableHashing.c
	gcc -shared -o thomas_wang_hash.so -fPIC thomas_wang_hash.c
	gcc -shared -o twistedTableHashing.so -fPIC twistedTableHashing.c
	gcc -shared -o djb2.so -fPIC djb2.c

xxhash.so : xxhash.c xxHash/xxhash.c
	gcc -shared -o xxhash.so -fPIC xxhash.c xxHash/xxhash.c

.PHONY : clean

clean : rm *.o temp
