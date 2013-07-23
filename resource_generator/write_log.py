# coding: utf-8
#
# write_log.py

import json

def write(change_log):

    with open('change_log.json', 'w') as fp:
        for entry in change_log:
            json.dump(entry, fp, sort_keys=True, indent=4, separators=(',', ':'))
