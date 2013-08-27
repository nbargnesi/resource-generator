# coding: utf-8
#
# write_log.py

import json

def write(change_log):

    with open('change_log.txt', 'w') as fp:
        for entry in change_log:
            json.dump(entry, fp, sort_keys=True, indent=2, separators=(', ', ':'))
