"""

"""
import os
from time import gmtime, strftime
import binascii


def crc32_count(path):

    max_file_load = 4096
    BLOCSIZE = 4096    # размер считываемого блока

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


def crc32_function(path, filename=None, ignore=()):
    """

    :param path:
    :param filename:
    :param ignore:
    :return:
    """
    header = ('{0:20} {1:>10} {2:8} {3}', 'Data', 'Size', 'Checksum', 'File name')

    if filename:
        fileTo = open(filename, 'w')
        fileTo.write(header[0].format(header[1], header[2], header[3], header[4]+'\n'))
    else:
        print(header[0].format(header[1], header[2],header[3], header[4]))

    for top, dirs, files in os.walk(path):
        if filename:
            fileTo.write(top+'\n')
        else:
            print(top)

        for file in files:

            if file in ignore:
                continue

            path_to_file = os.path.join(top, file)
            change_time = strftime('%d.%m.%Y %H:%M:%S', gmtime(os.path.getctime(path_to_file)))
            checksum = crc32_count(path_to_file)
            file_size = os.path.getsize(path_to_file)

            if filename:
                fileTo.write('{0:20} {1:10} {2:8x} {3}'.format(change_time, file_size, checksum, file+'\n'))
            else:
                print('{0:20} {1:10} {2:8x} {3}'.format(change_time, file_size, checksum, file))

    if filename:
        fileTo.close()

if __name__ == '__main__':
    path = 'D:\\Test'
    crc32_function(path, 'crc32checksum.txt')