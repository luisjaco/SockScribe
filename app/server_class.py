import sys
import socket
import selectors
import traceback
import os
import csocket_libserver as libserver
from csv_editor import CSVEditor
# TODO remove testing
# TODO make this class more robust: get rid of all the random stuff we dont need and start gearing up for actually being done, cause its done.
# TODO learn documentation
class Server:
    def __init__(self, host: str, port: int, path: str, delimiter: str=','):
        """
        Server to recieve data from a client.\n
        Parameters:\n
            host-- Host address of the server.\n
            port-- Port number of the server.\n
            path-- Path of the csv file this server will append.\n
        Returns: a Server instance.
        """
        self.fileEditor = CSVEditor(path, delimiter)
        self.host = host
        self.port = port
        self.open = False

    def start(self):
        if self.open:
            print("Server already open! Close first server before attempting new server.")
            sys.exit(1)
        else:
            self.open = True
            sel = selectors.DefaultSelector()
            self._start_connection(sel)
            self._events(sel)

    def _accept_wrapper(self, sock, sel):
        conn, addr = sock.accept()  # Blocks execution and waits for incoming connection
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        message = libserver.Message(sel, conn, addr)
        sel.register(conn, selectors.EVENT_READ, data=message)

    def _start_connection(self, sel):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket details
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #output socket
        lsock.bind((self.host, self.port)) 
        lsock.listen() # has the socket listen for connections
        print(f"Listening on {(self.host, self.port)}") 
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

    def _events(self, sel):
        try:
            while True:
                events = sel.select(timeout=None) #TODO implement a timeout field.
                for key, mask in events:
                    if key.data is None:

                        self._accept_wrapper(key.fileobj, sel)
                    else:
                        # the .data of key is the message class from client
                        message = key.data
                        try:
                            # then we try to process the data
                            message.process_events(mask, self.fileEditor)
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
            self.open = False

testing = Server('127.0.0.1', 65432, 'csvtesting.csv', ',')
testing.start()