CC = gcc
CFLAGS = -Wall -Wextra -std=c11

all: budget_tracker

budget_tracker: main.o helpers.o
	$(CC) $(CFLAGS) -o budget_tracker main.o helpers.o

main.o: main.c helpers.h
	$(CC) $(CFLAGS) -c main.c

helpers.o: helpers.c helpers.h
	$(CC) $(CFLAGS) -c helpers.c

clean:
	rm -f *.o budget_tracker
