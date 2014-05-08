#!/usr/bin/env python3.3
from string import Template

def bel_term(value,ns,f):
	""" Create bel term given value, namespace id, 
	and bel function string. """
	must_quote_values = ['a','SET']
	must_quote_chars = [':', '(', ')', '<', '>', '.', '-', '/', '@', ' ']
	if any(char in value for char in must_quote_chars) or value in must_quote_values:
		s = Template('${f}(${ns}:"${value}")')
	else:
		s = Template('${f}(${ns}:${value})')
	term = s.substitute(f=f, ns=ns, value=value)
	return term
# vim: ts=4 sts=4 sw=4 noexpandtab
