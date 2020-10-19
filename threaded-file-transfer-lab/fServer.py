#! /usr/bin/env python3

import sys, os
sys.path.append("../lib")       # for params
import re, socket, params, os

switchesVarDefaults = (
            (('-l', '--listenPort') ,'listenPort', 50001),
            (('-d', '--debug'), "debug", False), # boolean (set if present)
            (('-?', '--usage'), "usage", False), # boolean (set if present)
            )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
            params.usage()

#First the listening socket is created then binding the host with the port
#number. The capacity of the listening socket is 5.
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            payload = self.fsock.receive(debug)
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print(f"thread connected to {addr} done")
                self.fsock.close()
                return          # exit
            payload = payload.decode()
            payload += b"!"             # make emphatic!

            output = open(payload, wb)
            output.write(payload)
            self.fsock.send(payload, debug)

while True:
            sockAddr = lsock.accept()
            server = Server(sockAddr)
            server.start()
