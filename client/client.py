
import sys
import socket
import selectors
import traceback
from libclient import Message

class Client:
    """
    The Client class handles sending data to a server.

    You can send data by creating a Client object, then using the send_data method.
    """
    def __init__(self, host: str, port: int):
        """
        Instantiates a Client class, sets the connection to a specific host and port.
        
        Args:
            host: the host address of the server.
            port: the port number of the server.
        """
        self._host = host
        self._port = port
        print(f"Set connection to {host}, {port}")

    def _create_request(self, data):
        return dict(
            encoding="utf-8",
            content=dict(value=data)
        )
    
    def _start_connection(self, request):
        self._sel = selectors.DefaultSelector()
        addr = (self._host, self._port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        # Creates events.
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = Message(self._sel, sock, addr, request)
        self._sel.register(sock, events, data=message) # Registers a file object, adds it to events.

    def _event_loop(self):
        try:
            while True:
                events = self._sel.select(timeout=1)
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
                if not self._sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self._sel.close()

    def send_data(self, data: str) -> None:
        """
        Sends data to the set connection.

        Formats str data, creates socket between client and server, creates a Message, 
        then sends data to server.

        Args:
            data: the data to be sent to the server.
        """
        if isinstance(data, str):
            request = self._create_request(data)
            self._start_connection(request)
            self._event_loop()
        else:
            print("Given data is not type string, exiting.")
            sys.exit(1)

testing = Client('127.0.0.1', 65432)
while True:
    print("Give something to say: ", end="")
    testing.send_data(input())