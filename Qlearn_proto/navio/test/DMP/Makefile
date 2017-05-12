CC = g++
NAVIO = ../../Navio
INCLUDES = -I ../..

all:
	$(CC) $(INCLUDES) MPU.cpp $(NAVIO)/MPU9250.cpp -o MPU -lrt -lpthread -lpigpio

clean:
	rm MPU
