'\nDevice web interface for initial setup via access point and for configuration.\n'
_O='esp8266'
_N='/favicon.svg'
_M='dns_server'
_L='gateway'
_K='subnet_mask'
_J='ip_address'
_I='/restart.html'
_H='{"error": "Device not found"}'
_G='/mqtt_config'
_F='/restart'
_E='POST'
_D='application/json'
_C='Content-Type'
_B='GET'
_A=None
import gc,io,sys,machine,uasyncio
from micropython import const
from.import env
from.import networking
from.import rockwren
from.import utils
from phew import logging
from phew import server
from phew import template
DIR_PATH='/lib/rockwren'
STATUS_CODE_200=const(200)
STATUS_CODE_302=const(302)
STATUS_CODE_400=const(400)
STATUS_CODE_404=const(404)
webapp=server.Phew()
device=_A
def run(loop):' Run the web app as a task in the asyncio loop ';webapp.run_as_task(loop)
@webapp.route('/',methods=[_B])
def index(request):' Home page ';return template.render_template(DIR_PATH+'/index.html',web_path=DIR_PATH,device=device)
@webapp.route('/device',methods=[_B])
def device_control(request):
	' Return json formatted information about the device '
	if device:return server.Response(device.information(),200,{_C:_D})
	return'Device not found',STATUS_CODE_400
@webapp.route('/device/control',methods=[_E])
def device_control(request):
	' Handle device control messages ';A=request
	if not A.form:return server.Response('{"error": "Bad request"}',STATUS_CODE_400,{_C:_D})
	if device:
		try:C,D=device.web_post_handler(A.form);return server.Response(C,D,{_C:_D})
		except Exception as E:
			try:B=io.StringIO();sys.print_exception(E,B);utils.logstream(B)
			finally:return server.Response('{"error": "Error handling device control request"}',STATUS_CODE_400,{_C:_D})
	return server.Response(_H,STATUS_CODE_400,{_C:_D})
@webapp.route('/device/state',methods=[_B])
def device_state(request):
	' Get device state '
	if device:return server.Response(device.device_state(),STATUS_CODE_200,{_C:_D})
	return server.Response(_H,STATUS_CODE_400,{_C:_D})
async def delayed_restart(delay_secs):' Restart the device after delay_secs seconds. ';await uasyncio.sleep(delay_secs);machine.reset()
@webapp.route(_F)
def restart(request):' Restart the device after a delay. ';uasyncio.create_task(delayed_restart(5));return template.render_template(DIR_PATH+_I,web_path=DIR_PATH)
@webapp.route(_G,methods=[_B])
def mqtt_config(request):' MQTT configuration ';return template.render_template(DIR_PATH+'/mqtt_config.html',web_path=DIR_PATH,device=device,ip_address=env.CONNECTION_PARAMS[_J],subnet_mask=env.CONNECTION_PARAMS[_K],gateway=env.CONNECTION_PARAMS[_L],dns_server=env.CONNECTION_PARAMS[_M],mqtt_server=env.MQTT_SERVER,mqtt_port=str(env.MQTT_PORT),mqtt_client_cert=env.MQTT_CLIENT_CERT,mqtt_client_key_stored=env.MQTT_CLIENT_KEY is not _A)
@webapp.route(_N,methods=[_B])
def favicon(request):'" Serve favicon ';return server.serve_file(DIR_PATH+_N)
@webapp.route('/log',methods=[_B])
def favicon(request):
	'" Serve log file '
	if sys.platform==_O:' Do a gc before serving file to ensure sufficient memory ';gc.collect()
	return server.serve_file('/log.txt')
@webapp.route(_G,methods=[_E])
def mqtt_config_save(request):
	' Handle MQTT configuration form post ';L='mqtt_client_key';K='mqtt_client_cert';J='mqtt_port';E='mqtt_server';D=True;B=request
	if not B.form:return server.redirect(_G,status=STATUS_CODE_302)
	A=False;C=B.form.get(E,_A)
	if C:
		F=C.split('.')
		if len(F)==4 and all(A.isdigit()for A in F):networking.save_network_config_key(E,C);A=D
		elif utils.is_fqdn(C):networking.save_network_config_key(E,C);A=D
	else:networking.save_network_config_key(E,'')
	G=B.form.get(J,_A)
	if G:networking.save_network_config_key(J,int(G));A=D
	H=B.form.get(K,_A)
	if H:networking.save_network_config_key(K,H);A=D
	I=B.form.get(L,_A)
	if I:networking.save_network_config_key(L,I);A=D
	if A:return server.redirect(_F,status=STATUS_CODE_302)
	else:return server.redirect(_G,status=STATUS_CODE_302)
@webapp.route('/viewlogs',methods=[_B])
def view_logs(request):' View device logs ';return template.render_template(DIR_PATH+'/viewlogs.html',web_path=DIR_PATH,device=device)
@webapp.route('/information',methods=[_B])
def view_information(request):' View device information ';return template.render_template(DIR_PATH+'/information.html',web_path=DIR_PATH,device=device,ip_address=env.CONNECTION_PARAMS[_J],subnet_mask=env.CONNECTION_PARAMS[_K],gateway=env.CONNECTION_PARAMS[_L],dns_server=env.CONNECTION_PARAMS[_M],mqtt_server=env.MQTT_SERVER,mqtt_port=env.MQTT_PORT)
@webapp.route('/wifi_config',methods=[_B,_E])
def wifi_config(request):
	B=request;A=_A
	if B.method==_E:
		' WiFI Setup handle post. ';C=B.form.get('ssid',_A);D=B.form.get('password',_A)
		if C and D and C!=''and D!='':
			try:networking.save_network_config(C,D);return server.redirect(_F,status=303)
			except Exception as F:A='wifi_config: failed to save network config';logging.error(A)
		else:A='wifi_config: Invalid network parameters';logging.error(A)
	E=[]
	try:
		if sys.platform!=_O:E=networking.scan_networks(env.CONNECTION_PARAMS['wlan'])
	except:pass
	return template.render_template(DIR_PATH+'/wifi_config.html',web_path=DIR_PATH,networks=E,error=A)
async def delayed_restart(delay_secs):' Co-routine for delayed restart ';await uasyncio.sleep(delay_secs);machine.reset()
@webapp.route(_F)
def restart(request):
	' Restart device. '
	if networking.first_boot_present():uasyncio.create_task(delayed_restart(5))
	return template.render_template(DIR_PATH+_I,web_path=DIR_PATH)
@webapp.catchall()
def page_not_found(request):' 404 page not found ';return template.render_template(DIR_PATH+'/page_not_found.html',web_path=DIR_PATH),STATUS_CODE_404