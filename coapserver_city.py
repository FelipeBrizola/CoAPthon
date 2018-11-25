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
        
        # cameras, sensor de presenca, controle de luzes

        list.append(AvailableResources('/sensor-light', LightResource))
        list.append(AvailableResources('/sensor-presence', PresenceResource))
        list.append(AvailableResources('/cam-front', CamResource))
        list.append(AvailableResources('/cam-back', CamResource))
        list.append(AvailableResources('/cam-right', CamResource))
        list.append(AvailableResources('/cam-left', CamResource))

        return list

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))

        all_resources = AvailableResources().get_all()

        # quantidade de recursos por nodo
        quantity = random.randint(0, len(all_resources))

        # lista com id dos recursos
        ids = random.sample(range(0, quantity), quantity)

        for id in ids:
            if  id == 0:
                self.add_resource('/sensor-light', LightResource()) # 0
            elif id == 1:
                self.add_resource('/sensor-presence', PresenceResource()) # 1
            elif id == 2:
                self.add_resource('/cam-front', CamResource()) # 2
            elif id == 3:
                self.add_resource('/cam-back', CamResource()) # 3
            elif id == 4:
                self.add_resource('cam-right', CamResource()) # 2
            elif id == 5:
                self.add_resource('cam-left', CamResource()) # 3


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