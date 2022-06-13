# this is a helper file to the full_body_topas_creator.py file that finds all tissues associated with activity ratios from the xcat phantom

# specifies the .topas parameter file we will be writing to
f1 = open('tissues_list.txt', 'w')

# what xcat log metadata file we will be reading
f2 = open('xcat_full_body.out_log', 'r')
# inputs each line in the log file as an element of a list
lines = f2.readlines()

# writes a line for each tissue giving it 
for line in lines:
	if line != None:
		if '_act ' in line or '_activity ' in line or 'Air ' in line:
			if 'Air ' in line:
				pass
			elif 'left ' in line:
				f1.write('XCAT_left_' + line.split('=')[0].strip().split('left')[1].strip() + ' = -1\n')
			elif 'left_' in line:
				f1.write('XCAT_left' + line.split('=')[0].strip().split('left')[1].strip() + ' = -1\n')
			elif 'right ' in line:
				f1.write('XCAT_right_' + line.split('=')[0].strip().split('right')[1].strip() + ' = -1\n')
			elif 'right_' in line:
				f1.write('XCAT_right' + line.split('=')[0].strip().split('right')[1].strip() + ' = -1\n')
			else:
				f1.write('XCAT_' + line.split('=')[0].strip()+' = -1\n') 

# closes out of the two files to read/write
f1.close()
f2.close()
