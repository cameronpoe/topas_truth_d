import struct

## read in test binary
binary = open("C:/Users/camer/frisch-research/xcat/xcat_final_7.5.22.out_act_1.bin", 'rb')
out = open("binary.out", 'w')
binary.seek(0,2) ## seeks to the end of the file (needed for getting number of bytes)
num_bytes = binary.tell() ## how many bytes are in this file is stored as num_bytes
# print num_bytes
binary.seek(0) ## seeks back to beginning of file

tissues_dict = {}
total_voxels = 0

i = 0 ## index of bytes we are on
while i < num_bytes:
    binary_data = binary.read(4) ## reads in 4 bytes = 8 hex characters = 32-bits
    i += 4 ## we seeked ahead 4 bytes by reading them, so now increment index i
    activity = struct.unpack("<f", binary_data)[0] ## <f denotes little endian float encoding

    if not activity in tissues_dict:
        tissues_dict[activity] = 1
        total_voxels += 1
    else:
        tissues_dict[activity] += 1
        total_voxels += 1

for key, value in sorted(tissues_dict.items()):
    out.write(str(key) + ': ' + str(value) + '\n')
out.write('Total voxels: %s'%str(total_voxels))

binary.close()
out.close()