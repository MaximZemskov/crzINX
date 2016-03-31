#!/usr/bin/python3

import argparse
import os


def parse():
    parser = argparse.ArgumentParser(description='crzINX. Simple http server')
    parser.add_argument('-b', '--bind', type=str, help='Host name. Default: 0.0.0.0', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, help='Port number. Example: 8080. Default: 8080', default=8080)
    parser.add_argument('-r', '--rootdir', type=str, help='ROOTDIR. Example: /home/user/web_prj', default=os.getcwd())
    parser.add_argument('-c', '--cpu', type=int, help='NCPU. CPU number', default=1)
    args = parser.parse_args()
    host = args.bind
    port = args.port
    root_dir = os.path.normpath(args.rootdir)
    cpu_number = args.cpu
    is_dir = os.path.isdir(root_dir)
    if not is_dir:
        print('{} this derictory does not exist. Would you want to create it?'.format(root_dir))
        answer = input('--> ')
        if (answer == 'y') or (answer == 'Y') or (answer == 'yes') or (answer == 'Yes'):
            try:
                os.makedirs(root_dir)
            except IOError as e:
                print(e)
            else:
                print("Success!")
        else:
            print("Current dir will use as root. {}".format(os.getcwd()))
    print("Args:\nhost - {}\nport - {}\nroot_dir - {}\ncpu_number - {}".format(host, port, root_dir, cpu_number))
    return host, port, root_dir, cpu_number


def init_logger(root_dir):
    log_dir = root_dir + "/aelogs"
    is_dir = os.path.isdir(os.path.normpath(log_dir))
    if not is_dir:
        try:
            os.makedirs(log_dir)
        except IOError as e:
            print(e)
            exit(1)