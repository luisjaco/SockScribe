# SockScribe
A lightweight Python library for sending and receiving real-time data across a network, using **sockets**.

`SockScribe` is a Python library which contains classes to be used in your programs to send and receive data between a server and other client devices. Received data will be stored to a CSV file locally on the server device.

> [!NOTE]  
> This library is intended to be used with Raspberry Pi programs; however, it can be used on other devices without an issue.

### Installation

```bash
$ git clone https://github.com/luisjaco/SockScribe
```

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

# set up a client by simply giving the address and port.
sample_client = client.Client("127.0.0.1", 65432)

# format your fields then send your data!
data = user + "," + message + "," + datetime
sample_client.send_data(data)
```

### License
[MIT](https://choosealicense.com/licenses/mit/)
