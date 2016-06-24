import os.path

class PygModel:
    def __init__(self):
        self.archive_file = None
        self.file_list = list()

    def get_archive_name(self):
        if self.archive_file:
            return os.path.basename(self.archive_file)
