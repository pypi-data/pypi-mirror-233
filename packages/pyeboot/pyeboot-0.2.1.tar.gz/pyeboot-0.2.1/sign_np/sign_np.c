// Copyright (C) 2015       Hykem <hykem@hotmail.com>
// Licensed under the terms of the GNU GPL, version 3
// http://www.gnu.org/licenses/gpl-3.0.txt

#include "sign_np.h"

int sfo_get_key(u8 *sfo_buf, char *name, void *value)
{
	int i, offset;
	SFO_Header *sfo = (SFO_Header*)sfo_buf;
	SFO_Entry *sfo_keys = (SFO_Entry*)(sfo_buf + 0x14);

	if (sfo->magic != PSF_MAGIC)
		return -1;

	for (i = 0; i < sfo->key_count; i++)
	{
		offset = sfo_keys[i].name_offset;
		offset += sfo->key_offset;
		
		if (strcmp((char*)sfo_buf + offset, name) == 0)
		{
			offset = sfo_keys[i].data_offset;
			offset += sfo->val_offset;
			memcpy(value, sfo_buf + offset, sfo_keys[i].val_size);
			return sfo_keys[i].val_size;
		}
	}

	return -1;
}

int sfo_put_key(u8 *sfo_buf, char *name, void *value)
{
	int i, offset;
	SFO_Header *sfo = (SFO_Header*)sfo_buf;
	SFO_Entry *sfo_keys = (SFO_Entry*)(sfo_buf + 0x14);

	if (sfo->magic != PSF_MAGIC)
		return -1;

	for (i = 0; i < sfo->key_count; i++)
	{
		offset = sfo_keys[i].name_offset;
		offset += sfo->key_offset;
		
		if (strcmp((char*)sfo_buf + offset, name) == 0)
		{
			offset = sfo_keys[i].data_offset;
			offset += sfo->val_offset;
			memcpy(sfo_buf + offset, value, sfo_keys[i].val_size);
			return 0;
		}
	}

	return -1;
}

void encrypt_table(u8 *table)
{
	u32 *p = (u32*)table;
	u32 k0, k1, k2, k3;

	k0 = p[0]^p[1];
	k1 = p[1]^p[2];
	k2 = p[0]^p[3];
	k3 = p[2]^p[3];

	p[4] ^= k3;
	p[5] ^= k1;
	p[6] ^= k2;
	p[7] ^= k0;
}

