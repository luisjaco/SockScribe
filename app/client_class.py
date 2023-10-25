
import sys
import socket
import selectors
import traceback

import csocket_libclient as libclient 

# TODO make this into a class which can be used in other files.
# TODO we made everything work for the most part, just need to change it and make it into how we vision it.
class Client:
    def __init__(self, host, port):
        self.sel = selectors.DefaultSelector()
        self.host = host
        self.port = port

        def send_data(data):
            if data.isinstance(str):
                request = _create_request(data)
                _start_connection(self.host, self.port, request)
                _events()
            else:
                print("Given data is not in string format, exiting.")
                sys.exit(1)

        def _create_request(data):
            return dict(
                encoding="utf-8",
                content=dict(value=data)
            )
        
        def _events():
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
                self.sel.close()


        def _start_connection(host, port, request):
            addr = (host, port)
            print(f"Starting connection to {addr}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(addr)
            # Creates events.
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            message = libclient.Message(self.sel, sock, addr, request)
            self.sel.register(sock, events, data=message) # Registers a file object, adds it to events.

