CC = clang
CFLAGS = -Wall -std=c99 -pedantic
LIBS = -lm

# PYTHON_INCLUDE_PATH=/usr/include/python3.7m
# PYTHON_LIBRARY_PATH=/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu
# PYTHON_VERSION=python3.7m

PYTHON_INCLUDE_PATH=/Library/Frameworks/Python.framework/Versions/3.10/include/python3.10
PYTHON_LIBRARY_PATH=/Library/Frameworks/Python.framework/Versions/3.10/lib
PYTHON_VERSION=python3.10

all: libmol.so _molecule.so mol

libmol.so: mol.o
	$(CC) -shared mol.o -o libmol.so $(LIBS)

_molecule.so: molecule_wrap.o libmol.so
	$(CC) -shared -lmol -dynamiclib -L. -L$(PYTHON_LIBRARY_PATH) -l$(PYTHON_VERSION) -o _molecule.so molecule_wrap.o

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fpic -c mol.c -o mol.o

molecule_wrap.o: molecule_wrap.c 
	$(CC) $(CFLAGS) -c molecule_wrap.c -I $(PYTHON_INCLUDE_PATH) -fPIC -o molecule_wrap.o

mol: testPart1.c libmol.so mol.h
	$(CC) $(CFLAGS) -L. testPart1.c -o mol -lmol
clean:
	rm -rf *.o *.so