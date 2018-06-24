#ifndef MCP3208_H_
#define MCP3208_H_

int mcp3208_open(const char *dev);
int mcp3208_read(int fd, int channel);
int mcp3208_close(int fd);

#endif
