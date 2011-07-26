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
#define NVRAM_SIZE2 133120
#define NVRAM_FULL_SIZE 1048576

//#define NVRAM_DEBUG_STATUS ( ANA_DB_BASE - 7 ) // 0x1D8
#define NVRAM_DEBUG_STATUS 397 // 0x1D8

typedef unsigned char * string;

string DEBUG_STATES[6] = { "DEBUG", "EVENT", "RELEASE", "DEBUG", "EVENT", "RELEASE" };

#define NVRAM_BAUDRATE 1452    // 0x5AC

string BAUDRATE_STATES[8] = { "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200" };

#define NVRAM_MODEL 1330       // 0x532
#define NVRAM_MODEL_LEN 12

#define NVRAM_SERIAL 674       // 0x2A2
#define NVRAM_SERIAL_LEN 11

#define NVRAM_BLOCK_DATA_SIZE 128
#define NVRAM_BLOCK_HEADER_SIZE 2

#define NVRAM_BLOCK_SIZE=(NVRAM_BLOCK_DATA_SIZE+NVRAM_BLOCK_HEADER_SIZE)
