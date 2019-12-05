import os 

filename = '/tmp/tmpfile'
mode = 600

os.mknod(filename, mode)
filename.write('success')
