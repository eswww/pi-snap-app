#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>

#include "mcp3208.h"

static const unsigned char spi_bpw = 8;
static const unsigned char spi_mode = 0;
static const unsigned int  spi_delay = 0;
static const unsigned int  spi_speed = 1000000;

static int spi_rw(int fd, unsigned char *data, int len)
{
	struct spi_ioc_transfer spi;

    // Set spi protocol
	spi.tx_buf = (unsigned long)data;
	spi.rx_buf = (unsigned long)data;
	spi.len = len;
	spi.delay_usecs = spi_delay;
	spi.speed_hz = spi_speed;
	spi.bits_per_word = spi_bpw;

	return ioctl(fd, SPI_IOC_MESSAGE(1), &spi);
}

int mcp3208_open(const char *dev)
{
	int fd;

    // Open spi device
	if((fd = open(dev, O_RDWR)) < 0)
		return -1;
	if(ioctl(fd, SPI_IOC_WR_MODE, &spi_mode) < 0)
		return -1;
	if(ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &spi_bpw) < 0)
		return -1;
	if(ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &spi_speed) < 0)
		return -1;

	return fd;
}


int mcp3208_read(int fd, int channel)
{
	unsigned char data[3];
	unsigned int val = 0;

    // Read a 10 bit data from MCP3208
	data[0] = 1;
	data[1] = 0x80 | ((channel & 7) << 4);
	data[2] = 0;

	if (spi_rw(fd, data, 3) < 0)
		return -1;

	val = (data[1] << 8) & 0x300;
	val |= data[2] & 0xFF;

	return val;
}

int mcp3208_close(int fd)
{
    // Close spi device
    return close(fd);
}
