import socket
import sys

HOST = "localhost"   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	sct.connect((HOST,PORT))
except Exception as e:
	print e
	sys.exit(1)

while True:
    print "[RESPONSE] Server: ", sct.recv(1024)
    data = raw_input("[REQUEST] Client: ")
    sct.sendall(data)

sys.exit(0)