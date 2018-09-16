import select
import socket
import struct
import threading
import time


class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind(('', 9090))

    def _recvdata(self):
        data = ""
        try:
            while True:
                print "waiting data"
                chunk = self.client.recvfrom(1024)

                if chunk == '':
                    raise RuntimeError("socket connection broken")
                
                print 'chunk 1', chunk[1]
                data = data + chunk[0]
                self.client.sendto(chunk[0], chunk[1])

        except Exception as e:
            print "An error occurred in Client.cycle()\n" + str(e)
    


if __name__ == "__main__":

    # Create client and listen for incoming responses
    client = Client()
    
    client._recvdata()