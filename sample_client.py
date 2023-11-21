import client
import datetime

user = "Luis"
sample_client = client.Client("127.0.0.1", 65432)

while True:
    print("Enter a message: ", end="")
    message = input()
    time = str(datetime.datetime.now())
    sample_client.send_data(user + "," + message + "," + time)
    