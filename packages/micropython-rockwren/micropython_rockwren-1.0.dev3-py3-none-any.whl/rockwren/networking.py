'\nNetwork connectivity methods\n'
_C='Exception saving network config: '
_B=False
_A=None
import io,sys
from socket import socket
from time import sleep
import machine,network
from micropython import const
from.import env
from.import jsondb
from.import secrets
from.import utils
from phew import logging
FIRST_BOOT_KEY='first_boot'
SSID_KEY='ssid'
PASSWORD_KEY='password'
ENV_FILE='env.json'
def connect(hostname='rockwren'):
	'\n    Establish WiFi Network Connection\n    ';network.hostname(hostname);A=network.WLAN(network.STA_IF);A.active(True);A.connect(env.SSID,secrets.SSID_PASSWORD);B=0
	while not A.isconnected():
		logging.info('Waiting for connection...');logging.info(A.status());sleep(1)
		if env.FIRST_BOOT:
			if B>=10:reset_network_config();machine.reset()
			B+=1
	clear_first_boot();C,D,E,F=A.ifconfig();logging.info(f"Connected on {C}");return{'wlan':A,'ip_address':C,'subnet_mask':D,'gateway':E,'dns_server':F}
def open_socket(ip_address,port):'\n    Open a socket for an ip address and port\n    :param ip_address: IP Address\n    :return: connection\n    ';B=ip_address,port;A=socket.socket();A.bind(B);A.listen(1);logging.info(A);return A
def reset_network_config():' Reset network configuration.\n        Removes ssid and ssid password and resets first boot.  Rockwren will reenter access point mode on reboot after\n        calling this method. ';A=jsondb.JsonDB(ENV_FILE);A[FIRST_BOOT_KEY]=_B;A[SSID_KEY]='';A[PASSWORD_KEY]='';A.save();env.FIRST_BOOT=A[FIRST_BOOT_KEY];env.SSID=A[SSID_KEY];secrets.SSID_PASSWORD=A[PASSWORD_KEY]
def load_network_config():
	' Load network configuration from the json db file'
	try:
		A=jsondb.JsonDB(ENV_FILE);A.load()
		if A.get(FIRST_BOOT_KEY)is _A:A[FIRST_BOOT_KEY]=_B
		if A.get(SSID_KEY)is _A:A[SSID_KEY]=''
		if A.get(PASSWORD_KEY)is _A:A[PASSWORD_KEY]=''
		A.save();env.FIRST_BOOT=A[FIRST_BOOT_KEY];env.SSID=A[SSID_KEY];secrets.SSID_PASSWORD=A[PASSWORD_KEY]
		try:env.MQTT_SERVER=A['mqtt_server']
		except Exception:logging.info('mqtt_server not set using default')
		try:env.MQTT_PORT=A['mqtt_port']
		except Exception:logging.info('mqtt_port not set using default')
		try:env.MQTT_CLIENT_CERT=A['mqtt_client_cert']
		except Exception:logging.info('mqtt_client_cert not set using default')
		try:env.MQTT_CLIENT_KEY=A['mqtt_client_key']
		except Exception:logging.info('mqtt_client_key not set using default')
	except Exception as C:logging.error('Exception loading network config: ');B=io.StringIO();sys.print_exception(C,B);utils.logstream(B)
def save_network_config(ssid,password):
	' Save network configuration to the json db file'
	try:A=jsondb.JsonDB(ENV_FILE);A[FIRST_BOOT_KEY]=True;A[SSID_KEY]=ssid;A[PASSWORD_KEY]=password;A.save()
	except Exception as C:logging.error(_C);B=io.StringIO();sys.print_exception(C,B);utils.logstream(B)
def save_network_config_key(key,value):
	'\n    Save a network configuration key/value pair to the json db file.\n    :param key: network config key\n    :param value: network config value\n    '
	try:A=jsondb.JsonDB(ENV_FILE);A.load();A[key]=value;A.save()
	except Exception as C:logging.error(_C);B=io.StringIO();sys.print_exception(C,B);utils.logstream(B)
def clear_first_boot():' Clear first boot setting the save in json db ';A=jsondb.JsonDB(ENV_FILE);A.load();A[FIRST_BOOT_KEY]=_B;A.save()
def first_boot_present():' :returns True if first boot present otherwise False ';A=jsondb.JsonDB(ENV_FILE);A.load();B=A.get(FIRST_BOOT_KEY)is not _A and A[FIRST_BOOT_KEY];A.save();return B
def scan_networks(net):
	' Scan for WiFI networks. ';A=net.scan();A.sort(key=lambda x:x[3],reverse=True);B=[]
	for C in A:B.append((C[0].decode(),C[3]))
	return B