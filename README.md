# SockScribe
A lightweight Python library for sending and writing real-time data to a CSV file using **sockets**.

**SockScribe** is a Python library which contains classes to be used in your programs to send, recieve, and append real-time data to a CSV file between two devices.

### Setting up a server
```python
import server

# initialize a server by giving the desired address, port, and CSV file path.
sample_server = server.Server("127.0.0.1", 65432, "sample.csv")
# start the server.
sample_server.start()
```

### Setting up a client and sending data
```python
import client

user = "Luis"
message = "Hey!"
datetime = "2003-12-24 12:00:00.000000"

# set up a client by simply giving the address and port
sample_client = client.Client("127.0.0.1", 65432)
# format your fields then send your data!
data = user + "," + message + "," + datetime
sample_client.send_data(data)
```