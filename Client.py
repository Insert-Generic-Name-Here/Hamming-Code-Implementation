from sage.all import *
import HammingWord
import msginfo
import socket
import sys

#---------------------------------------------------------------------------------
#-------------------------------SERVER COMMUNICATION------------------------------
#---------------------------------------------------------------------------------
def ServerConnSendWord(wordN ,word_chksum, noise):
	try:
		wordErr = [HammingWord.makeNoise(vec, noise) for vec in wordN]

		print "\nEncoded-Noised Message: ", wordErr
		print "Entropy of Encoded-Noised Message: ", msginfo.entropy(msginfo.concatvct(wordErr))
		print "\n[REQUEST] Client: Sending Message and Checksum"
		sct.sendall(msginfo.buildJson(wordErr))
		sct.sendall(word_chksum)   
		print "[RESPONSE] Server: ", sct.recv(1024) #[ACK] Msg Transmission
		#print "[RESPONSE] Server: ", sct.recv(1024) #[ACK] Decoding
		str = sct.recv(1024)
		print "[RESPONSE] Server: ", str #[ACK] Correct/Incorrect Message    
		if str == "[ACK] Msg Received Flawed":
			yn = raw_input("> Do you want to Re-Transmit the Message? (y/n): ")
			if (yn.lower() == 'y'):
				ServerConnSendWord(wordN, word_chksum, noise)
	except ValueError as ve:
		print ve
		sct.close()
		return
	except KeyboardInterrupt as KeyErr:
		print "\nClient Forced Shutdown... Ending Connection..."
		sct.close()
		return
	except Exception as sct_exp:
		print "Fatal Error: Communication with Server Failed!"
		print sct_exp

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


#---------------------------------------------------------------------------------
#-------------------------------MAIN SOCKET CODE----------------------------------
#---------------------------------------------------------------------------------
enc_method = "";
try:
    C = codes.HammingCode(GF(int(sys.argv[1])), int(sys.argv[2])) #these two parameters will be given @terminal
    print "Prime Code: ", C
    enc_method = "Systematic"
except ValueError as vErr:
    print vErr
    sys.exit(0)

print "\nMinimum Distance: ", C.minimum_distance()
print "Maximum Error Correction: 1"
print "Maximum Error Detection: 2"
# Hamming Codes, both Simple & Extended are SECDED.
# In other words, they can *detect* *at most* *two* errors (Double Error Detection)
# but are capable of *only* *correcting* *one* (Single Error Correction)

if (C.dual_code() is not None):
    C = C.dual_code()
    print "\nDual Code: ", C, '\n'
    enc_method = "GeneratorMatrix"


q = C.base_field().cardinality()
dim = C.dimension()

word = [vector(HammingWord.makeWords(q-1, dim)) for i in range(20)]
wordN = [C.encode(vec, enc_method) for vec in word]

word_chksum = msginfo.sha256checksum(repr(word))

print "Original Message: ", word
print "Entropy of Original Message: ", msginfo.entropy(msginfo.concatvct(word))
print "Checksum of Original Message (SHA-256): ", word_chksum

print "\n[RESPONSE] Server: ", sct.recv(1024) #[ACK] Communication
print "[REQUEST] Client: Sending Hamming Code Parameters"
sct.sendall(sys.argv[1])
sct.sendall(sys.argv[2])
print "[RESPONSE] Server: ", sct.recv(1024) #[ACK] Code Prm Transmission
ServerConnSendWord(wordN, word_chksum, int(sys.argv[3]))
    
print "\n"
sys.exit(0)