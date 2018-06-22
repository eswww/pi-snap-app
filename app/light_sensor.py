import spidev


class MCP3208:
    def __init__(self, spi_channel=0):
        self.spi_dev = spidev.SpiDev(0, spi_channel)
        self.spi_dev.max_speed_hz = 1000000

    def __del__(self):
        self.close

    def read(self, adc_channel=0):
        recv = self.spi_dev.xfer2(
            [1, 8 + adc_channel << 4, 0]
        )

        data = ((recv[1] & 3) << 8 ) + recv[2]

        return data

    def close(self):
        if self.spi_dev != None:
            self.spi_dev.close
            self.spi_dev = None
