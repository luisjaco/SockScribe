"""
This module is a demonstration of the Client class. To be used with sample_server.py.

This module will send data in the format (user, message, datetime) to a server.
It will loop until interrupted.
"""
import client
import datetime

user = "Luis"

# To create a client, simply initialize a Client with the host address and port.
sample_client = client.Client("127.0.0.1", 65432)

try:
    while True:
        print("Enter a message: ", end="")
        message = input()
        time = str(datetime.datetime.now())

        # To send data, format the data with the set dilimiter and use the send_data function.
        sample_client.send_data(user + "," + message + "," + time)
except KeyboardInterrupt:
    print("\nCaught keyboard interrupt, exiting.")