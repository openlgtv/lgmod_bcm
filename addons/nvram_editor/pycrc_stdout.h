/**
 * \file pycrc_stdout
 * Functions and types for CRC checks.
 *
 * Generated on Thu Jul 21 12:00:42 2011,
 * by pycrc v0.7.8, http://www.tty1.net/pycrc/
 * using the configuration:
 *    Width        = 32
 *    Poly         = 0x04c11db7
 *    XorIn        = 0xffffffff
 *    ReflectIn    = False
 *    XorOut       = 0x00000000
 *    ReflectOut   = False
 *    Algorithm    = bit-by-bit-fast
 *****************************************************************************/
#ifndef __PYCRC_STDOUT__
#define __PYCRC_STDOUT__

#include <stdlib.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif


/**
 * The definition of the used algorithm.
 *****************************************************************************/
#define CRC_ALGO_BIT_BY_BIT_FAST 1


/**
 * The type of the CRC values.
 *
 * This type must be big enough to contain at least 32 bits.
 *****************************************************************************/
typedef uint32_t crc_t;


/**
 * Calculate the initial crc value.
 *
 * \return     The initial crc value.
 *****************************************************************************/
static inline crc_t crc_init(void)
{
    return 0xffffffff;
}


/**
 * Update the crc value with new data.
 *
 * \param crc      The current crc value.
 * \param data     Pointer to a buffer of \a data_len bytes.
 * \param data_len Number of bytes in the \a data buffer.
 * \return         The updated crc value.
 *****************************************************************************/
crc_t crc_update(crc_t crc, const unsigned char *data, size_t data_len);


/**
 * Calculate the final crc value.
 *
 * \param crc  The current crc value.
 * \return     The final crc value.
 *****************************************************************************/
static inline crc_t crc_finalize(crc_t crc)
{
    return crc ^ 0x00000000;
}


#ifdef __cplusplus
}           /* closing brace for extern "C" */
#endif

#endif      /* __PYCRC_STDOUT__ */

