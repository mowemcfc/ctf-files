#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

void target()
{
    system("/bin/bash");
}

void handler() {
    printf("Timeout.\n");
    exit(1);
}

void setup() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    signal(SIGALRM, handler);
    alarm(30);
}

typedef struct struc {
    int isadmin;
    char name[16];
} account;

int main(int argc, char **argv)
{
    setup();
    
    account *admin, *user;
    char buffer[64];

    printf("Welcome to the Secure Heap Login.\n");

    admin = malloc(sizeof(account));
    user = malloc(sizeof(account));
    
    admin->isadmin = 1;
    user->isadmin = 0;

    printf("Enter the name of the admin: ");
    scanf("%s", buffer);
    strcpy(admin->name, buffer);
     
    printf("Enter the name of the user: ");
    scanf("%s", buffer);
    strcpy(user->name, buffer);

    if (user->isadmin != 0) {
        printf("How user has this power?\n");
        target();
    } else {
        printf("System is secure.\n");
    }

    return 0;
}
