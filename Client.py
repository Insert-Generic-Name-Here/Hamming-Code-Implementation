from random import randint
from sage.all import *
import HammingWord
import socket
import pickle
import sys

#---------------------------------------------------------------------------------
#-----------------------------CONNECT TO SERVER SOCKET----------------------------
#---------------------------------------------------------------------------------
HOST = "localhost"		# Symbolic name meaning all available interfaces
PORT = 5000 			# Arbitrary non-privileged port

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	sct.connect((HOST,PORT))
except Exception as e:
	print e
	sys.exit(1)
#---------------------------------------------------------------------------------

enc_method = "";

try:
    C = codes.HammingCode(GF(int(sys.argv[1])), int(sys.argv[2])) #these two parameters will be given @terminal
    print "Prime Code: ", C
    enc_method = "Systematic"
except ValueError as vErr:
    print vErr
    sys.exit(0)

if (C.dual_code() is not None):
    C = C.dual_code()
    print "Dual Code: ", C, '\n'
    enc_method = "GeneratorMatrix"

q = C.base_field().cardinality()
dim = C.dimension()

word = [vector(HammingWord.makeWords(q-1, dim)) for i in range(20)]
wordN = [C.encode(vec, enc_method) for vec in word]
wordErr = [HammingWord.makeNoise(vec) for vec in wordN]

#---------------------------------------------------------------------------------
#-------------------------------SERVER COMMUNICATION------------------------------
#---------------------------------------------------------------------------------
try:
	print "[RESPONSE] Server: ", sct.recv(1024) #[ACK] Communication
	print "[REQUEST] Client: Sending Hamming Code Parameters"
	sct.sendall(sys.argv[1])
	sct.sendall(sys.argv[2])
	print "[RESPONSE] Server: ", sct.recv(1024) #[ACK] Code Prm Transmission
	print "[REQUEST] Client: Sending Message"
	sct.sendall(pickle.dumps(wordErr))
	print "[RESPONSE] Server: ", sct.recv(1024) #[ACK] Msg Transmission
	print "[RESPONSE] Server: ", sct.recv(1024) #[ACK] Decoding
except Exception as sct_exp:
	print "Communication with Server Failed!"
	print sct_exp

sys.exit(0)