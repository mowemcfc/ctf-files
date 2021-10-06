#include <stdio.h>


int compute(const char* a, const char* b) {
	int i = 0;
	while(*a && *b) {
		i += (*a++ != *b++);
        printf("%x\n", *a);
        printf("%x\n", *b);
	}
    printf("%x\n", *a);
    printf("%x\n", *b);
	return i;
}


int main(void) {
    char a[256] = "Hello World";
    char b[256] = "Piss Chillin";
    int i = compute(a, b);
    printf("%s\n %s\n", a, b);
    printf("%d\n", i);
}