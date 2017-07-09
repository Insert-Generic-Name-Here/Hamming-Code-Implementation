from random import randint
from sage.all import *
import HammingWord
import socket
import thread
import json
#import pickle
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
    conn.sendall('[ACK] Communication\n') #send only takes string
    
    q = conn.recv(4)
    #Sending message to connected client
    conn.sendall('[ACK] q Parameter Transmission\n')
    r = conn.recv(4)
    #Sending message to connected client
    conn.sendall('[ACK] r Parameter Transmission\n')
    
    # Creating Same Hamming[n, k] and it's Dual Code [if exists] #
    C = codes.HammingCode(GF(int(q)), int(r))
    print "Prime Code: ", C
    if (C.dual_code() is not None):
        C = C.dual_code()
        print "Dual Code: ", C
        
    wordErr = conn.recv(1024)
    wordErr = json.loads(wordErr)
    print wordErr
    
    #Sending message to connected client
    conn.sendall('[ACK] Message Transmission\n')
    
    wordD = [C.decode_to_message(vec, "Syndrome") for vec in wordErr]
    print  "Decoded Message (from Noised): ", wordD 


    conn.sendall('[ACK] Decoding\n')
    #Closing Communication
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = sct.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    thread.start_new_thread(clientthread ,(conn,))
 
sct.close()