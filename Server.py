import socket               # Import socket module


def CreateWords():

    print(word)

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print("Got connection from:" + str(addr))
    c.send(b'This message was sent from the server!')
    c.close()                # Close the connection
