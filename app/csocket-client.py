#!/usr/bin/env python3
# so first comes first, we should define how the client will send data
# then worry about how the server will read such data

import sys
import socket
import selectors
import traceback

import csocket_libclient as libclient 

sel = selectors.DefaultSelector()


def create_request(action, value):
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        # this call is sending binary data, i dont really know how it works
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


def create_csv_request(data):
    # data should already be in string format
    return dict(
        encoding="utf-8",
        content=data
    )

# TODO change message class to work with this
def start_connection(host, port, request):
    addr = (host, port)
    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    # actually makes connection
    sock.connect_ex(addr)
    # sets whether the event is read or write
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # all we do is intialize the Message class, nothing more
    message = libclient.Message(sel, sock, addr, request)
    # sends data (message) to socket
    sel.register(sock, events, data=message) 


if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} <host> <port> <action> <value>")
    sys.exit(1)

# initializing a connection
host, port = sys.argv[1], int(sys.argv[2])
action, value = sys.argv[3], sys.argv[4]
#request = create_request(action, value) # creates request using given arguments
request = create_csv_request("um, um, um, um")
start_connection(host, port, request) # starts connection and sends the desired request

# this is for receiving responses from the server and decoding them
try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
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

