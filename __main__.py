# python 3.11
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python


import logging
import os
import random
import argparse
from loxone_listener import loxone_listener_main
from mqtt import mqtt_run

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

broker_host = os.getenv('MQTT_HOST', '127.0.0.1')
broker_port = int(os.getenv('MQTT_PORT', 1883))
topic = os.getenv('MQTT_TOPIC', 'loxone')
client_id = os.getenv('MQTT_CLIENT_ID', f'loxone-{random.randint(0, 1000)}')

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        add_help=False, description='Simple Loxone to InfluxDB script')
    parser.add_argument('-h', '--host', type=str, required=False,
                        default=broker_host,
                        help='hostname of mqtt')
    parser.add_argument('-p', '--port', type=int, required=False, default=broker_port,
                        help='port of mqtt')
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
  
  mqtt_run(args.host, args.port, args.topic, args.client_id, args.debug)
  # loxone_listener_main(args.debug)