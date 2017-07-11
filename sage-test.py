import HammingWord
import sys
from random import randint
from sage.all import *

enc_method = ""; dec_method = ""

try:
    C = codes.HammingCode(GF(2), 3) #these two parameters will be given @terminal
    print "Prime Code: ", C
    enc_method = "ParityCheck"
    dec_method = "NearestNeighbor"
except ValueError as vErr:
    print vErr
    sys.exit(0)

if (C.dual_code() is not None):
    C = C.dual_code()
    print "Dual Code: ", C, '\n'
    enc_method = "GeneratorMatrix"
    dec_method = "NearestNeighbor"

q = C.base_field().cardinality()
dim = C.dimension()

word = [vector(HammingWord.makeWords(q-1, dim)) for i in range(20)]
print "Initial Message: ", word, '\n'

wordN = [C.encode(vec, enc_method) for vec in word]
print "Encoded Message: ", wordN, '\n'

wordErr = [HammingWord.makeNoise(vec) for vec in wordN]
print  "Noised Message: ", wordErr, '\n'

wordD = [C.decode_to_message(vec, dec_method) for vec in wordErr]
print  "Decoded Message (from Noised): ", wordD