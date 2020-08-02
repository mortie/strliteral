#include <stdio.h>

extern const unsigned char data[];
extern const unsigned int data_len;

int main(int argc, char **argv) {
	if (argc != 2) {
		printf("Usage: %s <path>\n", argv[0]);
		return 1;
	}

	FILE *f = fopen(argv[1], "rb");
	if (f == NULL) {
		perror(argv[1]);
		return 1;
	}

	int c;
	unsigned int i = 0;
	while ((c = fgetc(f)) != EOF) {
		if (i >= data_len) {
			fprintf(stderr, "File is bigger than embedded data!\n");
			fclose(f);
			return 1;
		}

		if ((unsigned char)c != data[i]) {
			fprintf(stderr, "Mismatch: Byte %i: Embedded was %02x, file was %02x\n",
					i, data[i], c);
			fclose(f);
			return 1;
		}

		i += 1;
	}

	if (i != data_len) {
		fprintf(stderr, "File length mismatch: Embedded data is %i bytes, file is %i\n",
				data_len, i);
		fclose(f);
		return 1;
	}

	fprintf(stderr, "OK.\n");
	fclose(f);
	return 0;
}
