# coding: utf-8

'''
 common.py

 Provides common functions used throughout the program.
 Currently these functions relate to the downloading
 and reading in of a file and is used in both gp_baseline
 and change_log.

'''

from ftplib import FTP
from sys import stderr
import gzip
import os
import re
import shutil
import time
import urllib.parse
import urllib.request

def download(url, fileName=None):
	def getFileName(url,openUrl):
		if 'Content-Disposition' in openUrl.info():
			# If the response has Content-Disposition, try to get filename from it
			cd = dict(map(
				lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
				openUrl.info()['Content-Disposition'].split(';')))
			if 'filename' in cd:
				filename = cd['filename'].strip("\"'")
				if filename: return filename
		# if no filename was found above, parse it out of the final URL.
		return os.path.basename(urllib.parse.urlsplit(openUrl.url)[2])

	if url.startswith("ftp://"):
		urltokens = urllib.parse.urlsplit(url)
		ftp = FTP(urltokens.netloc)
		ftp.login()
		moddt = ftp.sendcmd("MDTM " + urltokens.path)
		if fileName is None:
			fileName = os.path.basename(urltokens.path)
		with open(fileName, "wb") as ftpf, open(fileName + ".info", 'w') as info:
			ftp.retrbinary("RETR " + urltokens.path, ftpf.write)
			info.write("URL: " + url + "\n")
			info.write("Filename: " + fileName + "\n")
			info.write("Last modified: " + moddt.split(" ")[1] + "\n")
			info.write("Downloaded at: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
	else:
		with urllib.request.urlopen(url) as r, open(fileName, 'wb') as f, open(fileName + ".info", 'w') as info:
			fileName = fileName or getFileName(url,r)
			shutil.copyfileobj(r,f)
			info.write("URL: " + url + "\n")
			info.write("Filename: " + fileName + "\n")
			if 'Last-Modified' in r.info():
				info.write("Last modified: " + r.info()['Last-Modified'].strip("\"'") + "\n")
			info.write("Downloaded at: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

def gzip_to_text(gzip_file, encoding="ascii"):
	with gzip.open(gzip_file) as gzf:
		for line in gzf:
			yield str(line, encoding)

#
#	Funciton to fetch latest GO archive resource file
#	* used by class GOBPParser and GOCCParser
#
def get_latest_GO_filename(go_file):
	""" Get the name of the current GO termdb.obo-xml.gz file. """
	url = go_file
	if url[-3:] == '.gz':
		url = url[:url.rfind('/')]
	# read the index info of latest-full
	try:
		src = urllib.request.urlopen(url).read().decode("utf-8")
	except:
		print('WARNINIG! [function get_latest_GO_filename] Unable to fetch URL: %s\n' % (url))
		return go_file
	# file matching pattern for resoure filename
	p_fn = re.compile('go_\d+-termdb.obo-xml.gz', re.M|re.S)
	try:
		fn = p_fn.findall(src)[0]
		go_file = '/'.join([url, fn])
	except:
		# unable to locate resoure filename
		print('WARNINIG! [function get_latest_GO_filename] Unable to identify data file in %s\n' % (url))
		pass
	return go_file

p1 = re.compile('Last modified: ?(.*?)[\n|$]', re.M|re.S)
p2 = re.compile('Downloaded at: ?(.*?)[\n|$]', re.M|re.S)
data_file_info = {
	'affy-probeset-ids' : 'affy.xml.info',
	'chebi-ids' : 'chebi.owl.info',
	'chebi-names' : 'chebi.owl.info',
	'disease-ontology-ids' : 'doid.owl.info',
	'disease-ontology-names' : 'doid.owl.info',
	'entrez-gene-ids' : 'entrez_info.gz.info',
	'go-biological-processes-ids' : 'gobp.xml.gz.info',
	'go-biological-processes-names' : 'gobp.xml.gz.info',
	'go-cellular-component-ids' : 'gocc.xml.gz.info',
	'go-cellular-component-names' : 'gocc.xml.gz.info',
	'hgnc-approved-symbols' : 'hgnc.tsv.info',
	'mesh-biological-processes' : 'mesh.bin.info',
	'mesh-cellular-locations' : 'mesh.bin.info',
	'mesh-diseases' : 'mesh.bin.info',
	'mgi-approved-symbols' : 'mgi.rpt.info',
	'rgd-approved-symbols' : 'rgd.txt.info',
	'selventa-legacy-chemical-names' : 'schem.info',
	'selventa-legacy-diseases' : 'sdis.info',
	'selventa-named-complexes' : 'named_complex.info',
	'swissprot-accession-numbers' : 'swiss.xml.gz.info',
	'swissprot-entry-names' : 'swiss.xml.gz.info'
}


def get_citation_info(name, header):
	""" 
	Add Namespace, Citation and Author values
	"""
	header = header.replace('\nCreatedDateTime=[#VALUE#]',
		'\nCreatedDateTime='+time.strftime("%Y-%m-%dT%X"))
	header = header.replace('\nVersionString=[#VALUE#]',
		'\nVersionString='+time.strftime("%Y%m%d"))
	header = header.replace('\nCopyrightString=Copyright (c) [#VALUE#]', 
		'\nCopyrightString=Copyright (c) '+time.strftime("%Y"))

	info_file = data_file_info[name.split('.bel')[0]]
	info_text = open('./datasets/'+info_file).read()
	pubver = 'NA'
	try:
		pubdate = p1.search(info_text).group(1)
	except:
		try:
			pubdate = p2.search(info_text).group(1)
		except:
			pass
	if pubdate:
		if re.match('^\d+$', pubdate):
			tt = time.strptime(pubdate, '%Y%m%d%H%M%S')
			pubdate = time.strftime("%a, %d %b %Y %H:%M:%S", tt)
		pd = pubdate.replace(' GMT', '')
		if re.match('^[A-Za-z]{3}, \d\d [A-Za-z]{3} \d{4} \d\d:\d\d:\d\d$', pd):
			tv = time.strptime(pd,"%a, %d %b %Y %H:%M:%S")
		elif re.match('^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d', pd):
			tv = time.strptime(pd,"%Y-%m-%d %H:%M:%S")
		pubver = time.strftime("%Y_%m_%d", tv)
	else:
		pubdate = 'NA'
		
	header = header.replace('\nPublishedVersionString=[#VALUE#]',
		'\nPublishedVersionString='+pubver)
	header = header.replace('\nPublishedDate=[#VALUE#]',
		'\nPublishedDate='+pubdate)
	
	print('...%s : %s -- %s' % (name, pubdate, pubver))

	return header
