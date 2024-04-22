#!/usr/bin/python

# Simple script to import Loxone UDP logs into InfluxDB
import os
import socket
import json
import argparse
import re
import logging
from datetime import datetime
from dateutil import tz
# suppress warnings for unverified https request
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# =============== Configuration =====================
# local IP and port where the script is listening for UDP packets from Loxone
localIP = os.getenv('BIND_ADDRESS', '0.0.0.0')
localPort = int(os.getenv('BIND_PORT', 2222))

class LoxoneListenerOptions:
    def __init__(self, host: str, port: int, debug: bool):
        self.host = host
        self.port = port
        self.debug = debug


def parse_log_data(data, from_zone, to_zone, debug=False):
    """
    Parse received message
    Syntax: <timestamp>;<measurement_name>;<alias(optional)>:<value>;<tag_1(optional)>;<tag_2(optional)>;<tag_3(optional)>
    Example: "2020-09-10 19:46:20;Bedroom temperature;23.0"
    ** TO DO ** Need to add checks in case something goes wrong
    """
    logger.debug('Received: %s', data)

    end_timestamp = data.find(b';')
    end_name = data.find(b';', end_timestamp+1)
    end_alias = data.find(b':', end_name+1)
    if end_alias < 0:		# -1 means not found
        end_alias = end_name
    end_value = data.find(b';', end_alias+1)

    if end_value < 0:  # ; char not found after value
        end_tag1 = 0
        end_value = len(data)
    else:
        end_tag1 = data.find(b';', end_value + 1)

    if end_tag1 > 0:
        end_tag2 = data.find(b';', end_tag1+1)
    else:
        end_tag2 = 0
    if end_tag2 > 0:
        end_tag3 = data.find(b';', end_tag2+1)
    else:
        end_tag3 = 0
    numeric_const_pattern = r'[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    # Timestamp Extraction
    parsed_data = {'TimeStamp': data[0:end_timestamp]}
    parsed_data['TimeStamp'] = parsed_data['TimeStamp'].replace(b' ', b'T')+b'Z'
    # Timezone conversion to UTC
    local = datetime.strptime(parsed_data['TimeStamp'].decode('utf-8'), b'%Y-%m-%dT%H:%M:%SZ'.decode('utf-8'))
    local = local.replace(tzinfo=from_zone)
    utc = local.astimezone(to_zone)
    parsed_data['TimeStamp'] = utc.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Name Extraction
    parsed_data['Name'] = data[end_timestamp+1:end_name]

    # Alias Extraction
    if end_alias != end_name:
        parsed_data['Name'] = data[end_name+1:end_alias]

    # Value Extraction
    parsed_data['Value'] = rx.findall(data[end_alias+1:end_value].decode('utf-8'))[0]

    # Tag_1 Extraction
    parsed_data['Tag_1'] = data[end_value+1:end_tag1].rstrip()

    # Tag_2 Extraction
    parsed_data['Tag_2'] = data[end_tag1+1:end_tag2].rstrip()

    # Tag_3 Extraction
    parsed_data['Tag_3'] = data[end_tag2+1:end_tag3].rstrip()

    # Create Json body for Influx
    json_body = [
        {
            "measurement": parsed_data['Name'].decode('utf-8'),
            "tags": {
                "Tag_1": parsed_data['Tag_1'].decode('utf-8'),
                "Tag_2": parsed_data['Tag_2'].decode('utf-8'),
                "Tag_3": parsed_data['Tag_3'].decode('utf-8'),
                "Source": "Loxone",
            },
            "time": parsed_data['TimeStamp'],   # "2009-11-10T23:00:00Z",
            "fields": {
                "value": float(parsed_data['Value'])
            }
        }
    ]

    if debug:
        logger.debug(json.dumps(json_body, indent=2))

    return json_body


def init_loxone_listener(on_received, options: LoxoneListenerOptions):
    """Instantiate a connection to the InfluxDB and stard listening on UDP port for incoming messages"""
    # client = InfluxDBClient(host, port, dbuser, dbuser_code, dbname, ssl, verify)

    # get TZ info
    to_zone = tz.tzutc()
    from_zone = tz.tzlocal()

    # A UDP server
    # Set up a UDP server
    logger.info('Listening for incoming Loxone UDP packets on %s:%s', options.host, options.port)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Listen on local port
    # (to all IP addresses on this system)
    listen_addr = (options.host, options.port)
    udp_sock.bind(listen_addr)
    logger.debug('Socket attached')

    # Report on all data packets received and
    # where they came from in each case (as this is
    # UDP, each may be from a different source and it's
    # up to the server to sort this out!)
    while True:
        data, addr = udp_sock.recvfrom(1024)
        json_body_log = parse_log_data(data, from_zone, to_zone, options.debug)
        # Process message
        on_received(json_body_log)