NPUMDIMG_HEADER* forge_npumdimg(int iso_size, int iso_blocks, int block_basis, char *content_id, int np_flags, u8 *version_key, u8 *header_key, u8 *data_key)
{
	// Build NPUMDIMG header.
	NPUMDIMG_HEADER *np_header = (NPUMDIMG_HEADER *) malloc (sizeof(NPUMDIMG_HEADER));
	memset(np_header, 0, sizeof(NPUMDIMG_HEADER));
	
	// Set magic NPUMDIMG.
	np_header->magic[0] = 0x4E;
	np_header->magic[1] = 0x50;
	np_header->magic[2] = 0x55;
	np_header->magic[3] = 0x4D;
	np_header->magic[4] = 0x44;
	np_header->magic[5] = 0x49;
	np_header->magic[6] = 0x4D;
	np_header->magic[7] = 0x47;
	
	// Set flags and block basis.
	np_header->np_flags = np_flags;
	np_header->block_basis = block_basis;
	
	// Set content ID.
	memcpy(np_header->content_id, content_id, strlen(content_id));
	
	// Set inner body parameters.
	np_header->body.sector_size = 0x800;

	if (iso_size > 0x40000000) 
		np_header->body.unk_2 = 0xE001;
	else 
		np_header->body.unk_2 = 0xE000;
	
	np_header->body.unk_4 = 0x0;
	np_header->body.unk_8 = 0x1010;
	np_header->body.unk_12 = 0x0;
	np_header->body.unk_16 = 0x0;
	np_header->body.lba_start = 0x0;
	np_header->body.unk_24 = 0x0;
	
	if(((iso_blocks * block_basis) - 1) > 0x6C0BF)
		np_header->body.nsectors = 0x6C0BF;
	else
		np_header->body.nsectors = (iso_blocks * block_basis) - 1;
		
	np_header->body.unk_32 = 0x0;
	np_header->body.lba_end = (iso_blocks * block_basis) - 1;
	np_header->body.unk_40 = 0x01003FFE;
	np_header->body.block_entry_offset = 0x100;
	
	memcpy(np_header->body.disc_id, content_id + 7, 4);
	np_header->body.disc_id[4] = '-';
	memcpy(np_header->body.disc_id + 5, content_id + 11, 5);
	
	np_header->body.header_start_offset = 0x0;
	np_header->body.unk_68 = 0x0;
	np_header->body.unk_72 = 0x0;
	np_header->body.bbmac_param = 0x0;
	
	np_header->body.unk_74 = 0x0;
	np_header->body.unk_75 = 0x0;
	np_header->body.unk_76 = 0x0;
	np_header->body.unk_80 = 0x0;
	np_header->body.unk_84 = 0x0;
	np_header->body.unk_88 = 0x0;
	np_header->body.unk_92 = 0x0;
	
	// Set keys.
	memset(np_header->header_key, 0, 0x10);
	memset(np_header->data_key, 0, 0x10);
	memset(np_header->header_hash, 0, 0x10);
	memset(np_header->padding, 0, 0x8);
	
	// Copy header and data keys.
	memcpy(np_header->header_key, header_key, 0x10);
	memcpy(np_header->data_key, data_key, 0x10);

	// Generate random padding.
	sceUtilsBufferCopyWithRange(np_header->padding, 0x8, 0, 0, KIRK_CMD_PRNG);
	
	// Prepare buffers to encrypt the NPUMDIMG body.
	MAC_KEY mck;
	CIPHER_KEY bck;
	
	// Encrypt NPUMDIMG body.
	sceDrmBBCipherInit(&bck, 1, 2, np_header->header_key, version_key, 0);
	sceDrmBBCipherUpdate(&bck, (u8 *)(np_header) + 0x40, 0x60);
	sceDrmBBCipherFinal(&bck);
	
	// Generate header hash.
	sceDrmBBMacInit(&mck, 3);
	sceDrmBBMacUpdate(&mck, (u8 *)np_header, 0xC0);
	sceDrmBBMacFinal(&mck, np_header->header_hash, version_key);
	bbmac_build_final2(3, np_header->header_hash);
	
	// Prepare the signature hash input buffer.
	u8 npumdimg_sha1_inbuf[0xD8 + 0x4];
	u8 npumdimg_sha1_outbuf[0x14];
	memset(npumdimg_sha1_inbuf, 0, 0xD8 + 0x4);
	memset(npumdimg_sha1_outbuf, 0, 0x14);
	
	// Set SHA1 data size.
	npumdimg_sha1_inbuf[0] = 0xD8;
	memcpy(npumdimg_sha1_inbuf + 0x4, (u8 *)np_header, 0xD8);
	
	// Hash the input buffer.
	if (sceUtilsBufferCopyWithRange(npumdimg_sha1_outbuf, 0x14, npumdimg_sha1_inbuf, 0xD8 + 0x4, KIRK_CMD_SHA1_HASH) != 0)
	{
		printf("ERROR: Failed to generate SHA1 hash for NPUMDIMG header!\n");
		return NULL;
	}
	
	// Prepare ECDSA signature buffer.
	u8 npumdimg_sign_buf_in[0x34];
	u8 npumdimg_sign_buf_out[0x28];
	memset(npumdimg_sign_buf_in, 0, 0x34);
	memset(npumdimg_sign_buf_out, 0, 0x28);
	
	// Create ECDSA key pair.
	u8 npumdimg_keypair[0x3C];
	memcpy(npumdimg_keypair, npumdimg_private_key, 0x14);
	memcpy(npumdimg_keypair + 0x14, npumdimg_public_key, 0x28);
		
	// Encrypt NPUMDIMG private key.
	u8 npumdimg_private_key_enc[0x20];
	memset(npumdimg_private_key_enc, 0, 0x20);
	encrypt_kirk16_private(npumdimg_private_key_enc, npumdimg_keypair);
	
	// Generate ECDSA signature.
	memcpy(npumdimg_sign_buf_in, npumdimg_private_key_enc, 0x20);
	memcpy(npumdimg_sign_buf_in + 0x20, npumdimg_sha1_outbuf, 0x14);
	if (sceUtilsBufferCopyWithRange(npumdimg_sign_buf_out, 0x28, npumdimg_sign_buf_in, 0x34, KIRK_CMD_ECDSA_SIGN) != 0)
	{
		printf("ERROR: Failed to generate ECDSA signature for NPUMDIMG header!\n");
		return NULL;
	}
	
	// Verify the generated ECDSA signature.
	u8 test_npumdimg_sign[0x64];
	memcpy(test_npumdimg_sign, npumdimg_public_key, 0x28);
    memcpy(test_npumdimg_sign + 0x28, npumdimg_sha1_outbuf, 0x14);
    memcpy(test_npumdimg_sign + 0x3C, npumdimg_sign_buf_out, 0x28);
    if (sceUtilsBufferCopyWithRange(0, 0, test_npumdimg_sign, 0x64, KIRK_CMD_ECDSA_VERIFY) != 0)
	{
		printf("ERROR: ECDSA signature for NPUMDIMG header is invalid!\n");
		return NULL;
	}
	else
		printf("ECDSA signature for NPUMDIMG header is valid!\n");
	
	// Store the signature.
	memcpy(np_header->ecdsa_sig, npumdimg_sign_buf_out, 0x28);
	
	return np_header;
}

