#!/usr/bin/python3
from utils.utils import *
import eventlet


def main():
    print("Main function starts")
    host, port, root_dir, cpu_number = parse()
    access_log, error_log = init_logger(root_dir)
    print "Server starts on {}:{}".format(host, port)
    logger("Server starts on {}:{}".format(host, port), access_log)

    logger("Shutdown server.", access_log)
    access_log.close()
    error_log.close()

if __name__ == '__main__':
    main()
