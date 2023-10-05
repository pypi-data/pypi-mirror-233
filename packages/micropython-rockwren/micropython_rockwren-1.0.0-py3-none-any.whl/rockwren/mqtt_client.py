'\nMQTT device integration for Home Assistant discovery, connection, reconnection, state notification publication\nand command handling for a device.\n'
_C=b'online'
_B=None
_A=True
import io,sys,time,machine,uasyncio,ubinascii,ujson
from umqtt.robust2 import MQTTClient
from phew import logging
from.import env
from.import rockwren
from.import utils
def noop_topic_handler(topic,message):' No operation topic handler\n    :param topic: mqtt topic\n    :param message: mqtt message\n    :return:\n    '
class MqttDevice:
	'\n    MQTT device integration for Home Assistant discovery, connection, reconnection, state notification publication\n    and command handling for a device. Further details for configuring discovery messages can be found on the\n    Home Assistant website:\n    - https://www.home-assistant.io/integrations/mqtt/\n    - https://www.home-assistant.io/integrations/light.mqtt/\n    - https://www.home-assistant.io/integrations/switch.mqtt/\n    '
	def __init__(A,device,mqtt_server,connection_params,state_topic=b'/state',command_topic=b'/command',availability_topic=b'/LWT',command_handler=noop_topic_handler,mqtt_port=0,client_id=b'rockwren'):C=command_topic;B=device;A.device=B;A.device.register_mqtt_client(A);A.device.register_listener(A.mqtt_publish_state);A.mqtt_server=mqtt_server;A.mqtt_port=mqtt_port;A.connection_params=connection_params;A.client_id=client_id;A.unique_id=ubinascii.hexlify(machine.unique_id());A.device_id=A.client_id+b'_'+A.unique_id;A.device_topic=A.client_id+b'/'+A.unique_id;A._topic_handlers={};A.state_topic=A.device_topic+state_topic;A.command_topic=A.device_topic+C;A.availability_topic=A.device_topic+availability_topic;A.register_topic_handler(C,command_handler);A._discovery_functions=B.discovery_function();A._publish_interval=env.PUBLISH_INTERVAL;A._last_publish=0;A._mqtt_client=_B;A.status={};A._status_reported=_A;A._commands=[];A._max_commands=10
	def subscription_callback(B,topic,msg,retained,duplicate):
		' Received messages from subscribed topics will be delivered to this callback ';C=msg;A=topic;A=A
		if A not in B._topic_handlers.keys():return
		if len(B._commands)>B._max_commands:logging.error(f"subscription_callback: Command queue full, discarding. {A} {C.decode()}");return
		D=''
		try:D=ujson.loads(C)
		except Exception:D=C.decode();logging.debug(f"subscription_callback: Message not json using raw message {A.decode()} {C.decode()}")
		B._commands.append((A,D))
	def register_topic_handler(A,topic_suffix,topic_handler):'\n        :param topic_suffix: Suffix to associate with the topic_handler function\n        :param topic_handler:  Topic handler function\n        ';A._topic_handlers[A.device_topic+topic_suffix]=topic_handler
	def pop_message(A):
		' Pop the (topic, message) tuple '
		if len(A._commands)==0:return _B,_B
		return A._commands.pop(0)
	def run(A,uasyncio_loop):
		'\n        Initialise the mqtt client, establish the connection, execute the reconnection and command handler tasks\n        :param uasyncio_loop: asyncio loop used for the mqtt client.  The mqtt client, reconnection handler and\n                              command handler are all run as co-routines for this loop.\n        ';D=False;logging.info(f"Begin connection with MQTT Broker :: {A.mqtt_server}:{A.mqtt_port}");B=D;C=_B
		if env.MQTT_CLIENT_KEY and env.MQTT_CLIENT_CERT:C={'key':utils.pem_to_der(env.MQTT_CLIENT_KEY),'cert':utils.pem_to_der(env.MQTT_CLIENT_CERT),'server_side':D};B=_A
		A._mqtt_client=MQTTClient(A.device_id,A.mqtt_server,port=A.mqtt_port,keepalive=env.MQTT_KEEPALIVE,ssl=B,ssl_params=C);A._mqtt_client.DEBUG=_A;A._mqtt_client.set_last_will(A.availability_topic,b'offline',retain=_A);A._mqtt_client.connect();uasyncio.create_task(A.ensure_connection());uasyncio.create_task(A._mqtt_command_handler());A._mqtt_client.set_callback(A.subscription_callback);A._mqtt_client.subscribe(A.device_topic+b'/#');A._mqtt_client.publish(A.availability_topic,_C,retain=_A);logging.info(f"Connected to MQTT  Broker :: {A.mqtt_server}, and waiting for callback function to be called.");A.send_discovery_msgs()
	async def ensure_connection(A):
		' A asyncio co-routine for reconnecting to mqtt server '
		while _A:
			if A._mqtt_client.is_conn_issue():
				while A._mqtt_client.is_conn_issue():
					logging.info('mqtt trying to reconnect');await uasyncio.sleep(5)
					try:A._mqtt_client.reconnect()
					except Exception as C:B=io.StringIO();sys.print_exception(C,B);utils.logstream(B)
				A._mqtt_client.publish(A.availability_topic,_C,retain=_A);A._mqtt_client.resubscribe()
			await uasyncio.sleep(1)
	def mqtt_publish_state(A):' Publish the current device state on the state topic to the mqtt server ';logging.info(f"mqtt: {A.state_topic} {A.device.device_state()}");A._mqtt_client.publish(A.state_topic,A.device.device_state());A._status_reported=_A
	def send_discovery_msgs(B):
		' Send all registered discovery messages for the device. '
		try:
			for(A,E)in B._discovery_functions:
				if type(A)!=bytes:A=A.encode()
				C=b'homeassistant/'+A+b'/'+B.device_id+b'/config';B._mqtt_client.publish(C,ujson.dumps(E));logging.info(f"Sending discovery message with topic {C}")
		except Exception as F:logging.error(f"Failed to send discovery messages.");D=io.StringIO();sys.print_exception(F,D);utils.logstream(D)
	async def _mqtt_command_handler(A):
		' MQTT command handler\n            Asyncio co-routine '
		while _A:
			await uasyncio.sleep(0);A._mqtt_client.check_msg();E=time.time()
			if not A._status_reported or E-A._last_publish>=A._publish_interval:A.mqtt_publish_state();A._last_publish=E
			B,C=A.pop_message()
			if C is _B:continue
			logging.debug(f"_mqtt_command_handler: {B}: {C}");D=A._topic_handlers.get(B)
			if D is _B:continue
			try:D(B,C)
			except Exception as G:logging.error(f"Exception during execution of {D.__name__} for topic {B})");F=io.StringIO();sys.print_exception(G,F);utils.logstream(F)
			A.mqtt_publish_state()
def default_discovery(mqtt_client):' Default Home Assistant discovery message for a json based MQTT Light.\n        See https://www.home-assistant.io/integrations/light.mqtt/\n        :returns array of tuples (device_type, discovery_json)\n    ';B='name';A=mqtt_client;return[('light',{'unique_id':f"{A.device_id}_light",B:A.device.name,'platform':'mqtt','schema':'json','state_topic':A.state_topic,'command_topic':A.command_topic,'payload_on':'ON','payload_off':'OFF','availability':{'topic':A.availability_topic},'device':{'identifiers':[A.device_id],B:f"Rockwren Light",'sw_version':'1.0','model':'','manufacturer':'Rockwren','configuration_url':f"http://{A.connection_params['ip_address']}/"}})]