"""

"""
import os
from time import gmtime, strftime
import zlib
import binascii


def crc32_count(path):

    max_file_load = 4096
    BLOCSIZE = 4096

    if os.path.getsize(path) <= max_file_load:
        file = open(path, 'rb').read()
        crc32 = binascii.crc32(file)
        return crc32 & 0xffffffff
    else:
        file = open(path, 'rb')
        crc32 = 0
        while True:
            data = file.read(BLOCSIZE)
            if not data: break
            crc32 = binascii.crc32(data, crc32)
        return crc32 & 0xffffffff


def crc32_count_old(path):
    data = open(path, 'rb').read()
    crc32 = zlib.crc32(data)
    return crc32


def crc32_function(path, filename=None):
    """

    :param path:
    :param filename:
    :return:
    """
    if not filename:
        print('{0:20} {1:>10} {2:8} {3}'.format('Data', 'Size', 'Checksum', 'File name'))
    else:
        fileTo = open(filename, '')
    for top, dirs, files in os.walk(path):
        if not filename: print(top)
        for file in files:
            path_to_file = os.path.join(top, file)
            change_time = strftime('%d.%m.%Y %H:%M:%S', gmtime(os.path.getctime(path_to_file)))
            checksum = crc32_count(path_to_file)
            file_size = os.path.getsize(path_to_file)
            if not filename:
                print('{0:20} {1:10} {2:8x} {3}'.format(change_time, file_size, checksum, file))

if __name__ == '__main__':
    path = 'D:\\Test'
    crc32_function(path)