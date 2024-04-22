# python 3.11
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python


import logging
import os
import random
import argparse
from loxone_listener import LoxoneListenerOptions, init_loxone_listener
from mqtt import MqttOptions, mqtt_init

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

debug =  bool(os.getenv('DEBUG', False))

loxone_listener_host = os.getenv('LISTENER_HOST', '0.0.0.0')
loxone_listener_port = int(os.getenv('LISTENER_PORT', 2222))

listener_options = LoxoneListenerOptions(host=loxone_listener_host, port = loxone_listener_port, debug = debug)

broker_host = os.getenv('MQTT_HOST', '127.0.0.1')
broker_port = int(os.getenv('MQTT_PORT', 1883))
topic = os.getenv('MQTT_TOPIC', 'smarthome')
client_id = os.getenv('MQTT_CLIENT_ID', f'loxone-{random.randint(0, 1000)}')

mqtt_options = MqttOptions(host = broker_host, port = broker_port, client_id=client_id, topic = topic, debug = debug)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        add_help=False, description='Simple Loxone to InfluxDB script')
    parser.add_argument('-h', '--host', type=str, required=False,
                        default=broker_host,
                        help='hostname of mqtt')
    parser.add_argument('-hl', '--host-listener', type=str, required=False,
                        default=loxone_listener_host,
                        help='IP address to listen on')    
    parser.add_argument('-p', '--port', type=int, required=False, default=broker_port,
                        help='port of mqtt')
    parser.add_argument('-pl', '--port-listener', type=int, required=False, default=loxone_listener_port,
                        help='port to listen on')    
    parser.add_argument('-t', '--topic', default=topic, action="store_true",
                        help='name of mqtt topic to listen to')
    parser.add_argument('-c', '--client-id', default=client_id, action="store_true",
                        help='client id for mqtt connection')
    parser.add_argument('-d', '--debug', action="store_true", default=bool(os.getenv('DEBUG', False)),
                        help='debug code')
    parser.add_argument('-?', '--help', action='help',
                        help='show this help message and exit')
    return parser.parse_args()

if __name__ == '__main__':
    logger.info("Start")
    args = parse_args()

    listener_options.host = args.host
    listener_options.port = args.port
    listener_options.debug = args.debug

    mqtt_options.host = args.host
    mqtt_options.port = args.port
    mqtt_options.topic = args.topic
    mqtt_options.client_id = args.client_id
    mqtt_options.debug = args.debug

    mqtt = mqtt_init(mqtt_options)
  
    mqtt.publish('test')
    init_loxone_listener(on_received=mqtt.publish, options=listener_options)
    