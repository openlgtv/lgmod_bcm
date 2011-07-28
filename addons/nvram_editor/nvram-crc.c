/**
 * \file nvram-crc.c
 *
 * OpenLGTV BCM NVRAM checksum calculator and fixer by xeros, version 0.0.2
 * Source code released under GPL License
 *
 * Default input file:  /tmp/nvram     (can be changed with -f /path/to/nvram_file parameter)
 * Default output file: /tmp/nvram-out (can be changed with -o /path/to/nvram-out_file parameter)
 *
 * copile: (mipsel-linux-)gcc -o nvram-crc nvram.c
 *
 * CRC calculation code generated for CRC32 MPEG2 checksum with pycrc v0.7.8, http://www.tty1.net/pycrc/
 * using the configuration:
 *    Width        = 32
 *    Poly         = 0x04c11db7
 *    XorIn        = 0xffffffff
 *    ReflectIn    = False
 *    XorOut       = 0x00000000
 *    ReflectOut   = False
 *    Algorithm    = bit-by-bit-fast
 *****************************************************************************/
#include "pycrc_stdout.h"     /* include the header file generated with pycrc */
/*
#include "u_types.h"
#include "nvm.h"
*/
#include "nvram_map.h"
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

/**
 * Update the crc value with new data.
 *
 * \param crc      The current crc value.
 * \param data     Pointer to a buffer of \a data_len bytes.
 * \param data_len Number of bytes in the \a data buffer.
 * \return         The updated crc value.
 *****************************************************************************/
crc_t crc_update(crc_t crc, const unsigned char *data, size_t data_len)
{
    unsigned int i;
    bool bit;
    unsigned char c;

    while (data_len--) {
        c = *data++;
        for (i = 0x80; i > 0; i >>= 1) {
            bit = crc & 0x80000000;
            if (c & i) {
                bit = !bit;
            }
            crc <<= 1;
            if (bit) {
                crc ^= 0x04c11db7;
            }
        }
        crc &= 0xffffffff;
    }
    return crc & 0xffffffff;
}




#include <stdio.h>
#include <getopt.h>
#include <stdbool.h>
#include <string.h>


//static char str[256] = "123456789";
//unsigned char str[133120];
//unsigned char str[NVRAM_SIZE];
unsigned char str[NVRAM_SIZE2];
//unsigned char str_out[1048576];
unsigned char str_out[NVRAM_FULL_SIZE];
unsigned char num1a[1];
unsigned char num2a[1];
unsigned char num3a[1];
unsigned char num4a[1];
//unsigned char str[];
FILE *finput;
FILE *foutput;
int ninput;
int noutput;
int write_ofile=0;
int debug_status=9; // lets pickup wrong values at start
int debug_status_new=9;
char debug_status_str[]="0";
int baudrate=9;
int baudrate_new=9;
char baudrate_str[]="0";
int recalculate_crc=0;
unsigned char file[200] = "/tmp/nvram";
unsigned char ofile[200] = "/tmp/nvram-out";

static bool verbose = false;

void print_params(void);
static int get_config(int argc, char *argv[]);

static int get_config(int argc, char *argv[])
{
    int c;
    int option_index;
    static struct option long_options[] = {
        {"verbose",         0, 0, 'v'},
        {"check-string",    1, 0, 's'},
        {0, 0, 0, 0}
    };

    while (1) {
        option_index = 0;

        c = getopt_long (argc, argv, "w:p:n:i:u:o:f:d:b:vt", long_options, &option_index);
        if (c == -1)
            break;

        switch (c) {
            case 0:
                printf ("option %s", long_options[option_index].name);
                if (optarg)
                    printf (" with arg %s", optarg);
                printf ("\n");
            case 'f':
                //memcpy(file, optarg, strlen(optarg) < sizeof(file) ? strlen(optarg) + 1 : sizeof(file));
                memcpy(file, optarg, strlen(optarg) + 1);
                //memcpy(str, optarg, strlen(optarg) < 133120 ? strlen(optarg) + 1 : 133120);
                //file[sizeof(file) - 1] = '\0';
                //printf("%s\n", file);
                break;
            case 'o':
                memcpy(ofile, optarg, strlen(optarg) + 1);
                break;
            case 'd':
                memcpy(debug_status_str, optarg, strlen(optarg) + 1);
                debug_status_new=atoi(debug_status_str);
                break;
            case 'b':
                memcpy(baudrate_str, optarg, strlen(optarg) + 1);
                baudrate_new=atoi(baudrate_str);
                break;
            case 'v':
                verbose = true;
                break;
            case '?':
                return -1;
            case ':':
                fprintf(stderr, "missing argument to option %c\n", c);
                return -1;
            default:
                fprintf(stderr, "unhandled option %c\n", c);
                return -1;
        }
    }

    return 0;
}

