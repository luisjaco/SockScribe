"""
This module is a demonstration for the Server class. To be used with sample_client.py.

This module will listen for data, then append to the "sample.csv" CSV file. It
will loop until interrupted.
"""
import server

# To set up a server, initialize the Server class with a valid host
# address, port, file path, and a dilimiter (default=',').
sample_server = server.Server("127.0.0.1", 65432, "sample.csv")

# To begin listening for messages, simply use the start function.
sample_server.start()