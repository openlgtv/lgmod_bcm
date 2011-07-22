/**
 * \file nvram_map.h
 * by xeros
 *
 * for use by nvram-crc.c
 *
 * offsets in NVRAM for useful options
 *
 *****************************************************************************/


/**
 *
 *****************************************************************************/
#define NVRAM_SIZE 133120
#define NVRAM_FULL_SIZE 1048576

#define NVRAM_DEBUG_STATUS 397 // 0x1D8

typedef unsigned char * string;

string DEBUG_STATES[6] = { "UNKNOWN: 0", "UNKNOWN: 1", "UNKNOWN: 2", "DEBUG", "EVENT", "RELEASE" };

#define NVRAM_BAUDRATE 1452    // 0x5AC

string BAUDRATE_STATES[8] = { "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200" };
