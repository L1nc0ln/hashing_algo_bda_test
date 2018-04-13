CC = gcc

SOURCES = avalancheTest.c seven_shift.c jenkins_full_avalanche.c xxhash.c \
	  tableHashing.c twistedTableHashing.c djb2.c thomas_wang_hash.c \
	  xxHash/xxhash.c knuth_hash.c

SHARED_LIB_SOURCES = seven_shift.c jenkins_full_avalanche.c tableHashing.c \
		     thomas_wang_hash.c twistedTableHashing.c djb2.c knuth_hash.c

SHARED_LIBS = seven_shift.so jenkins_full_avalanche.so tableHashing.so \
	      thomas_wang_hash.so twistedTableHashing.so djb2.so knuth_hash.so

EXECUTABLE = avalancheTestMain

SHARED_AVALANCHE_LIB = avalanche_so

$(SHARED_AVALANCHE_LIB) : $(SOURCES)
	$(CC) -shared -o avalancheTest.so -fPIC $(SOURCES)

$(EXECUTABLE) : $(SOURCES)
	$(CC) -o $(EXECUTABLE) $(SOURCES) avalancheTestMain.c

hash_shared_libs : $(SHARED_LIB_SOURCES)
	gcc -shared -o seven_shift.so -fPIC seven_shift.c
	gcc -shared -o jenkins_full_avalanche.so -fPIC jenkins_full_avalanche.c
	gcc -shared -o tableHashing.so -fPIC tableHashing.c
	gcc -shared -o thomas_wang_hash.so -fPIC thomas_wang_hash.c
	gcc -shared -o twistedTableHashing.so -fPIC twistedTableHashing.c
	gcc -shared -o djb2.so -fPIC djb2.c
	gcc -shared -o knuth_hash.so -fPIC knuth_hash.c

xxhash.so : xxhash.c xxHash/xxhash.c
	gcc -shared -o xxhash.so -fPIC xxhash.c xxHash/xxhash.c

.PHONY : clean

clean : rm *.o temp
