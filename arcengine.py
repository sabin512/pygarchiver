import tarfile

BZIP2 = 'bz2'
GZIP = 'gz'
LZMA = 'xz'

DEFAULT_COMPRESSION = LZMA

def get_entries(filename):
    entries = list()
    tar = tarfile.open(filename, 'r')

    for tarinfo in tar:
        entries.append(tarinfo)
    tar.close()
    return entries

def extract_to(filename, destination):
    tar = tarfile.open(filename, 'r')
    tar.extractall(path=destination)
    tar.close()

def compress_files(filename,
                   file_list,
                   compression=DEFAULT_COMPRESSION):
    write_mode = 'w:' + compression
    with tarfile.open(filename, write_mode) as tar:
        for file_to_add in file_list:
            tar.add(file_to_add)

