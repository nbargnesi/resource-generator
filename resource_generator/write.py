# coding: utf-8
#
# As of now, this is just a module to print out the datasets
# in some readable format so the results can be evaluated.
#
# write.py

import namespaces
import equiv
import json

def write_out():
    with open('entrez-namespace.belns', 'w') as fp:
        for key in sorted(namespaces.entrez_ns_dict):
            fp.write('{0}|{1}\n'.format(key, namespaces.entrez_ns_dict[key]))

    with open('hgnc-namespace.belns', 'w') as fp:
        for key in sorted(namespaces.hgnc_ns_dict):
            fp.write('{0}|{1}\n'.format(key, namespaces.hgnc_ns_dict[key]))

    with open('mgi-namespace.belns', 'w') as fp:
        for key in sorted(namespaces.mgi_ns_dict):
            fp.write('{0}|{1}\n'.format(key, namespaces.mgi_ns_dict[key]))

    with open('rgd-namespace.belns', 'w') as fp:
        for key in sorted(namespaces.rgd_ns_dict):
            fp.write('{0}|{1}\n'.format(key, namespaces.rgd_ns_dict[key]))

    with open('swissprot-namespace.belns', 'w') as fp:
        for key in sorted(namespaces.sp_ns_dict):
            fp.write('{0}|{1}\n'.format(key, namespaces.sp_ns_dict[key]))

    with open('swissprot-accessions-namespace.belns', 'w') as fp:
        for key in sorted(namespaces.sp_acc_ns_dict):
            fp.write('{0}|{1}\n'.format(key, namespaces.sp_acc_ns_dict[key]))

    with open('affy-namespace.belns', 'w') as fp:
        for key in sorted(namespaces.affy_ns_dict):
            fp.write('{0}|{1}\n'.format(key, namespaces.affy_ns_dict[key]))

    with open('entrez-uuids.txt', 'w') as fp:
        for key in sorted(equiv.entrez_eq):
            fp.write('{0}|{1}\n'.format(key, equiv.entrez_eq[key]))

    with open('hgnc-uuids.txt', 'w') as fp:
        for key in sorted(equiv.hgnc_eq):
            fp.write('{0}|{1}\n'.format(key, equiv.hgnc_eq[key]))

    with open('rgd-uuids.txt', 'w') as fp:
        for key in sorted(equiv.rgd_eq):
            fp.write('{0}|{1}\n'.format(key, equiv.rgd_eq[key]))

    with open('mgi-uuids.txt', 'w') as fp:
        for key in sorted(equiv.mgi_eq):
            fp.write('{0}|{1}\n'.format(key, equiv.mgi_eq[key]))

    with open('sp-uuids.txt', 'w') as fp:
        for key in sorted(equiv.sp_eq):
            fp.write('{0}|{1}\n'.format(key, equiv.sp_eq[key]))

    with open('sp-accession-uuids.txt', 'w') as fp:
        for key in sorted(equiv.sp_acc_eq):
            fp.write('{0}|{1}\n'.format(key, equiv.sp_acc_eq[key]))

    with open('affy-uuids.txt', 'w') as fp:
        for key in sorted(equiv.affy_eq):
            fp.write('{0}|{1}\n'.format(key, equiv.affy_eq[key]))

    with open('new-hgnc.txt', 'w') as fp:
        for val in equiv.hgnc_list:
            fp.write(val +'\n')

    with open('new-mgi.txt', 'w') as fp:
        for val in equiv.mgi_list:
            fp.write(val +'\n')

    with open('new-rgd.txt', 'w') as fp:
        for val in equiv.rgd_list:
            fp.write(val +'\n')

    with open('new-sp.txt', 'w') as fp:
        for val in equiv.sp_list:
            fp.write(val +'\n')

    print('refseq size: ' +str(len(equiv.refseq)))
    with open('refseq.txt', 'w') as fp:
        for x in equiv.refseq:
            json.dump(x, fp, sort_keys=True, indent=4, separators=(',', ':'))

def changes():
    print('Number of new HGNC uuids: ' +str(len(equiv.hgnc_list)))
    print('Number of new MGI uuids: ' +str(len(equiv.mgi_list)))
    print('Number of new RGD uuids: ' +str(len(equiv.rgd_list)))
    print('Number of new SP uuids: ' +str(len(equiv.sp_list)))
