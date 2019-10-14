import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyagender import PyAgender
import cv2
import logging
import cgi
import json
import shutil
import random
import string
import numpy

BASE62_CHARSET=string.ascii_lowercase + string.digits + string.ascii_uppercase

def rand_string(n=8, charset=BASE62_CHARSET):
    res = ""
    for i in range(n):
        res += random.choice(charset)
    return res

def sanitize_json(data):
    data = bytes(json.loads(json.dumps(str(data))), 'utf8')
    return data

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        elements = self._set_headers()

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE":   self.headers['Content-Type']
            })

        dirpath = os.getcwd()
        _, ext = os.path.splitext(form["file"].filename)

        file_name = rand_string() + ext
        while os.path.isfile(file_name):
            file_name = rand_string() + ext

        fdst = open(file_name, "wb")
        shutil.copyfileobj(form["file"].file, fdst)
        fdst.close()

        agender = PyAgender()
        faces = agender.detect_genders_ages(cv2.imread(file_name))
        os.remove(file_name)
        self.wfile.write(sanitize_json(faces))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
