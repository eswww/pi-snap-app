#include <stdio.h>
#include <stdlib.h>

#include "mcp3208.h"

#define SPI_DEV_NAME "/dev/spidev0.0"

static int get_light_sensor_data(int spi_fd, int channel)
{
	int data = mcp3208_read(spi_fd, channel);

    // ADC read error
	if(data < 0)
        return -1;

    return data;
}

int main(void)
{
	int fd = mcp3208_open(SPI_DEV_NAME);

    // ADC open error
	if(fd < 0)
        return -1;

    //printf("light sensor data: %d\n", get_light_sensor_data(fd, 0));
    printf("%d", get_light_sensor_data(fd, 0));

    mcp3208_close(fd);
	return 0;
}
