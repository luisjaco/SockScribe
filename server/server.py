import socket
import selectors
import traceback
import libserver
import csv_editor
import sys
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
            delimiter-- delimiter expected to receive from client.\n
        Returns: a Server instance.
        """
        self.file_editor = csv_editor.CSVEditor(path, delimiter)
        self.host = host
        self.port = port

    def start(self):
        """
        Starts the server
        """
        sel = selectors.DefaultSelector()
        self._start_connection(sel)
        self._event_loop(sel)

    def _accept_wrapper(self, sock, sel):
        conn, addr = sock.accept()  # Blocks execution and waits for incoming connection
        # Confirm connection is accepted
        print(f"{addr[0]}, {addr[1]}")
        conn.setblocking(False)
        message = libserver.Message(sel, conn, addr)
        sel.register(conn, selectors.EVENT_READ, data=message)

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
                            sel.close()
                            sys.exit(1)
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

testing = Server('127.0.0.1', 65432, 'csv_example.csv', ',')
# testing = Server('64.187.251.230', 50663, 'csvtesting.csv', '-')
testing.start()