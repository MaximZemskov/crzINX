import server_utils as server_utils

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


# from time import strftime, gmtime
#
# from eventlet.green import socket as green_socket
# from eventlet.green import os as green_os
# from server_utils import *
#
# import os
# import socket
# import urllib
#
# SERVER = "crzINX. Zemskov Maxim"
# CONNECTION = "keep-alive"
#
#
# def parse_request(c):
#     headers = c.split('\r\n')
#     first_line = headers[0].split(' ')
#     method = first_line[0]
#     url = first_line[1]
#     url = urllib.unquote(url)
#     url = os.path.normpath(url)
#     split_url = url.split(".")
#     if len(split_url) == 2:
#         content_type = split_url[-1]
#         return url, method, content_type
#     elif len(split_url) == 1:
#         content_type = "html"
#         return url, method, content_type
#     # !TODO: JS and PNG fails here
#     content_type = "bad"
#     return url, method, content_type
#
#
# def respond(http_version, status, content_length, content_type='application/octet-stream'):
#     http_response = "{} {}".format(http_version, status) + '\r\n'
#     http_response += "Date: " + get_date() + '\r\n'
#     http_response += "Sever: {}".format(SERVER) + '\r\n'
#     http_response += "Content-Length: {}".format(content_length) + '\r\n'
#     http_response += "Connection: {}".format(CONNECTION) + '\r\n'
#     http_response += "Content-Type: {}".format(content_type) + '\r\n'
#     http_response += '\r\n'
#     return http_response
#
#
# def index_respond(url, content_type, method):
#     uri = url + "/index.html"
#     if os.path.isfile(uri):
#         f = open(uri, "rb")
#         http_version = "HTTP/1.1"
#         status = "200 OK"
#         content_length = os.path.getsize(uri)
#         http_response = respond(http_version, status, content_length, content_type)
#         if method == "GET":
#             return f, http_response
#         elif method == "HEAD":
#             f = False
#             return f, http_response
#     else:
#         http_response = respond_403()
#         f = False
#         return f, http_response
#
#
# def file_respond(url, content_type, method):
#     if os.path.isfile(url):
#         f = open(url, "rb")
#         http_version = "HTTP/1.1"
#         status = "200 OK"
#         content_length = os.path.getsize(url)
#         http_response = respond(http_version, status, content_length, content_type)
#         if method == "GET":
#             return f, http_response
#         elif method == "HEAD":
#             f = False
#             return f, http_response
#     else:
#         respond_404()
#
#
# def respond_403():
#     http_version = "HTTP/1.1"
#     status = "403 Forbidden"
#     http_response = respond(http_version, status, 0, 'application/octet- stream')
#     return http_response
#
#
# def respond_404(url):
#     pass
#
#
# def handle(client):
#     root_dir = os.getcwd()
#     print get_date()
#     c = client.recv(1024)
#     print c
#     try:
#         url, method, content_type = parse_request(c)
#         content_type = check_content_type(content_type)
#         if os.path.isdir(root_dir + url):
#             body, headers = index_respond((root_dir + url), content_type, method)
#             client.sendall(headers)
#             if body:
#                 data_send(client, body)
#                 body.close()
#             print "Directory exist"
#         elif os.path.isfile(root_dir + url):
#             body, headers = file_respond((root_dir + url), content_type, method)
#             client.sendall(headers)
#             if body:
#                 data_send(client, body)
#                 body.close()
#             print "File exist"
#         else:
#             # respond_404
#             print 404
#     except Exception as e:
#         print e
#     finally:
#         client.shutdown(socket.SHUT_RDWR)
#         client.close()
