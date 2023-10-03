import os, sys


def cur_dir():
	return '%cd%' if sys.platform in ['win32', 'cygwin'] else '`pwd`'


def extract_file_from_zip(local_zipfile, extractedfile):
	import zipfile

	if not os.path.exists(extractedfile):
		cur_folder = os.path.abspath(os.curdir)
		with zipfile.ZipFile(local_zipfile,"r") as zip_ref:
			zip_ref.extractall(cur_folder)
		os.remove(local_zipfile)

	return extractedfile if os.path.exists(extractedfile) else None

def extract_ova_from_zip(local_zipfile):
	if False:
		import zipfile

		ovafile = os.path.basename(local_zipfile).replace('.zip','.ova')
		if not os.path.exists(ovafile):
			cur_folder = os.path.abspath(os.curdir)
			with zipfile.ZipFile(local_zipfile,"r") as zip_ref:
				zip_ref.extractall(cur_folder)
			os.remove(local_zipfile)

		return ovafile if os.path.exists(ovafile) else None
	else:
		return extract_file_from_zip(local_zipfile, os.path.basename(local_zipfile).replace('.zip','.ova'))

def open_port():
	"""
	https://gist.github.com/jdavis/4040223
	"""

	import socket

	sock = socket.socket()
	sock.bind(('', 0))
	x, port = sock.getsockname()
	sock.close()

	return port

def checkPort(port):
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = bool(sock.connect_ex(('127.0.0.1', int(port))))
	sock.close()
	return result

def getPort(ports=[], prefix="-p",dup=True):
	if ports is None or ports == []:
		return ''
	if not isinstance(ports, list):
		ports = [ports]
	if prefix is None:
		prefix = ''

	ports = [port for port in ports if port != None and str(port).strip() != '']

	if dup:
		return ' '.join([
			f"{prefix} {port if checkPort(port) else open_port()}:{port}" for port in ports
		])
	else: #Created a flag to support the direct usage of the port instead of linking it to the original port
		return ' '.join([
			f"{prefix} {port if checkPort(port) else open_port()}" for port in ports
		])
