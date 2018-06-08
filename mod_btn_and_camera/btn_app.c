#include <stdio.h>
#include <sys/fcntl.h>

void main(void) {
        int dev;
        char c;
        dev = open("/dev/btn_test",O_RDWR);
        scanf("%c",&c);
        close(dev);
}