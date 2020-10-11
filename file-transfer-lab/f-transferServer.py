#! /usr/bin/env python3

import sys, os
sys.path.append("../lib")       # for params
import re, socket, params

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

#sock, addr = lsock.accept()

#print("connection rec'd from", addr)

from framedSock import framedSend, framedReceive

while True:
        sock, addr = lsock.accept()
        if not os.fork():
                break
        payload, contents = framedRecieve(sock, debug)
        if not payload:
                sys.exit(1)

        filename = payload.decode()
        if filename:
                output = open(filename, 'wb')
                output.write(contents)
                output.close
                print("File", filename, "accepted")
                sys.exit(1)
        else:
                print("File", filename, "not accepted")
                sys.exit(1)
