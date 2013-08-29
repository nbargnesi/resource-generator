# coding: utf-8

'''
 write_log.py

 A simple module to write the contents of the change-log
 to a human-readable file in json format.

'''

import json

def write(change_log):

    with open('change_log.json', 'w') as fp:
        json.dump(change_log, fp, sort_keys=True, indent=4, separators=(', ', ':'))
