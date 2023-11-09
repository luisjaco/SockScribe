
import sys
import socket
import selectors
import traceback
import libclient

class Client:
    def __init__(self, host: str, port: int):
        """
        Client to send data to a server.\n
        Parameters:\n
            host-- the host address of the server\n
            port-- the port number of the server\n
        Returns: a Client instance.
        """
        self.host = host
        self.port = port
        print(f"Set connection to {host}, {port}")

    def _create_request(self, data):
        return dict(
            encoding="utf-8",
            content=dict(value=data)
        )
    
    def _start_connection(self, host, port, request):
        self.sel = selectors.DefaultSelector()
        addr = (host, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        # Creates events.
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(self.sel, sock, addr, request)
        self.sel.register(sock, events, data=message) # Registers a file object, adds it to events.

    def _event_loop(self):
        try:
            while True:
                events = self.sel.select(timeout=1)
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
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

    def send_data(self, data):
        """
        Initiates the protocol to send data to the server Client is connected to.\n
        Parameters:\n
            data -- data to be sent to the server\n
        """
        if isinstance(data, str):
            request = self._create_request(data)
            self._start_connection(self.host, self.port, request)
            self._event_loop()
        else:
            print("Given data is not type string, exiting.")
            sys.exit(1)

testing = Client('127.0.0.1', 65432)
while True:
    print("Give something to say: ", end="")
    testing.send_data(input())