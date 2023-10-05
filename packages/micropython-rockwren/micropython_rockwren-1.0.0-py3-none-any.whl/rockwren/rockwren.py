'\n\n'
_B='OFF'
_A='state'
import gc,io,os,sys,machine,ntptime,uasyncio,ubinascii,ujson
from phew import logging,server
from.import accesspoint
from.import env as rockwren_env
from.import mqtt_client
from.import networking
from.import utils
from.import web
from.version import __version__
class Device:
	'\n    Device represents the specific behaviour of the device to be implemented.\n    This class is extended to implement the logic to send a discovery message\n    to home assistant, handle mqtt commands, send mqtt status updates, change\n    device state, handle web ui state changes and so on.\n    '
	def __init__(A,name='RockwrenDevice'):A.name=name;A.state=_B;A.web=None;A.mqtt_client=None;A.listeners=[];A.apply_state();' HTML template path for use for controlling the device from the web ui. ';A.template='/lib/rockwren/controls.html'
	def __str__(A):return f"{A.name}(state={A.state})"
	def web_post_handler(B,form):
		' Handle web ui device control changes. Extend or override to provide handling for the\n            device change post requests.\n            :returns tuple (device state json, HTML response code)\n        ';A=form;logging.debug(A)
		if not A:return'Form not provided.',400
		if A.get(_A)and A.get(_A).upper()=='ON':B.on()
		elif A.get(_A)and A.get(_A).upper()==_B:B.off()
		elif A.get('toggle'):' Ignore value ';B.toggle()
		B.apply_state();return B.device_state(),200
	def command_handler(A,topic,message):'\n        Apply the state of the device on change and notify listeners\n        The implementation must call ``super.command_handler()`` last.\n        ';A.apply_state()
	def device_state(A):'\n        Return a json representation of the device encoded as a str. Used by `mqtt_client` to publish\n        frequent state updates to the MQTT server. Overridden for each device that has more capability than on or off.\n        :return: device state as json\n        ';return ujson.dumps({_A:A.state})
	def information(A):'\n        Return a json representation of the device information encoded as a str. Extended or overridden for each device\n        that has additional information.  Normally, best practice is to extended: get the information dictionary\n        from this function then add to it to provide addition information.\n        :return: device state as json\n        ';E='dns_server';D='gateway';C='subnet_mask';B='ip_address';return ujson.dumps({'device':{'name':A.name,'rockwren_version':__version__,'unique_id':ubinascii.hexlify(machine.unique_id()),'platform':sys.platform,'python_version':sys.version,'implementation':str(sys.implementation)},'mqtt':{'server':rockwren_env.MQTT_SERVER,'port':rockwren_env.MQTT_PORT,'command-topic':A.mqtt_client.command_topic if A.mqtt_client else'','availability-topic':A.mqtt_client.availability_topic if A.mqtt_client else'','state-topic':A.mqtt_client.state_topic if A.mqtt_client else''},'network':{'ssid':rockwren_env.SSID,B:rockwren_env.CONNECTION_PARAMS.get(B),C:rockwren_env.CONNECTION_PARAMS.get(C),D:rockwren_env.CONNECTION_PARAMS.get(D),E:rockwren_env.CONNECTION_PARAMS[E]}})
	def on(A):' Update the device state to ON.  Override or extend when needed.\n        If overridden, self.apply_state() must be called. ';A.state='ON';A.apply_state()
	def off(A):' Update the device state to OFF.  Override or extend when needed.\n        If overridden, self.apply_state() must be called. ';A.state=_B;A.apply_state()
	def toggle(A):
		' Update the device state by toggling.  Override or extend when needed.\n        If overridden, self.apply_state() must be called. '
		if A.is_on():A.off()
		else:A.on()
	def is_on(A):'\n        Check if the device is in the ON state. Override or extend when needed.\n        :return: True if device is on, False if the device is off.\n        ';return A.state=='ON'
	def apply_state(A):'\n        Apply the state of the device on change and notify listeners\n        The implementation must call ``super.apply_state()`` last.\n        ';A.notify_listeners()
	def notify_listeners(A):
		'\n        Notify all registered listeners of a change of state of the device.\n        Listeners are registered using ``Device.register_listener(func).``\n        '
		for B in A.listeners:uasyncio.create_task(listener_task(B))
	def register_listener(A,func):'\n        Register state change listener functions.\n        :param func: listener function\n        ';A.listeners.append(func)
	def register_web(A,_web):'\n        Register the web server with the device.\n        :param _web: Phew web server instance\n        ';A.web=_web
	def register_mqtt_client(A,_mqtt_client):'\n        Register the ``mqtt_client``\n        :param _mqtt_client:\n        ';A.mqtt_client=_mqtt_client
	def discovery_function(A):'\n        The dicovery function to run for this device\n        :return: an array of tuples (device_type, discovery_json).\n        ';return[]
def set_global_exception(loop):
	' Set global exception to catch and output uncaught exceptions to aid debugging. '
	def A(loop,context):C='exception';A=context;B=io.StringIO();sys.print_exception(A[C],B);utils.logstream(B);raise A[C]
	loop.set_exception_handler(A)
async def ntptime_retries():
	while True:
		try:ntptime.settime();logging.debug('ntptime set.');break
		except:logging.debug('ntptime failed.  Retry in 5 seconds.');await uasyncio.sleep(5);continue
def fly(the_device):
	'\n    Convenience method to start a device with web and mqtt capabilities.\n    :param the_device: device implementation\n    ';B=the_device
	while True:
		gc.collect();gc.threshold(gc.mem_free()//4+gc.mem_alloc());web.device=B;D=os.statvfs('/');logging.info(f"Free storage: {D[0]*D[3]/1024} KB");networking.load_network_config()
		if rockwren_env.SSID=='':
			try:set_global_exception(uasyncio.get_event_loop());accesspoint.start_ap()
			except Exception as C:A=io.StringIO();sys.print_exception(C,A);utils.logstream(A)
			finally:sys.exit()
		try:
			set_global_exception(uasyncio.get_event_loop());rockwren_env.CONNECTION_PARAMS=networking.connect();uasyncio.create_task(ntptime_retries())
			if rockwren_env.MQTT_SERVER:logging.info('MQTT client starting.');E=mqtt_client.MqttDevice(B,rockwren_env.MQTT_SERVER,rockwren_env.CONNECTION_PARAMS,command_handler=B.command_handler,mqtt_port=int(rockwren_env.MQTT_PORT));E.run(uasyncio.get_event_loop())
			else:logging.info('MQTT client not started.  Set MQTT Server ip or fqdn to enable')
			web.run(uasyncio.get_event_loop());uasyncio.get_event_loop().run_forever()
		except KeyboardInterrupt:logging.info('Keyboard interrupt at loop level.');break
		except Exception as C:
			try:A=io.StringIO();sys.print_exception(C,A);utils.logstream(A);uasyncio.new_event_loop()
			finally:machine.reset()
async def listener_task(listener):listener()