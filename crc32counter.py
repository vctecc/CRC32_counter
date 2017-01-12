import os
from time import gmtime, strftime
import zlib
import binascii


def crc32_count1(path):
    max_file_load = 4096
    blocksize = 4096

    if os.path.getsize(path) <= max_file_load:
        file = open(path, 'rb').read()
        crc32 = binascii.crc32(file)
        return crc32 & 0xffffffff
    else:
        file = open(path, 'rb')
        crc32 = 0
        while True:
            data = file.read(blocksize)
            if not data: break
            crc32 = binascii.crc32(data, crc32)
        return crc32 & 0xffffffff



def crc32_count(path):
    data = open(path, 'rb').read()
    crc32 = zlib.crc32(data)
    return crc32


def crc32_function():
    None

if __name__ == '__main__':
    print('{0:20} {1:>10} {2:8} {3}'.format('Data', 'Size', 'Checksum', 'File name'))
    for top, dirs, files in os.walk('D:\\Test'):
        print(top)
        for file in files:
            path = os.path.join(top, file)
            change_time = strftime('%d.%m.%Y %H:%M:%S', gmtime(os.path.getctime(path)))
            checksum = crc32_count(path)
            file_size = os.path.getsize(path)
            print('{0:20} {1:10} {2:8x} {3}'.format(change_time, file_size, checksum, file))
