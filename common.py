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
                info.write("Last modified: " + r.info()['Last-Modified'].strip("\"'"))
            info.write("Downloaded at: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

def gzip_to_text(gzip_file, encoding="ascii"):
    with gzip.open(gzip_file) as gzf:
        for line in gzf:
            yield str(line, encoding)

#
#   Funciton to fetch latest GO archive resource file
#   * used by class GOBPParser and GOCCParser
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
		sys.stderr.write('WARNINIG! [function get_latest_GO_filename] Unable to fetch URL: %s\n' % (url))
		return go_file
	# file matching pattern for resoure filename
	p_fn = re.compile('go_\d+-termdb.obo-xml.gz', re.M|re.S)
	try:
		fn = p_fn.findall(src)[0]
		go_file = '/'.join([url, fn])
	except:
		# unable to locate resoure filename
		pass
	return go_file
