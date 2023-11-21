import server

sample_server = server.Server("127.0.0.1", 65432, "sample.csv")
sample_server.start()