void print_params(void)
{
    char format[20];

    snprintf(format, sizeof(format), "%%-16s = 0x%%0%dx\n", (unsigned int)(32 + 3) / 4);
    printf("%-16s = %d\n", "width", (unsigned int)32);
    printf(format, "poly", (unsigned int)0x04c11db7);
    printf("%-16s = %s\n", "reflect_in", "false");
    printf(format, "xor_in", 0xffffffff);
    printf("%-16s = %s\n", "reflect_out", "false");
    printf(format, "xor_out", (unsigned int)0x00000000);
    printf(format, "crc_mask", (unsigned int)0xffffffff);
    printf(format, "msb_mask", (unsigned int)0x80000000);
}

char* substring(const char* strn, size_t begin, size_t len)
{
  if (strn == 0 || strlen(strn) == 0 || strlen(strn) < begin || strlen(strn) < (begin+len))
    return 0;

  return strndup(strn + begin, len);
}

int get_offset(int in_offset)
{
    return in_offset+(((in_offset/NVRAM_BLOCK_DATA_SIZE)+1)*NVRAM_BLOCK_HEADER_SIZE);
}

int get_size(int in_size)
{
    if ( in_size % NVRAM_BLOCK_DATA_SIZE == 0 )
    {
	return in_size+((in_size/NVRAM_BLOCK_DATA_SIZE)*NVRAM_BLOCK_HEADER_SIZE);
    } else {
	return in_size+(((in_size/NVRAM_BLOCK_DATA_SIZE)+1)*NVRAM_BLOCK_HEADER_SIZE);
    }
}


/**
 * C main function.
 *
 * \return     0 on success, != 0 on error.
 *****************************************************************************/
