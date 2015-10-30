#!/usr/bin/env python3
# coding: utf-8
'''
Executes queries against the configured SPARQL endpoint and exits when no
input is received.
'''
import os
import sys
import rdflib as rl
from datetime import datetime as dt


def main():
    ###################################
    # BEGIN sanity checking environment
    url = os.getenv('RG_RDF_SPARQL_URL')
    if url is None:
        print('no RG_RDF_SPARQL_URL is set')
        sys.exit(1)
    if not url.endswith('/'):
        url += '/'
    # END sanity checking environment
    #################################

    NSs = {}
    NSs['affx'] = 'http://www.openbel.org/bel/namespace/affy-probeset/'
    NSs['belv'] = 'http://www.openbel.org/vocabulary/'
    NSs['chebi'] = 'http://www.openbel.org/bel/namespace/chebi/'
    NSs['cl'] = 'http://www.openbel.org/bel/namespace/cell-ontology/'
    NSs['clo'] = 'http://www.openbel.org/bel/namespace/cell-line-ontology/'
    NSs['dcterms'] = 'http://purl.org/dc/terms/'
    NSs['do'] = 'http://www.openbel.org/bel/namespace/disease-ontology/'
    NSs['efo'] = 'http://www.openbel.org/bel/namespace/experimental-factor-ontology/'
    NSs['egid'] = 'http://www.openbel.org/bel/namespace/entrez-gene/'
    NSs['gobp'] = 'http://www.openbel.org/bel/namespace/go-biological-process/'
    NSs['gocc'] = 'http://www.openbel.org/bel/namespace/go-cellular-component/'
    NSs['hgnc'] = 'http://www.openbel.org/bel/namespace/hgnc-human-genes/'
    NSs['mesha'] = 'http://www.openbel.org/bel/namespace/mesh-anatomy/'
    NSs['meshc'] = 'http://www.openbel.org/bel/namespace/mesh-chemicals/'
    NSs['meshcs'] = 'http://www.openbel.org/bel/namespace/mesh-cellular-structures/'
    NSs['meshd'] = 'http://www.openbel.org/bel/namespace/mesh-diseases/'
    NSs['meshpp'] = 'http://www.openbel.org/bel/namespace/mesh-processes/'
    NSs['mgi'] = 'http://www.openbel.org/bel/namespace/mgi-mouse-genes/'
    NSs['rdf'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    NSs['rdfs'] = 'http://www.w3.org/2000/01/rdf-schema#'
    NSs['rgd'] = 'http://www.openbel.org/bel/namespace/rgd-rat-genes/'
    NSs['schem'] = 'http://www.openbel.org/bel/namespace/selventa-legacy-chemicals/'
    NSs['scomp'] = 'http://www.openbel.org/bel/namespace/selventa-named-complexes/'
    NSs['sdis'] = 'http://www.openbel.org/bel/namespace/selventa-legacy-diseases/'
    NSs['sfam'] = 'http://www.openbel.org/bel/namespace/selventa-protein-families/'
    NSs['skos'] = 'http://www.w3.org/2004/02/skos/core#'
    NSs['sp'] = 'http://www.openbel.org/bel/namespace/swissprot/'
    NSs['taxon'] = 'http://www.openbel.org/bel/namespace/ncbi-taxonomy/'
    NSs['uberon'] = 'http://www.openbel.org/bel/namespace/uberon/'
    NSs['xml'] = 'http://www.w3.org/XML/1998/namespace'
    NSs['xsd'] = 'http://www.w3.org/2001/XMLSchema#'

    g = rl.ConjunctiveGraph('SPARQLStore')
    url = url + 'query'
    g.open(url)

    def do_query(query):
        t0 = dt.now()
        try:
            results = [x for x in g.query(query, initNs=NSs)]
            t1 = dt.now()
            for x in results:
                print(x)
            print('(query time: %s seconds)' % (round((t1 - t0).total_seconds(), 2)))
        except Exception as e:
            print(e)

    def ql():
        print('Starting query loop, [ENTER] to exit.')
        try:
            response = input('query> ')
            while response != '':
                do_query(response)
                response = input('query> ')
        except EOFError:
            print('\nGot EOF, exiting...')
            return
        except KeyboardInterrupt:
            print('\nInterrupted, exiting...')
            return

    ql()


if __name__ == '__main__':
    main()
    sys.exit(0)
