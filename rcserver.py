#!/usr/bin/python env
"""
rcserver.py
mpmsimo
11/10/2016
"""

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import logging
import logging.handlers
import urllib.parse
import sqlite3

# Can be moved to a config file later
host = '127.0.0.1'
#host = 'localhost'
port = 4000
logfile = 'server.log'

# Dict with host/port vars to pass to string
s = {'host': host, 'port': port}

# Create logging format
FORMAT = '%(asctime)s %(threadName)s %(levelname)s %(message)s in %(module)s on line %(lineno)d'

# Create logging handler for application
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# In-memory database
conn = sqlite3.connect(':memory:')
c = conn.cursor()


# HTTP Server
class HTTPReqHandler(BaseHTTPRequestHandler):
    """Handler for GET HTTP(S) requests."""

    def do_GET(self):
        """Print what the client sees during GET requests."""
        # Extract values for URL 
        ulpup = urllib.parse.urlparse(self.path)

        # Get key/value
        value_list = ulpup.query.split('=')
        query_key = value_list[0]
        query_value = value_list[1]

        # Key lookup
        

        # Set message
        get_output = 'The value associated with the key \'{k}\' is {v}.\n'.format(k=query_key, v=query_value)
        self.wfile.write(get_output.encode('utf-8'))

        # Check JSON file for key/value pairing
        #get_output.append('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}'.format(self.client_address, self.server, self.command, self.path, self.request_version, self.rfile, self.wfile, self.protocol_version, self.MessageClass, self.responses, self.error_message_format))
        #get_output.append('{k}, {v}'.format(k=self.headers.keys(), v=self.headers.values()))

        # Return a 200, letting the client know everything is OK.
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()

    def do_POST(self):
        """Update a key/value pair."""
        # What is POST vs SET
        # Get header URL
        # Check if key exists, overwrite value
        pass

def start_server(host, port):
    """Starts the HTTP server."""
    server = HTTPServer((host, port), HTTPReqHandler)
    print('HTTP server has started on [{h}:{p}].'.format(h=host,p=port))
    server.serve_forever()

if __name__ == '__main__':
    start_server(host, port)
