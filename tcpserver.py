#!/usr/bin/python env
"""
tcpserver.py
mpmsimo
11/2/2016
"""

import socketserver
import logging
import logging.handlers

# Can be moved to a config file later
host = 'localhost'
port = '4000'
logfile = 'server.log'

# Dict with host/port vars to pass to string
s = {'host': host, 'port': port}

# Create logging format
FORMAT = '%(asctime)s %(threadName)s %(levelname)s %(message)s in %(module)s on line %(lineno)d'

# Create handler for TCP server
class RCServer(socketserver.TCPServer):

    def __init__(self, host, handler_class=RCRequestHandler,):
        self.logger.get
    logging.basicConfig(format=FORMAT)

    # Create logger object and set min logging level
    logger = logging.getLogger('tcps-logger')
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=100, backupCount=10,)
    logger.addHandler(handler)
    #logger.warning('Protocol problem: %s', 'connection reset', extra=s)

class MyTCPHandler(socketserver.BaseRequestHandler):
    """A basic implementation of a TCP RequestHandler, from the BaseServer template."""

    def handle(self):
        """Handles a request sent to the server."""
        # Recieve 1024 bits of data and strip newline char
        self.data = self.request.recv(1024).strip()
        logging.info("{ca} wrote: ".format(self.client_address[0]))
        logging.info(self.data)
        # Return the data back to the user in Uppercase
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    # Create log files up to 10MB (with backup of prior logs) then rotate the file


    # Start the server
    server = socketserver.TCPServer((host, port), MyTCPHandler)
    server.serve_forever()
