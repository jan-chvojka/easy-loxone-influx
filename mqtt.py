import logging
import os
import random
import time
from paho.mqtt import client as mqtt_client

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

logger = logging.getLogger(__name__)

def connect_mqtt(host: str, port: int, client_id: str):
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.error("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, port)
    return client
  
def on_disconnect(client, userdata, rc):
    logger.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logger.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logger.info("Reconnected successfully!")
            return
        except Exception as err:
            logger.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logger.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    
def publish(client, topic):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logger.debug(f"Send `{msg}` to topic `{topic}`")
        else:
            logger.error(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break    
  
def mqtt_run(host: str, port: int, topic: str, client_id: str, debug: bool = False):
  logger.info(f"MQTT Run: {host} {port} {topic} {client_id} {debug}")
  client = connect_mqtt(host, port, client_id)
  client.on_disconnect = on_disconnect
  client.loop_start()
  publish(client, topic)
  client.loop_stop()
  