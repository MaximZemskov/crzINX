from time import strftime, gmtime

from eventlet.green import socket as green_socket
from eventlet.green import os as green_os
from server_utils import *

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
    url = urllib.unquote(url)
    url = os.path.normpath(url)
    split_url = url.split(".")
    if len(split_url) == 2:
        content_type = split_url[-1]
        return url, method, content_type
    elif len(split_url) == 1:
        content_type = "html"
        return url, method, content_type
    content_type = "bad"
    return url, method, content_type


def respond(http_version, status, content_length, content_type):
    http_response = "{} {}".format(http_version, status) + '\r\n'
    http_response += "Date: " + get_date() + '\r\n'
    http_response += "Sever: {}".format(SERVER) + '\r\n'
    http_response += "Content-Length: {}".format(content_length) + '\r\n'
    http_response += "Connection: {}".format(CONNECTION) + '\r\n'
    http_response += "Content-Type: {}".format(content_type) + '\r\n'
    http_response += '\r\n'
    return http_response


def index_respond(url, content_type):
    uri = url + "/index.html"
    if os.path.isfile(uri):
        f = open(uri, "rb")
        http_version = "HTTP/1.1"
        status = "200 OK"
        content_length = os.path.getsize(uri)
        http_response = respond(http_version, status, content_length, content_type)
        return f, http_response
    else:
        respond_403(uri)


def file_respond(url, content_type):
    if os.path.isfile(url):
        f = open(url, "rb")
        http_version = "HTTP/1.1"
        status = "200 OK"
        content_length = os.path.getsize(url)
        http_response = respond(http_version, status, content_length, content_type)
        return f, http_response
    else:
        respond_404()


def respond_403(url):
    pass


def respond_404(url):
    pass


def handle(client):
    root_dir = os.getcwd()
    print get_date()
    c = client.recv(1024)
    print c
    try:
        url, method, content_type = parse_request(c)
        content_type = check_content_type(content_type)
        if os.path.isdir(root_dir + url):
            body, headers = index_respond((root_dir + url), content_type)
            client.sendall(headers)
            if body:
                data_send(client, body)
                body.close()
            print "Directory exist"
        elif os.path.isfile(root_dir + url):
            body, headers = file_respond((root_dir + url), content_type)
            client.sendall(headers)
            if body:
                data_send(client, body)
                body.close()
                # TODO: DRY
            print "File exist"
        else:
            # respond_404
            print 404
    except Exception as e:
        print e
    finally:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
