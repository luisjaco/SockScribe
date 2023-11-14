import socket
import selectors
import traceback
import sys
import csv_editor
from libserver import Message

class Server:
    """
    The Server class handles creating a server and receiving messages.

    You can start a socket server by initializing a Server object, then using the
    start method.
    """
    def __init__(self, host: str, port: int, path: str, delimiter: str=","):
        """
        Instantiate a Server class, takes in server information along with file information.

        Args:
            host: host address for creating a Socket server.
            port: port number for creating a Socket server.
            path: file path for the csv file used in receiving data.
            delimiter: delimiter for the csv data. default is ",".
        """
        self._file_editor = csv_editor.CSVEditor(path, delimiter)
        self._host = host
        self._port = port

    def _start_connection(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Socket details
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Socket output details
        lsock.bind((self._host, self._port))
        lsock.listen()
        print(f"Listening on {self._host}, {self._port}")
        lsock.setblocking(False)
        self._sel.register(lsock, selectors.EVENT_READ, data=None)

    def _event_loop(self):
        try:
            while True:
                events = self._sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self._accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask, self._file_editor)
                        except FileNotFoundError:
                            self.stop(True)
                        except Exception:
                            print(
                                f"Main: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            message.close()
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting")
        finally:
            self.stop()

    def _accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Blocks execution and waits for incoming connection
        # Confirm connection is accepted
        print(f"{addr[0]}, {addr[1]}")
        conn.setblocking(False)
        message = Message(self._sel, conn, addr)
        self._sel.register(conn, selectors.EVENT_READ, data=message)

    def stop(self, exit=False):
        """
        Stop the server.
        
        Args:
            exit: if true will exit the console. default is False."""
        self._sel.close()
        if exit:
            sys.exit(1)

    def start(self) -> None:
        """
        Start the server.

        This method will create a socket server then begin to listen for messages,
        presumably from another device using the Client class. The server will wait
        for any incoming messages. Messages will be handled and then appended to the 
        csv file. The server will close once a keyboard interuption is caught.
        """
        self._sel = selectors.DefaultSelector()
        self._start_connection()
        self._event_loop()

testing = Server('127.0.0.1', 65432, 'sample.csv')
testing.start()