import socket
import selectors
import traceback
import sys
import csv_editor
import libserver

class Server:
    def __init__(self, host: str, port: int, path: str, delimiter: str=','):
        """
        Server to recieve data from a client.\n
        Parameters:\n
            host-- Host address of the server.\n
            port-- Port number of the server.\n
            path-- Path of the csv file this server will append.\n
            delimiter-- delimiter expected to receive from client.\n
        Returns: a Server instance.
        """
        self.file_editor = csv_editor.CSVEditor(path, delimiter)
        self.host = host
        self.port = port

    def _start_connection(self, sel):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket details
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Socket output details
        lsock.bind((self.host, self.port))
        lsock.listen()
        print(f"Listening on {self.host}, {self.port}")
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

    def _event_loop(self, sel):
        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self._accept_wrapper(key.fileobj, sel)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask, self.file_editor)
                        except FileNotFoundError:
                            self.stop(sel, True)
                        except Exception:
                            print(
                                f"Main: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            message.close()
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting")
        finally:
            self.stop(sel)

    def _accept_wrapper(self, sock, sel):
        conn, addr = sock.accept()  # Blocks execution and waits for incoming connection
        # Confirm connection is accepted
        print(f"{addr[0]}, {addr[1]}")
        conn.setblocking(False)
        message = libserver.Message(sel, conn, addr)
        sel.register(conn, selectors.EVENT_READ, data=message)

    def start(self):
        """
        Starts the server.
        """
        sel = selectors.DefaultSelector()
        self._start_connection(sel)
        self._event_loop(sel)

    def stop(self, sel, exit=False):
        sel.close()
        if exit:
            sys.exit(1)

testing = Server('127.0.0.1', 65432, 'sample.csv')
testing.start()