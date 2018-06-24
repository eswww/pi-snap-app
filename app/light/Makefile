SOURCES=$(shell find . -type f -iname '*.c')
TARGET=light_sensor.out

all: $(TARGET)

$(TARGET): $(SOURCES)
	gcc $(SOURCES) -o $(TARGET) -W -Wall -Wno-unused-parameter

clean:
	rm -f $(TARGET)
