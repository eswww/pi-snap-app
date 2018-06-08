obj-m := btn.o
KDIR := ~/linux-rpi/
ARM := ARCH=arm CROSS_COMPILE=/usr/bin/arm-linux-gnueabi-
PWD := $(shell pwd)

default:
        $(MAKE) -C $(KDIR) M=$(PWD) $(ARM) modules
        arm-linux-gnueabi-gcc -o btn_app btn_app.c
clean:
        $(MAKE) -C $(KDIR) M=$(PWD) $(ARM) clean