int main(int argc, char *argv[])
{

    printf("Broadcom platform based LG Digital TV NVRAM editor\n");
    printf("Version 0.0.3 by xeros (openlgtv.org.ru) 28.07.2011\n\n");

    crc_t crc;

    get_config(argc, argv);

    /*if (strlen(file) == 0)
    {
	file="/tmp/nvram";
    }*/

    finput = fopen(file, "rb");
    if (finput)
    {
	ninput = fread(str, sizeof(str), 1, finput);
	ninput = fread(num1a, 1, 1, finput);
	ninput = fread(num2a, 1, 1, finput);
	ninput = fread(num3a, 1, 1, finput);
	ninput = fread(num4a, 1, 1, finput);
	fclose(finput);
    } else {
	printf("%s %s\n", "error opening input file for read:", file);
	return 1;
    }

    printf("Input file:       %s\n\n", file);
    debug_status=str[NVRAM_DEBUG_STATUS];
    baudrate=str[NVRAM_BAUDRATE];
    
    char model[NVRAM_MODEL_LEN];
    char serial[NVRAM_SERIAL_LEN];

    int nr;
    for (nr = 0; nr <= NVRAM_MODEL_LEN; nr++)
    {
	model[nr]=str[NVRAM_MODEL+nr];
    }
    printf("Model name:       %s\n", model);

    for (nr = 0; nr <= NVRAM_SERIAL_LEN; nr++)
    {
	serial[nr]=str[NVRAM_SERIAL+nr];
    }
    printf("Serial number:    %s\n", serial);
    
    
    /*
    printf("Debug status offset: %x\n", NVRAM_DEBUG_STATUS-((NVRAM_DEBUG_STATUS/NVRAM_BLOCK_DATA_SIZE)*NVRAM_BLOCK_HEADER_SIZE));
    printf("Debug status offset: %x\n", get_offset(NVRAM_DEBUG_STATUS));
    */
    
    if (debug_status < 3)
    {
	printf("Platform:         MSTAR Saturn7\n");
    } else {
	if (debug_status < 6)
	{
	    printf("Platform:         Broadcom BCM3549/3556\n");
	} else {
	    printf("Platform:         UNKNOWN!\n");
	}
    }
/*
printf(" NVM_ID_BASE : \t\t 0x%x \t\t %i \t %i\n", NVM_ID_BASE, NVM_ID_BASE, NVM_ID_SIZE );
printf(" NVM_HEADER_BASE : \t 0x%x \t\t %i \t %i\n", NVM_HEADER_BASE, NVM_HEADER_BASE, NVM_HEADER_SIZE );
printf(" TNVM_MAGIC_BASE : \t 0x%x \t\t %i \t %i\n", TNVM_MAGIC_BASE, TNVM_MAGIC_BASE, TNVM_MAGIC_SIZE );
printf(" SYS_DB_BASE : \t\t 0x%x \t\t %i \t %i\n", SYS_DB_BASE, SYS_DB_BASE, SYS_DB_SIZE );
printf(" ANA_DB_BASE : \t\t 0x%x \t\t %i \t %i\n", ANA_DB_BASE, ANA_DB_BASE, ANA_DB_SIZE );
printf(" TOOL_OPTION_DB_BASE : \t 0x%x \t\t %i\n", TOOL_OPTION_DB_BASE, TOOL_OPTION_DB_BASE );
printf(" FACTORY_DB_BASE : \t 0x%x \t\t %i\n", FACTORY_DB_BASE, FACTORY_DB_BASE );
printf(" UI_DB_BASE : \t\t 0x%x \t\t %i\n", UI_DB_BASE, UI_DB_BASE );
printf(" UI_EXPERT_DB_BASE : \t 0x%x \t %i\n", UI_EXPERT_DB_BASE, UI_EXPERT_DB_BASE );
printf(" CH_DB_BASE : \t\t 0x%x \t %i\n", CH_DB_BASE, CH_DB_BASE );
printf(" BT_DB_BASE : \t\t 0x%x \t %i\n", BT_DB_BASE, BT_DB_BASE );
printf(" EMP_DB_BASE : \t\t 0x%x \t %i\n", EMP_DB_BASE, EMP_DB_BASE );
printf(" ACAP_DB_BASE : \t 0x%x \t %i\n", ACAP_DB_BASE, ACAP_DB_BASE );
printf(" THX_DB_BASE : \t\t 0x%x \t %i\n", THX_DB_BASE, THX_DB_BASE );
printf(" NVRAM_SIZE : \t\t 0x%x \t %i\n", NVRAM_SIZE, NVRAM_SIZE );

printf("NVRAM OFFSETS:\n");

printf(" NVM_ID_BASE : \t\t 0x%x \t\t %i \t %i\n", get_offset(NVM_ID_BASE), NVM_ID_BASE, NVM_ID_SIZE );
printf(" NVM_HEADER_BASE : \t 0x%x \t\t %i \t %i\n", get_offset(NVM_HEADER_BASE), NVM_HEADER_BASE, NVM_HEADER_SIZE );
printf(" TNVM_MAGIC_BASE : \t 0x%x \t\t %i \t %i\n", get_offset(TNVM_MAGIC_BASE), TNVM_MAGIC_BASE, TNVM_MAGIC_SIZE );
printf(" SYS_DB_BASE : \t\t 0x%x \t\t %i \t %i\n", get_offset(SYS_DB_BASE), SYS_DB_BASE, SYS_DB_SIZE );
printf(" ANA_DB_BASE : \t\t 0x%x \t\t %i \t %i\n", get_offset(ANA_DB_BASE), ANA_DB_BASE, ANA_DB_SIZE );
printf(" TOOL_OPTION_DB_BASE : \t 0x%x \t\t %i\n", get_offset(TOOL_OPTION_DB_BASE), TOOL_OPTION_DB_BASE );
printf(" FACTORY_DB_BASE : \t 0x%x \t\t %i\n", get_offset(FACTORY_DB_BASE), FACTORY_DB_BASE );
printf(" UI_DB_BASE : \t\t 0x%x \t\t %i\n", get_offset(UI_DB_BASE), UI_DB_BASE );
printf(" UI_EXPERT_DB_BASE : \t 0x%x \t %i\n", get_offset(UI_EXPERT_DB_BASE), UI_EXPERT_DB_BASE );
printf(" CH_DB_BASE : \t\t 0x%x \t %i\n", get_offset(CH_DB_BASE), CH_DB_BASE );
printf(" BT_DB_BASE : \t\t 0x%x \t %i\n", get_offset(BT_DB_BASE), BT_DB_BASE );
printf(" EMP_DB_BASE : \t\t 0x%x \t %i\n", get_offset(EMP_DB_BASE), EMP_DB_BASE );
printf(" ACAP_DB_BASE : \t 0x%x \t %i\n", get_offset(ACAP_DB_BASE), ACAP_DB_BASE );
printf(" THX_DB_BASE : \t\t 0x%x \t %i\n", get_offset(THX_DB_BASE), THX_DB_BASE );
printf(" NVRAM_SIZE : \t\t 0x%x \t %i\n", get_size(NVRAM_SIZE), NVRAM_SIZE );
printf(" NVMDRV_TOTAL_SIZE : \t\t 0x%x \t %i \t %i\n", get_size(NVMDRV_TOTAL_SIZE), get_size(NVMDRV_TOTAL_SIZE), NVMDRV_TOTAL_SIZE );
*/
    if ((debug_status > 5) || (baudrate > 7))
    {
	printf("NVRAM DUMP IS WRONG!\nPoweroff and poweron TV to get good one (do not use reboot) or use yours older NVRAM dump!\n");
	return -1;
    }
    
    string *debug_status_type = &DEBUG_STATES[debug_status];
    string *baudrate_type = &BAUDRATE_STATES[baudrate];

    printf("Debug status:     %s (%i)\n", *debug_status_type, debug_status);
    printf("Baudrate:         %s bps (%i)\n", *baudrate_type, baudrate);


    crc = crc_init();
    crc = crc_update(crc, (unsigned char *)str, sizeof(str));
    crc = crc_finalize(crc);

    if (verbose) {
        print_params();
    }
    
    int i;

    //for(i = 0;i < 133120;++i)
    //printf("%c", ((char *)str)[i]);
    
    char buffer[5];
    sprintf(buffer, "%lx", (long unsigned int)crc);
    //char buffer2[5];
    //sprintf(buffer2, "%lx", str2);
    
    char* num1 = substring(buffer, 6, 2);
    char* num2 = substring(buffer, 4, 2);
    char* num3 = substring(buffer, 2, 2);
    char* num4 = substring(buffer, 0, 2);
    
    printf("\n");
    printf("Read CRC:         %x %x %x %x\n", *num1a, *num2a, *num3a, *num4a);
    printf("Calculated CRC:   %s %s %s %s\n", num1, num2, num3, num4);
    char crc1[9], crc2[9];
    int ret  = sprintf(crc1, "%x%x%x%x", *num1a, *num2a, *num3a, *num4a);
    int ret2 = sprintf(crc2, "%s%s%s%s", num1, num2, num3, num4);
    //printf("Read CRC:         %s\n", crc1);
    //printf("Calculated CRC:   %s\n", crc2);
    //printf("ret, ret2: %i, %i\n",ret,ret2);
    if (strcmp(crc1, crc2))
    {
	printf("\nChecksum is WRONG!\n\n");
	write_ofile=1;
    } else {
	printf("\nChecksum is OK!\n\n");
    }

    if ((debug_status_new > 2) && (debug_status_new < 6))
    {
	string *debug_status_old = &DEBUG_STATES[str[NVRAM_DEBUG_STATUS]];
	string *debug_status_str = &DEBUG_STATES[debug_status_new];
	debug_status=debug_status_new;
	printf("Changing debug status from %s to %s ...\n", *debug_status_old, *debug_status_str);

	str[NVRAM_DEBUG_STATUS]=debug_status;
	
	recalculate_crc=1;
    }

    if ((baudrate_new < 8))
    {
	string *baudrate_old = &BAUDRATE_STATES[str[NVRAM_BAUDRATE]];
	string *baudrate_str = &BAUDRATE_STATES[baudrate_new];
	baudrate=baudrate_new;
	printf("Changing baudrate from %s to %s ...\n", *baudrate_old, *baudrate_str);

	str[NVRAM_BAUDRATE]=baudrate;
	
	recalculate_crc=1;
    }

    if (recalculate_crc == 1)
    {
	crc = crc_init();
	crc = crc_update(crc, (unsigned char *)str, sizeof(str));
	crc = crc_finalize(crc);

	sprintf(buffer, "%lx", (long unsigned int)crc);
    
	num1 = substring(buffer, 6, 2);
	num2 = substring(buffer, 4, 2);
	num3 = substring(buffer, 2, 2);
	num4 = substring(buffer, 0, 2);
    
	printf("\nRecalculated CRC: %s %s %s %s\n\n", num1, num2, num3, num4);

	write_ofile=1;
    }

    if (write_ofile == 1)
    {
	//printf("Trying to write changed file to %s ...\n", ofile);
	finput = fopen(file, "rb");
        if (finput)
	{
	    ninput = fread(str_out, sizeof(str_out), 1, finput);
	    int num1x;
	    int num2x;
	    int num3x;
	    int num4x;
	    sscanf(num1, "%x", &num1x);
	    sscanf(num2, "%x", &num2x);
	    sscanf(num3, "%x", &num3x);
	    sscanf(num4, "%x", &num4x);
	    str_out[NVRAM_DEBUG_STATUS]=debug_status;
	    str_out[NVRAM_BAUDRATE]=baudrate;
	    str_out[sizeof(str) + 0 ] = num1x;
	    str_out[sizeof(str) + 1 ] = num2x;
	    str_out[sizeof(str) + 2 ] = num3x;
	    str_out[sizeof(str) + 3 ] = num4x;
	    foutput = fopen(ofile, "wb");
	    if (foutput)
	    {
		noutput = fwrite(str_out, 1, sizeof(str_out), foutput);
		fclose(foutput);
		printf("File: %s saved.\n", ofile);
		printf("\nTo commit changes, flash the %s file to nvram partition and reboot TV (do not use power button for that)!\n", ofile);
	    } else {
		printf("%s %s\n", "error opening file to write to: ", ofile);
		return 1;
	    }
	} else {
	    printf("%s %s\n", "error opening input file: ", file);
	    return 1;
	}
    }
    
    //free(buffer);
    free(num1);
    free(num2);
    free(num3);
    free(num4);
    
    return 0;
}

