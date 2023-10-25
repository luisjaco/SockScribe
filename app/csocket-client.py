#!/usr/bin/env python3
# made it so it works, just need to clean it up at a later point
# TODO clean up.

import sys
import socket
import selectors
import traceback

import csocket_libclient as libclient 

sel = selectors.DefaultSelector()

# Data that will be sent when program starts. Later should be through system argument.
data = "apples!!! -luis jaco."

def create_request(data):
    return dict(
        encoding="utf-8",
        content=dict(value=data)
    )

def start_connection(host, port, request):
    addr = (host, port)
    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    # Creates events.
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message) # Registers a file object, adds it to events.


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

# initializing a connection
host, port = sys.argv[1], int(sys.argv[2])
# data = sys.argv[3]
request = create_request(data) # Add request into the events of the socket.
start_connection(host, port, request)

# Handles all events. First event to go is the writing event.
def send_and_recieve():
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask) # gets called when either writing or reading data in the events dict
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

send_and_recieve()
