#include <stdlib.h>
#include <stdio.h>

int main (void) {
	int* hello = 0x01020304;
	char buf[32];
	scanf("%s", buf);
	printf(buf);
	printf("\n");

	return 0;
}
