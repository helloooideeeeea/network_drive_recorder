from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir("www")
port = 5555

httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
httpd.serve_forever()