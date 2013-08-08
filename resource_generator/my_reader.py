# coding: utf-8
#
# my_reader.py

import ipdb

class MyReader:
    def __init__(self, filename, columns):
        self.file = filename
        self.columns = columns
        self.isopen = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.isopen:
            ipdb.set_trace()
            yield self.fp.readline()
        else:
            self.isopen = True
            ipdb.set_trace()
            self.fp = open(self.file, 'r')
            yield self.fp.readline()

    def __str__(self):
        return 'Reader Object'
