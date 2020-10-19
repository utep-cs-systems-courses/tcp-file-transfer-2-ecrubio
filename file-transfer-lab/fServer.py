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

while True:
        sock, addr = lsock.accept()

        from framedSock import framedSend, framedReceive
        
        if not os.fork():
                while True:
                        payload = framedReceive(sock, debug)
                        if debug: print("rec'd: ", payload)
                        if not payload:
                                break
                        payload = payload.decode()
                
                        output = open(payload, wb)
                        output.write(payload2)
                        sock.close()
