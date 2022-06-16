import struct

## read in test binary
binary = open("C:/Users/camer/Desktop/xcat_full_body.out_act_1.bin", 'rb')
out = open("binary.out", 'w')
binary.seek(0,2) ## seeks to the end of the file (needed for getting number of bytes)
num_bytes = binary.tell() ## how many bytes are in this file is stored as num_bytes
# print num_bytes
binary.seek(0) ## seeks back to beginning of file
i = 0 ## index of bytes we are on
while i < num_bytes:
    binary_data = binary.read(4) ## reads in 4 bytes = 8 hex characters = 32-bits
    i += 4 ## we seeked ahead 4 bytes by reading them, so now increment index i
    unpacked = struct.unpack("<f", binary_data) ## <f denotes little endian float encoding
    out.write(str(unpacked) + "\n")

binary.close()
out.close()