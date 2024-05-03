import argparse
import socket
import logging

logger = logging.getLogger(__name__)

bufsize = 1024 

# set these values
target_host = "127.0.0.1"
target_port = 64153

listen_host = "0.0.0.0"
listen_port = 8080

# def forward(data, port):
#     print "*** Forwarding: '%s' from port %s" % (data, port)
#     sock = socket.socket(AF_INET, SOCK_DGRAM)
#     sock.bind(("localhost", port)) # Bind to the port data came in on
#     sock.sendto(data, (target_host, target_port))

# def listen(host, port):
#     listen_socket = socket.socket(AF_INET, SOCK_DGRAM)
#     listen_socket.bind((host, port))
#     print "*** Listening on %s:%s" % ( host, port )
#     while True:
#         data, addr = listen_socket.recvfrom(bufsize)
#         forward(data, addr[1]) # data and port

## listen(listen_host, listen_port)

def parse_args():
    parser = argparse.ArgumentParser(
        add_help=False, description='UPD Port Forwarder')    
    parser.add_argument('-p', '--port', type=int, help='port')
    parser.add_argument('-h', '--host', type=str, help='host ip', required=False, default=listen_host)    
    parser.add_argument('-t', '--target', type=str, help='target ip')    

    return parser.parse_args()


logger.info("Start UDP Forwarder")

args = parse_args()

logger.info(f"Listening on {args.host}:${args.port}")
logger.info(f"Forwarding to {args.target}:${args.port}")

