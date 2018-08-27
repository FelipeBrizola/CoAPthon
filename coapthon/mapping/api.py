import socket
import sys
import getopt
import json

class Datagram():
    def __init__(self, add_resource=None, del_resource=None, list_resource=False):
        self.add_resource = add_resource
        self.del_resource = del_resource
        self.list_resource = list_resource

def usage():  # pragma: no cover
    print 'api_local.py -ar'


def main(argv):  # pragma: no cover
    ip = '127.0.0.1'
    port = 5000
    datagram = Datagram()

    try:
        opts, args = getopt.getopt(
            argv, 'a:d:l', ['add_resource=', 'del_resource=', 'list_resource'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-a', '--add_resource'):
            datagram.add_resource = arg
        elif opt in ('-d', '--del_resource'):
            datagram.del_resource = arg
        elif opt in ('-l', '--list_resource'):
            datagram.list_resource = True

    # object to json
    print 'SEND DATAGRAM ', json.dumps(datagram.__dict__)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(datagram.__dict__), (ip, port))


if __name__ == '__main__':  # pragma: no cover
    main(sys.argv[1:])
