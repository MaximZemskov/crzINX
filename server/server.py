from time import strftime, gmtime

from eventlet.green import socket

import urllib
import os


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

    pass


def file_respond(url):
    pass


def respond_404(url):
    pass


def handle(client):
    root_dir = os.getcwd()
    while True:
        c = client.recv(1024)
        print c
        try:
            url, method = parse_request(c)
            if os.path.isdir(root_dir + url):
                # index_respond()
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
