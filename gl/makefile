# Make sucks but CMake sucks more
# Just replace this with things that work on windows if you really need to. I don't care.

PROGRAM = "OpenGL"
CXX = g++
ARGS = -std=c++17 -O3 -lGL -lglfw -lGLEW -lSOIL -o OpenGL

SOURCE = $(wildcard *.cpp)
INVR_SOURCE = $(wildcard invr/*.cpp)
OBJECTS = $(wildcard *.o)

all: clean build

build:
	${CXX} ${ARGS} ${INVR_SOURCE} ${SOURCE}
	strip ${PROGRAM}

clean:
	rm -f ${PROGRAM} ${OBJECTS}
