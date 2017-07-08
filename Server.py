#from sage.all import *
import socket
import thread
import sys
 
HOST = "localhost"   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port
 
sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'
 
try:
    sct.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'
 
sct.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
        conn.sendall(reply)
 
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = sct.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    thread.start_new_thread(clientthread ,(conn,))
 
sct.close()