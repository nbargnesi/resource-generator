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
from lxml import etree
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

def get_latest_GO_filename(go_file):
	""" Get the name of the current GO termdb.obo-xml.gz file. """
	url = go_file
	if url[-3:] == '.gz':
		url = url[:url.rfind('/')]
	# read the index info of latest-full
	try:
		src = urllib.request.urlopen(url).read().decode("utf-8")
	except:
		print('WARNING! [function get_latest_GO_filename] Unable to fetch URL: %s\n' % (url))
		return go_file
	# file matching pattern for resoure filename
	p_fn = re.compile('go_\d+-termdb.obo-xml.gz', re.M|re.S)
	try:
		fn = p_fn.findall(src)[0]
		go_file = '/'.join([url, fn])
	except:
		# unable to locate resoure filename
		print('WARNING! [function get_latest_GO_filename] Unable to identify data file in %s\n' % (url))
		pass
	return go_file

def get_latest_MeSH_filename(url, prefix, suffix):
	""" Get the URL of the current MeSH file, given the directory url and file prefix.
	For example, the ASCII MeSH Descriptors file will start with prefix 'd' and be found in 
	ftp://nlmpubs.nlm.nih.gov/online/mesh/.asciimesh/. """
	try:
		directory = urllib.request.urlopen(url)
	except:
		print('WARNING! unable to fetch URL: {0}'.format(url))
	filenames = []
	for line in directory:
		line=line.decode('cp1252')
		filenames.append(line.split()[-1])
	filenames = sorted( [filename for filename in filenames if (filename.startswith(prefix) and filename.endswith(suffix))] )
	current_file = '/'.join([url,filenames[-1]])
	return current_file
	
p1 = re.compile('Last modified: ?(.*?)[\n|$]', re.M|re.S)
p2 = re.compile('Downloaded at: ?(.*?)[\n|$]', re.M|re.S)
p3 = re.compile('Filename: ?(.*?)[\n|$]', re.M|re.S)
p4 = re.compile('URL: ?(.*?)[\n|$]', re.M|re.S)

p_chebi_1 = re.compile('\<owl:versionIRI .*?\>(\d+)\<\/owl:versionIRI\>')
p_chebi_2 = re.compile('\<dc:date .*?>(\d\d\d\d-\d\d-\d\d).*?\<\/dc:date\>')
p_do_1 = re.compile('\<oboInOwl:date .*?>(\d\d:\d\d:\d\d\d\d).*?\<\/oboInOwl:date\>')

p_go_1 = re.compile('\<data-version\>.*?(\d\d\d\d-\d\d-\d\d)\<\/data-version\>')
p_go_2 = re.compile('\<date\>(\d\d:\d\d:\d\d\d\d).*?\<\/date\>')

p_rgd_1 = re.compile('# GENERATED-ON: (\d\d\d\d\/\d\d\/\d\d)')

def get_citation_info(name, header, data_file):
	""" 
	Add Namespace, Citation and Author values
	
	+ affy: (datasets/affy.xml) 
		
	+ chebi: (datasets/chebi.owl)
		<owl:versionIRI rdf:datatype="http://www.w3.org/2001/XMLSchema#string">109</owl:versionIRI>
		<dc:date rdf:datatype="http://www.w3.org/2001/XMLSchema#string">2013-11-01 17:17</dc:date>
	+ do: (datasets/doid.owl)
		<oboInOwl:date rdf:datatype="http://www.w3.org/2001/XMLSchema#string">05:11:2013 12:57</oboInOwl:date>
	+ go: (datasets/gobp.xml.gz)
		<data-version>2013-09-28</data-version>
		<date>27:09:2013 10:57</date>
	mesh: ?
		
	+ rgd: (datasets/rgd.txt)
		# GENERATED-ON: 2013/11/01
	"""
	from configuration import data_file_info
	header = header.replace('\nCreatedDateTime=[#VALUE#]',
		'\nCreatedDateTime='+time.strftime("%Y-%m-%dT%X"))
	header = header.replace('\nVersionString=[#VALUE#]',
		'\nVersionString='+time.strftime("%Y%m%d"))
	header = header.replace('\nCopyrightString=Copyright (c) [#VALUE#]', 
		'\nCopyrightString=Copyright (c) '+time.strftime("%Y"))

	new_data_file = data_file_info.get(name)
	if new_data_file:
		data_file = new_data_file  
	info_file = data_file + '.info'
	info_text = open('./datasets/'+info_file).read()
