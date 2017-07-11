from sage.all import *
import msginfo
import socket
import thread
import pickle
import sys
 
#---------------------------------------------------------------------------------
#---------------------------SOCKET CREATION; SOCKET BIND--------------------------
#---------------------------------------------------------------------------------    
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
#---------------------------------------------------------------------------------
 
    
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.sendall('[ACK] Server Connection') #send only takes string
    
    q = conn.recv(4)
    r = conn.recv(4)
    #Sending message to connected client
    conn.sendall('[ACK] Param. Transmission')
    
    # Creating Same Hamming[n, k] and it's Dual Code [if exists] #
    C = codes.HammingCode(GF(int(q)), int(r))
    print "Prime Code: ", C
    if (C.dual_code() is not None):
        C = C.dual_code()
        print "Dual Code: ", C, "\n"
        
    tmp = conn.recv(2048)
    checksum_origin = conn.recv(2048)
    
    rcv_msg = pickle.loads(tmp)
    print "Noised Message: ", rcv_msg, '\n'
    
    #Sending message to connected client
    conn.sendall('[ACK] Message/Checksum Transmission')
    
    wordD = [C.decode_to_message(vec, "Syndrome") for vec in rcv_msg]
    print  "Decoded Message (from Noised): ", wordD 

    #conn.sendall('[ACK] Decoding Successful')
    print "Message Checksum (SHA-256): ", checksum_origin
    checksum_decoded = msginfo.sha256checksum(repr(wordD))
    
    if (checksum_origin == checksum_decoded):
        conn.sendall('[ACK] Msg Received Correctly')
    else:
        conn.sendall('[ACK] Msg Received Flawed') 
    
    print "\n"
    #Closing Communication
    conn.close()
 
#---------------------------------------------------------------------------------
#------------------------LISTENING TO INCOMING CONNECTIONS------------------------
#--------------------------------------------------------------------------------- 
while 1:
    #wait to accept a connection - blocking call
    conn, addr = sct.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    thread.start_new_thread(clientthread ,(conn,))
#--------------------------------------------------------------------------------- 

sct.close()