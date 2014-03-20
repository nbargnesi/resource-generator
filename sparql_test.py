#!/usr/bin/env python3
# -*- coding: utf8 -*-
# vim: ts=4 sw=4:
from json import dumps
from urllib.error import HTTPError
from SPARQLWrapper import SPARQLWrapper, GET, JSON


def query(query, endpoint):
	sparql = SPARQLWrapper(endpoint)
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	sparql.setMethod(GET)

	try:
		result = sparql.query()
		return result.convert()
	except HTTPError as e:
		print(str(e))

if __name__ == '__main__':
	import sys

	if len(sys.argv) != 2:
		sys.stderr.write('usage: sparql_test.py [SPARQL_ENDPOINT_URL]\n')
		sys.exit(1)

	endpoint_url = sys.argv[1]
	EXACT_MATCH_ORPHANS = """
	prefix skos: <http://www.w3.org/2004/02/skos/core#>
	select (count(distinct ?uri2) as ?count)
	where {
	  ?uri1 skos:exactMatch ?uri2 .
	  minus { ?uri2 skos:inScheme ?scheme .}
	}
	"""
	ORTHOLOGOUS_MATCH_ORPHANS = """
	prefix skos: <http://www.w3.org/2004/02/skos/core#>
	prefix belv: <http://www.openbel.org/vocabulary/>
	select (count(distinct ?uri2) as ?count)
	where {
	  ?uri1 belv:orthologousMatch ?uri2 .
	  minus { ?uri2 skos:inScheme ?scheme .}
	}
	"""
	ID_CONFLICTS = """
	prefix skos: <http://www.w3.org/2004/02/skos/core#>
	prefix dc: <http://purl.org/dc/terms/>
	select (count(distinct ?uri2) as ?count)
	where {
	?uri1 dc:identifier ?id1 .
	?uri2 dc:identifier ?id1 .
	?uri1 skos:inScheme ?scheme .
	?uri2 skos:inScheme ?scheme .
	FILTER (?uri1 != ?uri2) .
	}
	""" 	
	PREFLABEL_CONFLICTS = """
	prefix skos: <http://www.w3.org/2004/02/skos/core#>
	prefix dc: <http://purl.org/dc/terms/>
	select(count(distinct ?uri2) as ?count)
	where {
	?uri1 skos:prefLabel ?label .
	?uri2 skos:prefLabel ?label .
	?uri1 skos:inScheme ?scheme .
	?uri2 skos:inScheme ?scheme .
	FILTER (?uri1 != ?uri2) .
	}
	"""	 
	print("Orphans for exactMatch:")
	print(dumps(query(EXACT_MATCH_ORPHANS, endpoint_url), indent=4))

	print("Orphans for orthologousMatch:")
	print(dumps(query(ORTHOLOGOUS_MATCH_ORPHANS, endpoint_url), indent=4))

	print("ID conflicts:")
	print(dumps(query(ID_CONFLICTS, endpoint_url), indent=4))

	print("prefLabel conflicts:")
	print(dumps(query(PREFLABEL_CONFLICTS, endpoint_url), indent=4))
