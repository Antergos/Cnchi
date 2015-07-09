#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logserver.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import pickle
import logging
import logging.handlers
import socketserver
import struct
import threading
import datetime
import time
import sys
import cgi
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from collections import deque
import socket

from pymongo import CursorType
from pymongo import MongoClient
from bson import InvalidDocument

class ContextFilter(logging.Filter):
    def filter(self, record):
        uid = str(uuid.uuid1()).split("-")
        record.uuid = uid[3] + "-" + uid[1] + "-" + uid[2] + "-" + uid[4]
        return True

# Taken from the logging package documentation by Vinay Sajip
# Also fragments of code by Gabriel A. Genellina and doug farrell
# MongodbHandler taken from mongodb-log from Jorge Puente Sarrín

# Create collection:
# > use cnchi
# > db.createCollection('log', {capped:true, size:100000})

class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """
    Handler for a streaming logging request.
    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_forever(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

class MongoHandler(logging.Handler):
    """
    Custom log handler
    Logs all messages to a mongo collection. This  handler is
    designed to be used with the standard python logging mechanism.
    """

    @classmethod
    def to(cls, collection, db='mongolog', host='localhost', port=None,
        username=None, password=None, level=logging.NOTSET):
        """ Create a handler for a given  """
        return cls(collection, db, host, port, username, password, level)

    def __init__(self, collection, db='mongolog', host='localhost', port=None,
        username=None, password=None, level=logging.NOTSET):
        """ Init log handler and store the collection handle """
        logging.Handler.__init__(self, level)

        if isinstance(collection, str):
            connection = MongoClient(host, port)
            if username and password:
                connection[db].authenticate(username, password)
            self.collection = connection[db][collection]
        elif isinstance(collection, Collection):
            self.collection = collection
        else:
            raise TypeError('collection must be an instance of basestring or '
                             'Collection')
        self.formatter = logging.Formatter(
            fmt="[%(uuid)s] [%(asctime)s] [%(module)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

    def count(self):
        return self.collection.count()

    def find(self, filter=None):
        return self.collection.find(filter=filter)

    def emit(self, record):
        """ Store the record to the collection. Async insert """
        try:
            self.collection.insert_one(record.__dict__)
        except TypeError as type_error:
            logging.error(type_error)
        except InvalidDocument as invalid_error:
            logging.error(
                "Unable to save log record: %s",
                invalid_error.message,
                exc_info=True)

class LogginWebMonitorRequestHandler(BaseHTTPRequestHandler):
    with open("logserver.html", 'r') as html:
        summary_html = html.read()

    def do_GET(self):
        ''' Serve a GET request. '''
        sts, response, type = self.build_response(self.path)
        self.send_response(sts)
        if sts == 301:
            self.send_header('Location', response)
        if type:
            self.send_header('Content-type', type)
            self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        if response:
            self.wfile.write(response)

    def build_response(self, path):
        valid_files = [
            ("/css/bootstrap.min.css", "text/css"),
            ("/js/bootstrap.min.js", "text/javascript"),
            ("/js/bootstrap.min.js", "text/javascript"),
            ("/js/bootstrap-theme.min.css", "text/javascript"),
            ("/fonts/glyphicons-halflings-regular.woff2", "application/font-woff"),
            ("/fonts/glyphicons-halflings-regular.woff", "application/font-woff"),
            ("/fonts/glyphicons-halflings-regular.ttf", "application/x-font-ttf")]

        try:
            get_vars_dict = None

            if '?' in path:
                try:
                    get_vars = path.split('?')[1]
                    if '&' in get_vars:
                        get_vars = get_vars.split('&')
                        get_vars_dict = {}
                        for get_var in get_vars:
                            get_vars_dict[get_var.split('=')[0]] = get_var.split('=')[1]
                    else:
                        get_vars_dict = {get_vars.split('=')[0]:get_vars.split('=')[1]}
                except IndexError as index_error:
                    get_vars_dict = None
                path = path.split('?')[0]

            if path == '/index.html' or path == "/summary.html":
                return 200, self.summary_page(get_vars_dict).encode(), 'text/html'

            # Redirects to our index.html
            if path == '/':
                return 301, '/index.html', 'text/html'

            for valid_file in valid_files:
                (valid_path, mime) = valid_file
                if path == valid_path:
                    # Remove starting slash
                    path = path[1:]

                    if "text" in mime:
                        with open(path, 'r') as data_file:
                            data = data_file.read().encode()
                    else:
                        with open(path, 'rb') as data_file:
                            data = data_file.read()

                    return 200, data, mime
            # Not found
            return 404, None, None
        except Exception:
            import traceback
            print ('While handling %r:' % path)
            traceback.print_exc(file=sys.stderr)
            return 500, None, None

    def summary_page(self, get_vars_dict):
        escape = cgi.escape
        handler = self.server.handler
        datefmt = "%Y-%m-%d %H:%M:%S"
        starttime = escape(self.server.starttime.strftime(datefmt))
        uptime = datetime.datetime.now() - self.server.starttime
        uptime = escape(str(datetime.timedelta(uptime.days, uptime.seconds)))

        items = []
        keys = ["uuid", "asctime", "module", "levelname", "message"]
        classes = {
            "info":"info",
            "debug":"success",
            "warning":"warning",
            "error":"danger"}

        num_page = 0
        items_per_page = 10
        search_text = None

        if get_vars_dict:
            if "page" in get_vars_dict.keys():
                try:
                    num_page = int(get_vars_dict["page"])
                except ValueError as value_error:
                    num_page = 0
            if "search" in get_vars_dict.keys():
                search_text = get_vars_dict["search"]

        if search_text:
            query = {"uuid": search_text}
            cursor = handler.find(filter=query)
        else:
            cursor = handler.find()

        num_items = cursor.count()
        # print("num_items", num_items)

        if num_page < 0:
            num_page = 0

        max_num_pages = num_items // items_per_page

        if num_page > max_num_pages:
            num_page = max_num_pages

        start = num_page * items_per_page
        end = start + items_per_page

        if end > num_items:
            end = num_items

        # print("start", start, "end", end)

        for record in cursor[start:end]:
            try:
                cells = ""
                for key in keys:
                    cells += "<td>{0}</td>".format(record[key])
                level = escape(record['levelname'].lower())
                item = '<tr class="{0}">{1}\n</tr>'.format(
                    classes[level],
                    cells)
                items.append(item)
            except Exception as fatal_error:
                print(fatal_error)
                import traceback
                print('While generating %r:' % record)
                traceback.print_exc(file=sys.stderr)

        records = '\n'.join(items)
        d = dict(numpages=max_num_pages + 1,
                 starttime=starttime,
                 uptime=uptime,
                 logrecordstotal=num_items,
                 records=records)
        return self.summary_html % d

    def log_message(self, format, *args):
        pass


class LoggingWebMonitor(HTTPServer):
    'A simple web page for displaying logging records'

    def __init__(self, host='localhost',
                 port=None,
                 handler=LogginWebMonitorRequestHandler):
        if port is None:
            port = logging.handlers.DEFAULT_TCP_LOGGING_PORT + 1
        HTTPServer.__init__(self, (host, port), handler)
        self.starttime = datetime.datetime.now()


def main():
    # Get server IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    myip = s.getsockname()[0]

    logger = logging.getLogger()

    filter = ContextFilter()
    logger.addFilter(filter)

    # Create Mongodb handler
    mongo_handler = MongoHandler.to(db='cnchi', collection='log')
    mongo_handler.setLevel(logging.DEBUG)
    logger.addHandler(mongo_handler)

    # Web monitor
    webmonitor = LoggingWebMonitor(host=myip)
    webmonitor.handler = mongo_handler
    webmonitor_thread = threading.Thread(target=webmonitor.serve_forever)
    webmonitor_thread.daemon = True
    print("{0} started at {1}".format(webmonitor.__class__.__name__, webmonitor.server_address))
    webmonitor_thread.start()

    # Log server
    logserver = LogRecordSocketReceiver(host=myip)
    logserver_thread = threading.Thread(target=logserver.serve_forever)
    logserver_thread.daemon = True
    logserver_thread.start()

    # import webbrowser
    # webbrowser.open('http://%s:%s/' % webmonitor.server_address)

    while True:
        try:
            time.sleep(3600)
        except (KeyboardInterrupt, SystemExit) as exit_error:
            logserver.shutdown()
            webmonitor.shutdown()
            break

if __name__ == '__main__':
    main()
