#!/usr/bin/python env
"""
rcserver.py
mpmsimo
11/10/2016
"""

import http.server
import logging
import logging.handlers
import urllib.parse
import urllib.request
import sqlite3

# Can be moved to a config file later
host = '127.0.0.1'
port = 4000
logfile = 'server.log'

# Create logging format
FORMAT = '%(asctime)s %(threadName)s %(levelname)s %(message)s in %(module)s on line %(lineno)d'
# Create logging handler for application
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# In-memory database
dbc = sqlite3.connect(':memory:')

# Handle closing of connection when shutdown.
with dbc:
    cursor = dbc.cursor()
    # Create table that will store key/values.
    cursor.execute('CREATE TABLE items(key TEXT PRIMARY KEY, value TEXT);')

# HTTP Server
class HTTPReqHandler(http.server.BaseHTTPRequestHandler):
    """Handler for GET HTTP(S) requests."""

    logger = logging.getLogger('httplog')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=100, backupCount=10,)
    logger.addHandler(handler)

    def do_GET(self):
        """Print what the client sees during GET requests."""
        # Extract values for URL 
        ulpup = urllib.parse.urlparse(self.path)
        self.logger.debug(str(self.path[:5]))

        # Huge Hack :(
        if str(self.path[:5]) == '/set?':
            get_output = 'Redirecting to SET/POST API call.'
            self.logger.warning(get_output)
            self.wfile.write(get_output.encode('utf-8'))
            self.send_response(307)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.do_POST()
        else:
            # Get value from header
            value_list = ulpup.query.split('=')
            query_key = value_list[1]

            # Value lookup based on key provided in header.
            ce = cursor.execute("SELECT value FROM items WHERE key='{k}';".format(k=query_key))

            # Format value, slice off excess punctuation
            return_value = str(ce.fetchone())[2:-3]
            if return_value in [None, '']:
                get_output = "Key '{k}' does not exist.\n".format(k=query_key)
            else:
                get_output = 'dblookup for {k}: {v}\n'.format(k=query_key, v=return_value)

            # Send to client
            self.wfile.write(get_output.encode('utf-8'))

            # Return a 200, letting the client know everything is OK.
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()

    def do_POST(self):
        """Update a key/value pair."""
        # Get header URL
        ulpup = urllib.parse.urlparse(self.path)

        # Get key/value from header
        value_list = ulpup.query.split('=')
        query_key = value_list[0]
        self.logger.debug(value_list)
        try:
            query_value = value_list[1]
        except IndexError as ie:
            self.logger.warning(ie)
            query_value = ''

        # Check if key exists, overwrite value
        #ce = cursor.execute("SELECT value FROM items WHERE key='{k}';".format(k=query_key))
        #self.logger.debug(str(ce.fetchone()))
        #if str(ce.fetchone())[2:-3] not in [None, '']:

        try:
            cursor.execute("INSERT INTO items(key, value) VALUES ('{k}', '{v}');".format(k=query_key, v=query_value))
        except sqlite3.IntegrityError as sie:
            self.logger.error(sie)

        get_output = 'Added {k} = {v} to database.'.format(k=query_key, v=query_value)
'''
        self.logger.info(get_output)
        self.wfile.write(get_output.encode('utf-8'))
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
'''
def start_server(host, port):
    """Starts the HTTP server."""

    server = http.server.HTTPServer((host, port), HTTPReqHandler)
    print('HTTP server has started on [{h}:{p}].'.format(h=host,p=port))
    server.serve_forever()

if __name__ == '__main__':
    start_server(host, port)