void print_usage()
{
	printf("************************************************************\n\n");
	printf("sign_np v1.0.4b - Convert PSP ISOs to signed PSN PBPs.\n");
	printf("                - Written by Hykem (C).\n\n");
	printf("************************************************************\n\n");
	printf("Usage: sign_np -elf <input> <output> <tag>\n");
	printf("\n");
	printf("- Modes:\n");
	printf("[-elf]: Encrypt and sign a ELF file into an EBOOT.BIN\n");
	printf("\n");
	printf("- ELF mode:\n");
	printf("<input>: A valid ELF file\n");
	printf("<output>: Resulting signed EBOOT.BIN file\n");
	printf("<tag>: 00 - EBOOT tag 0x8004FD03  14 - EBOOT tag 0xD91617F0\n");
    printf("       01 - EBOOT tag 0xD91605F0  15 - EBOOT tag 0xD91618F0\n");
    printf("       02 - EBOOT tag 0xD91606F0  16 - EBOOT tag 0xD91619F0\n");
    printf("       03 - EBOOT tag 0xD91608F0  17 - EBOOT tag 0xD9161AF0\n");
    printf("       04 - EBOOT tag 0xD91609F0  18 - EBOOT tag 0xD9161EF0\n");
    printf("       05 - EBOOT tag 0xD9160AF0  19 - EBOOT tag 0xD91620F0\n");
    printf("       06 - EBOOT tag 0xD9160BF0  20 - EBOOT tag 0xD91621F0\n");
    printf("       07 - EBOOT tag 0xD91610F0  21 - EBOOT tag 0xD91622F0\n");
    printf("       08 - EBOOT tag 0xD91611F0  22 - EBOOT tag 0xD91623F0\n");
    printf("       09 - EBOOT tag 0xD91612F0  23 - EBOOT tag 0xD91624F0\n");
    printf("       10 - EBOOT tag 0xD91613F0  24 - EBOOT tag 0xD91628F0\n");
    printf("       11 - EBOOT tag 0xD91614F0  25 - EBOOT tag 0xD91680F0\n");
    printf("       12 - EBOOT tag 0xD91615F0  26 - EBOOT tag 0xD91681F0\n");
    printf("       13 - EBOOT tag 0xD91616F0  27 - EBOOT tag 0xD91690F0\n");
}

int main(int argc, char *argv[])
{
	if ((argc <= 1) || (argc > 9))
	{
		print_usage();
		return 0;
	}
	
	// Keep track of each argument's offset.
	int arg_offset = 0;
	
	// ELF signing mode.
	if (!strcmp(argv[arg_offset + 1], "-elf") && (argc > (arg_offset + 4)))
	{
		// Skip the mode argument.
		arg_offset++;
		
		// Open files.
		char *elf_name = argv[arg_offset + 1];
		char *bin_name = argv[arg_offset + 2];
		int tag = atoi(argv[arg_offset + 3]);
		FILE* elf = fopen(elf_name, "rb");
		FILE* bin = fopen(bin_name, "wb");
		
		// Check input file.
		if (elf == NULL)
		{
			printf("ERROR: Please check your input file!\n");
			fclose(elf);
			fclose(bin);
			return 0;
		}
		
		// Check output file.
		if (bin == NULL)
		{
			printf("ERROR: Please check your output file!\n");
			fclose(elf);
			fclose(bin);
			return 0;
		}
		
		// Check tag.
		if ((tag < 0) || (tag > 27))
		{
			printf("ERROR: Invalid EBOOT tag!\n");
			fclose(elf);
			fclose(bin);
			return 0;
		}
		
		// Get ELF size.
		fseek(elf, 0, SEEK_END);
		int elf_size = ftell(elf);
		fseek(elf, 0, SEEK_SET);
		
		// Initialize KIRK.
		printf("Initializing KIRK engine...\n\n");
		kirk_init();
	
		// Read ELF file.
		u8 *elf_buf = (u8 *) malloc (elf_size);
		fread(elf_buf, elf_size, 1, elf);
		
		// Sign the ELF file.
		u8 *seboot_buf = (u8 *) malloc (elf_size + 4096);
		memset(seboot_buf, 0, elf_size + 4096);
		int seboot_size = sign_eboot(elf_buf, elf_size, tag, seboot_buf);
		
		// Exit in case of error.
		if (seboot_size < 0)
		{
			fclose(elf);
			fclose(bin);
			return 0;
		}
		
		// Write the signed EBOOT.BIN file.
		fwrite(seboot_buf, seboot_size, 1, bin);
		
		// Clean up.
		fclose(bin);
		fclose(elf);
		free(seboot_buf);
		free(elf_buf);
		
		printf("Done!\n");
		
		return 0;
	}
	else
	{
		print_usage();
		return 0;
	}
}
