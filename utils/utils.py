import argparse
import os
import time


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
        print('{} this directory does not exist. Would you want to create it?'.format(root_dir))
        answer = raw_input('--> ')
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
    log_dir = os.path.normpath(root_dir + "/aelogs")
    is_dir = os.path.isdir(log_dir)
    access_log_path = os.path.normpath(log_dir + "/access.log")
    error_log_path = os.path.normpath(log_dir + "/error.log")
    access_log = False
    error_log = False
    if not is_dir:
        try:
            os.makedirs(log_dir)
            access_log = open(access_log_path, 'w')
            error_log = open(error_log_path, 'w')
        except IOError as e:
            print(e)
            exit(1)
    else:
        try:
            access_log = open(access_log_path, 'a')
            error_log = open(error_log_path, 'a')
        except IOError as e:
            print (e)
            exit(1)
    return access_log, error_log


def logger(msg, f):
    f.write(time.ctime() + " : " + msg + "\n")
