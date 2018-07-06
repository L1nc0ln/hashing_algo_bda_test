Project for the master's thesis "PERFORMANCE EVALUATION OF HASH FUNCTIONS 
IN BIG DATA ALGORITHMS USING EMPIRICAL METHODS" by Michael Kaspera.

The code is meant to do test runs on the performance of hash algorithms in 
probabilistic data structures such as Count-Min Sketch, Bloom Filter and 
HyperLogLog as well as determine the general distribution characteristica 
of the utilized hash algorithms by doing chi-square and avalanche tests.

Results of the tests, along with a few diagrams,  can be found on the following
google spreadsheet: https://goo.gl/JefqGX
A preliminary draft of the thesis can be found via the following link:
https://mega.nz/#!VYlnxI6K!RVVywi-oijQlywYEIFbIMSShZrQPiSfZLOETiYQPjRs

Currently available hash algorithms for testing:
 - xxHash
 - Sha-256
 - Simple tabulation
 - Twisted tabulation
 - Mixed tabulation
 - Jenkins Full Avalanche
 - Seven Shift
 - Thomas Wang's hash
 - Knuth's hash

Simply adding another hash algorithm by defining the parameters of the algorithm
in the config file does not work at the moment since the parameters are
hard-coded at the moment to avoid having to define the parameters for each
test. 
In the future an implementation of this feature might be done.


COMPILATION OF HASH ALGORITHMS
Since the hash algorithms are coded in c, as well as the avalanche test, they
have to be compiled on your system first. To make this as easy as possible
a make file is included in the folder of the hash algorithms 
"xxx/code/hash\_algorithms". Go into this folder and call:

make hash\_shared\_libs

this will compile the files into .so files that can be used by the ctypes 
library of python.
The command

make avalanche\_so

will create the avalanche test as .so file, which is needed to run avalanche 
tests.


SAMPLE CONFIG FILE
A sample config file is included, it is named "configFile.example".
In it, the way to define a test run is described and a few example tests
are written. In order to use this project a file named "configFile" that
described the tests that should be executed has to exist, so either rename
the sample config file or create a new file with the information from
the example config file.


REQUIREMENTS
This project was written in Python 3.6, used packages that have to be installed
via pip3 are:
 - numpy
 - bitarray
