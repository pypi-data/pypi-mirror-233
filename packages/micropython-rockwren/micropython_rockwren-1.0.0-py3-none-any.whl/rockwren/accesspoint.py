' Access Point for Device WiFi setup. '
_C='/favicon.svg'
_B='/restart'
_A=None
import io,os,sys,machine,network,uasyncio
from micropython import const
from phew import logging
from phew import server
from phew import template
from.import networking
from.import utils
try:import usocket as socket
except Exception:import socket
ap=_A
accesspointapp=server.Phew()
dir_path='/lib/rockwren'
STATUS_CODE_404=const(404)
@accesspointapp.route('/',methods=['GET','POST'])
def wifi_setup(request):
	B=request;A=_A
	if B.method=='POST':
		' WiFI Setup handle post. ';C=B.form.get('ssid',_A);D=B.form.get('password',_A)
		if C and D and C!=''and D!='':
			try:networking.save_network_config(C,D);return server.redirect(_B,status=303)
			except Exception as F:A='wifi_config: failed to save network config';logging.error(A)
		else:A='wifi_config: Invalid network parameters';logging.error(A)
	E=[]
	try:
		if sys.platform!='esp8266':E=networking.scan_networks(ap)
	except:pass
	return template.render_template(dir_path+'/wifi_setup.html',web_path=dir_path,networks=E,error=A)
async def delayed_restart(delay_secs):' Co-routine for delayed restart ';await uasyncio.sleep(delay_secs);machine.reset()
@accesspointapp.route(_B)
def restart(request):
	' Restart device. '
	if networking.first_boot_present():uasyncio.create_task(delayed_restart(5))
	return template.render_template(dir_path+'/restart.html',web_path=dir_path)
@accesspointapp.route(_C,methods=['GET'])
def favicon(request):' Serve favicon. ';return server.serve_file(dir_path+_C)
@accesspointapp.catchall()
def page_not_found(request):' Handle page not found. ';return template.render_template(dir_path+'/page_not_found.html',web_path=dir_path),STATUS_CODE_404
async def serve_client(reader,writer):' Serve client co-routine ';await accesspointapp.serve_client(reader,writer)
def start_ap():
	' Start the access point. ';global ap;A='rockwren';B='12345678';ap=network.WLAN(network.AP_IF);print(f"essid={A}, password={B}");ap.config(essid=A,password=B);ap.active(True)
	while not ap.active():logging.info('Waiting for connection...');logging.info(ap.status())
	logging.info('Access point active');logging.info(ap.ifconfig())
	try:accesspointapp.run()
	except Exception as D:C=io.StringIO();sys.print_exception(D,C);utils.logstream(C)