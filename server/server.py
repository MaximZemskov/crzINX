from time import strftime, gmtime

from eventlet.green import socket as green_socket
from eventlet.green import os as green_os
from server_utils import get_date

import os
import socket
import urllib

SERVER = "crzINX. Zemskov Maxim"
CONNECTION = "keep-alive"

def parse_request(c):
    headers = c.split('\r\n')
    first_line = headers[0].split(' ')
    method = first_line[0]
    url = first_line[1]
    print method
    print url
    url = urllib.unquote(url)
    url = os.path.normpath(url)
    return url, method


def index_respond(url):
    uri = url + "/index.html"
    if os.path.isfile(uri):
        f = open(uri, "rb")
        http_response = "Date: " + get_date() + '\r\n'
        http_response += "Sever: {}".format(SERVER) + '\r\n'
        http_response += "Content-Length: {}".format(os.path.getsize(uri)) + '\r\n'
        # http_response += "Content-Type: {}".format() + '\r\n'
        http_response += "Connection: {}".format(CONNECTION) + '\r\n'
        return f, http_response
    else:
        respond_404(uri)


def file_respond(url):
    pass


def respond_404(url):
    pass


def handle(client):
    root_dir = os.getcwd()
    print get_date()
    c = client.recv(1024)
    print c
    try:
        url, method = parse_request(c)
        if os.path.isdir(root_dir + url):
            body, headers = index_respond(root_dir + url)
            client.sendall(headers)
            if body:
                l = body.read(4096)
                while l:
                    client.send(l)
                    l = body.read(4096)
                body.close()
            print "Directory exist"
        elif os.path.isfile(root_dir + url):
            # file_respond
            print "File exist"
        else:
            # respond_404
            print 404
    except Exception as e:
        print e
    finally:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
