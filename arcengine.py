#!/usr/bin/python3
import tarfile

BZIP2 = 'bz2'
GZIP = 'gz'
LZMA = 'xz'

DEFAULT_COMPRESSION = LZMA

class ArcEngine():
    def __init__(self):
        self.filename = None

    def load_file(self, filename):
        self.filename = filename

    def get_entries(self):
        entries = list()
        if not self.filename:
            return entries

        tar = tarfile.open(self.filename, 'r')

        for tarinfo in tar:
            entries.append(tarinfo)
        tar.close()
        return entries

    def extract_to(self, destination):
        if not self.filename:
            print('No file loaded ArcEngine will not extract anything')
            return

        tar = tarfile.open(self.filename, 'r')
        tar.extractall(path=destination)
        tar.close()

    def compress_files(self, file_list, compression=DEFAULT_COMPRESSION):
        write_mode = 'w:' + compression
        with tarfile.open(self.filename, write_mode) as tar:
            for file_to_add in file_list:
                tar.add(file_to_add)

