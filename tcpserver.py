#!/usr/bin/python env
"""
tcpserver.py
mpmsimo
11/2/2016
"""

import socketserver
import logging

# Can be moved to a config file later
host = 'localhost'
port = '4000'
logfile = 'tcpserver.log'

class MyTCPHandler(socketserver.BaseRequestHandler):
    """A basic implementation of a TCP RequestHandler, from the BaseServer
template."""

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
    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10240, backupCount=10)
    handler.setLevel(logging.WARNING)

    # File logging timestamp (flask default)
    handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))

    app.logger.addHandler(handler)
    app.logger.warning('WARNING test')
    app.logger.error('ERROR test')

    # Start the server
    server = socketserver.TCPServer((host, port), MyTCPHandler)
    server.serve_forever()
