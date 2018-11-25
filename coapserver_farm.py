#!/usr/bin/env python

import getopt
import sys
import socket
import threading
import random
from coapthon.server.coap import CoAP
from exampleresources import *

__author__ = 'Felipe Brizola'

class AvailableResources():
    def __init__(self, uri=None, resource_class=None):
        self.uri = uri
        self.resource_class = resource_class

    def get_all(self):
        list = []

        list.append(AvailableResources('/temperature', TemperatureResource))
        list.append(AvailableResources('/identifier', IdentifierResource))
        list.append(AvailableResources('/weight', WeightResource))
        list.append(AvailableResources('/food', FoodResource))
        list.append(AvailableResources('/water', WaterResource))

        return list

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))

        self.add_resource('/temperature', TemperatureResource())
        self.add_resource('/identifier', IdentifierResource())
        self.add_resource('/weight', WeightResource())
        self.add_resource('/food', FoodResource())
        self.add_resource('/water', WaterResource())

        print 'CoAP Server start on ' + host + ':' + str(port)
        print self.root.dump()

def worker(server):

    print 'worker running on address: ' + str(server.server_address[0]) + ' and port ' + str(5000)

    worker_server_address = (server.server_address[0], 5000)
    sock_worker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_worker.bind(worker_server_address)

    while True:
        try:
            data, client_address = sock_worker.recvfrom(1024)

            operation = data[0]
            resource = data[2:]

            if operation == 'l':
                sock_worker.sendto('    Resources: ' + str(server.root.dump()), client_address)  
                continue

            for r in AvailableResources().get_all():
                if (r.uri == resource):

                    if operation == 'a':
                        if server.add_resource(r.uri, r.resource_class()):
                            sock_worker.sendto('    Resource created: ' + str(server.root.dump()), client_address)                
                        else:
                            sock_worker.sendto('    Resource not created: ' + str(server.root.dump()), client_address)                
                        continue
                    elif operation == 'd':
                        if server.remove_resource(r.uri):
                            sock_worker.sendto('    Resource removed: ' + str(server.root.dump()), client_address)
                        else:
                            sock_worker.sendto('    Resource not removed: ' + str(server.root.dump()), client_address)
                        continue
                
            sock_worker.sendto('    Resource not found', client_address)
                        

        except socket.timeout:
            print 'TIMEOUT'
            continue    

def usage():
    print 'resource not found'


if __name__ == '__main__':  # pragma: no cover

    ip = socket.gethostbyname(socket.gethostname())
    port = 5683
    server = CoAPServer(ip, port)
    threading.Thread(target=worker, args=(server,)).start()

    try:
        server.listen(10)
    except KeyboardInterrupt:
        print 'Server Shutdown'
        server.close()
        print 'Exiting...'
    finally:
        server.close()