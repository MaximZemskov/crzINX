from time import gmtime, strftime


CONTENT_TYPE = {
    'txt': 'text/html',
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'swf': 'application/x-shockwave-flash',
    'other': 'application/octet- stream',
}


def get_date():
    return strftime("%a, %d %b %Y %X GMT", gmtime())


def check_content_type(type):
    if type in CONTENT_TYPE:
        return CONTENT_TYPE[type]
    else:
        return CONTENT_TYPE['other']


def data_send(client, body):
    l = body.read(4096)
    while l:
        client.send(l)
        l = body.read(4096)