#	try:
#		data_file = p3.search(info_text).group(1)
#	except:
#		data_file = None
	pubver = 'NA'	
	if data_file.find('chebi') >= 0:
		f = open('./datasets/'+data_file, 'r')
		while 1:
			line = f.readline().strip()
			if not line: break
			if line.find('owl:versionIRI') > 0:
				pubver = p_chebi_1.search(line).group(1)
			elif line.find('dc:date') > 0:
				pubdate = p_chebi_2.search(line).group(1)
				break
		f.close()
	
	elif data_file.find('doid') >= 0:
		f = open('./datasets/'+data_file, 'r')
		while 1:
			line = f.readline().strip()
			if not line: break
			if line.find('oboInOwl:date') > 0:
				pubdate = p_do_1.search(line).group(1)
				d,m,y = pubdate.split(':')
				pubdate = '-'.join([y,m,d])
				pubver = pubdate
				break
		f.close()
	
	elif data_file.find('go') >= 0 and data_file:
		f = gzip.open('./datasets/'+data_file, 'r')
		while 1:
			line = f.readline().strip()
			if not line: break
			line = str(line, 'utf-8')
			if line.find('<data-version>') >= 0:
				pubver = p_go_1.search(line).group(1)
			elif line.find('<date>') >= 0:
				pubdate = p_go_2.search(line).group(1)
				d,m,y = pubdate.split(':')
				pubdate = '-'.join([y,m,d])
				break
		f.close()
	
	elif data_file.find('rgd') >= 0:
		f = open('./datasets/'+data_file, 'r')
		while 1:
			line = f.readline().strip()
			if not line: break
			if line.find('# GENERATED-ON') >= 0:
				pubdate = p_rgd_1.search(line).group(1)
				pubdate = pubdate.replace('/','-')
				pubver = pubdate
				break
		f.close()
	
	elif data_file.find('affy') >= 0:
		f = etree.iterparse('./datasets/'+data_file)
		for action, elem in f:
			# mapping version and date to HG-U133_Plus_2 Array
			if elem.tag == 'Array' and elem.get('name') == 'HG-U133_Plus_2':
				for n in elem.findall('Annotation'):
					if n.get('type') == 'Annot CSV':
						# date format e.g., "Oct 30, 2012"
						annofile = n.find('File')
						date = annofile.get('date')
						tv = time.strptime(date, "%b %d, %Y")
						pubdate = time.strftime("%Y-%m-%d", tv)
						pubver = annofile.get('name').split('.')[1]
				break
	elif data_file.find('mesh') >= 0:
		# get MeSH version from info file download URL, pubdate from last modified date
		pubver = p4.search(info_text).group(1)
		pubver = pubver.split('/')[-1]
		pubver = pubver.lstrip('d').rstrip('.bin')
		pubdate = p1.search(info_text).group(1)
		if re.match('^\d+$', pubdate):
			tt = time.strptime(pubdate, '%Y%m%d%H%M%S')
			pubdate = time.strftime("%Y-%m-%d", tt)
	else:
	
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
				#pubdate = time.strftime("%a, %d %b %Y %H:%M:%S", tt)
				pubdate = time.strftime("%a, %d %b %Y %H:%M:%S", tt)
			pubdate = pubdate.replace(' GMT', '')
			if re.match('^[A-Za-z]{3}, \d\d [A-Za-z]{3} \d{4} \d\d:\d\d:\d\d$', pubdate):
				tv = time.strptime(pubdate,"%a, %d %b %Y %H:%M:%S")
			elif re.match('^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d', pubdate):
				tv = time.strptime(pubdate,"%Y-%m-%d %H:%M:%S")
			pubver = time.strftime("%a, %d %b %Y %H:%M:%S", tv)
			pubdate = time.strftime("%Y-%m-%d", tv)
		else:
			pubdate = 'NA'
		
	header = header.replace('\nPublishedVersionString=[#VALUE#]',
		'\nPublishedVersionString='+pubver)
	header = header.replace('\nPublishedDate=[#VALUE#]',
		'\nPublishedDate='+pubdate)
	
	print('...%s : %s -- %s' % (name, pubdate, pubver))

	return header
# vim: ts=4 sts=4 sw=4 noexpandtab
# vim: ts=4 sts=4 sw=4 noexpandtab
