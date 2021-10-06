#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// gcc -m32 -g -w -o pwn2 -fno-stack-protector pwn2.c
// /usr/bin/socat -dd TCP4-LISTEN:9002,fork,reuseaddr EXEC:/home/pwn2/pwn2,pty,echo=0,raw,iexten=0 &
// install libc6-i386 to get the 32 bit libraries necessary to run in 32 bit mode

void numDigits() {
    char buffer[64];
    printf("Enter a number to count the number of digits:\n");
    printf("Note: using the atoi function at address: %08x\n", &atoi);
    gets(&buffer);
    int x = atoi(buffer);
    if (x < 0) {
        x = x * (-1);
    }
    int digits = 0;
    while (x > 0) {
        x = x / 10;
        digits += 1;
    }
    printf("There are %d digits in %s\n", digits, buffer);
}

void setup() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

int main(int argc, char **argv) {
    setup();
    numDigits();
    return 0;
}
