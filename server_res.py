from server import server_utils

import os
import socket
import urllib

SERVER = "crzINX. Maxim Zemskov"
CONNECTION = "keep-alive"


def http_response_template(status, content_length, content_type, httpv='HTTP/1.1'):
    http_response = "{} {}".format(httpv, status) + '\r\n'
    http_response += "Date: " + server_utils.get_date() + '\r\n'
    http_response += "Server: {}".format(SERVER) + '\r\n'
    http_response += "Content-Length: {}".format(content_length) + '\r\n'
    http_response += "Connection: {}".format(CONNECTION) + '\r\n'
    http_response += "Content-Type: {}".format(content_type) + '\r\n'
    http_response += '\r\n'
    return http_response


def respond_file(path, method):
    f = open(path, 'rb')
    status = '200 OK'
    content_length = os.path.getsize(path)
    c_type = path.split('.')[-1].lower()
    content_type = server_utils.check_content_type(c_type)
    http_response = http_response_template(status, content_length, content_type)
    if method == 'GET':
        return http_response, f
    else:
        f.close()
        f = False
        return http_response, f


def respond_error(code, reason, method, path):
    if code == 403:
        path += '/server/403.html'
        f = open(path, 'rb')
    elif code == 404:
        path += '/server/404.html'
        f = open(path, 'rb')
    elif code == 400:
        path += '/server/400.html'
        f = open(path, 'rb')
    else:
        path = '/server/404.html'
        f = open(path, 'rb')
        print "0.o0.o0.o0.o0.o0.o0.o0.o"
    status = str(code) + ' {}'.format(reason)
    content_type = 'text/html'
    content_length = os.path.getsize(path)
    http_response = http_response_template(status, content_length, content_type)
    if method == 'HEAD':
        f.close()
        f = False
        return http_response, f
    else:
        return http_response, f


def handle(client):
    root_dir = os.getcwd()
    try:
        c = client.recv(10000)
        request_headers = c.decode().split("\r\n")
        request = request_headers[0].split(' ')
        method, url, httpv = request[0], request[1], request[2]
        url = urllib.unquote(url).decode('utf8')
        if method not in ['GET', 'HEAD'] or '..' in url:
            # bad request
            headers, body = respond_error(400, 'Bad request', method, root_dir)
            if method == 'POST':
                print headers
                print body
            client.sendall(headers)
            if body:
                server_utils.data_send(client, body)
                body.close()
        else:
            cur_path = root_dir + url
            if '?' in cur_path:
                cur_path = cur_path.split('?')[0]
            if os.path.isdir(cur_path):
                cur_path += '/index.html'
                if os.path.isfile(cur_path):
                    headers, body = respond_file(cur_path, method)
                    client.sendall(headers)
                    if body:
                        server_utils.data_send(client, body)
                        body.close()
                else:
                    headers, body = respond_error(403, 'Forbidden', method, root_dir)
                    client.sendall(headers)
                    if body:
                        server_utils.data_send(client, body)
                        body.close()
            elif os.path.isfile(cur_path):
                headers, body = respond_file(cur_path, method)
                client.sendall(headers)
                if body:
                    server_utils.data_send(client, body)
                    body.close()
            else:
                headers, body = respond_error(404, 'Not Found', method, root_dir)
                client.sendall(headers)
                if body:
                    server_utils.data_send(client, body)
                    body.close()
        print(request)
    except Exception as e:
        print e
    finally:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
