import select
import socket
import struct
import threading
import time


class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind(('', 0))
        self.readers = []
        self.writers = []
        self.rbuff = ''
        self.wbuff = ''
        self.reader_callback = None
        self.quit = False

    def _senddata(self, writer):
        sentcount = 0
        bufferlen = len(self.wbuff)
        while sentcount < bufferlen:
            sent = self.client.sendto(
                self.wbuff[sentcount:], ('127.0.0.1', 5000))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            sentcount += sent
            if sentcount == bufferlen:
                self.wbuff = ''
                self.writers.remove(writer)

    def _recvdata(self):
        SVR_RESP = '\FF'
        data = ""
        try:
            while True:
                chunk = self.client.recvfrom(1024)
                if chunk == '':
                    raise RuntimeError("socket connection broken")

                data = data + chunk[0]
        except:
            pass
        finally:
            if not self.reader_callback == None:
                self.reader_callback(data)

    def cycle(self):
        try:
            self._stop = False
            self.client.settimeout(1)
            while self._stop == False:
                rlist, wlist, xlist = select.select(
                    self.readers, self.writers, [], 1)
                for reader in rlist:
                    self._recvdata()
                for writer in wlist:
                    self._senddata(writer)

        except Exception as e:
            print "An error occurred in Client.cycle()\n" + str(e)

    def close(self):
        try:
            # Should shutdown, but gives me an error - related to UDP?
            # self.server.shutdown(socket.SHUT_RD)
            self.client.close()
            self._stop = True
        except Exception as e:
            print("An error occurred in Listener.close():\n" + str(e))


def callback(message):
    print(message)


if __name__ == "__main__":

    # Create client and listen for incoming responses
    client = Client()
    client.readers.append(client.client)
    client.reader_callback = callback
    listener_thread = threading.Thread(target=client.cycle)
    listener_thread.start()

    # Wait 3 seconds before broadcasting 0x00
    # time.sleep(3)
    client.wbuff = 'r /storage'
    client.writers.append(client.client)

    # Wait for a timeout period (in case of slow resp) before closing
    time.sleep(10)
    client.close()
