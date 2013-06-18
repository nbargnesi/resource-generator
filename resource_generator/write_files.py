# coding: utf-8
#
# write_files.py

import namespaces
import equiv
import parsers

with open('entrez-namespace.belns', 'w') as fp:
    for key in sorted(entrez_ns_dict):
        #equiv(key, 'entrez')
        fp.write('{0}|{1}\n'.format(key, entrez_ns_dict[key]))

with open('hgnc-namespace.belns', 'w') as fp:
    for key in sorted(hgnc_ns_dict):
        equiv(key, 'hgnc')
        fp.write('{0}|{1}\n'.format(key, hgnc_ns_dict[key]))

with open('mgi-namespace.belns', 'w') as fp:
    for key in sorted(mgi_ns_dict):
        equiv(key, 'mgi')
        fp.write('{0}|{1}\n'.format(key, mgi_ns_dict[key]))

with open('rgd-namespace.belns', 'w') as fp:
    for key in sorted(rgd_ns_dict):
        equiv(key, 'rgd')
        fp.write('{0}|{1}\n'.format(key, rgd_ns_dict[key]))

with open('swissprot-namespace.belns', 'w') as fp:
    for key in sorted(sp_ns_dict):
        fp.write('{0}|{1}\n'.format(key, sp_ns_dict[key]))

with open('swissprot-accessions-namespace.belns', 'w') as fp:
    for key in sorted(sp_acc_ns_dict):
        fp.write('{0}|{1}\n'.format(key, sp_acc_ns_dict[key]))

with open('affy-namespace.belns', 'w') as fp:
    for key in sorted(affy_ns_dict):
        fp.write('{0}|{1}\n'.format(key, affy_ns_dict[key]))

with open('entrez-uuids.txt', 'w') as fp:
    for key in sorted(entrez_eq):
        fp.write('{0}|{1}\n'.format(key, entrez_eq[key]))

with open('hgnc-uuids.txt', 'w') as fp:
    for key in sorted(hgnc_eq):
        fp.write('{0}|{1}\n'.format(key, hgnc_eq[key]))

with open('rgd-uuids.txt', 'w') as fp:
    for key in sorted(rgd_eq):
        fp.write('{0}|{1}\n'.format(key, rgd_eq[key]))

with open('mgi-uuids.txt', 'w') as fp:
    for key in sorted(mgi_eq):
        fp.write('{0}|{1}\n'.format(key, mgi_eq[key]))

with open('sp-uuids.txt', 'w') as fp:
    for key in sorted(sp_eq):
        fp.write('{0}|{1}\n'.format(key, sp_eq[key]))

with open('new-hgnc.txt', 'w') as fp:
    for val in hgnc_list:
        fp.write(val +'\n')

with open('new-mgi.txt', 'w') as fp:
    for val in mgi_list:
        fp.write(val +'\n')

with open('new-rgd.txt', 'w') as fp:
    for val in rgd_list:
        fp.write(val +'\n')

with open('new-sp.txt', 'w') as fp:
    for val in sp_list:
        fp.write(val +'\n')
