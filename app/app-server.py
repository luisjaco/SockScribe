#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()

# setup (.socket, .bind, .listen) -> 
# listening
# get connection (events = sel.select)
# receive data (message = key.data)
# try to process when data is full (accept_wrapper) ->
# process message in Message ->
# send back message to declare success (sel.register)

def accept_wrapper(sock):
    conn, addr = sock.accept()  # blocks execution and waits for incoming connection
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

# Setting up the socket to listen for connections
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket details
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #output socket
lsock.bind((host, port)) # associates socket with host and port number
lsock.listen() # has the socket listen for connections
print(f"Listening on {(host, port)}") 
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:

                accept_wrapper(key.fileobj)
            else:
                # the .data of key is the message class from client
                message = key.data
                try:
                    # then we try to process the data
                    message.process_events(mask)
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()