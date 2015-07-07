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
from http.server import BaseHTTPRequestHandler, HTTPServer
from collections import deque
import socket

# Taken from the logging package documentation by Vinay Sajip
# Also fragments of code by Gabriel A. Genellina and doug farrell

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

# Idea and page layout taken from python-loggingserver by doug.farrell
# http://code.google.com/p/python-loggingserver/

class MostRecentHandler(logging.Handler):
    """
    A Handler which keeps the most recent logging records in memory.
    """

    def __init__(self, max_records=200):
        logging.Handler.__init__(self)
        self.logrecordstotal = 0
        self.max_records = max_records
        self.db = deque([], max_records)

    def emit(self, record):
        self.logrecordstotal += 1
        try:
            self.db.append(record)
            # pre 2.6
            while len(self.db) > self.max_records:
                self.db.popleft()
        except Exception:
            self.handleError(record)

class LogginWebMonitorRequestHandler(BaseHTTPRequestHandler):
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(
            # fmt='%(asctime)s\n%(name)s\n%(levelname)s\n%(funcName)s (%(filename)s:%(lineno)d)\n%(message)s',
            fmt="%(uuid)s\n%(asctime)s\n%(module)s\n%(levelname)s\n%(message)s",
            datefmt=datefmt)

    with open("logserver.css", 'r') as css:
        default_css = css.read()

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
            self.wfile.write(response.encode())

    def build_response(self, path):
        try:
            if path == '/summary.html':
                return 200, self.summary_page(), 'text/html'
            if path == '/default.css':
                return 200, self.default_css, 'text/css'
            if path == '/':
                return 301, '/summary.html', 'text/html'
            return 404, None, None
        except Exception:
            import traceback
            print ('While handling %r:' % path)
            traceback.print_exc(file=sys.stderr)
            return 500, None, None

    def summary_page(self):
        escape = cgi.escape
        mostrecent = self.server.mostrecent

        starttime = escape(self.server.starttime.strftime(self.datefmt))
        uptime = datetime.datetime.now() - self.server.starttime
        uptime = escape(str(datetime.timedelta(uptime.days, uptime.seconds)))
        logrecordstotal = escape(str(mostrecent.logrecordstotal))

        formatter = self.formatter
        items = []
        for record in reversed(list(mostrecent.db)):
            try:
                cells = escape(formatter.format(record)).split('\n', 4)
                cells = ['<td>%s</td>' % cell for cell in cells]
                cells[-1] = cells[-1].replace('\n', '<br>\n') # message & stack trace
                items.append('<tr class="%s">%s\n</tr>' %
                    (escape(record.levelname.lower()), ''.join(cells)))
            except Exception:
                import traceback
                print >>sys.stderr, 'While generating %r:' % record
                traceback.print_exc(file=sys.stderr)
        records = '\n'.join(items)
        d = dict(starttime=starttime,
                 uptime=uptime,
                 logrecordstotal=logrecordstotal,
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
    logger = logging.getLogger()

    mostrecent = MostRecentHandler()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(mostrecent)

    formatter = logging.Formatter(
        fmt="[%(uuid)s] [%(asctime)s] [%(module)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    # Create file handler
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            '/tmp/cnchi-server.log',
            maxBytes=1000000, backupCount=5)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError as permission_error:
        print("Can't open /tmp/cnchi-server.log : ", permission_error)



    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    myip = s.getsockname()[0]

    # Web monitor
    webmonitor = LoggingWebMonitor(host=myip)
    webmonitor.mostrecent = mostrecent
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
