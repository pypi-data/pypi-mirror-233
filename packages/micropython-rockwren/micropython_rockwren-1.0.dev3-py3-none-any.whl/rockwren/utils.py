import io,re,ubinascii
from phew import logging
def is_fqdn(hostname):
	'\n    Check that the hostname is a fully qualified domain name\n    :param hostname: hostname to check\n    :return: True if an FQDN otherwise False\n    ';A=hostname
	if not 1<len(A)<253:return False
	if A[-1]=='.':A=A[0:-1]
	B=A.lower().split('.');C=re.compile('^[a-z0-9]([a-z-0-9-]*[a-z0-9])?$');return all(C.match(A)for A in B)
def pem_to_der(pem):'\n    Convert a PEM formatted certificate or key and encode as DER (base64)\n    :param pem: PEM formatted key or certificate\n    :return:\n    ';A=pem;A=''.join(A.split('\n')[1:-2]);B=ubinascii.a2b_base64(A);return B
def logstream(stream):
	' Log stream line by line to avoid allocating a large chunk of memory';B=stream;B.seek(0);A=B.readline();logging.error(A)
	while A:A=B.readline();logging.error(A)