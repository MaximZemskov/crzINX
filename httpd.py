import eventlet
import sys
from utils.utils import *
from server.server import *
# from server_res import *


def main():
    print("Main function starts")
    host, port, root_dir, cpu_number = parse()
    access_log, error_log = init_logger(root_dir)

    os.chdir(root_dir)

    server = eventlet.listen((host, port), backlog=100)
    print "Server starts on {}:{}".format(host, port)
    logger("Server starts on {}:{}".format(host, port), access_log)

    for i in range(cpu_number):
        pid = os.fork()
        if pid == 0:
            pool = eventlet.GreenPool(10000)
            child_pid = os.getpid()
            while True:
                try:
                    new_sock, address = server.accept()
                    pool.spawn_n(handle, new_sock)
                except (SystemExit, KeyboardInterrupt):
                    sys.exit(1)
    try:
        os.waitpid(-1, 0)
    except KeyboardInterrupt:
        sys.exit()

    logger("Shutdown server.", access_log)
    access_log.close()
    error_log.close()


if __name__ == '__main__':
    main()
