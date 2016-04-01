from time import strftime, gmtime

from eventlet.green import socket


def parse_request(c):
    headers = c.split('\r\n')
    first_line = headers[0].split(' ')
    method = first_line[0]
    url = first_line[1]
    print method
    print url


def handle(client):
    while True:
        c = client.recv(1024)
        print c
        try:
            parse_request(c)
            client.sendall(c)
        except Exception as e:
            print e
        finally:
            pass
