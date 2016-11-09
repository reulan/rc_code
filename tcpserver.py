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
#host = 'localhost'
host = '127.0.0.1'
port = '4000'
logfile = 'server.log'

# Dict with host/port vars to pass to string
s = {'host': host, 'port': port}

# Create logging format
FORMAT = '%(asctime)s %(threadName)s %(levelname)s %(message)s in %(module)s on line %(lineno)d'

# Create handler for TCP server
logging.basicConfig(level=logging.DEBUG, format=FORMAT,)

class RCRequestHandler(socketserver.BaseRequestHandler):
    """The TCP handler for the server class defined."""

    def __init__(self, request, client_address, host):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, host)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        # Echo the back to the client
        data = self.request.recv(1024)
        self.logger.debug('recv()->"%s"', data)
        self.request.send(data)
        return

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)

# Create TCP server
class RCServer(socketserver.TCPServer):
    def __init__(self, host, handler_class=RCRequestHandler,):
        self.logger.get('RCServer')
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
    # Start the server
    server = socketserver.TCPServer((host, port), MyTCPHandler)
    server.serve_forever()
