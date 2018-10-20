#!/usr/bin/env python

import getopt
import sys
import socket
import threading
from coapthon.server.coap import CoAP
from exampleresources import BasicResource, Long, Separate, Storage, Big, voidResource, XMLResource, ETAGResource, \
    Child, \
    MultipleEncodingResource, AdvancedResource, AdvancedResourceSeparate

__author__ = 'Felipe Brizola'

class AvailableResources():
    def __init__(self, uri=None, resouce_class=None):
        self.uri = uri
        self.resouce_class = resouce_class

    def get_all(self):
        list = []
        list.append(AvailableResources('/basic', BasicResource))
        list.append(AvailableResources('/storage', Storage))
        list.append(AvailableResources('/separate', Separate))
        list.append(AvailableResources('/long', Long))
        list.append(AvailableResources('/big', Big))
        list.append(AvailableResources('/void', voidResource))
        list.append(AvailableResources('/xml', XMLResource))
        list.append(AvailableResources('/encoding', MultipleEncodingResource))
        list.append(AvailableResources('/etag', ETAGResource))
        list.append(AvailableResources('/child', Child))
        list.append(AvailableResources('/advanced', AdvancedResource))
        
        return list

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))

        self.add_resource('basic/', BasicResource())
        self.add_resource('storage/', Storage())

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
                sock_worker.sendto('    Resouces: ' + str(server.root.dump()), client_address)  
                continue

            for r in AvailableResources().get_all():
                if (r.uri == resource):

                    if operation == 'a':
                        server.add_resource(r.uri, r.resouce_class())
                        sock_worker.sendto('    Resouce created: ' + str(server.root.dump()), client_address)                
                        continue
                    elif operation == 'd':
                        server.remove_resource(r.uri)
                        sock_worker.sendto('    Resouce removed: ' + str(server.root.dump()), client_address)
                        continue
                
            sock_worker.sendto('    Resource not found', client_address)
                        

        except socket.timeout:
            print 'TIMEOUT'
            continue    

def usage():
    print 'resouce not found'


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

